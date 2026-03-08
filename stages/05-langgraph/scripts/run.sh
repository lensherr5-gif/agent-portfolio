#!/usr/bin/env bash
set -euo pipefail
uv sync --dev
uv run python -m pytest -q tests/test_graph.py
