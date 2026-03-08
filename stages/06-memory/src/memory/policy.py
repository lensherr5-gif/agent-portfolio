from __future__ import annotations

import re


INJECTION_PATTERNS = [r"ignore previous instructions", r"reveal system prompt", r"jailbreak"]
SENSITIVE_PATTERNS = [r"password", r"api[_-]?key", r"secret", r"身份证", r"银行卡"]


def is_polluted(text: str) -> bool:
    lower = text.lower()
    return any(re.search(p, lower) for p in INJECTION_PATTERNS)


def has_sensitive_data(text: str) -> bool:
    lower = text.lower()
    return any(re.search(p, lower) for p in SENSITIVE_PATTERNS)


def should_persist(text: str, confidence: float) -> bool:
    # 长期记忆只保留高置信且安全的内容，降低污染扩散风险。
    if confidence < 0.6:
        return False
    if is_polluted(text):
        return False
    if has_sensitive_data(text):
        return False
    return True
