# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods for AutoML remote runs."""
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from azureml._restclient.constants import RUN_ORIGIN
from azureml._restclient.jasmine_client import JasmineClient
from azureml._tracing import get_tracer
from azureml.automl.core._experiment_observer import ExperimentStatus, ExperimentObserver
from azureml.automl.core.shared.constants import SupportedModelNames, TelemetryConstants
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.telemetry_activity_logger import TelemetryActivityLogger
from azureml.automl.runtime.distributed.utilities import PollForMaster, is_master_process
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared import memory_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Experiment, Run
from azureml.train.automl._automl_datamodel_utilities import CaclulatedExperimentInfo
from azureml.train.automl._automl_feature_config_manager import AutoMLFeatureConfigManager
from azureml.train.automl._azure_experiment_observer import AzureExperimentObserver
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings

from azureml.train.automl.runtime._data_preparer import DataPreparer, DataPreparerFactory
from azureml.train.automl.runtime._entrypoints import entrypoint_util

logger = logging.getLogger(__name__)
activity_logger = TelemetryActivityLogger()
tracer = get_tracer(__name__)


def _prep_input_data(
    run: Run,
    iteration_name: str,
    automl_settings_obj: AzureAutoMLSettings,
    script_directory: Optional[str],
    dataprep_json: str,
    entry_point: Optional[str],
    parent_run: Run,
    verifier: Optional[VerifierManager] = None
) -> Tuple[Dict[str, Any], ExperimentObserver, AutoMLFeatureConfigManager]:
    """called by featurization only"""

    with tracer.start_as_current_span(
            TelemetryConstants.SPAN_FORMATTING.format(
                TelemetryConstants.COMPONENT_NAME, TelemetryConstants.DATA_PREPARATION
            ),
            user_facing_name=TelemetryConstants.DATA_PREPARATION_USER_FACING
    ):
        logger.info('Preparing input data for {} iteration for run {}.'.format(iteration_name, run.id))

        calculated_experiment_info = None
        data_preparer = None
        if dataprep_json:
            data_preparer = DataPreparerFactory.get_preparer(dataprep_json)
            conducive_for_streaming = _are_inputs_conducive_for_streaming(automl_settings_obj, data_preparer)
            if conducive_for_streaming and data_preparer.data_characteristics is not None:
                calculated_experiment_info = \
                    CaclulatedExperimentInfo(data_preparer.data_characteristics.num_rows,
                                             data_preparer.data_characteristics.num_numerical_columns,
                                             data_preparer.data_characteristics.num_categorical_columns,
                                             data_preparer.data_characteristics.num_text_columns,
                                             memory_utilities.get_available_physical_memory())

        feature_config_manager = _build_feature_config_manager(run.experiment)
        feature_config_manager.fetch_all_feature_profiles_for_run(
            parent_run_id=parent_run.id,
            automl_settings=automl_settings_obj,
            caclulated_experiment_info=calculated_experiment_info
        )

        if feature_config_manager.is_streaming_enabled():
            logger.info('Service responded with streaming enabled')
            entrypoint_util.modify_settings_for_streaming(
                automl_settings_obj,
                dataprep_json)
        else:
            logger.info('Service responded with streaming disabled')

        fit_iteration_parameters_dict = entrypoint_util.prepare_data(
            data_preparer=data_preparer,
            automl_settings_obj=automl_settings_obj,
            script_directory=script_directory,
            entry_point=entry_point,
            verifier=verifier
        )

    experiment_observer = AzureExperimentObserver(parent_run, file_logger=logger)

    if automl_settings_obj.enable_streaming:
        logger.info("Streaming enabled")

    return fit_iteration_parameters_dict, experiment_observer, feature_config_manager


def _cache_dataset(
    cache_store: CacheStore,
    dataset: DatasetBase,
    experiment_observer: ExperimentObserver,
    parent_run_id: str
) -> None:
    """Called by featurization and featurization_fit entrypoints only"""
    try:
        cache_store.set(entrypoint_util.DATASET_BASE_CACHE_KEY, dataset)
        logger.info("Successfully cached dataset.")
    except Exception:
        logger.error("Failed to cache dataset.")
        raise

    logger.info('Preparation for run id {} finished successfully.'.format(parent_run_id))
    experiment_observer.report_status(ExperimentStatus.ModelSelection, "Beginning model selection.")


