from __future__ import annotations

import json
import re
import sys


def parse_jd(text: str) -> dict[str, str]:
    skills = []
    for k in ["python", "sql", "llm", "docker", "kubernetes", "langchain"]:
        if k in text.lower():
            skills.append(k)

    years_match = re.search(r"(\d+)\+?\s*years", text.lower())
    years = years_match.group(1) if years_match else "unspecified"

    location = "remote"
    for city in ["shanghai", "beijing", "shenzhen", "hangzhou"]:
        if city in text.lower():
            location = city
            break

    role = text.split(",")[0].strip() if "," in text else "unknown-role"
    return {"role": role, "skills": ",".join(skills), "years": years, "location": location}


if __name__ == "__main__":
    jd = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(parse_jd(jd), ensure_ascii=True))
