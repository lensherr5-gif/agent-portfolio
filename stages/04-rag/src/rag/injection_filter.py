from __future__ import annotations

import re


PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"reveal\s+system\s+prompt",
    r"sudo\s+",
    r"rm\s+-rf",
]


def is_injection(text: str) -> bool:
    # 规则优先策略：先做显式命中拦截，后续可替换为模型分类器。
    lower = text.lower()
    return any(re.search(pattern, lower) for pattern in PATTERNS)


def sanitize_query(text: str) -> str:
    if is_injection(text):
        return "[BLOCKED_PROMPT_INJECTION]"
    return text
