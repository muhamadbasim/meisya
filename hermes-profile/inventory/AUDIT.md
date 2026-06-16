# Hermes Server Audit Snapshot

Date: 2026-06-17

## Included
- `SOUL.md`
- `memories/MEMORY.md` and `memories/USER.md`
- `config/config.sanitized.yaml`
- `cron/jobs.sanitized.json`
- `skills-local-custom/` with 22 custom local non-Agency skills
- inventory files under `inventory/`

## Excluded
- `.env`, `.env.*`, `auth.json`, locks, pid files
- sessions, logs, state databases, WhatsApp sessions
- cache directories, backups, node_modules, venv
- raw Telegram/WhatsApp chat IDs and delivery routes

## Current Counts
- All skill directories observed: 334
- Custom local non-Agency skills packaged: 22
- Cron jobs packaged in sanitized form: 7
- Hermes doctor: core checks passed; non-blocking advisories remain for optional provider logins, npm advisories, missing Docker/agent-browser/browser-cdp/computer_use, and optional tool credentials.

## Secret Scan Notes
- Forbidden runtime files were not included.
- Text scan found only environment-variable references/placeholders inside skill code/docs, such as `REPLIZ_SECRET_KEY` and `Bearer sk-xxxxxxxxxxxxxxxxxxxx`.
- No concrete API key, token, OAuth credential, auth store, session database, or raw delivery route was intentionally included.
