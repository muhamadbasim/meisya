# Audit Report

Date: 2026-06-17

## Scope

Audited the Hermes skill pack generated from `agency-agents` and prepared this
repository for portable use by Hermes or other agents.

## Source

- Source repo: `msitarzewski/agency-agents`
- Source snapshot observed locally: `3f78a30`
- License: MIT
- Generated Hermes skills: 232

## Hermes Compatibility

The generated skills follow Hermes' documented `SKILL.md` structure and are
installed under the `agency` category namespace. Skill names use the
`agency-` prefix to avoid collisions with built-in Hermes skills.

## Safety Decisions

- Live Hermes profile data was not copied.
- Secrets and auth material were excluded.
- Generated skills include a wrapper making Hermes system, developer, user,
  security, and tool-use instructions higher priority than Agency role text.
- The pack includes source and generated files so other agents can audit,
  regenerate, or install without needing the original local machine.

## Validation Commands

```bash
./scripts/audit-skills.py
```

Result:

```text
OK: 232 skills validated
```

Additional repository scan:

```bash
find . -path ./.git -prune -o \( -name '.env' -o -name 'auth.json' -o -name 'state.db' -o -path '*/sessions/*' -o -path '*/logs/*' -o -path '*/memories/*' \) -print
rg -n --hidden --glob '!.git/**' '(OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|github_pat_|sk-[A-Za-z0-9]{20,}|BEGIN (RSA|OPENSSH|EC|PRIVATE) KEY|password\s*=|secret\s*=|token\s*=)' .
```

The forbidden-file scan returned no live Hermes profile files. The text scan
found example strings such as `GITHUB_TOKEN`, `token = ...`, and `password = ...`
inside security/code examples in the Agency source prompts; these are
instructional placeholders, not real credentials.

Additional local validation performed before packaging:

```bash
hermes skills list --source local --enabled-only
hermes prompt-size --json
```

## Known Non-Blocking Local Hermes Findings

These findings were observed in the local Hermes profile and are not part of
this repository:

- Optional provider logins were missing for some providers.
- Telegram gateway had recent network timeout warnings.
- Some Hermes workspace npm dependency advisories were reported by
  `hermes doctor`.

They do not block installing or loading this skill pack.
