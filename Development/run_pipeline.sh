#!/bin/bash


# Start Mlflow
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://mlflow-artifacts-bucket-m5/ \
  --host 0.0.0.0 \
  --port 5000 > mlflow.log 2>&1 &

sleep 5

prefect init 

prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

# Start server in background
prefect server start &

sleep 10

# Start worker in background
prefect worker start -p mypool -t process &

sleep 5

# Run deployment command and automatically answer 'n' to prompt
echo "n" | prefect deploy pipeline_training.py:m5_pipeline -n mydeployment -p mypool

# Then run the pipeline deployment manually
prefect deployment run 'm5_pipeline/mydeployment'
