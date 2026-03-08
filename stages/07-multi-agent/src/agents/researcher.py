from __future__ import annotations


class Researcher:
    def gather(self, query: str) -> dict[str, str]:
        return {"query": query, "evidence": f"evidence-for-{query}"}
