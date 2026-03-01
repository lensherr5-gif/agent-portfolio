.PHONY: help sync run test test-v lint format precommit-install

help:
	@echo "Targets: sync run test test-v lint format precommit-install"

sync:
	uv sync --dev

run:
	uv run python -m app

test:
	uv run python -m pytest -q

test-v:
	uv run python -m pytest -v

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .

precommit-install:
	uv run pre-commit install
