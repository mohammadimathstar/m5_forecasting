import os
from kaggle.api.kaggle_api_extended import KaggleApi
import logging
import zipfile

from codes.config import RAW_DATA_DIR

logger = logging.getLogger(__name__)

def download_m5_data(destination_dir: str = RAW_DATA_DIR):
    os.makedirs(destination_dir, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    logger.info("Downloading M5 Forecasting dataset...")
    api.competition_download_files(
        competition="m5-forecasting-accuracy",
        path=destination_dir
    )

    logger.info("Unzipping files...")
    
    zip_path = os.path.join(destination_dir, "m5-forecasting-accuracy.zip")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination_dir)

    os.remove(zip_path)
    logger.info("Downloading is done.")

