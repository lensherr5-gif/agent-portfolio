from __future__ import annotations


class Planner:
    def plan(self, goal: str) -> dict[str, str]:
        return {"goal": goal, "query": f"research:{goal}", "next_action": "execute"}
