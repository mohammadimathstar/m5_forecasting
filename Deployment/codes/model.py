import mlflow
from pathlib import Path
from codes.config import MODEL_DIR, EXPERIMENT_ID, RUN_ID, CREDINCIAL_ON
from dotenv import load_dotenv
import boto3


if CREDINCIAL_ON:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    s3 = boto3.client("s3")


def load_model():
    model_uri = f"s3://mlflow-artifacts-bucket-m5/{EXPERIMENT_ID}/{MODEL_DIR}/{RUN_ID}/artifacts"
    return mlflow.pyfunc.load_model(model_uri)
