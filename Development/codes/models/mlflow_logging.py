import mlflow
import mlflow.lightgbm
from typing import Dict
import pandas as pd

from codes.config import MLFLOW_MODEL_DIR, PROCESSED_DATA_DIR


def log_model_and_metrics(
    model,
    metrics: Dict[str, float],
    params: Dict,
    predictions: pd.Series = None,
    reference_df: pd.DataFrame = None,
    model_path: str = MLFLOW_MODEL_DIR,
):
    """
    Logs metrics, parameters, model, and optionally predictions to MLflow.
    """
    mlflow.log_params(params)
    for name, value in metrics.items():
        mlflow.log_metric(name, value)

    if reference_df is not None and predictions is not None:
        assert len(reference_df) == len(predictions), (
            "Reference and predictions length mismatch"
        )
        reference_df["prediction"] = predictions
        reference_df.to_csv(PROCESSED_DATA_DIR / "reference_data.csv", index=False)

    mlflow.lightgbm.log_model(model, artifact_path=model_path)
