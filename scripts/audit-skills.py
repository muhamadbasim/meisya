#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"PyYAML is required for this audit: {exc}", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills" / "agency"
EXPECTED_COUNT = 232

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
]


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError("missing closing frontmatter")
    frontmatter = yaml.safe_load(parts[1]) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError("frontmatter is not a mapping")
    return frontmatter, parts[2]


def main() -> int:
    errors: list[str] = []
    names: dict[str, Path] = {}
    skill_files = sorted(SKILLS.glob("agency-*/SKILL.md"))

    if len(skill_files) != EXPECTED_COUNT:
        errors.append(f"expected {EXPECTED_COUNT} skills, found {len(skill_files)}")

    for path in skill_files:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        try:
            meta, body = split_frontmatter(text)
        except Exception as exc:
            errors.append(f"{rel}: {exc}")
            continue

        name = str(meta.get("name") or "")
        description = str(meta.get("description") or "")
        hermes = ((meta.get("metadata") or {}).get("hermes") or {})

        if not name.startswith("agency-"):
            errors.append(f"{rel}: name must start with agency-")
        if path.parent.name != name:
            errors.append(f"{rel}: directory name does not match frontmatter name")
        if not description:
            errors.append(f"{rel}: missing description")
        if hermes.get("category") != "agency":
            errors.append(f"{rel}: metadata.hermes.category must be agency")
        if name in names:
            errors.append(f"{rel}: duplicate skill name also in {names[name].relative_to(ROOT)}")
        names[name] = path

        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: possible secret-like token")
                break

        if "Follow all higher-priority Hermes system" not in body:
            errors.append(f"{rel}: missing Hermes priority wrapper")

    skills = []
    for name, path in sorted(names.items()):
        text = path.read_text(encoding="utf-8")
        meta, _ = split_frontmatter(text)
        hermes = ((meta.get("metadata") or {}).get("hermes") or {})
        skills.append(
            {
                "name": name,
                "description": str(meta.get("description") or ""),
                "category": hermes.get("category"),
                "tags": hermes.get("tags") or [],
                "path": str(path.relative_to(ROOT)),
            }
        )

    report = {
        "pack": "meisya-hermes-agency-skills",
        "source": "https://github.com/msitarzewski/agency-agents",
        "install_root": "skills/agency",
        "skills": len(skill_files),
        "expected": EXPECTED_COUNT,
        "errors": errors,
        "items": skills,
    }
    (ROOT / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"FAILED: {len(errors)} issue(s)", file=sys.stderr)
        return 1

    print(f"OK: {len(skill_files)} skills validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
