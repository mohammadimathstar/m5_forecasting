import numpy as np


def smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Symmetric Mean Absolute Percentage Error.

    Args:
        y_true (np.ndarray): Ground truth values.
        y_pred (np.ndarray): Predicted values.

    Returns:
        float: SMAPE value in percentage.
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    diff = np.abs(y_true - y_pred) / np.where(denominator == 0, 1, denominator)
    diff[denominator == 0] = 0.0
    return np.mean(diff) * 100


def mase(y_true: np.ndarray, y_pred: np.ndarray, seasonality: int = 1) -> float:
    """
    Mean Absolute Scaled Error.

    Args:
        y_true (np.ndarray): Ground truth values.
        y_pred (np.ndarray): Predicted values.
        seasonality (int): Seasonal lag (default is 1 for naive forecast).

    Returns:
        float: MASE score.
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    if len(y_true) <= seasonality:
        return np.inf

    naive_forecast = y_true[:-seasonality]
    y_trimmed = y_true[seasonality:]
    pred_trimmed = y_pred[seasonality:]

    denominator = np.mean(np.abs(y_trimmed - naive_forecast))
    numerator = np.mean(np.abs(y_trimmed - pred_trimmed))

    return numerator / denominator if denominator != 0 else np.inf
