from __future__ import annotations

import hashlib
import json
import time
import uuid
from typing import Any


def generate_run_id() -> str:
    return uuid.uuid4().hex[:12]


def digest_obj(data: Any) -> str:
    raw = json.dumps(data, ensure_ascii=True, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def log_event(level: str, message: str, run_id: str, **extra: object) -> None:
    payload = {
        "ts": int(time.time()),
        "level": level.upper(),
        "message": message,
        "run_id": run_id,
    }
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=True))
