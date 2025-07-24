from hyperopt import hp, fmin, tpe, Trials, STATUS_OK
import mlflow
from prefect import task
from typing import Any

from codes.tuning.hyperopt_objective import objective
from codes.config import MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME, NUM_TRIALS


@task(name="Run_hyperopt", log_prints=True)
def run_hyperopt(
    X_train, y_train, X_valid, y_valid, max_evals: int = NUM_TRIALS
) -> Any:
    """
    Run hyperparameter optimization with Hyperopt and log results in MLflow.

    Args:
        X_train, y_train: training data
        X_valid, y_valid: validation data
        max_evals (int): number of trials

    Returns:
        dict: best parameters
    """
    search_space = {
        "learning_rate": hp.uniform("learning_rate", 0.001, 0.2),
        "num_leaves": hp.quniform("num_leaves", 31, 256, 1),
        "min_data_in_leaf": hp.quniform("min_data_in_leaf", 20, 100, 1),
        "feature_fraction": hp.uniform("feature_fraction", 0.6, 1.0),
        "bagging_fraction": hp.uniform("bagging_fraction", 0.6, 1.0),
        "lambda_l1": hp.uniform("lambda_l1", 0.0, 5.0),
        "lambda_l2": hp.uniform("lambda_l2", 0.0, 5.0),
    }

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    trials = Trials()

    def mlflow_wrapped(params):
        results = objective(params, X_train, y_train, X_valid, y_valid)
        with mlflow.start_run(nested=True):
            mlflow.log_params(results["params"])
            for k, v in results["metrics"].items():
                mlflow.log_metric(k, v)
        return {"loss": results["loss"], "status": STATUS_OK}

    with mlflow.start_run(run_name="hyperopt_sweep"):
        mlflow.log_param("search_algorithm", "TPE")
        best = fmin(
            fn=mlflow_wrapped,
            space=search_space,
            algo=tpe.suggest,
            max_evals=max_evals,
            trials=trials,
        )

    return best
