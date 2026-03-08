from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from memory.policy import should_persist


@dataclass
class MemoryItem:
    text: str
    topic: str
    confidence: float
    created_at: float
    expires_at: float | None
    source: str


class MemoryStore:
    def __init__(self, short_window: int = 3, default_ttl_seconds: int | None = 7 * 24 * 3600) -> None:
        self.short_window = short_window
        self.default_ttl_seconds = default_ttl_seconds
        self.short_term: dict[str, list[str]] = {}
        self.long_term: dict[str, list[MemoryItem]] = {}
        self.audit_log: list[dict[str, Any]] = []

    def add_turn(self, user_id: str, message: str) -> None:
        turns = self.short_term.setdefault(user_id, [])
        turns.append(message)
        # 短期记忆只保留最近 N 轮，控制上下文膨胀。
        self.short_term[user_id] = turns[-self.short_window :]

    def short_summary(self, user_id: str) -> str:
        return " | ".join(self.short_term.get(user_id, []))

    def write_memory(
        self,
        user_id: str,
        text: str,
        *,
        topic: str,
        confidence: float,
        source: str,
        ttl_seconds: int | None = None,
    ) -> bool:
        if not should_persist(text, confidence):
            # 被策略拒绝也要落审计，便于复盘为什么没写入。
            self.audit_log.append({"user_id": user_id, "event": "blocked", "text": text, "reason": "policy"})
            return False

        now = time.time()
        ttl = self.default_ttl_seconds if ttl_seconds is None else ttl_seconds
        expires_at = now + ttl if ttl else None

        item = MemoryItem(
            text=text,
            topic=topic,
            confidence=confidence,
            created_at=now,
            expires_at=expires_at,
            source=source,
        )
        self.long_term.setdefault(user_id, []).append(item)
        self.audit_log.append({"user_id": user_id, "event": "written", "topic": topic, "source": source})
        return True

    def recall(self, user_id: str, topic: str | None = None) -> list[str]:
        now = time.time()
        records = self.long_term.get(user_id, [])
        out: list[str] = []
        for item in records:
            if item.expires_at is not None and item.expires_at < now:
                continue
            if topic is not None and item.topic != topic:
                continue
            out.append(item.text)
        return out
