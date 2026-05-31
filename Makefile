.PHONY: help install dev format lint test run clean docs

help:
	@echo "AlgoTrading Bot - Development Commands"
	@echo "======================================"
	@echo "make install     - Install dependencies"
	@echo "make dev         - Install dev dependencies"
	@echo "make format      - Format code with black and isort"
	@echo "make lint        - Run linting (flake8, pylint)"
	@echo "make type-check  - Run type checking with mypy"
	@echo "make test        - Run tests with pytest"
	@echo "make test-cov    - Run tests with coverage report"
	@echo "make run         - Run the trading bot"
	@echo "make backtest    - Run backtesting engine"
	@echo "make clean       - Remove build artifacts and cache"
	@echo "make docs        - Generate documentation"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 pylint mypy isort

format:
	black src/ tests/
	isort src/ tests/

lint:
	flake8 src/ tests/ --max-line-length=100
	pylint src/ --disable=C0111,C0103

type-check:
	mypy src/ --ignore-missing-imports

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

run:
	python src/main.py

backtest:
	python -m src.backtesting.backtest_engine

clean:
	find . -type f -name '*.py[cod]' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage

docs:
	@echo "Documentation commands to be added"

.DEFAULT_GOAL := help
