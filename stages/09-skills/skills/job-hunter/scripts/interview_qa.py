from __future__ import annotations

import json
import sys

from parse_jd import parse_jd


def generate_questions(jd_text: str) -> list[str]:
    info = parse_jd(jd_text)
    qs = [
        f"请介绍你在 {info['role']} 相关项目中的关键贡献。",
        "请说明你如何做故障定位与复盘。",
        "请描述一次性能优化的量化结果。",
    ]
    if "python" in info["skills"]:
        qs.append("请解释 Python 中协程与线程的差异和适用场景。")
    if "llm" in info["skills"]:
        qs.append("你如何设计工具调用的失败恢复与审计日志？")
    return qs


if __name__ == "__main__":
    jd = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(generate_questions(jd), ensure_ascii=True))
