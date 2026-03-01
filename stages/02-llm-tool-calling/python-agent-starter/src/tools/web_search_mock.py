from __future__ import annotations


def run(args: dict[str, object]) -> dict[str, object]:
    query = str(args.get("query", "")).strip()
    return {
        "query": query,
        "items": [
            {"title": f"Mock result for {query}", "url": "https://example.com/a"},
            {"title": f"Another {query}", "url": "https://example.com/b"},
        ],
    }