def transfer_files_from_setup(run: Run, setup_container_id: str,
                              feature_config_path: str, engineered_names_path: str) -> None:
    """
    Helper function that transfers essential files from the setup run's data container to the featurization run.
    Note that download only occurs for the master process.

    :param run: the run object to which we are downloading the files.
    :param setup_container_id: the id string of the setup run's data container.
    :param feature_config_path: the path to the feature_config object in the setup run's data container.
    :param engineered_names_path: the path to the engineered_feature_names object in the setup run's data container.
    :return: None
    """
    if is_master_process():
        run._client.artifacts.download_artifact(RUN_ORIGIN, setup_container_id,
                                                feature_config_path, feature_config_path)
        run._client.artifacts.download_artifact(RUN_ORIGIN, setup_container_id,
                                                engineered_names_path, engineered_names_path)

    with PollForMaster(
            proceed_on_condition=lambda: os.path.exists(feature_config_path) and os.path.exists(engineered_names_path)
    ):
        # TODO replace this with an MPI barrier
        logger.info("Setup artifacts successfully retrieved.")


def _are_inputs_conducive_for_streaming(
        automl_settings: AzureAutoMLSettings,
        data_preparer: DataPreparer
) -> bool:
    """called by featurization only"""
    if automl_settings.force_streaming:
        return True

    # List storing all the reasons due to which streaming could not be enabled
    incompatibility_reasons = []    # type: List[str]

    if data_preparer._original_training_data is None:
        incompatibility_reasons.append("'training_data' is not provided")

    if automl_settings.is_timeseries:
        incompatibility_reasons.append("Forecasting is not supported")

    if automl_settings.n_cross_validations is not None:
        incompatibility_reasons.append("'n_cross_validations' was non-empty")

    if automl_settings.enable_onnx_compatible_models:
        incompatibility_reasons.append("ONNX compatibility is not supported")

    if automl_settings.enable_dnn:
        incompatibility_reasons.append("DNN is not supported")

    if automl_settings.enable_subsampling:
        incompatibility_reasons.append("Subsampling is enabled")

    if automl_settings.whitelist_models is not None:
        supported_set = set([model.customer_model_name for model in SupportedModelNames.SupportedStreamingModelList])
        if not set(automl_settings.whitelist_models).issubset(supported_set):
            incompatibility_reasons.append("Allowed models are unsupported. "
                                           "Supported models: [{}]".format(','.join(supported_set)))

    if incompatibility_reasons:
        logger.info("Streaming is not conducive due to incompatible settings. "
                    "Reason[s]: [{}]".format(', '.join(incompatibility_reasons)))
        return False

    return True


def _build_feature_config_manager(experiment: Experiment) -> AutoMLFeatureConfigManager:
    """Build an AutoML feature config manager for the run."""
    jasmine_client = JasmineClient(
        experiment.workspace.service_context,
        experiment.name,
        experiment.id,
        user_agent=type(JasmineClient).__name__)
    return AutoMLFeatureConfigManager(jasmine_client=jasmine_client)


def cache_onnx_init_metadata(
    cache_store: CacheStore,
    fit_iteration_parameters_dict: Dict[str, Any],
    parent_run_id: str
) -> None:
    onnx_metadata_dict = OnnxConverter.get_onnx_metadata(
        X=fit_iteration_parameters_dict.get('X'),
        x_raw_column_names=fit_iteration_parameters_dict.get("x_raw_column_names"))

    # If the cache store and the onnx converter init metadata are valid, save it into cache store.
    if onnx_metadata_dict:
        logger.info('Successfully initialized ONNX converter for run {}.'.format(parent_run_id))
        logger.info('Begin saving onnx initialization metadata for run {}.'.format(parent_run_id))
        cache_store.add([entrypoint_util.CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA],
                        [onnx_metadata_dict])
        logger.info('Successfully Saved onnx initialization metadata for run {}.'.format(parent_run_id))
    else:
        logger.info('Failed to initialize ONNX converter for run {}.'.format(parent_run_id))


def get_input_datamodel_from_dataprep_json(dataprep_json,
                                           automl_settings):
    """
    Convert dataprep data from json to data dictionary.

    :param dataprep_json: The dataprep object in json format.
    :param automl_settings: The automl settings.
    :return: Dictionary containing datasets.
    """
    try:
        logger.info("getting input data from dataprep json...")

        Contract.assert_value(dataprep_json, "dataprep_json")
        Contract.assert_value(automl_settings, "automl_settings")

        data_preparer = DataPreparerFactory.get_preparer(dataprep_json)
        data_dict = entrypoint_util.prepare_data(
            data_preparer=data_preparer, automl_settings_obj=automl_settings,
            script_directory=None, entry_point=None)
        return data_dict
    except Exception:
        logger.error("Error from getting input data from dataprep json")
        raise
