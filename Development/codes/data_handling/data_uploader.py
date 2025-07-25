import pandas as pd
import logging
from pathlib import Path
from codes.config import PROCESSED_DATA_DIR, PROCESSED_DATA_BUCKET
import boto3


logger = logging.getLogger(__name__)


def save_and_upload_to_s3(df_reference: pd.DataFrame, df_test: pd.DataFrame, 
                          local_dir: Path = PROCESSED_DATA_DIR,
                          s3_bucket: str = PROCESSED_DATA_BUCKET):
    """
    Save two DataFrames to CSV and upload them to an S3 bucket.

    Args:
        df_reference (pd.DataFrame): First DataFrame.
        df_test (pd.DataFrame): Second DataFrame.
        local_dir (Path): Directory to save the local CSV files.
        filenames (tuple): Filenames to save locally (e.g., ("data1.csv", "data2.csv")).
        s3_bucket (str): Name of the S3 bucket.
        s3_keys (tuple): S3 object keys for the files (e.g., ("folder/data1.csv", "folder/data2.csv")).
        aws_region (str): AWS region (default: "us-east-1").
    """

    reference_path = local_dir / 'reference_data.csv'
    test_path = local_dir / 'test_data.csv'

    df_reference.to_csv(reference_path, index=False)
    df_test.to_csv(test_path, index=False)

    # Upload to S3
    s3 = boto3.client("s3")
    s3.upload_file(str(reference_path), s3_bucket, "/".join(str(reference_path).split("/")[-3:]))
    s3.upload_file(str(test_path), s3_bucket, "/".join(str(test_path).split("/")[-3:]))

    print(f"Uploaded {local_dir} to s3://{s3_bucket} bucket.")
