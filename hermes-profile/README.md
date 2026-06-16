# Hermes Profile Snapshot

Portable, sanitized snapshot of the Ubuntu Hermes setup.

This folder is not a full `~/.hermes` backup. It contains only files that are
useful for rebuilding behavior on another machine without publishing runtime
secrets, sessions, logs, token stores, or caches.

## Included

- `SOUL.md` — active Hermes persona file.
- `memories/MEMORY.md` — operational memory.
- `memories/USER.md` — user preference memory.
- `config/config.sanitized.yaml` — selected Hermes config with sensitive fields
  redacted.
- `cron/jobs.sanitized.json` — cron definitions with prompts and schedules, but
  raw chat IDs and delivery routes redacted.
- `skills-local-custom/` — 22 local custom non-Agency skills.
- `inventory/` — audit notes and skill inventories.

## Excluded

- `.env`, `.env.*`, `auth.json`, provider credentials, OAuth tokens.
- `sessions/`, `logs/`, `state.db`, locks, pid files.
- WhatsApp session stores and backups.
- cache directories, `node_modules`, virtualenvs, large backups.
- raw Telegram/WhatsApp chat IDs and delivery routes.

## Restore Memory

```bash
mkdir -p ~/.hermes/memories
cp hermes-profile/SOUL.md ~/.hermes/SOUL.md
cp hermes-profile/memories/MEMORY.md ~/.hermes/memories/MEMORY.md
cp hermes-profile/memories/USER.md ~/.hermes/memories/USER.md
```

## Restore Custom Local Skills

```bash
rsync -a hermes-profile/skills-local-custom/ ~/.hermes/skills/
```

Start a new Hermes session after restoring skills.

## Cron Restore

`cron/jobs.sanitized.json` is documentation-first, not a drop-in replacement,
because chat IDs and delivery routes are redacted. Recreate jobs manually from
the schedules, prompts, skills, providers, and models in that file.

## Audit

See `inventory/AUDIT.md`.

