from __future__ import annotations

from src.agent.tool_policy import ToolContext
from src.agent.tool_registry import ToolRegistry, ToolSpec


def _echo(args: dict[str, object]) -> dict[str, object]:
    return {"x": args["x"]}


def test_allowlist_and_schema() -> None:
    reg = ToolRegistry(allowlist={"echo"})
    reg.register(
        ToolSpec(
            name="echo",
            input_schema={
                "type": "object",
                "required": ["x"],
                "properties": {"x": {"type": "number"}},
            },
            output_schema={
                "type": "object",
                "required": ["x"],
                "properties": {"x": {"type": "number"}},
            },
        ),
        _echo,
    )

    ok = reg.invoke("echo", {"x": 1}, "r1", ToolContext(confirm_sensitive=True))
    assert ok.ok is True

    bad = reg.invoke("echo", {"x": "oops"}, "r2", ToolContext(confirm_sensitive=True))
    assert bad.ok is False
    assert bad.error_code == "SCHEMA_ERROR"


def test_policy_block_high_risk_tool() -> None:
    reg = ToolRegistry(allowlist={"danger"})
    reg.register(
        ToolSpec(
            name="danger",
            input_schema={"type": "object", "properties": {}, "required": []},
            output_schema={"type": "object", "properties": {}, "required": []},
            risk_level="high",
        ),
        lambda _args: {},
    )
    ret = reg.invoke("danger", {}, "r3", ToolContext(confirm_sensitive=False))
    assert ret.ok is False
    assert ret.error_code == "POLICY_BLOCKED"
