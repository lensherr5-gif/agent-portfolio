from __future__ import annotations

import json
import time
import uuid


def generate_run_id() -> str:
    """生成简短的运行 ID，用于日志关联。"""
    return uuid.uuid4().hex[:12]


def log_event(level: str, message: str, run_id: str, **extra: object) -> None:
    """输出一条结构化 JSON 日志，便于解析与检索。"""
    # 保持基础字段统一，方便后续做日志聚合和排障。
    payload = {
        "ts": int(time.time()),
        "level": level.upper(),
        "message": message,
        "run_id": run_id,
    }
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=True))
