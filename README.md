# Meisya Hermes Agency Skills

Portable Hermes Agent skill pack generated from
[`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents).

This repository is organized for download, transfer, and reuse by Hermes or
other agents. It contains ready-to-install Hermes skills under `skills/agency/`
and the source/conversion workspace under `source/agency-agents/`.

## Contents

- `skills/agency/` — 232 Hermes-native `SKILL.md` directories using the
  `agency-` prefix.
- `source/agency-agents/` — source Agency agent definitions plus the patched
  `convert.sh` and `install.sh` target for Hermes.
- `scripts/install-hermes-skills.sh` — copies this pack into
  `~/.hermes/skills/agency/`.
- `scripts/audit-skills.py` — validates skill count, frontmatter, duplicate
  names, and common secret patterns.
- `docs/AUDIT.md` — audit notes for this packaged snapshot.
- `docs/HERMES_COMPATIBILITY.md` — layout and usage notes based on Hermes docs.
- `docs/SKILLS_INDEX.md` — generated index of all packaged skills.
- `manifest.json` — machine-readable skill manifest.

## Install Into Hermes

From this repo:

```bash
./scripts/install-hermes-skills.sh
```

Or choose a custom Hermes skills directory:

```bash
HERMES_SKILLS_DIR=/path/to/.hermes/skills ./scripts/install-hermes-skills.sh
```

Then start a new Hermes session and use a skill:

```text
/agency-frontend-developer
Review this React component for accessibility and performance.
```

Or preload from the CLI:

```bash
hermes -s agency-code-reviewer
hermes chat -s agency-code-reviewer -q "Review the current git diff."
```

## Audit

Run:

```bash
./scripts/audit-skills.py
```

Expected result for this snapshot:

```text
OK: 232 skills validated
```

## What This Repo Does Not Include

This is intentionally not a backup of a live Hermes profile. It does not include
`.env`, API keys, sessions, logs, memory files, `state.db`, or other personal
runtime data.

## Regenerate From Source

```bash
cd source/agency-agents
./scripts/convert.sh --tool hermes
./scripts/install.sh --tool hermes --dry-run
```

Generated output appears under:

```text
source/agency-agents/integrations/hermes/skills/agency/
```

Copy or sync that directory back to top-level `skills/agency/` before
publishing a refreshed pack.

## License

Agency Agents source content is MIT licensed by AgentLand Contributors. See
`LICENSE` and `NOTICE.md`.
