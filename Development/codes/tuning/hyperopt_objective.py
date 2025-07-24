import lightgbm as lgb
from sklearn.metrics import root_mean_squared_error
from typing import Dict, Any

from codes.metrics.error_metrics import smape, mase
from codes.metrics.lgb_metrics import mase_lgb_metric




def objective(params: Dict[str, Any], X_train, y_train, X_valid, y_valid) -> Dict[str, Any]:
    """
    Objective function for Hyperopt tuning using MASE as loss.
    """
    # Cast hyperparams
    params['num_leaves'] = int(params['num_leaves'])
    params['min_data_in_leaf'] = int(params['min_data_in_leaf'])

    model_params = {
        'objective': 'regression',
        'metric': 'None',
        'verbose': -1,
        **params
    }

    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_valid, label=y_valid)

    model = lgb.train(
        model_params,
        train_data,
        num_boost_round=200,
        valid_sets=[valid_data],
        feval=mase_lgb_metric
    )

    y_pred = model.predict(X_valid)

    # Metrics
    smape_val = smape(y_valid.values, y_pred)
    mase_val = mase(y_valid.values, y_pred)
    rmse = root_mean_squared_error(y_valid, y_pred)

    return {
        "loss": mase_val,
        "status": "ok",
        "metrics": {
            "rmse": rmse,
            "sMAPE": smape_val,
            "MASE": mase_val
        },
        "params": model_params
    }

