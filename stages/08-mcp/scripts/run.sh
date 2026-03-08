#!/usr/bin/env bash
set -euo pipefail
uv sync --dev
uv run python -m pytest -q mcp-server/tests/test_server.py
