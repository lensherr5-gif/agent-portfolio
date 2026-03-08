from __future__ import annotations

from pathlib import Path

from evals.run_eval import run_eval, write_report


def test_eval_runner_generates_summary() -> None:
    summary = run_eval("smoke")
    assert summary["total"] >= 1
    assert 0.0 <= summary["success_rate"] <= 1.0


def test_eval_report_written(tmp_path: Path) -> None:
    summary = run_eval("smoke")
    report = tmp_path / "eval_report.md"
    write_report(report, summary)
    content = report.read_text(encoding="utf-8")
    assert "# Eval Report" in content
