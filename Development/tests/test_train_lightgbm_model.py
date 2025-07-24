
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from codes.models.train import train_lightgbm_model


def test_train_lightgbm_model():

    X = pd.DataFrame(np.random.randn(100, 5), columns=[f"f{i}" for i in range(5)])
    y = pd.Series(np.random.randn(100))

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

    params = {
        "learning_rate": 0.1,
        "num_leaves": 31,
        "min_data_in_leaf": 20,
        "feature_fraction": 0.8,
        "bagging_fraction": 0.8,
        "lambda_l1": 1.0,
        "lambda_l2": 1.0
    }

    model, metrics, preds = train_lightgbm_model(X_train, y_train, X_valid, y_valid, params)
    assert "rmse" in metrics and "sMAPE" in metrics
    assert len(preds) == len(X_valid)
