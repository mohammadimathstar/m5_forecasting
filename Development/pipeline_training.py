
from prefect import flow, task
from typing import Tuple
import pandas as pd
import logging

from codes.data_loader import (
    load_sales_data,
    load_calendar_data,
    load_sell_prices
)
from codes.feature_engineering import (
    melt_sales_data,
    add_lag_features,
    add_rolling_features,
    add_date_features
)
from codes.best_model import train_model
from codes.tuning.param_tunning import run_hyperopt
from codes.config import (
    PROCESSED_DATA_DIR,
    START_DATE_TRAIN,
    END_DATE_TRAIN,
    END_DATE_VAL,
    NUM_TRIALS
)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@task(name="Prepare_data", log_prints=True)
def prepare_data() -> pd.DataFrame:
    """Loads raw M5 data and applies feature engineering."""
    logger.info("Loading raw data...")
    sales = load_sales_data()
    calendar = load_calendar_data()
    prices = load_sell_prices()

    logger.info("Transforming and merging...")
    sales = melt_sales_data(sales)
    sales = sales.merge(calendar, on="d", how="left")
    sales = sales.merge(prices, on=["store_id", "item_id", "wm_yr_wk"], how="left")

    logger.info("Applying feature engineering...")
    sales = add_lag_features(sales)
    sales = add_rolling_features(sales)
    sales = add_date_features(sales)

    logger.info(f"Saving to {PROCESSED_DATA_DIR / 'processed_data.csv'}")
    sales.to_csv(PROCESSED_DATA_DIR / 'processed_data.csv', index=False)
    return sales


@task(name="Split_data", log_prints=True)
def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """Splits data into train/validation/test sets for modeling."""
    categorical_columns = ['item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    features = categorical_columns + [
        'sell_price', 'lag_7', 'lag_28',
        'rolling_mean_7', 'rolling_mean_28',
        'weekday', 'week', 'month', 'year'
    ]

    for col in categorical_columns:
        df[col] = df[col].astype('category')

    target = 'sales'

    train_mask = df['d'].isin([f'd_{i}' for i in range(START_DATE_TRAIN, END_DATE_TRAIN)])
    valid_mask = df['d'].isin([f'd_{i}' for i in range(END_DATE_TRAIN, END_DATE_VAL)])
    test_mask = df['d'].isin([f'd_{i}' for i in range(END_DATE_VAL, df.shape[0])])

    X_train = df[train_mask][features]
    y_train = df[train_mask][target]
    X_valid = df[valid_mask][features]
    y_valid = df[valid_mask][target]

    df_reference = df[valid_mask][features + ['d', target]]
    df_test = df[test_mask][features + ['d', target]]
    df_reference.to_csv(PROCESSED_DATA_DIR / 'reference_data.csv', index=False)
    df_test.to_csv(PROCESSED_DATA_DIR / 'test_data.csv', index=False)

    logger.info(f"Train/Validation/Test splits created with shapes: "
                f"{X_train.shape}, {X_valid.shape}")

    return X_train, y_train, X_valid, y_valid

@flow(name="m5_pipeline", log_prints=True)
def m5_pipeline():
    
    """
    Full training pipeline for M5 forecasting:
    - Data prep
    - Feature engineering
    - Hyperparameter tuning
    - Model training
    """
    logger.info("Starting M5 Forecasting Pipeline")

    df = prepare_data()
    X_train, y_train, X_valid, y_valid = split_data(df)

    logger.info("Running Hyperparameter Search")
    best_params = run_hyperopt(
        X_train, y_train, X_valid, y_valid, max_evals=NUM_TRIALS
    )

    logger.info("Training Final Model")
    model = train_model(
        X_train, y_train, X_valid, y_valid, best_params
    )

    logger.info("Pipeline completed successfully.")
    return model


if __name__ == "__main__":
    m5_pipeline()



# s3://mlflow-artifacts-bucket-m5/1/models/m-fe1335d0dccd438a98c6030058f62702/artifacts/
# RUN_ID = 'm-a75cef28101e4b6f850a42f844a2cb85'
# EXPERIMENT_ID = '1'
# MODEL_DIR = 'models'
# model_uri = f"s3://mlflow-artifacts-bucket-m5/{EXPERIMENT_ID}/{MODEL_DIR}/{RUN_ID}/artifacts"