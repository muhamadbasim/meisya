# Agent Instructions

This repository is a portable Hermes skill pack.

## Boundaries

- Do not commit live Hermes profile state such as `.env`, API keys, sessions,
  logs, `state.db`, or personal memory files.
- Keep installable skills under `skills/agency/<skill-name>/SKILL.md`.
- Keep source conversion work under `source/agency-agents/`.
- Prefer changing the converter in `source/agency-agents/scripts/convert.sh`
  and regenerating skills instead of manually patching many generated files.

## Validation

Before committing changes, run:

```bash
./scripts/audit-skills.py
```

If the generated skills changed, also verify a sample Hermes load locally:

```bash
hermes skills list --source local | grep agency-
hermes -s agency-code-reviewer --help
```

