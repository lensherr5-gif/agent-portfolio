from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any


class AuthError(Exception):
    pass


class ParamError(Exception):
    pass


class TodoMCPServer:
    def __init__(self, db_path: str, token: str) -> None:
        self.db_path = Path(db_path)
        self.token = token
        self.audit_log: list[dict[str, Any]] = []
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)"
            )
            conn.commit()
        finally:
            conn.close()

    def _digest(self, payload: Any) -> str:
        raw = json.dumps(payload, ensure_ascii=True, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:16]

    def _authorize(self, supplied_token: str) -> None:
        # 所有工具入口统一鉴权，避免漏校验。
        if supplied_token != self.token:
            raise AuthError("invalid_token")

    def _audit(self, caller: str, tool: str, args: dict[str, Any], result: Any, started_at: float) -> None:
        # 审计记录只存摘要，减少敏感明文落盘风险。
        self.audit_log.append(
            {
                "caller": caller,
                "tool": tool,
                "args_digest": self._digest(args),
                "result_digest": self._digest(result),
                "latency_ms": int((time.monotonic() - started_at) * 1000),
            }
        )

    def add_task(self, *, token: str, caller: str, text: str) -> dict[str, Any]:
        started = time.monotonic()
        self._authorize(token)
        if not text.strip():
            raise ParamError("text_required")
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("INSERT INTO tasks(text, done) VALUES (?, 0)", (text.strip(),))
            conn.commit()
            result = {"id": cur.lastrowid, "text": text.strip(), "done": False}
        finally:
            conn.close()
        self._audit(caller, "add_task", {"text": text}, result, started)
        return result

    def list_tasks(self, *, token: str, caller: str) -> dict[str, Any]:
        started = time.monotonic()
        self._authorize(token)
        conn = sqlite3.connect(self.db_path)
        try:
            rows = conn.execute("SELECT id, text, done FROM tasks ORDER BY id ASC").fetchall()
        finally:
            conn.close()
        tasks = [{"id": r[0], "text": r[1], "done": bool(r[2])} for r in rows]
        result = {"tasks": tasks}
        self._audit(caller, "list_tasks", {}, result, started)
        return result

    def done_task(self, *, token: str, caller: str, task_id: int) -> dict[str, Any]:
        started = time.monotonic()
        self._authorize(token)
        if task_id <= 0:
            raise ParamError("task_id_invalid")
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
            conn.commit()
            if cur.rowcount == 0:
                raise ParamError("task_not_found")
            row = conn.execute("SELECT id, text, done FROM tasks WHERE id=?", (task_id,)).fetchone()
        finally:
            conn.close()
        result = {"id": row[0], "text": row[1], "done": bool(row[2])}
        self._audit(caller, "done_task", {"task_id": task_id}, result, started)
        return result
