.PHONY: lint, install, update, backend, frontend, run-dev, install-pre-commit, install-backend, install-frontend, tests

lint:
	cd backend && \
	poetry run pre-commit run -a

install-pre-commit:
	pre-commit uninstall && \
	pre-commit install && \
	pre-commit install-hooks

install-backend:
	cd backend && \
	poetry install --no-root

install-frontend:
	cd frontend && \
	npm install

test-frontend:
	cd frontend && \
	k6 run tests/test-basic.js

test-backend:
	cd backend && \
	PYTHONPATH=src poetry run pytest

install: install-backend install-pre-commit install-frontend

tests: test-backend test-frontend

update:
	pre-commit autoupdate

run-dev: backend frontend

backend:
	docker compose -f docker/docker-compose.dev.yaml down && \
	docker compose -f docker/docker-compose.dev.yaml up -d && \
	cd backend && \
	PYTHONPATH=src poetry run python src/fitlife/main.py

frontend:
	cd frontend && npm run dev
