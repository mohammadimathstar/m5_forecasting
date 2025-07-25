# Makefile for M5 Forecasting Project

.PHONY: install test lint format clean run clean-mlflow

# Create virtual environment and install dependencies
install:
	uv venv
	uv pip install -r requirements.txt

# Run all unit tests
test:
	uv pip install pytest && PYTHONPATH=. pytest tests -v

# Check code formatting and linting (does NOT modify files)
lint:
	uv pip install ruff && ruff check codes tests

# Auto-fix common issues (formatting, imports, etc.)
lint-fix:
	ruff check codes tests --fix

# Format code (like black/isort)
format:
	ruff format codes tests

# Clean pycache and temp files and prefect
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	
	
# Clean data folder and meta-data (in db)
clean-mlflow:
	sudo rm -r data
	sudo rm -r mlflow.db
	


# Run the pipeline
run:
	./run_pipeline.sh
