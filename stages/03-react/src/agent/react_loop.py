from __future__ import annotations

import json
import random
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


class ReactLoopError(Exception):
    pass


class PolicyError(ReactLoopError):
    pass


class ToolExecutionError(ReactLoopError):
    pass


@dataclass
class ReactConfig:
    max_steps: int = 5
    timeout_seconds: float = 8.0
    max_failures: int = 2
    deterministic_seed: int | None = None


class ReactLoop:
    """A minimal think -> act -> observe -> decide loop with guardrails."""

    def __init__(self, tools: dict[str, Callable[[dict[str, Any]], Any]], run_dir: str = "runs") -> None:
        self.tools = tools
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        task: str,
        planner: Callable[[dict[str, Any]], dict[str, Any]],
        *,
        run_id: str | None = None,
        allowlist: set[str] | None = None,
        config: ReactConfig | None = None,
    ) -> dict[str, Any]:
        cfg = config or ReactConfig()
        if cfg.deterministic_seed is not None:
            random.seed(cfg.deterministic_seed)

        started_at = time.monotonic()
        rid = run_id or str(uuid.uuid4())
        allow = allowlist or set(self.tools.keys())
        state: dict[str, Any] = {
            "run_id": rid,
            "task": task,
            "steps": [],
            "status": "running",
            "failure_taxonomy": None,
        }

        failures = 0
        for step_idx in range(1, cfg.max_steps + 1):
            # 全局超时护栏：超过预算直接终止，避免无限循环。
            if time.monotonic() - started_at > cfg.timeout_seconds:
                state["status"] = "timeout"
                state["failure_taxonomy"] = "execution_timeout"
                break

            try:
                plan = planner(state)
            except Exception as exc:  # pragma: no cover - defensive
                state["status"] = "failed"
                state["failure_taxonomy"] = "planning_error"
                state["error"] = str(exc)
                break

            thought = str(plan.get("thought", ""))
            action = plan.get("action")
            if action == "finish":
                answer = str(plan.get("answer", ""))
                state["steps"].append(
                    {
                        "step": step_idx,
                        "thought": thought,
                        "action": "finish",
                        "observation": answer,
                        "latency_ms": 0,
                    }
                )
                state["status"] = "succeeded"
                state["answer"] = answer
                break

            if action != "tool":
                # 规划输出动作不合法，归类为 planning_error。
                state["status"] = "failed"
                state["failure_taxonomy"] = "planning_error"
                state["error"] = f"invalid action: {action}"
                break

            tool_name = plan.get("tool")
            args = plan.get("args", {})
            if tool_name not in allow:
                raise PolicyError(f"tool not allowed: {tool_name}")
            if tool_name not in self.tools:
                raise PolicyError(f"tool missing: {tool_name}")
            if not isinstance(args, dict):
                raise ReactLoopError("tool args must be dict")

            tool_start = time.monotonic()
            try:
                observation = self.tools[tool_name](args)
                latency_ms = int((time.monotonic() - tool_start) * 1000)
                state["steps"].append(
                    {
                        "step": step_idx,
                        "thought": thought,
                        "action": tool_name,
                        "args": args,
                        "observation": observation,
                        "latency_ms": latency_ms,
                    }
                )
                failures = 0
            except Exception as exc:
                # 工具连续失败达到阈值后终止，避免无意义重试。
                failures += 1
                latency_ms = int((time.monotonic() - tool_start) * 1000)
                state["steps"].append(
                    {
                        "step": step_idx,
                        "thought": thought,
                        "action": tool_name,
                        "args": args,
                        "observation": f"error:{exc}",
                        "latency_ms": latency_ms,
                    }
                )
                if failures >= cfg.max_failures:
                    state["status"] = "failed"
                    state["failure_taxonomy"] = "tool_error"
                    state["error"] = str(exc)
                    break

        if state["status"] == "running":
            state["status"] = "max_steps_reached"
            state["failure_taxonomy"] = "execution_budget"

        state["total_latency_ms"] = int((time.monotonic() - started_at) * 1000)
        out_path = self.run_dir / f"{rid}.json"
        out_path.write_text(json.dumps(state, ensure_ascii=True, indent=2), encoding="utf-8")
        return state

    @staticmethod
    def replay(run_path: str) -> dict[str, Any]:
        return json.loads(Path(run_path).read_text(encoding="utf-8"))
