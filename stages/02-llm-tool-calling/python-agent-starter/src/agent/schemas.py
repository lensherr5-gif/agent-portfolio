from __future__ import annotations

from typing import Any

from src.common.errors import SchemaError


TOOL_CALL_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["tool_name", "args"],
    "properties": {
        "tool_name": {"type": "string"},
        "args": {"type": "object"},
    },
}

AGENT_OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["final_answer", "tool_call"],
    "properties": {
        "final_answer": {"type": "string"},
        "tool_call": {
            "type": "object",
            "required": ["tool_name", "args"],
            "properties": {
                "tool_name": {"type": "string"},
                "args": {"type": "object"},
            },
        },
    },
}


def _type_ok(value: Any, expected: str) -> bool:
    mapping = {
        "string": str,
        "object": dict,
        "number": (int, float),
        "boolean": bool,
        "array": list,
    }
    py_type = mapping.get(expected)
    if py_type is None:
        return False
    return isinstance(value, py_type)


def validate_schema(data: Any, schema: dict[str, Any], *, path: str = "$") -> None:
    if schema.get("type") == "object":
        if not isinstance(data, dict):
            raise SchemaError(f"{path} must be object")

        for key in schema.get("required", []):
            if key not in data:
                raise SchemaError(f"{path}.{key} is required")

        for key, prop in schema.get("properties", {}).items():
            if key not in data:
                continue
            expected = prop.get("type")
            if expected and not _type_ok(data[key], expected):
                raise SchemaError(f"{path}.{key} must be {expected}")
            if expected == "object":
                validate_schema(data[key], prop, path=f"{path}.{key}")
