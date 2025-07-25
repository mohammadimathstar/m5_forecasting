# 🛠 Development: Model Training Pipeline

An end-to-end machine learning pipeline for training a sales forecasting model using the M5 dataset. Built with modular components using **LightGBM**, **Hyperopt**, **Prefect**, and **MLflow**, the pipeline supports data ingestion, feature engineering, hyperparameter optimisation, and model training with custom evaluation metrics.


---


## 🔄 Workflow

1. Load and preprocess data
2. Perform feature engineering
3. Split data into train/validation/test sets (save validation/test sets in an S3 bucket)
4. Run hyperparameter tuning with Hyperopt
5. Train a LightGBM model

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
│ ├── feature_engineering.py
│ ├── best_model.py
│ ├── config.py
│ ├── data_handling/
│ ├── tuning/
│ ├── metrics/
│ └── models/
├── tests/                  # Unit tests
├── data/
├── pipeline_training.py
├── params.yaml             # Pipeline configuration
├── requirements.txt
├── Makefile                # Workflow automation
├── run_pipeline.sh
├── Dockerfile
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

### 2. Create AWS infrastructure

Before running this workflow, you need to create infrastructures in AWS (see the Terraform folder).

**Note**. As we use S3 AWS, you should set the credentials, i.e. `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY`.


### 3. 📁 Data

As we use the data from Kaggle, you need to setup your Kaggle credentials:

- Go to https://www.kaggle.com/account

- Go to Setting > API, click "Create New API Token"

- This will download a file named `kaggle.json`

- Move it to your home directory under .kaggle/:

```bash
mkdir -p ~/.kaggle
mv /path/to/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

---

## 🚀 Running the Pipeline 

You can run the pipeline in two ways:

### Way 1. Running without Make and Docker

Follow these steps to run the M5 forecasting pipeline:

#### 1. Create and activate a virtual environment and then install dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

#### 2. Run the pipeline

You can run the pipeline using `run_pipeline.sh` 

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

It opens a menu. You can select `Store code on a local filesystem` for simplicity.

- If you use `S3`, make sure that you enter a valid bucket name (check `terraform/main.tf`)

### Way 2. Running by make

#### 1. Create and activate a virtual environment and then install dependencies

```bash
make install
source .venv/bin/activate
```

#### 2. Run the pipeline

You can run the pipeline using `run_pipeline.sh` 

```bash
chmod +x run_pipeline.sh
make run
```

It opens a menu. You can select `Store code on a local filesystem`.

### Way 3. Running By Docker

The pipeline can be run in a container, using Docker. 

```bash
# Build the Docker image
docker build -t m5-pipeline-dev .

# Run an interactive container
docker run -it \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -v $(pwd):/app \
  -v $HOME/.kaggle:/root/.kaggle \
  -p 5000:5000 -p 4200:4200 \
  --name m5-dev \
  m5-pipeline-dev
```

It opens a menu. You can select `Store code on a local filesystem`.

---

### MLflow

To track the experiment, we use Mlflow. You can modify its configuration in `run_pipeline.sh` script:

- backend-store-uri: the location for storing the meta-data, such as metrics, hyperparameters and etc. Here, we use sqlite.

- default-artifact-root: the location for storing the final model with its artifacts. Here, we use AWS S3.

- host and port: to see the experiment runs (default is `localhost:5000`)

Note. You must create the S3 bucket before running the script.

![Mlflow](pics/mlflow-training.png)

----

### Prefect

To see the progress of the workflow, you can open:
```bash
localhost:4200
```
and click on `Runs` tab.


![Prefect](pics/prefect-training.png)



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

- `make run`
  To run the pipeline.

- `make clean`  
  Removes Python bytecode files (`__pycache__`, `.pyc`, `.pyo`) to keep the repo clean.



