from __future__ import annotations

import json
import re
from typing import Any

from src.agent.schemas import validate_schema
from src.common.errors import JsonGuardError, SchemaError
from src.common.logging_utils import log_event


def default_repair_json(raw_text: str) -> str:
    """最小修复器：提取 JSON 主体 + 单引号替换 + 去尾逗号。"""
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return raw_text
    text = raw_text[start : end + 1]
    text = text.replace("'", '"')
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return text


def parse_with_guard(
    raw_text: str,
    schema: dict[str, Any],
    run_id: str,
    max_repair_rounds: int = 2,
) -> dict[str, Any]:
    err: Exception | None = None
    candidate = raw_text
    for attempt in range(max_repair_rounds + 1):
        try:
            data = json.loads(candidate)
            validate_schema(data, schema)
            return data
        except (json.JSONDecodeError, SchemaError) as exc:
            err = exc
            log_event(
                "WARNING",
                "json_guard_retry",
                run_id,
                module="json_guard",
                error_code=getattr(exc, "error_code", "JSON_PARSE_FAILED"),
                attempt=attempt + 1,
                reason=str(exc),
            )
            candidate = default_repair_json(candidate)

    raise JsonGuardError(f"parse failed after repair rounds: {err}", hint="check model output")
