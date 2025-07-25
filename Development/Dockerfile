# Base image with Python and build tools
FROM python:3.12-slim

# Avoids writing .pyc files and buffers logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements first for caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make kaggle directory
RUN mkdir -p /root/.kaggle

# Copy entire project
COPY . .

# Prefect & MLflow ports (optional)
EXPOSE 4200 5000

# Make your script executable
RUN chmod +x run_pipeline.sh

# Optional: run the pipeline on container start
CMD ["./run_pipeline.sh"]


