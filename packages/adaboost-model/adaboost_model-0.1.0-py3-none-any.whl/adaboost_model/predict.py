import numpy as np
import pandas as pd

from adaboost_model.processing.data_management import load_pipeline
from adaboost_model.config import config
from adaboost_model.processing.validation import validate_inputs
from adaboost_model import __version__ as _version

import logging


_logger = logging.getLogger(__name__)

pipeline_file_name = f"{config.PIPELINE_SAVE_FILE}{_version}.pkl"
_grade_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(*, input_data) -> dict:
    """Make a prediction using the saved model pipeline."""

    data = pd.DataFrame(input_data, index=[0])
    validated_data = validate_inputs(input_data=data)
    prediction = _grade_pipe.predict(validated_data[config.FEATURES])
    output = prediction

    results = {"predictions": output, "version": _version}

    _logger.info(
        f"Making predictions with model version: {_version} "
        f"Inputs: {validated_data} "
        f"Predictions: {results}"
    )

    return results
