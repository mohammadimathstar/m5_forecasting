# Base image with Python and build tools
FROM python:3.12-slim

# Avoids writing .pyc files and buffers logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy entire project
COPY . .

# Install pip requirements first for caching
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make your script executable
RUN chmod +x run_deployment.sh

# Optional: run the pipeline on container start
CMD ["./run_deployment.sh"]


