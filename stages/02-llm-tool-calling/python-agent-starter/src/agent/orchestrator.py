from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.agent.llm_client import LLMClient
from src.agent.schemas import AGENT_OUTPUT_SCHEMA, TOOL_CALL_SCHEMA, validate_schema
from src.agent.tool_policy import ToolContext
from src.agent.tool_registry import ToolRegistry
from src.common.errors import JsonGuardError


@dataclass
class OrchestratorConfig:
    tool_timeout_seconds: float = 3.0


def run_once(
    prompt: str,
    run_id: str,
    llm: LLMClient,
    registry: ToolRegistry,
    context: ToolContext,
    cfg: OrchestratorConfig | None = None,
) -> dict[str, Any]:
    cfg = cfg or OrchestratorConfig()

    model_out = llm.generate_structured(prompt, AGENT_OUTPUT_SCHEMA, run_id)
    validate_schema(model_out["tool_call"], TOOL_CALL_SCHEMA)

    tool_name = model_out["tool_call"]["tool_name"]
    args = model_out["tool_call"]["args"]

    result = registry.invoke(
        tool_name, args, run_id, context, timeout_seconds=cfg.tool_timeout_seconds
    )
    if result.ok:
        return {
            "ok": True,
            "final_answer": model_out["final_answer"],
            "tool_name": tool_name,
            "tool_output": result.output,
        }

    # 恢复策略：失败时降级返回可解释错误。
    return {
        "ok": False,
        "final_answer": f"tool failed: {result.error_code}",
        "tool_name": tool_name,
        "tool_error_code": result.error_code,
        "tool_reason": result.reason,
    }


def run_with_repair(
    prompt: str,
    run_id: str,
    llm: LLMClient,
    registry: ToolRegistry,
    context: ToolContext,
) -> dict[str, Any]:
    try:
        return run_once(prompt, run_id, llm, registry, context)
    except JsonGuardError as exc:
        return {
            "ok": False,
            "final_answer": "json guard failed",
            "tool_error_code": exc.error_code,
            "tool_reason": str(exc),
        }
