from __future__ import annotations

import os
from dataclasses import dataclass

from src.agent.llm_client import LLMClient
from src.agent.tool_policy import ToolContext
from src.agent.tool_registry import ToolRegistry, ToolSpec
from src.tools import calculator, web_search_mock, write_file_guarded


@dataclass
class Runtime:
    llm: LLMClient
    registry: ToolRegistry
    context: ToolContext


def build_runtime(replay: dict[str, str] | None = None) -> Runtime:
    mode = os.getenv("LLM_MODE", "mock").strip() or "mock"
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    confirm = os.getenv("SENSITIVE_TOOL_CONFIRM", "false").lower() == "true"

    llm = LLMClient(mode=mode, model=model, replay=replay or {})
    reg = ToolRegistry(allowlist={"calculator", "web_search_mock", "write_file_guarded"})

    reg.register(
        ToolSpec(
            name="calculator",
            input_schema={
                "type": "object",
                "required": ["expression"],
                "properties": {"expression": {"type": "string"}},
            },
            output_schema={
                "type": "object",
                "required": ["result"],
                "properties": {"result": {"type": "number"}},
            },
            risk_level="low",
        ),
        calculator.run,
    )
    reg.register(
        ToolSpec(
            name="web_search_mock",
            input_schema={
                "type": "object",
                "required": ["query"],
                "properties": {"query": {"type": "string"}},
            },
            output_schema={
                "type": "object",
                "required": ["query", "items"],
                "properties": {
                    "query": {"type": "string"},
                    "items": {"type": "array"},
                },
            },
            risk_level="low",
        ),
        web_search_mock.run,
    )
    reg.register(
        ToolSpec(
            name="write_file_guarded",
            input_schema={
                "type": "object",
                "required": ["path", "content"],
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
            },
            output_schema={
                "type": "object",
                "required": ["path", "bytes"],
                "properties": {
                    "path": {"type": "string"},
                    "bytes": {"type": "number"},
                },
            },
            risk_level="high",
        ),
        write_file_guarded.run,
    )

    return Runtime(llm=llm, registry=reg, context=ToolContext(confirm_sensitive=confirm))
