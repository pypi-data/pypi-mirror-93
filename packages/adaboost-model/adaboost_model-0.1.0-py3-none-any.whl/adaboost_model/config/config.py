import pathlib

import adaboost_model

import pandas as pd


pd.options.display.max_rows = 10
pd.options.display.max_columns = 10

PACKAGE_ROOT = pathlib.Path(adaboost_model.__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / 'trained_models'
DATASET_DIR = PACKAGE_ROOT / 'datasets'

# data
TESTING_DATA_FILE = DATASET_DIR / 'test.csv'
TRAINING_DATA_FILE = DATASET_DIR / 'train.csv'
TARGET = 'Performance'

# variables
FEATURES = ['Age',
            'Gender',
            'TuitionSupport',
            'SchoolType',
            'Strand',
            'CGPA',
            'SelectedCollegeScore',
            'TotalUnits']

# categorical variables with NA in train set
CATEGORICAL_VARS_WITH_NA = ['Gender',
                            'TuitionSupport',
                            'SchoolType',
                            'Strand']

# categorical variables to encode
CATEGORICAL_VARS = ['Gender',
                    'TuitionSupport',
                    'SchoolType',
                    'Strand']

# numerical variables with NA in train set
NUMERICAL_VARS_WITH_NA = ['Age',
                          'CGPA',
                          'SelectedCollegeScore',
                          'TotalUnits']

NUMERICAL_NA_NOT_ALLOWED = [
    feature
    for feature in FEATURES
    if feature not in CATEGORICAL_VARS + NUMERICAL_VARS_WITH_NA
]

CATEGORICAL_NA_NOT_ALLOWED = [
    feature for feature in CATEGORICAL_VARS if feature not in CATEGORICAL_VARS_WITH_NA
]

PIPELINE_NAME = "adaboost_model"
PIPELINE_SAVE_FILE = f"{PIPELINE_NAME}_output_v"

# used for differential testing
ACCEPTABLE_MODEL_DIFFERENCE = 0.05
