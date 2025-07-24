import os
from pathlib import Path
import yaml

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load configuration from params.yaml
params_file = BASE_DIR / 'params.yaml'
if not params_file.exists():
    raise FileNotFoundError(f"params.yaml not found at: {params_file}")

with open(params_file) as conf_file:
    config = yaml.safe_load(conf_file)

# Development directory
DEV_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Time splits
START_DATE_TRAIN = config['split']['starting_date_idx_training']
END_DATE_TRAIN = config['split']['end_date_idx_training']
END_DATE_VAL = config['split']['end_date_idx_validation']

# MLflow config
MLFLOW_EXPERIMENT_NAME = config['mlflow']['experiment_name']
MLFLOW_TRACKING_URI = config['mlflow']['tracking_uri']
MLFLOW_MODEL_DIR = config['mlflow']['model_dir']

# Hyperparameter tuning config
NUM_TRIALS = config['hyperparams']['number_of_trials']

# Create required directories if missing
for path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    os.makedirs(path, exist_ok=True)

print(f"Loaded config. Tracking URI: {MLFLOW_TRACKING_URI}, Trials: {NUM_TRIALS}")

