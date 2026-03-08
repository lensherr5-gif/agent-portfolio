#!/usr/bin/env bash
set -euo pipefail
uv sync --dev
uv run python scripts/run_eval.py --dataset-dir evals --report reports/eval_report.md
