from .error_metrics import smape, mase
import numpy as np


def smape_lgb_metric(preds, train_data):
    """
    LightGBM-compatible SMAPE metric.

    Returns:
        tuple: (metric_name, value, is_higher_better)
    """
    y_true = train_data.get_label()
    return "sMAPE", smape(y_true, preds), False


def mase_lgb_metric(preds, train_data):
    """
    LightGBM-compatible MASE metric using naive seasonal forecast.

    Returns:
        tuple: (metric_name, value, is_higher_better)
    """
    y_true = train_data.get_label()

    if len(y_true) <= 1:
        return "MASE", np.inf, False

    # Trim the arrays to calculate lag-1 naive forecast
    return "MASE", mase(y_true, preds, seasonality=1), False
