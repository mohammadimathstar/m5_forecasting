import pandas as pd
from codes.feature_engineering import (
    melt_sales_data,
    add_lag_features,
    add_rolling_features,
    add_date_features
)


def test_melt_sales_data():
    df = pd.DataFrame({
        'id': ['A'], 'item_id': ['i1'], 'dept_id': ['d'], 'cat_id': ['c'],
        'store_id': ['s'], 'state_id': ['CA'],
        'd_1': [1], 'd_2': [2]
    })
    melted = melt_sales_data(df)
    assert 'sales' in melted.columns
    assert melted.shape[0] == 2


def test_add_lag_features():
    df = pd.DataFrame({
        'id': ['A'] * 5,
        'sales': [10, 20, 30, 40, 50]
    })
    lagged = add_lag_features(df.copy(), lags=[2])
    assert 'lag_2' in lagged.columns
    assert pd.isna(lagged.iloc[0]['lag_2'])


def test_add_rolling_features():
    df = pd.DataFrame({
        'id': ['A'] * 5,
        'lag_28': [1, 2, 3, 4, 5]
    })
    rolled = add_rolling_features(df.copy(), windows=[3])
    assert 'rolling_mean_3' in rolled.columns
    assert pd.isna(rolled.iloc[0]['rolling_mean_3'])  # not enough data for first row


def test_add_date_features():
    df = pd.DataFrame({'date': ['2020-01-01', '2020-01-02']})
    df = add_date_features(df)
    assert 'weekday' in df.columns
    assert df.loc[0, 'weekday'] == 2  # Jan 1, 2020 was Wednesday
