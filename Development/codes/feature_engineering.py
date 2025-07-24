import pandas as pd
import logging
from typing import List

logger = logging.getLogger(__name__)


def melt_sales_data(sales_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert wide-format sales data to long-format using 'melt'.

    Args:
        sales_df (pd.DataFrame): Raw sales data in wide format.

    Returns:
        pd.DataFrame: Long-format DataFrame with columns: id, item_id, ..., d, sales.
    """
    required_columns = {'id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'}
    if not required_columns.issubset(sales_df.columns):
        raise ValueError(f"Sales data missing required columns: {required_columns - set(sales_df.columns)}")

    logger.info("Melting sales data to long format")
    return sales_df.melt(
        id_vars=list(required_columns),
        var_name='d',
        value_name='sales'
    )


def add_lag_features(df: pd.DataFrame, lags: List[int] = [7, 28]) -> pd.DataFrame:
    """
    Add lag features (e.g., sales 7/28 days ago) to each item.

    Args:
        df (pd.DataFrame): DataFrame with 'id' and 'sales' columns.
        lags (List[int]): List of lag periods.

    Returns:
        pd.DataFrame: DataFrame with lag columns added.
    """
    for lag in lags:
        col_name = f'lag_{lag}'
        logger.debug(f"Adding lag feature: {col_name}")
        df[col_name] = df.groupby('id')['sales'].shift(lag)
    return df


def add_rolling_features(df: pd.DataFrame, windows: List[int] = [7, 28], base_lag_col: str = 'lag_28') -> pd.DataFrame:
    """
    Add rolling mean features over lagged sales.

    Args:
        df (pd.DataFrame): DataFrame with lag features.
        windows (List[int]): List of rolling window sizes.
        base_lag_col (str): Column to compute rolling stats over (default: 'lag_28').

    Returns:
        pd.DataFrame: DataFrame with rolling mean columns added.
    """
    if base_lag_col not in df.columns:
        raise ValueError(f"Missing base lag column '{base_lag_col}' for rolling features.")

    for window in windows:
        col_name = f'rolling_mean_{window}'
        logger.debug(f"Adding rolling mean feature: {col_name}")
        df[col_name] = df.groupby('id')[base_lag_col].transform(lambda x: x.rolling(window).mean())
    return df


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add temporal features (weekday, week, month, year) from 'date'.

    Args:
        df (pd.DataFrame): DataFrame with a 'date' column.

    Returns:
        pd.DataFrame: DataFrame with time-based features.
    """
    if 'date' not in df.columns:
        raise ValueError("Column 'date' must be present in the DataFrame to extract date features.")

    logger.info("Adding date features")
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.weekday
    df['week'] = df['date'].dt.isocalendar().week.astype(int)
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    return df








