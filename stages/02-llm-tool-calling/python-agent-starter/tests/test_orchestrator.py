from __future__ import annotations

from src.agent.orchestrator import run_with_repair
from src.agent.runtime import build_runtime


def test_orchestrator_mock_happy_path() -> None:
    replay = {
        "do calc": '{"final_answer":"calc","tool_call":{"tool_name":"calculator","args":{"expression":"2+3"}}}'
    }
    rt = build_runtime(replay=replay)
    ret = run_with_repair("do calc", "r1", rt.llm, rt.registry, rt.context)
    assert ret["ok"] is True
    assert ret["tool_output"]["result"] == 5.0


def test_orchestrator_recover_when_tool_failed() -> None:
    replay = {"unknown": '{"final_answer":"x","tool_call":{"tool_name":"unknown","args":{}}}'}
    rt = build_runtime(replay=replay)
    ret = run_with_repair("unknown", "r2", rt.llm, rt.registry, rt.context)
    assert ret["ok"] is False
    assert ret["tool_error_code"] == "TOOL_NOT_ALLOWED"
