from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any


class WorkflowGraph:
    def __init__(self, checkpoint_dir: str = "runs/checkpoints") -> None:
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _checkpoint_path(self, run_id: str) -> Path:
        return self.checkpoint_dir / f"{run_id}.json"

    def _save_checkpoint(self, state: dict[str, Any]) -> None:
        self._checkpoint_path(state["run_id"]).write_text(
            json.dumps(state, ensure_ascii=True, indent=2), encoding="utf-8"
        )

    def load_checkpoint(self, run_id: str) -> dict[str, Any]:
        return json.loads(self._checkpoint_path(run_id).read_text(encoding="utf-8"))

    def run(
        self,
        task: str,
        *,
        run_id: str | None = None,
        approved: bool = False,
        resume: bool = False,
        max_retries: int = 1,
    ) -> dict[str, Any]:
        rid = run_id or str(uuid.uuid4())
        if resume:
            state = self.load_checkpoint(rid)
            state["resumed"] = True
            if approved:
                state["approved"] = True
            # 从等待审批恢复时，需要回到 running 才能继续状态迁移。
            if state.get("status") == "awaiting_approval":
                state["status"] = "running"
        else:
            state = {
                "run_id": rid,
                "task": task,
                "approved": approved,
                "resumed": False,
                "node": "plan",
                "retries": 0,
                "events": [],
                "status": "running",
            }

        started_at = time.monotonic()

        while state["status"] == "running":
            node = state["node"]
            if node == "plan":
                # 关键词命中高风险任务时，强制进入人工审批节点。
                high_risk = any(k in state["task"].lower() for k in ["delete", "drop", "wipe"])
                state["high_risk"] = high_risk
                state["events"].append({"node": "plan", "high_risk": high_risk})
                state["node"] = "human_approval" if high_risk else "act"

            elif node == "human_approval":
                if state.get("approved"):
                    state["events"].append({"node": "human_approval", "decision": "approved"})
                    state["node"] = "act"
                else:
                    state["status"] = "awaiting_approval"
                    state["events"].append({"node": "human_approval", "decision": "pending"})
                    self._save_checkpoint(state)
                    break

            elif node == "act":
                fail_keyword = "fail" in state["task"].lower()
                if fail_keyword and state["retries"] < max_retries:
                    # 可恢复失败先重试，超过阈值再进入失败决策。
                    state["retries"] += 1
                    state["events"].append({"node": "act", "result": "temporary_failure"})
                    state["node"] = "act"
                elif fail_keyword:
                    state["events"].append({"node": "act", "result": "failed"})
                    state["node"] = "decide"
                    state["observation"] = "tool_failed"
                else:
                    state["events"].append({"node": "act", "result": "ok"})
                    state["node"] = "observe"
                    state["observation"] = "tool_ok"

            elif node == "observe":
                state["events"].append({"node": "observe", "observation": state.get("observation")})
                state["node"] = "decide"

            elif node == "decide":
                if state.get("observation") == "tool_ok":
                    state["status"] = "succeeded"
                    state["events"].append({"node": "decide", "decision": "finish"})
                else:
                    state["status"] = "failed"
                    state["events"].append({"node": "decide", "decision": "stop"})
            else:  # pragma: no cover - defensive
                state["status"] = "failed"
                state["events"].append({"node": node, "error": "unknown_node"})

        state["latency_ms"] = int((time.monotonic() - started_at) * 1000)
        self._save_checkpoint(state)
        return state
