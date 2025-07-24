import psycopg
from codes.config import DB_CONFIG, TABLE_NAME

CREATE_TABLE_SQL = f"""
DROP TABLE IF EXISTS {TABLE_NAME};
CREATE TABLE {TABLE_NAME} (
    day_idx INTEGER,
    timestamp TIMESTAMP,
    num_drifted_columns INTEGER,
    sales_drift FLOAT,
    prediction_drift FLOAT,
    error_drift FLOAT,
    mean_abs_error FLOAT
);
"""


def create_database_if_missing():

    t = "host=%s port=%s user=%s password=%s" % (DB_CONFIG['host'], DB_CONFIG['port'], DB_CONFIG['user'], DB_CONFIG['password'])
    with psycopg.connect(t, autocommit=True) as conn:
        res = conn.execute(
            "SELECT 1 FROM pg_database WHERE datname='%s'" % DB_CONFIG["dbname"]
        )
        if not res.fetchall():
            conn.execute("CREATE DATABASE %s;" % DB_CONFIG["dbname"])


def setup_metrics_table():
    with psycopg.connect(**DB_CONFIG, autocommit=True) as conn:
        conn.execute(CREATE_TABLE_SQL)
