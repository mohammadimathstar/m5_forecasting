import pandas as pd
from codes.model import load_model
from codes.config import CATEGORICAL_FEATURES, NUMERICAL_FEATURES


_model = None  # lazy load


def predict(data: pd.DataFrame) -> pd.Series:
    global _model
    if _model is None:
        _model = load_model()

    for col in CATEGORICAL_FEATURES:
        data[col] = data[col].astype("category")

    return _model.predict(data[CATEGORICAL_FEATURES + NUMERICAL_FEATURES])
