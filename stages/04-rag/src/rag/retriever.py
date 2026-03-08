from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any


@dataclass
class Chunk:
    title: str
    path: str
    text: str


class SimpleRetriever:
    def __init__(self, docs_dir: str, chunk_size: int = 120, overlap: int = 20) -> None:
        self.docs_dir = Path(docs_dir)
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks: list[Chunk] = []
        self._build_index()

    def _build_index(self) -> None:
        # 将文档按固定窗口切分为 chunk，作为最小可运行检索索引。
        for file_path in sorted(self.docs_dir.glob("*.md")):
            text = file_path.read_text(encoding="utf-8")
            title = file_path.stem
            for i in range(0, max(len(text), 1), max(self.chunk_size - self.overlap, 1)):
                piece = text[i : i + self.chunk_size]
                if piece.strip():
                    self.chunks.append(Chunk(title=title, path=str(file_path), text=piece))

    @staticmethod
    def _score(query: str, text: str) -> int:
        # 用 \w+ 做基础清洗，避免 "asyncio?" 这类标点导致 miss。
        q_tokens = {t.lower() for t in re.findall(r"\w+", query) if t.strip()}
        t_tokens = {t.lower() for t in re.findall(r"\w+", text) if t.strip()}
        return len(q_tokens & t_tokens)

    def search(self, query: str, top_k: int = 3) -> list[Chunk]:
        ranked = sorted(self.chunks, key=lambda c: self._score(query, c.text), reverse=True)
        return [c for c in ranked[:top_k] if self._score(query, c.text) > 0]

    def answer(self, query: str, top_k: int = 3) -> dict[str, Any]:
        matches = self.search(query, top_k=top_k)
        if not matches:
            return {"answer": "未命中知识库。", "sources": []}
        summary = " ".join(m.text.strip().replace("\n", " ") for m in matches)
        sources = [{"title": m.title, "path": m.path, "snippet": m.text[:100]} for m in matches]
        return {"answer": summary[:240], "sources": sources}
