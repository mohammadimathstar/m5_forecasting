# 🛒 M5 Forecasting Pipeline: Sales Forecasting for Retail Chains

## 1. Problem Description

In the retail industry, accurate sales forecasting is crucial for making informed decisions related to:

- 📦 Inventory management

- 💸 Revenue planning

- ❌ Reducing overstock and understock situations

- 🕒 Aligning supply chains with demand patterns

This project is built around the M5 Forecasting Challenge, which provides a real-world dataset from Walmart and challenges participants to forecast daily item-level sales.

### 🧠 Objective

The primary objective is to develop a machine learning pipeline that can:

- Train a predictive model on historical data

- Incorporate external features like calendar events and prices

- Produce reliable and scalable forecasts

- Handle data from thousands of products sold across multiple stores in different U.S. states

#### 📊 Problem Type

- **Type**: Supervised Machine Learning

- **Task**: Regression (continuous target = daily sales quantity)

- **Deployment type:** Batch model training and inference

- **Evaluation Metrics**: 

    * sMAPE (Symmetric Mean Absolute Percentage Error)

    * MASE (Mean Absolute Scaled Error)


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

We propose a modular and production-ready **MLOps pipeline** to forecast sales. The solution is divided into three distinct components:

### 📁 `terraform/`: creating required infrastructure

Here, we use Terraform to construct the required infrastructure in the cloud (AWS):

- Constructing the infrastructure needed to store the data and the model's artefacts in S3 (AWS).

### 📁 `development/`: Model Development

This folder contains all the code related to training the machine learning model. Key steps:

- Data preprocessing and feature engineering
- Model selection and training (LightGBM)
- Hyperparameter optimisation (Hyperopt)
- Experiment tracking (MLflow)
- Prefect orchestration

### 📁 `deployment/`: Model Inference and Monitoring

This folder simulates a **production batch inference** pipeline. It:

- Loads the trained model and daily input data
- Generates predictions per day
- Monitors model drift and performance over time
- Uses Prefect to schedule and monitor batch jobs

## 3. Project Structure
```
.
├── terraform /
│ ├── main.tf
│ ├── variables.tf
├── Development/
│ ├── codes/
│ ├── data/
│ ├── tests/
│ ├── pipeline_training.py
│ ├── params.yaml
│ ├── requirements.txt
│ ├── Makefile
│ ├── run_pipeline.sh
│ └── README.md ← explains development pipeline
├── Deployment/
│ ├── codes/
│ ├── config/
│ ├── dashboards/
│ ├── data/
│ ├── tests/
│ ├── monitoring_pipeline.py
│ ├── run_deployment.sh
│ ├── docker-compose.yaml
│ ├── params.yaml
│ ├── requirements.txt
│ ├── Makefile
│ └── README.md ← explains deployment + monitoring
└── README.md ← this file
```

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
| Language       | Python     |
| Workflow       | [Prefect](https://www.prefect.io) |
| Model Tracking | [MLflow](https://mlflow.org) |
| Model          | [LightGBM](https://lightgbm.readthedocs.io/en/latest/) |
| Tuning         | [Hyperopt](https://github.com/hyperopt/hyperopt) |
| Monitoring     | EvidentlyAI|
| Dashboard      | Grafana    |
| Testing        | `pytest` |
| Formatting     | `ruff` |
| Orchestration  | Shell + `make` |
| Storage        | Local / AWS S3 (for MLflow artifacts) |

---
