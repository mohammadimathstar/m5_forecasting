from codes.prediction import predict
import numpy as np


def test_predict_returns_series(sample_input_df):
    result = predict(sample_input_df)

    assert isinstance(result, np.ndarray), "Prediction should return a numpy array"
    assert len(result) == 1, "Prediction should return one result"


def test_predict_missing_feature(sample_input_df):
    bad_input = sample_input_df.drop(columns=["lag_7"])

    try:
        predict(bad_input)
        assert False, "Should raise an error if input is missing required features"
    except Exception as e:
        assert "lag_7" in str(e)
