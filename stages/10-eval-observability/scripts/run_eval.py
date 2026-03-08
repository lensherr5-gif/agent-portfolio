from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path
from typing import Any


def simulate_agent(case: dict[str, Any]) -> dict[str, Any]:
    query = case["query"].lower()
    started = time.monotonic()

    # 这里用可重复的规则模拟失败分类，便于离线演示评估流水线。
    if "schema" in query:
        result = {"ok": False, "error_type": "schema_error", "schema_valid": False, "tool_ok": False}
    elif "timeout" in query:
        result = {"ok": False, "error_type": "tool_timeout", "schema_valid": True, "tool_ok": False}
    elif "retrieval miss" in query:
        result = {"ok": False, "error_type": "retrieval_miss", "schema_valid": True, "tool_ok": True}
    elif "policy" in query:
        result = {"ok": False, "error_type": "policy_block", "schema_valid": True, "tool_ok": False}
    else:
        result = {"ok": True, "error_type": None, "schema_valid": True, "tool_ok": True}

    result["latency_ms"] = int((time.monotonic() - started) * 1000) + 20
    return result


def load_cases(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(dataset_dir: str) -> dict[str, Any]:
    base = Path(dataset_dir)
    all_cases: list[dict[str, Any]] = []
    for name in ["smoke.json", "regression.json", "adversarial.json"]:
        all_cases.extend(load_cases(base / name))

    results = [simulate_agent(case) for case in all_cases]
    total = len(results)
    success = sum(1 for r in results if r["ok"])
    schema_valid = sum(1 for r in results if r["schema_valid"])
    tool_ok = sum(1 for r in results if r["tool_ok"])
    latencies = [r["latency_ms"] for r in results]

    failure_counts: dict[str, int] = {
        "schema_error": 0,
        "tool_timeout": 0,
        "retrieval_miss": 0,
        "policy_block": 0,
    }
    for r in results:
        if r["error_type"]:
            failure_counts[r["error_type"]] += 1

    return {
        "total": total,
        "success_rate": round(success / total, 3),
        "schema_valid_rate": round(schema_valid / total, 3),
        "tool_success_rate": round(tool_ok / total, 3),
        "avg_latency_ms": round(statistics.mean(latencies), 2),
        "p95_latency_ms": sorted(latencies)[max(int(total * 0.95) - 1, 0)],
        "failure_counts": failure_counts,
    }


def write_report(metrics: dict[str, Any], report_path: str) -> None:
    top_failure = max(metrics["failure_counts"], key=lambda k: metrics["failure_counts"][k])
    content = f"""# Eval Report

- total: {metrics['total']}
- success_rate: {metrics['success_rate']}
- schema_valid_rate: {metrics['schema_valid_rate']}
- tool_success_rate: {metrics['tool_success_rate']}
- avg_latency_ms: {metrics['avg_latency_ms']}
- p95_latency_ms: {metrics['p95_latency_ms']}

## Failure Counts

- schema_error: {metrics['failure_counts']['schema_error']}
- tool_timeout: {metrics['failure_counts']['tool_timeout']}
- retrieval_miss: {metrics['failure_counts']['retrieval_miss']}
- policy_block: {metrics['failure_counts']['policy_block']}

Top failure: {top_failure}
"""
    Path(report_path).write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", default="evals")
    parser.add_argument("--report", default="reports/eval_report.md")
    args = parser.parse_args()

    metrics = evaluate(args.dataset_dir)
    write_report(metrics, args.report)
    print(json.dumps(metrics, ensure_ascii=True))


if __name__ == "__main__":
    main()
