# 🛒 M5 Forecasting Pipeline: Sales Forecasting for Retail Chains

## 1. Problem Description

In the retail industry, accurately forecasting future sales is critical for managing inventory, reducing waste, and improving profitability. This project addresses the **M5 Forecasting** challenge, which involves predicting **daily item-level sales** across thousands of products and multiple stores over a period of time.

The goal is to build a machine learning pipeline that generates reliable and scalable forecasts using historical sales, calendar events, and price data.

**Problem type:** Supervised Learning / Regression  
**Deployment type:** Batch model training and inference

### Dataset

This project uses the **M5 Forecasting - Accuracy** dataset from [Kaggle](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data), which includes:

- `sales_train_validation.csv`: Historical daily unit sales of products
- `calendar.csv`: Dates and special events (e.g., holidays)
- `sell_prices.csv`: Price data for products

Sample data:

| id                 | item_id       | dept_id | store_id | state_id | d_1 | d_2 | ... |
|--------------------|---------------|---------|----------|----------|-----|-----|-----|
| HOBBIES_1_001_CA_1 | HOBBIES_1_001 | HOBBIES | CA_1     | CA       | 0   | 1   | ... |

---

## 2. Proposed Solution

The solution follows a modular and production-grade ML pipeline based on MLOps best practices.

We propose a modular and production-ready **MLOps pipeline** to forecast sales. The solution is divided into two distinct components:

### 📁 `development/`: Model Development

This folder contains all the code related to training the machine learning model. Key steps:

- Data preprocessing and feature engineering
- Model selection and training (LightGBM)
- Hyperparameter optimization (Hyperopt)
- Experiment tracking (MLflow)
- Prefect orchestration

### 📁 `deployment/`: Model Inference and Monitoring

This folder simulates a **production batch inference** pipeline. It:

- Loads the trained model and daily input data
- Generates predictions per day
- Monitors model drift and performance over time
- Uses Prefect to schedule and monitor batch jobs

## 3. Project Structure

.
├── Development/
│ ├── codes/
│ ├── data/
│ ├── tests/
│ ├── pipeline_training.py
│ ├── params.yaml
│ ├── requirements.txt
│ ├── Makefile
│ ├── start_prefect.sh
│ └── README.md ← explains development pipeline
├── Deployment/
│ ├── codes/
│ ├── config/
│ ├── dashboards/
│ ├── data/
│ ├── tests/
│ ├── monitoring_pipeline.py
│ ├── start_prefect_deployment.sh
│ ├── docker-compose.yaml
│ ├── params.yaml
│ ├── requirements.txt
│ ├── Makefile
│ └── README.md ← explains deployment + monitoring
└── README.md ← this file


### 5. Tech stack

| Category   | Tools                        |
| ---------- | ---------------------------- |
| Language   | Python                       |
| Workflow   | Prefect                      |
| Model      | LightGBM                     |
| Tuning     | Hyperopt                     |
| Tracking   | MLflow                       |
| Monitoring | Evidently AI, Grafana        |
| Formatting | Ruff                         |
| Testing    | Pytest                       |



### Key Components:

- **Data Preparation**: Merges and preprocesses the sales, calendar, and price datasets.
- **Feature Engineering**: Adds lag features, rolling windows, and time-based variables.
- **Hyperparameter Tuning**: Uses **Hyperopt** and **MLflow** to search for the best LightGBM model parameters.
- **Model Training**: Trains a LightGBM model and logs results using MLflow.
- **Evaluation**: Uses regression metrics like **sMAPE**, **MASE**, and **RMSE**.
- **Pipeline Orchestration**: Managed using **Prefect**, enabling scheduled and reliable batch runs.
- **Reproducibility**: Code versioned, structured, and automatically tested using `pytest` and `make`.

This pipeline can be deployed for regular batch inference or integrated into a larger forecasting system.

---

## 3. Tech Stack

| Category       | Tools Used |
|----------------|------------|
| Language       | Python 3.10 |
| Workflow       | [Prefect](https://www.prefect.io) |
| Model Tracking | [MLflow](https://mlflow.org) |
| Model          | [LightGBM](https://lightgbm.readthedocs.io/en/latest/) |
| Tuning         | [Hyperopt](https://github.com/hyperopt/hyperopt) |
| Testing        | `pytest` |
| Formatting     | `black`, `isort`, `ruff` |
| Orchestration  | Shell + `make` |
| Storage        | Local / AWS S3 (for MLflow artifacts) |

---

## 4. How to Run

### 📦 Setup

```bash
make install      # Install dependencies
make format       # Auto-format code
make lint         # Lint check
make test         # Run unit tests
```
