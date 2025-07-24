import pandas as pd
import logging
from pathlib import Path
from codes.config import RAW_DATA_DIR, START_DATE_TRAIN

logger = logging.getLogger(__name__)


def load_sales_data(
    raw_data_dir: Path = RAW_DATA_DIR, start_date_train: int = START_DATE_TRAIN
) -> pd.DataFrame:
    """
    Load the M5 sales training data and drop older dates before the training start.

    Args:
        raw_data_dir (Path): Path to the raw data directory
        start_date_train (int): First day (d_*) to keep for training

    Returns:
        pd.DataFrame: Trimmed sales_train_validation dataset
    """
    sales_path = raw_data_dir / "sales_train_validation.csv"
    if not sales_path.exists():
        logger.error(f"Sales data not found at {sales_path}")
        raise FileNotFoundError(sales_path)

    logger.info(f"Loading sales data from {sales_path}")
    df = pd.read_csv(sales_path)

    # Remove columns before start date
    older_dates = [f"d_{i}" for i in range(1, start_date_train)]
    df.drop(columns=[col for col in older_dates if col in df.columns], inplace=True)

    return df


def load_calendar_data(raw_data_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """
    Load the calendar file with date mappings and events.

    Args:
        raw_data_dir (Path): Path to the raw data directory

    Returns:
        pd.DataFrame: calendar.csv dataset
    """
    path = raw_data_dir / "calendar.csv"
    if not path.exists():
        logger.error(f"Calendar file not found at {path}")
        raise FileNotFoundError(path)

    logger.info(f"Loading calendar data from {path}")
    return pd.read_csv(path)


def load_sell_prices(raw_data_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """
    Load item price history data.

    Args:
        raw_data_dir (Path): Path to the raw data directory

    Returns:
        pd.DataFrame: sell_prices.csv dataset
    """
    path = raw_data_dir / "sell_prices.csv"
    if not path.exists():
        logger.error(f"Sell prices file not found at {path}")
        raise FileNotFoundError(path)

    logger.info(f"Loading sell prices from {path}")
    return pd.read_csv(path)
