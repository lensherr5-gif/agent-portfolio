from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from dataclasses import dataclass
from typing import Any, Callable

from src.agent.schemas import validate_schema
from src.agent.tool_policy import ToolContext, check_policy
from src.common.errors import SchemaError, ToolExecutionError, ToolPolicyError, ToolTimeoutError
from src.common.logging_utils import digest_obj, log_event


@dataclass
class ToolSpec:
    name: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    risk_level: str = "low"


@dataclass
class ToolResult:
    ok: bool
    output: dict[str, Any] | None = None
    error_code: str | None = None
    reason: str | None = None


class ToolRegistry:
    def __init__(self, allowlist: set[str]) -> None:
        self.allowlist = allowlist
        self._specs: dict[str, ToolSpec] = {}
        self._handlers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}

    def register(self, spec: ToolSpec, handler: Callable[[dict[str, Any]], dict[str, Any]]) -> None:
        self._specs[spec.name] = spec
        self._handlers[spec.name] = handler

    def invoke(
        self,
        tool_name: str,
        args: dict[str, Any],
        run_id: str,
        context: ToolContext,
        timeout_seconds: float = 3.0,
    ) -> ToolResult:
        start = time.perf_counter()
        if tool_name not in self.allowlist:
            return ToolResult(ok=False, error_code="TOOL_NOT_ALLOWED", reason=tool_name)

        spec = self._specs.get(tool_name)
        handler = self._handlers.get(tool_name)
        if spec is None or handler is None:
            return ToolResult(ok=False, error_code="TOOL_NOT_FOUND", reason=tool_name)

        try:
            check_policy(tool_name, spec.risk_level, context)
            validate_schema(args, spec.input_schema)

            with ThreadPoolExecutor(max_workers=1) as ex:
                fut = ex.submit(handler, args)
                out = fut.result(timeout=timeout_seconds)

            validate_schema(out, spec.output_schema)
            latency = int((time.perf_counter() - start) * 1000)
            log_event(
                "INFO",
                "tool_invoked",
                run_id,
                module="tool_registry",
                tool_name=tool_name,
                event="success",
                error_code="",
                attempt=1,
                latency_ms=latency,
                args_digest=digest_obj(args),
                result_digest=digest_obj(out),
            )
            return ToolResult(ok=True, output=out)
        except FuturesTimeout as exc:
            err = ToolTimeoutError()
            return self._fail(run_id, tool_name, args, start, err.error_code, str(err), exc)
        except ToolPolicyError as exc:
            return self._fail(run_id, tool_name, args, start, exc.error_code, str(exc), exc)
        except SchemaError as exc:
            return self._fail(run_id, tool_name, args, start, exc.error_code, str(exc), exc)
        except Exception as exc:  # noqa: BLE001
            err = ToolExecutionError(str(exc))
            return self._fail(run_id, tool_name, args, start, err.error_code, str(err), exc)

    def _fail(
        self,
        run_id: str,
        tool_name: str,
        args: dict[str, Any],
        start: float,
        error_code: str,
        reason: str,
        exc: Exception,
    ) -> ToolResult:
        latency = int((time.perf_counter() - start) * 1000)
        log_event(
            "ERROR",
            "tool_invoked",
            run_id,
            module="tool_registry",
            tool_name=tool_name,
            event="failed",
            error_code=error_code,
            attempt=1,
            latency_ms=latency,
            args_digest=digest_obj(args),
            result_digest="",
            reason=reason,
        )
        return ToolResult(ok=False, error_code=error_code, reason=reason)
