# Makefile for M5 Forecasting Project

.PHONY: install test lint format clean run

# Create virtual environment and install dependencies
install:
	pip install -r requirements.txt

# Run all unit tests
test:
	PYTHONPATH=. pytest tests -v

# Check code formatting and linting (does NOT modify files)
lint:
	ruff check codes tests

# Auto-fix common issues (formatting, imports, etc.)
lint-fix:
	ruff check codes tests --fix

# Format code (like black/isort)
format:
	ruff format codes tests

# Clean pycache and temp files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete




# Run the pipeline
run:
	./start_prefect.sh
