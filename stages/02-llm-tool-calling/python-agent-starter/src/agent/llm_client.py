from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass, field
from typing import Any

from src.common.errors import LLMError


@dataclass
class LLMClient:
    mode: str = "mock"
    model: str = "gpt-4o-mini"
    replay: dict[str, str] = field(default_factory=dict)

    def generate_raw(self, prompt: str, run_id: str) -> str:
        if self.mode == "mock":
            if prompt in self.replay:
                return self.replay[prompt]
            return '{"final_answer":"mock","tool_call":{"tool_name":"calculator","args":{"expression":"1+1"}}}'

        if self.mode != "openai":
            raise LLMError(f"unsupported LLM_MODE: {self.mode}")

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise LLMError(
                "OPENAI_API_KEY is required", hint="set OPENAI_API_KEY or use LLM_MODE=mock"
            )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Return valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        }
        req = urllib.request.Request(
            url="https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            raise LLMError(f"openai request failed: {exc}") from exc

    def generate_structured(
        self, prompt: str, schema: dict[str, Any], run_id: str
    ) -> dict[str, Any]:
        # 结构化解析交由 json_guard 处理；此函数保留公共接口。
        from src.agent.json_guard import parse_with_guard

        raw = self.generate_raw(prompt, run_id)
        return parse_with_guard(raw, schema, run_id)
