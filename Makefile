.PHONY: lint, install, update

HOST = 0.0.0.0
PORT = 8000

lint:
	pre-commit run -a

install:
	pre-commit uninstall && pre-commit install && pre-commit install-hooks

update:
	pre-commit autoupdate

run-dev:
	cd backend && PYTHONPATH=src poetry run uvicorn fitlife.main:app --reload --host $(HOST) --port $(PORT)
