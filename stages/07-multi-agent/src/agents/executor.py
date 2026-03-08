from __future__ import annotations

from typing import Any


class AuthorizationError(Exception):
    pass


class Executor:
    def __init__(self, allowed_actions: set[str]) -> None:
        self.allowed_actions = allowed_actions

    def run(self, action: str, payload: dict[str, Any]) -> dict[str, Any]:
        if action not in self.allowed_actions:
            raise AuthorizationError(f"action not allowed: {action}")
        if payload.get("force_fail"):
            raise RuntimeError("executor failed")
        return {"status": "ok", "action": action, "payload": payload}
