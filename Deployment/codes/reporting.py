import pandas as pd
from datetime import timedelta
from evidently import Dataset, DataDefinition, Regression
from evidently.presets import DataDriftPreset, RegressionPreset
from evidently import Report
from codes.prediction import predict
from codes.config import DRIFT_FEATURES, TARGET, PREDICTION, START_DATE

import warnings

warnings.filterwarnings("ignore")


report = Report(metrics=[DataDriftPreset(), RegressionPreset()])

SCHEMA = DataDefinition(
    regression=[Regression(target=TARGET, prediction=PREDICTION)],
    numerical_columns=DRIFT_FEATURES,
)


def prepare_reference_data(reference_data: pd.DataFrame):
    reference_data["error"] = reference_data[PREDICTION] - reference_data[TARGET]
    return Dataset.from_pandas(reference_data[DRIFT_FEATURES], data_definition=SCHEMA)


def calculate_metrics(
    reference_dataset, current_batch: pd.DataFrame, day_index: int
) -> dict:
    current_batch[PREDICTION] = predict(current_batch.drop(["d", TARGET], axis=1))
    # current_batch['error'] = current_batch[PREDICTION] - current_batch[TARGET]

    current_data = prepare_reference_data(
        current_batch
    )  # Dataset.from_pandas(current_batch[DRIFT_FEATURES], data_definition=SCHEMA)
    result = report.run(current_data=current_data, reference_data=reference_dataset)
    metrics = result.dict()["metrics"]

    return {
        "day_idx": day_index,
        "timestamp": START_DATE + timedelta(days=day_index - 1),
        "num_drifted_columns": metrics[0]["value"]["count"],
        "sales_drift": float(metrics[1]["value"]),
        "prediction_drift": float(metrics[2]["value"]),
        "error_drift": float(metrics[3]["value"]),
        "mean_abs_error": metrics[11]["value"]["mean"],
    }
