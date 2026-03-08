from __future__ import annotations

import pytest

from src.agent.json_guard import parse_with_guard
from src.agent.schemas import AGENT_OUTPUT_SCHEMA
from src.common.errors import JsonGuardError


def test_json_guard_schema_pass() -> None:
    raw = '{"final_answer":"ok","tool_call":{"tool_name":"calculator","args":{"expression":"1+1"}}}'
    out = parse_with_guard(raw, AGENT_OUTPUT_SCHEMA, run_id="r1")
    assert out["tool_call"]["tool_name"] == "calculator"


def test_json_guard_repair_success() -> None:
    raw = "noise {'final_answer':'ok','tool_call':{'tool_name':'calculator','args':{'expression':'1+1',}}} trailer"
    out = parse_with_guard(raw, AGENT_OUTPUT_SCHEMA, run_id="r2")
    assert out["final_answer"] == "ok"


def test_json_guard_repair_failed() -> None:
    with pytest.raises(JsonGuardError):
        parse_with_guard("not json", AGENT_OUTPUT_SCHEMA, run_id="r3", max_repair_rounds=1)
