import lightgbm as lgb
import pandas as pd
from sklearn.metrics import root_mean_squared_error
from typing import Dict, Tuple

from codes.metrics.lgb_metrics import smape, mase, mase_lgb_metric


def train_lightgbm_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_valid: pd.DataFrame,
    y_valid: pd.Series,
    params: Dict,
    num_boost_round: int = 500
) -> Tuple[lgb.Booster, Dict[str, float]]:
    """
    Train a LightGBM model and return evaluation metrics and the model.

    Returns:
        model: trained lgb.Booster
        metrics: Dict with RMSE, sMAPE, MASE
    """
    model_params = {
        'objective': 'regression',
        'metric': 'None',
        'verbose': -1,
        **{k: int(v) if k in ['num_leaves', 'min_data_in_leaf'] else v for k, v in params.items()}
    }

    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_valid, label=y_valid)

    model = lgb.train(
        model_params,
        train_data,
        valid_sets=[valid_data],
        feval=mase_lgb_metric,
        num_boost_round=num_boost_round
    )

    y_pred = model.predict(X_valid)
    metrics = {
        'rmse': root_mean_squared_error(y_valid, y_pred),
        'sMAPE': smape(y_valid.values, y_pred),
        'MASE': mase(y_valid.values, y_pred)
    }

    return model, metrics, y_pred
