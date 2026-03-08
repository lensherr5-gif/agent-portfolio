from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class SkillMeta:
    name: str
    version: str
    risk: str
    enabled: bool
    approved_users: set[str]
    handler: Callable[[str], str]


class SkillRouter:
    def __init__(self) -> None:
        self.registry: dict[str, SkillMeta] = {}
        self.audit_log: list[dict[str, str]] = []

    def register(self, meta: SkillMeta) -> None:
        self.registry[meta.name] = meta

    def route(self, query: str) -> str | None:
        # 关键词路由最小实现：后续可替换为向量/分类器路由。
        q = query.lower()
        if any(k in q for k in ["jd", "job", "interview", "resume"]):
            return "job-hunter"
        return None

    def execute(self, user_id: str, query: str) -> str:
        skill_name = self.route(query)
        if skill_name is None:
            self.audit_log.append({"user_id": user_id, "event": "no_match"})
            return "NO_SKILL_MATCH"

        skill = self.registry.get(skill_name)
        if skill is None or not skill.enabled:
            self.audit_log.append({"user_id": user_id, "event": "disabled", "skill": skill_name})
            return "SKILL_UNAVAILABLE"

        if user_id not in skill.approved_users:
            # 高风险技能默认拒绝未授权调用。
            self.audit_log.append({"user_id": user_id, "event": "blocked", "skill": skill_name})
            return "SKILL_BLOCKED"

        output = skill.handler(query)
        self.audit_log.append({"user_id": user_id, "event": "executed", "skill": skill_name})
        return output
