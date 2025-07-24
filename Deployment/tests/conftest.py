# tests/conftest.py
import pytest
import pandas as pd


@pytest.fixture
def sample_input_df():
    return pd.DataFrame(
        {
            "item_id": ["ITEM_001"],
            "dept_id": ["DEPT_001"],
            "cat_id": ["CAT_001"],
            "store_id": ["STORE_001"],
            "state_id": ["CA"],
            "sell_price": [9.99],
            "lag_7": [12],
            "lag_28": [10],
            "rolling_mean_7": [11.2],
            "rolling_mean_28": [10.8],
            "weekday": [2],
            "week": [30],
            "month": [7],
            "year": [2025],
            "prediction": [2],
            "sales": [3],
        }
    )
