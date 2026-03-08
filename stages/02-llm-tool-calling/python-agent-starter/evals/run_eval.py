from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from src.agent.orchestrator import run_with_repair
from src.agent.runtime import build_runtime
from src.common.logging_utils import generate_run_id


def load_cases(base: Path, mode: str) -> list[dict[str, Any]]:
    files: list[Path]
    if mode == "smoke":
        files = [base / "smoke.json"]
    elif mode == "regression":
        files = [base / "regression.json"]
    elif mode == "adversarial":
        files = [base / "adversarial.json"]
    else:
        files = [base / "smoke.json", base / "regression.json", base / "adversarial.json"]

    out: list[dict[str, Any]] = []
    for f in files:
        out.extend(json.loads(f.read_text(encoding="utf-8")))
    return out


def run_eval(mode: str) -> dict[str, Any]:
    cases = load_cases(Path("evals/cases"), mode)
    replay = {case["prompt"]: case["llm_raw"] for case in cases}
    runtime = build_runtime(replay=replay)

    results: list[dict[str, Any]] = []
    parse_success = 0
    tool_success = 0
    repair_success = 0
    failures: Counter[str] = Counter()

    for case in cases:
        run_id = generate_run_id()
        ret = run_with_repair(
            case["prompt"], run_id, runtime.llm, runtime.registry, runtime.context
        )
        ok = bool(ret.get("ok"))
        expected_ok = bool(case.get("expect_ok", True))

        if "tool_name" in ret:
            parse_success += 1
        if ok:
            tool_success += 1
        raw = case["llm_raw"]
        if "'" in raw and ok:
            repair_success += 1

        if ok != expected_ok:
            failures[ret.get("tool_error_code", "EXPECTATION_MISMATCH")] += 1

        results.append({"id": case["id"], "ok": ok, "expected_ok": expected_ok, "ret": ret})

    total = len(cases)
    schema_valid_rate = parse_success / total if total else 0.0
    tool_success_rate = tool_success / total if total else 0.0
    auto_repair_rate = repair_success / total if total else 0.0
    success_rate = sum(1 for r in results if r["ok"] == r["expected_ok"]) / total if total else 0.0

    return {
        "mode": mode,
        "total": total,
        "success_rate": success_rate,
        "schema_valid_rate": schema_valid_rate,
        "tool_success_rate": tool_success_rate,
        "auto_repair_success_rate": auto_repair_rate,
        "top_failures": failures.most_common(3),
    }


def write_report(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Eval Report",
        "",
        f"- mode: `{summary['mode']}`",
        f"- total: `{summary['total']}`",
        f"- success_rate: `{summary['success_rate']:.2%}`",
        f"- schema_valid_rate: `{summary['schema_valid_rate']:.2%}`",
        f"- tool_success_rate: `{summary['tool_success_rate']:.2%}`",
        f"- auto_repair_success_rate: `{summary['auto_repair_success_rate']:.2%}`",
        "",
        "## Top3 Failures",
    ]
    if not summary["top_failures"]:
        lines.append("- none")
    else:
        for code, cnt in summary["top_failures"]:
            lines.append(f"- `{code}`: {cnt}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", default="all", choices=["all", "smoke", "regression", "adversarial"]
    )
    parser.add_argument("--report", default="reports/eval_report.md")
    args = parser.parse_args()

    summary = run_eval(args.mode)
    write_report(Path(args.report), summary)
    print(json.dumps(summary, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
