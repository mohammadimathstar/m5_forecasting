import numpy as np
from codes.metrics.error_metrics import smape, mase


def test_smape_basic():
    y_true = np.array([100, 200, 300])
    y_pred = np.array([110, 190, 310])
    score = smape(y_true, y_pred)
    assert 0 <= score < 10


def test_smape_zero_handling():
    y_true = np.array([0, 0])
    y_pred = np.array([0, 0])
    assert smape(y_true, y_pred) == 0.0


def test_mase_perfect_prediction():
    y = np.array([10, 12, 14, 16, 18])
    assert mase(y, y) == 0.0


def test_mase_finite_value():
    y_true = np.array([10, 12, 14, 16, 18])
    y_pred = np.array([11, 13, 15, 17, 19])
    assert 0 < mase(y_true, y_pred) < 1.5
