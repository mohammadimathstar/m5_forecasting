from prefect import task
import mlflow

from codes.models.train import train_lightgbm_model
from codes.models.mlflow_logging import log_model_and_metrics
from codes.config import MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME, PROCESSED_DATA_DIR, PROCESSED_DATA_BUCKET

import pandas as pd
import boto3


@task(name="Train_model", log_prints=True)
def train_model(X_train, y_train, X_valid, y_valid, params):
    """
    Prefect task to train and log a LightGBM model using MLflow.
    """
    
    s3 = boto3.client("s3")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME) 
    
    val_path = PROCESSED_DATA_DIR / "reference_data.csv"

    with mlflow.start_run():
        model, metrics, predictions = train_lightgbm_model(
            X_train, y_train, X_valid, y_valid, params
        )

        reference_df = pd.read_csv(val_path)
        reference_df['prediction'] = predictions
        
        reference_df.to_csv(val_path, index=False)               
        
        s3.upload_file(
            str(val_path), PROCESSED_DATA_BUCKET, "/".join(str(val_path).split("/")[-3:])
        )

    
        log_model_and_metrics(
            model, metrics, params, predictions=predictions, reference_df=reference_df
        )

        return model
