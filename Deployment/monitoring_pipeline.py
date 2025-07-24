import time
import pandas as pd
import logging
from prefect import flow, task
import psycopg

from codes.config import START_DATE_FORCASTING, HOW_MANY_DAYS, SEND_TIMEOUT, DATA_DIR, DB_CONFIG
from codes.db import create_database_if_missing, setup_metrics_table
from codes.reporting import prepare_reference_data, calculate_metrics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")


@task
def load_data():
    reference_data = pd.read_csv(DATA_DIR / "reference_data.csv")
    test_data = pd.read_csv(DATA_DIR / "test_data.csv")
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

    # loading the data (both reference data, and test data)
    reference_dataset, test_data = load_data()
    
    with psycopg.connect(**DB_CONFIG, autocommit=True) as conn:
        for i in range(START_DATE_FORCASTING, START_DATE_FORCASTING + HOW_MANY_DAYS):
            batch = test_data.loc[test_data.d == f"d_{i}"]
            with conn.cursor() as cursor:
                metrics = calculate_metrics(reference_dataset, batch, i)
                insert_metrics(cursor, metrics)
                logging.info(f"Metrics for day d_{i} inserted.")
            time.sleep(SEND_TIMEOUT)
