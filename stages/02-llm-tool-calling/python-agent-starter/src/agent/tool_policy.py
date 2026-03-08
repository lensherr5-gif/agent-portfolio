from __future__ import annotations

from dataclasses import dataclass

from src.common.errors import ToolPolicyError


@dataclass
class ToolContext:
    confirm_sensitive: bool = False


def check_policy(tool_name: str, risk_level: str, context: ToolContext) -> None:
    if risk_level == "high" and not context.confirm_sensitive:
        raise ToolPolicyError(
            f"tool '{tool_name}' blocked by policy",
            hint="set confirm_sensitive=true",
        )
