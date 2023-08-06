from sklearn.ensemble import AdaBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from adaboost_model.processing import preprocessors as pp
from adaboost_model.config import config

import logging


_logger = logging.getLogger(__name__)


PIPELINE_NAME = "adaboost_model"

grading_pipe = Pipeline(
    [
        ('categorical_imputer',
            pp.CategoricalImputer(variables=config.CATEGORICAL_VARS_WITH_NA)),

        ('categorical_encoder',
            pp.CategoricalEncoder(variables=config.CATEGORICAL_VARS)),

        ('numerical_imputer',
         pp.NumericalImputer(variables=config.NUMERICAL_VARS_WITH_NA)),

        ('scaler', MinMaxScaler()),
        (PIPELINE_NAME, AdaBoostClassifier(random_state=0,learning_rate=1,n_estimators=50)
         )
    ]
)
