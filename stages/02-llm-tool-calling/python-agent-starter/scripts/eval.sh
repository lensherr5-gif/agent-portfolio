#!/usr/bin/env bash
set -euo pipefail
uv run python -m evals.run_eval --mode all --report reports/eval_report.md
