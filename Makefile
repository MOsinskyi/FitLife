.PHONY: help install run dev clean test lint format check env setup

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
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code with black and isort"
	@echo "  make check      - Run all checks (lint + test)"
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

# Run tests (placeholder for future implementation)
test:
	@echo "Running tests..."
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest tests/ -v || echo "No tests found yet"

# Linting
lint:
	@echo "Running linting checks..."
	cd $(BACKEND_DIR) && $(PYTHON) -m flake8 src/ || echo "flake8 not installed"
	cd $(BACKEND_DIR) && $(PYTHON) -m mypy src/ || echo "mypy not installed"

# Format code
format:
	@echo "Formatting code..."
	cd $(BACKEND_DIR) && $(PYTHON) -m black src/ || echo "black not installed"
	cd $(BACKEND_DIR) && $(PYTHON) -m isort src/ || echo "isort not installed"

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