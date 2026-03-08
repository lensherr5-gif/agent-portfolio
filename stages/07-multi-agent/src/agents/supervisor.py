from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agents.executor import AuthorizationError, Executor
from agents.planner import Planner
from agents.researcher import Researcher


class Supervisor:
    def __init__(self, permissions_path: str) -> None:
        data = json.loads(Path(permissions_path).read_text(encoding="utf-8"))
        self.permissions = {k: set(v) for k, v in data.items()}
        self.planner = Planner()
        self.researcher = Researcher()
        self.executor = Executor(self.permissions.get("executor", set()))

    def run(self, goal: str, *, action: str = "execute", force_fail: bool = False) -> dict[str, Any]:
        trace: list[dict[str, Any]] = []
        run_id = f"run-{abs(hash(goal)) % 100000}"
        plan = self.planner.plan(goal)
        trace.append({"agent_id": "planner", "run_id": run_id, "step": "plan", "plan": plan})

        research = self.researcher.gather(plan["query"])
        trace.append({"agent_id": "researcher", "run_id": run_id, "step": "gather", "research": research})

        payload = {"goal": goal, "research": research, "force_fail": force_fail}
        try:
            result = self.executor.run(action, payload)
            trace.append({"agent_id": "executor", "run_id": run_id, "step": "execute", "result": result})
            return {"status": "succeeded", "run_id": run_id, "trace": trace, "result": result}
        except AuthorizationError as exc:
            # 越权调用直接阻断，不允许自动绕过权限策略。
            trace.append({"agent_id": "supervisor", "run_id": run_id, "step": "policy_block", "error": str(exc)})
            return {"status": "blocked", "run_id": run_id, "trace": trace, "error": str(exc)}
        except Exception as exc:
            # 失败降级路径：不中断整条链路，返回可解释的降级结果。
            degraded = {"status": "degraded", "report": f"fallback-report:{goal}", "reason": str(exc)}
            trace.append({"agent_id": "supervisor", "run_id": run_id, "step": "degrade", "result": degraded})
            return {"status": "degraded", "run_id": run_id, "trace": trace, "result": degraded}
