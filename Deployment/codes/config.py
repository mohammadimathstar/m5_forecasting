import os
from pathlib import Path
import yaml
import json
import pandas as pd


#: Project base directory and subdirectories for development.
BASE_DIR = Path(__file__).resolve().parent.parent


with open(BASE_DIR / "params.yaml") as conf_file:
    config = yaml.safe_load(conf_file)

with open(BASE_DIR / "docker-compose.yaml") as conf_docker:
    docker_config = yaml.safe_load(conf_docker)


# Data directory
DATA_DIR = BASE_DIR / "data"

# Time interval
START_DATE_FORCASTING = config["forecasting_period"]["start_forecasting_date"]
HOW_MANY_DAYS = config["forecasting_period"]["how_many_days"]

# MLflow configuration
EXPERIMENT_ID = config["mlflow"]["experiment_id"]
RUN_ID = config["mlflow"]["run_id"]
MODEL_DIR = config["mlflow"]["model_dir"]
CREDINCIAL_ON = config["mlflow"]["creds_on"]

# Dashboards
DASH_DIR = BASE_DIR / config["dashboards"]["dash_dir"]
DASH_CONFIG_FILE = DASH_DIR / config["dashboards"]["config_file"]

os.makedirs(DASH_DIR, exist_ok=True)
if not os.path.exists(DASH_CONFIG_FILE):
    with open(DASH_CONFIG_FILE, "w") as f:
        json.dump({}, f)


# DB
DB_CONFIG = {
    "host": "db", # db is the name of the PostgreSQL service in your Docker Compose file, 
    "port": int(docker_config["services"]["db"]["ports"][0].split(":")[0]),
    "user": docker_config["services"]["db"]["environment"]["POSTGRES_USERNAME"],
    "password": docker_config["services"]["db"]["environment"]["POSTGRES_PASSWORD"],
    "dbname": config["dashboards"]["db_name"],
}


TABLE_NAME = config["dashboards"]["table_name"]

SEND_TIMEOUT = 5  # 10 seconds between each sending


# Features

CATEGORICAL_FEATURES = ["item_id", "dept_id", "cat_id", "store_id", "state_id"]
NUMERICAL_FEATURES = [
    "sell_price",
    "lag_7",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_28",
    "weekday",
    "week",
    "month",
    "year",
]

DRIFT_FEATURES = [
    "sales",
    "prediction",
    "error",
    "lag_7",
    "lag_28",
    "rolling_mean_7",
    "sell_price",
]
TARGET = "sales"
PREDICTION = "prediction"

START_DATE = pd.Timestamp(
    "2011-01-29"
)  # the first date in the dataset, corresponding to d_1
