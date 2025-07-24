# 🚀 Deployment: Batch Inference & Monitoring

This folder simulates a **production pipeline** where daily data is ingested, predictions are made using the trained model, and the model is monitored for drift and performance degradation.


---


## 🔄 Workflow

1. Load a trained model from MLflow or local disk
2. Simulate daily input data
3. Predict using the model
4. Log predictions and metrics
5. Monitor drift and update the dashboard


---

## 🚀 Features

- 📉 **Drift detection** using Evidently (e.g., sMAPE, MASE, data stats)
- 🛢 **PostgreSQL** for storing monitoring metrics
- 🔍 **Adminer** for database browsing
- 📊 **Grafana** for model monitoring dashboards
- ⚙️ **Prefect** to orchestrate the entire pipeline


---
## 📂 Structure

Deployment/
├── codes/
│ ├── db.py
│ ├── model.py
│ ├── prediction.py
│ ├── config.py
│ └── reporting.py
├── config/
├── dashboards/
├── data/
├── tests/
├── monitoring_pipeline.py
├── start_prefect_deployment.sh
├── docker-compose.yaml
├── params.yaml             # Pipeline configuration
├── .env.example            # Environment variables template (for AWS S3)
├── requirements.txt
├── Makefile                # Workflow automation
├── .gitignore
└── README.md ← this file



---

## 🔧 Setup Instructions

### 1. 📦 Install Python Dependencies

Create a virtual environment and install dependencies:

```bash
make install
```

Or manually:

```bash
pip install -r requirements.txt
```

### 2. 🌍 Environment Setup

Copy the .env.example and populate it:

```bash
cp .env.example .env
```

Update the following:

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` for S3 (MLflow)

Check `params.yaml`, and modify it accordingly.

### 3. 🐳 Start Services via Docker

This brings up:

- PostgreSQL

- Adminer (http://localhost:8080)

- Grafana (http://localhost:3000)

```bash
docker-compose up -d
```

### 4. 🚀 Start Deployment Pipeline
Start Prefect + Worker + Deploy:

```bash
bash start_prefect_deployment.sh
```

This script:

- Launches Prefect server

- Registers your pipeline as a Prefect deployment

- Starts a Prefect worker

- Run Inference + Monitoring

## Workflow

After deployment:, it follows the following workflow:

- Loads new data for a day (daily)

- Makes predictions (for the given day)

- Calculates metrics and drift (via Evidently)

- Saves evaluation reports (in PostgreSQL)

- Update the dashboard with the reports (in Grafana)


## 📊 Visualization & Monitoring

### 📉 Evidently

Drift metrics and distribution reports are automatically generated.

### 🗃 Adminer
To explore your PostgreSQL database (containing drift metrics):

```arduino
http://localhost:8080
```

Login :

- Username: postgres

- Password: example

- Database: test

### 📈 Grafana

To view monitoring dashboards:

```arduino
http://localhost:3000
```

Login (default):

- Username: admin

- Password: admin



