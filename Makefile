.PHONY: help install run dev clean test lint format check env setup pre-commit-install pre-commit-run pre-commit-all

# Variables
BACKEND_DIR = backend
PYTHON = poetry run python
UVICORN = poetry run uvicorn
HOST = 0.0.0.0
PORT = 8000

# Default target
help:
	@echo "FitLife - Available commands:"
	@echo ""
	@echo "  make install    - Install dependencies using Poetry"
	@echo "  make setup      - Complete setup (install + create .env)"
	@echo "  make run        - Run the application in production mode"
	@echo "  make dev        - Run the application with auto-reload (development)"
	@echo "  make shell      - Open Poetry shell"
	@echo "  make test       - Run tests (when implemented)"
	@echo "  make lint       - Run linting checks (ruff, mypy)"
	@echo "  make format     - Format code with black and isort"
	@echo "  make check      - Run all checks (lint + test)"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make pre-commit-run     - Run pre-commit on staged files"
	@echo "  make pre-commit-all     - Run pre-commit on all files"
	@echo "  make env        - Create .env file from template"
	@echo "  make clean      - Remove cache files and build artifacts"
	@echo "  make clean-all  - Remove cache files, build artifacts, and venv"
	@echo ""

# Installation
install:
	@echo "Installing dependencies..."
	cd $(BACKEND_DIR) && poetry install --no-root

# Complete setup
setup: install env
	@echo "Setup complete!"
	@echo "Please edit $(BACKEND_DIR)/.env and set your SECRET_KEY"
	@echo "Generate a secret key with: openssl rand -hex 32"

# Create .env from template
env:
	@if [ ! -f $(BACKEND_DIR)/.env ]; then \
		echo "Creating .env file from template..."; \
		cp $(BACKEND_DIR)/.env.templates $(BACKEND_DIR)/.env; \
		echo ".env file created. Please update with your settings."; \
	else \
		echo ".env file already exists."; \
	fi

# Run application
run:
	@echo "Starting FitLife API..."
	cd $(BACKEND_DIR) && PYTHONPATH=src $(UVICORN) fitlife.main:app --host $(HOST) --port $(PORT)

# Run application in development mode with auto-reload
dev:
	@echo "Starting FitLife API in development mode..."
	cd $(BACKEND_DIR) && PYTHONPATH=src $(UVICORN) fitlife.main:app --reload --host $(HOST) --port $(PORT)

# Open Poetry shell
shell:
	cd $(BACKEND_DIR) && poetry shell

# Run tests
test:
	@echo "Running tests..."
	cd $(BACKEND_DIR) && PYTHONPATH=src $(PYTHON) -m pytest tests/ -v

# Linting
lint:
	@echo "Running linting checks..."
	cd $(BACKEND_DIR) && poetry run ruff check src/ tests/
	cd $(BACKEND_DIR) && poetry run mypy src/

# Format code
format:
	@echo "Formatting code..."
	cd $(BACKEND_DIR) && poetry run black src/ tests/
	cd $(BACKEND_DIR) && poetry run isort src/ tests/
	cd $(BACKEND_DIR) && poetry run ruff format src/ tests/

# Pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	cd $(BACKEND_DIR) && poetry run pre-commit install
	@echo "Pre-commit hooks installed!"

pre-commit-run:
	@echo "Running pre-commit on staged files..."
	cd $(BACKEND_DIR) && poetry run pre-commit run

pre-commit-all:
	@echo "Running pre-commit on all files..."
	cd $(BACKEND_DIR) && poetry run pre-commit run --all-files

# Run all checks
check: lint test
	@echo "All checks complete!"

# Clean cache and build artifacts
clean:
	@echo "Cleaning cache files and build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "Clean complete!"

# Clean everything including virtual environment
clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf $(BACKEND_DIR)/.venv
	@echo "Clean all complete!"

# Development utilities
.PHONY: docs update-deps add-dep info

# Open API documentation in browser
docs:
	@echo "API documentation available at:"
	@echo "  Swagger UI: http://localhost:$(PORT)/api/v1/docs"
	@echo "  ReDoc:      http://localhost:$(PORT)/api/v1/redoc"
	@echo ""
	@echo "Make sure the server is running with 'make dev' or 'make run'"

# Update dependencies
update-deps:
	@echo "Updating dependencies..."
	cd $(BACKEND_DIR) && poetry update

# Add a new dependency (usage: make add-dep DEP=package-name)
add-dep:
	@if [ -z "$(DEP)" ]; then \
		echo "Usage: make add-dep DEP=package-name"; \
		exit 1; \
	fi
	cd $(BACKEND_DIR) && poetry add $(DEP)

# Show project info
info:
	@echo "FitLife Project Information"
	@echo "==========================="
	@echo "Backend directory: $(BACKEND_DIR)"
	@echo "Python: $(PYTHON)"
	@echo "Server: $(HOST):$(PORT)"
	@echo ""
	@echo "Installed packages:"
	@cd $(BACKEND_DIR) && poetry show --tree
