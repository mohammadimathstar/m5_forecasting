import time
import pandas as pd
import logging
from prefect import flow, task
import psycopg
import os
from typing import Tuple

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from codes.config import (
    START_DATE_FORCASTING, 
    HOW_MANY_DAYS, SEND_TIMEOUT, 
    DATA_DIR, BUCKET_NAME, S3_KEY_REF, S3_KEY_TEST, 
    DB_CONFIG)
from codes.db import create_database_if_missing, setup_metrics_table
from codes.reporting import prepare_reference_data, calculate_metrics


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@task(name="Download_data_from_S3", log_prints=True)
def download_file_from_s3(bucket_name=BUCKET_NAME, s3_key_ref=S3_KEY_REF, s3_key_test=S3_KEY_TEST, local_path=DATA_DIR) -> Tuple[str, str]:

    ref_local_path = str(local_path / 'reference_data.csv')
    test_local_path = str(local_path / 'test_data.csv')

    s3 = boto3.client("s3")
    try:
        os.makedirs(local_path, exist_ok=True)

        s3.download_file(bucket_name, s3_key_ref, ref_local_path)
        logger.info(f"Downloaded s3://{bucket_name}/{s3_key_ref} to {ref_local_path}")
        print('hi', s3_key_ref)

        s3.download_file(bucket_name, s3_key_test, test_local_path)
        logger.info(f"Downloaded s3://{bucket_name}/{s3_key_test} to {test_local_path}")
        print(s3_key_test)

    except NoCredentialsError:
        logger.error("AWS credentials not found. Make sure they are configured properly.")
    except ClientError as e:
        logger.error(f"Error downloading file: {e}")

    return ref_local_path, test_local_path


@task
def load_data(ref_local_path, test_local_path):
    
    reference_data = pd.read_csv(ref_local_path)
    test_data = pd.read_csv(test_local_path)
    print(reference_data.shape, test_data.shape)
    reference_dataset = prepare_reference_data(reference_data)
    return reference_dataset, test_data


@task
def prepare_db():
    create_database_if_missing()
    setup_metrics_table()
    

@task
def insert_metrics(cursor, metrics: dict):
    cursor.execute("""
        INSERT INTO dummy_metrics(day_idx, timestamp, num_drifted_columns, sales_drift, prediction_drift, error_drift, mean_abs_error)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        metrics['day_idx'], metrics['timestamp'], metrics['num_drifted_columns'],
        metrics['sales_drift'], metrics['prediction_drift'], metrics['error_drift'], metrics['mean_abs_error']
    ))


@flow
def monitor_model():

    # initialize database
    prepare_db()

    # downloading the data (both reference data, and test data)
    ref_path, test_path = download_file_from_s3()

    # loading the data
    reference_dataset, test_data = load_data(ref_path, test_path)
    
    with psycopg.connect(**DB_CONFIG, autocommit=True) as conn:
        for i in range(START_DATE_FORCASTING, START_DATE_FORCASTING + HOW_MANY_DAYS):
            batch = test_data.loc[test_data.d == f"d_{i}"]
            with conn.cursor() as cursor:
                metrics = calculate_metrics(reference_dataset, batch, i)
                insert_metrics(cursor, metrics)
                logging.info(f"Metrics for day d_{i} inserted.")
            time.sleep(SEND_TIMEOUT)
