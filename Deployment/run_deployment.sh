#!/bin/bash

prefect init

prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

# Start server in background
prefect server start &

sleep 10

# Start worker in background
prefect worker start -p my-pool -t process &

sleep 5

# Run deployment command and automatically answer 'n' to prompt
echo "n" | prefect deploy monitoring_pipeline.py:monitor_model -n my-deployment -p my-pool

# Then run the pipeline deployment manually
prefect deployment run 'monitor-model/my-deployment'
