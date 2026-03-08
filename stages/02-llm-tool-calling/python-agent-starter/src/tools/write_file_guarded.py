from __future__ import annotations

from pathlib import Path


def run(args: dict[str, object]) -> dict[str, object]:
    rel_path = str(args.get("path", "output.txt"))
    content = str(args.get("content", ""))
    root = Path("tool_outputs")
    root.mkdir(parents=True, exist_ok=True)
    out_path = root / rel_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return {"path": str(out_path), "bytes": len(content.encode("utf-8"))}
