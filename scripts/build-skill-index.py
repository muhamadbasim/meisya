#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
OUT = ROOT / "docs" / "SKILLS_INDEX.md"


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = [
        "# Skills Index",
        "",
        f"Total skills: {data['skills']}",
        "",
        "| Skill | Description |",
        "| --- | --- |",
    ]
    for item in data["items"]:
        name = item["name"]
        desc = item["description"].replace("|", "\\|")
        path = item["path"]
        rows.append(f"| [`{name}`](../{path}) | {desc} |")
    OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

