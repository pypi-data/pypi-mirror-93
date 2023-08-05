# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import datetime
import logging
import os
import tempfile

import numpy as np
import pandas as pd
from azureml.automl.core import dataset_utilities
from azureml.automl.core.shared import constants, logging_utilities as log_utils
from azureml.automl.core.shared.exceptions import PredictionException
from azureml.automl.runtime.shared import metrics
from azureml.core import Run, Dataset
from azureml.data.abstract_dataset import AbstractDataset
from azureml.train.automl._model_download_utilities import _download_automl_model
from azureml.train.automl.model_proxy import RESULTS_PROPERTY

OUTPUT_FILE_NAME_TEMPLATE = "predictions{}.csv"


logger = logging.getLogger(__name__)


def get_model_from_training_run(experiment, training_run_id):
    """
    Get the fitted model from the specified training run.

    :param experiment: The experiment which contains the training run.
    :param training_run_id: The id for the AutoML child run which contains the model.
    :return: The fitted model
    """
    logger.info("Fetching model from training run.")
    training_run = Run(experiment, training_run_id)
    fitted_model = _download_automl_model(training_run)
    return fitted_model


def get_target_metrics(task, automl_settings):
    """
    Get the types of metrics which should
    be computed for the specified task.

    :param task: The task type (see constants.py).
    :param automl_settings: AzureAutoMLSettings for the parent run.
    :return: A list of metric types
    """
    # TODO: the metrics methods are deprecated.
    # Used here to mimic the behavior of pipeline_run_helper.run_pipeline()
    # Note, the default target metrics used in ClientRunner
    # (scoring_utilities.get_scalar_metrics(task))
    # do not return the metrics graphs.
    # Metrics.get_default_metrics(task) does return the graphs data.
    target_metrics = metrics.get_default_metrics(task)
    if automl_settings.is_timeseries:
        target_metrics += metrics.get_default_metrics(constants.Subtasks.FORECASTING)
    return target_metrics


def _get_pandas(results):
    if results is None:
        raise Exception("Inferencing returned no results.")
    elif isinstance(results, pd.DataFrame):
        logger.info("Inference output as pandas.")
        return results
    elif isinstance(results, AbstractDataset):
        logger.info("Inference output as AbstractDataset, casting to pandas.")
        return results.to_pandas_dataframe()
    else:
        # if its not any of the above types, assume its some primitive array type that pandas can accept
        logger.info("Inference output is not pandas or AbstractDataset, casting to pandas.")
        return pd.DataFrame(results)


def _save_results(results, run):
    """
    Save the prediction(s) to the default datastore.
    """
    logger.info("Saving predicted results.")

    if isinstance(results, tuple) or isinstance(results, list):
        logger.info("Multiple inference outputs, casting to pandas.")
        results_pd = [_get_pandas(result) for result in results]
    else:
        logger.info("Single inference output, casting to pandas.")
        results_pd = [_get_pandas(results)]

    file_names = []

    with tempfile.TemporaryDirectory() as project_folder:
        if len(results_pd) > 1:
            max_chars = len(str(len(results_pd)))

            for i, df in enumerate(results_pd, start=1):
                suffix = "_" + str(i).zfill(max_chars)
                file_name = OUTPUT_FILE_NAME_TEMPLATE.format(suffix)
                file_names.append(file_name)

                local_path = os.path.join(project_folder, file_name)
                df.to_csv(local_path, index=False)
        else:
            file_name = OUTPUT_FILE_NAME_TEMPLATE.format("")
            file_names.append(file_name)

            local_path = os.path.join(project_folder, file_name)
            results_pd[0].to_csv(local_path, index=False)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        inference_results_dir = "{}_{}".format(run.id, timestamp)

        logger.info("Uploading results to {}".format(inference_results_dir))

        datastore = run.experiment.workspace.get_default_datastore()
        datastore.upload(src_dir=project_folder,
                         target_path=inference_results_dir,
                         overwrite=True)

        remote_paths = [os.path.join(inference_results_dir, file_name)
                        for file_name in file_names]

        for remote_path in remote_paths:
            # Mark the output files as "output datasets" for the run.
            # This happens in the ensure_saved method.
            dataset = Dataset.Tabular.from_delimited_files(datastore.path(remote_path))
            dataset_utilities.ensure_saved(run.experiment.workspace, output_data=dataset)

        run.add_properties({RESULTS_PROPERTY: remote_paths})


def inference(task, model, X_test, y_context=None, is_timeseries=False):
    """
    Return predictions from the given model with a provided task type.

    :param task: The task type (see constants.py).
    :param model: The model used to make predictions.
    :param X_test: The inputs on which to predict.
    :param y_context: Used for forecasting. The target value combining definite
                      values for y_past and missing values for Y_future.
                      If None the predictions will be made for every X_pred.
    :param is_timeseries: Whether or not this is a forecasting task.
    :return: The predictions of the model on X_test
        The shape of the array returned depends on the task type
        Classification will return probabilities for each class.
    """
    with log_utils.log_activity(logger, activity_name=constants.TelemetryConstants.PREDICT_NAME):
        if task == constants.Tasks.CLASSIFICATION:
            y_pred = model.predict_proba(X_test)

        elif task == constants.Tasks.REGRESSION:
            if is_timeseries and hasattr(model, 'forecast'):
                y_pred, _ = model.forecast(X_test, y_context)

            else:
                y_pred = model.predict(X_test)

        else:
            raise NotImplementedError

        # Some pipelines will fail silently by predicting NaNs
        # E.g. a pipeline with a preprocessor that does not normalize and a linear model
        #   Pipeline[SVD, SGD] will fail if the dataset contains features on vastly different scales
        # Task to fix for ID features: 550564
        if np.issubdtype(y_pred.dtype, np.number):
            if np.isnan(y_pred).any():
                error_message = ("Silent failure occurred during prediction. "
                                 "This could be a result of unusually large values in the dataset. "
                                 "Normalizing numeric features might resolve this.")
                raise PredictionException.create_without_pii(error_message)

        return y_pred
