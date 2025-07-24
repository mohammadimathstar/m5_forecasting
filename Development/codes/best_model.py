
from prefect import task
import mlflow
from dotenv import load_dotenv

from codes.models.train import train_lightgbm_model
from codes.models.mlflow_logging import log_model_and_metrics
from codes.config import MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME, PROCESSED_DATA_DIR, CREDINCIAL_ON

import pandas as pd
from pathlib import Path
import boto3


@task(name="Train_model", log_prints=True)
def train_model(X_train, y_train, X_valid, y_valid, params):
    """
    Prefect task to train and log a LightGBM model using MLflow.
    """
    #if CREDINCIAL_ON:
     #   env_path = Path(__file__).resolve().parent.parent / '.env'
      #  load_dotenv(dotenv_path=env_path)
    boto3.client("s3")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    with mlflow.start_run():
        model, metrics, predictions = train_lightgbm_model(
            X_train, y_train, X_valid, y_valid, params
        )

        reference_df = pd.read_csv(PROCESSED_DATA_DIR / 'reference_data.csv')
        log_model_and_metrics(
            model,
            metrics,
            params,
            predictions=predictions,
            reference_df=reference_df
        )

        return model
    
