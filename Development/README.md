# 🛠 Development: Model Training Pipeline

An end-to-end machine learning pipeline for training a sales forecasting model using the M5 dataset. Built with modular components using **LightGBM**, **Hyperopt**, **Prefect**, and **MLflow**, the pipeline supports data ingestion, feature engineering, hyperparameter optimization, and model training with custom evaluation metrics.


---


## 🔄 Workflow

1. Load and preprocess data
2. Perform feature engineering
3. Run hyperparameter tuning with Hyperopt
4. Train a LightGBM model

---

## 🚀 Features

- ✅ Modular pipeline architecture using [Prefect](https://docs.prefect.io/)
- 🔁 Full feature engineering: lag features, rolling stats, calendar joins
- 🧪 Hyperparameter tuning via [Hyperopt](https://github.com/hyperopt/hyperopt)
- 📊 Custom metrics: sMAPE and MASE
- 📝 Experiment tracking with [MLflow](https://mlflow.org/)
- 🧼 Testable, maintainable, and MLOps-ready
- 📦 Lightweight with YAML-configured parameters

---

## 📂 Structure

```
development/
├── codes/
│ ├── data_loader.py
│ ├── feature_engineering.py
│ ├── best_model.py
│ ├── config.py
│ ├── tuning/
│ ├── metrics/
│ └── models/
├── tests/                  # Unit tests
├── data/
├── pipeline_training.py
├── params.yaml             # Pipeline configuration
├── .env.example # Environment variables template
├── requirements.txt
├── Makefile                # Workflow automation
├── start_prefect.sh
├── .gitignore
└── README.md ← this file
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/mohammadimathstar/m5-forecasting.git
cd m5-forecasting/Development
```

### 2. Install dependencies

```bash
uv venv
uv pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Then edit `.env` with your credentials (for using S3)
```


### 📁 Data

- Place the original `sales_train_validation.csv`, `calendar.csv`, and `sell_prices.csv` inside: `data/raw/`

- Processed features and `test/reference` sets will be saved in: `data/processed/`



## 🚀 Running the Pipeline (with make)

Follow these steps to run the M5 forecasting pipeline locally:

#### 1. Install dependencies

```bash
uv venv
uv pip install -r requirements.txt
source .venv/bin/activate
```

#### 2. Run the pipeline

You can run the pipeline using `run_pipeline.sh` 

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

You need to start the Mlflow server:

```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://mlflow-artifacts-bucket-m5/ \
  --host 0.0.0.0 \
  --port 5000
```

Note. Here I use S3 (AWS) to save the model (I assume the bucket `mlflow-artifacts-bucket-m5` has already existed) (see params.yaml).


#### 3. Prepare the environment variables (if any)

If your project requires environment variables, create a .env file or export them manually:

```bash
export PREFECT_API_URL=http://127.0.0.1:4200/api
# or use your .env file setup instructions here
```

#### 4. Start Prefect server and worker (in separate terminals or using scripts)

You need to start the Prefect server and a worker to run the flow.

In Terminal 1:

```bash
prefect server start
```

In Terminal 2:

```bash
prefect worker start -p my-pool -t process
```


Note. For this you need to first in your terminal window write:

```bash
chmod +x start_prefect.sh
```

#### 5. Deploy the pipeline

Register the pipeline flow to Prefect:

```bash
prefect deployment create pipeline_training.py:m5_pipeline -n my-deployment -p my-pool
```

#### 6. Run the pipeline

Trigger the pipeline run:

```bash
prefect deployment run 'm5_pipeline/my-deployment'
```

#### Optional: Running the entire workflow with a script

You can automate steps 2–6 with a shell script:

```bash
chmod +x start_prefect.sh
./run_pipeline.sh
```



### 📦 Makefile Commands

- `make install`  
  Installs all required Python dependencies listed in `requirements.txt`.

- `make test`  
  Runs all unit tests using `pytest` to verify code correctness.

- `make lint`  
  Checks code style and quality using `ruff`, `black`, and `isort`.  
  *Note:* This command **checks** formatting and reports issues but does **not** modify the code.

- `make lint-fix`  
  Automatically fixes linting and formatting issues with `ruff`.

- `make format`  
  Formats code using `ruff`.

- `make clean`  
  Removes Python bytecode files (`__pycache__`, `.pyc`, `.pyo`) to keep the repo clean.


