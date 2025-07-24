import pytest
from tempfile import TemporaryDirectory
from pathlib import Path

from codes.data_loader import load_sales_data, load_calendar_data, load_sell_prices


def create_dummy_csv(path: Path, data: str):
    path.write_text(data)


def test_load_sales_data():
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        dummy_data = "id,item_id,store_id,d_1,d_2,d_3\nFOO,FOO_1,CA_1,1,2,3"
        create_dummy_csv(tmp_path / "sales_train_validation.csv", dummy_data)

        df = load_sales_data(raw_data_dir=tmp_path, start_date_train=2)
        assert df.shape[1] == 5  # id, item_id, store_id, d_2, d_3
        df = load_sales_data(raw_data_dir=tmp_path, start_date_train=4)
        assert df.shape[1] == 3  # id, item_id, store_id, d_2, d_3


def test_load_calendar_data():
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        dummy_data = "date,event_name_1,event_type_1\n2011-01-29,NaN,NaN"
        create_dummy_csv(tmp_path / "calendar.csv", dummy_data)

        df = load_calendar_data(raw_data_dir=tmp_path)
        assert "date" in df.columns


def test_load_sell_prices():
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        dummy_data = "store_id,item_id,wm_yr_wk,sell_price\nCA_1,FOO_1,11101,1.5"
        create_dummy_csv(tmp_path / "sell_prices.csv", dummy_data)

        df = load_sell_prices(raw_data_dir=tmp_path)
        assert "sell_price" in df.columns


def test_missing_file():
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        with pytest.raises(FileNotFoundError):
            load_calendar_data(raw_data_dir=tmp_path)
