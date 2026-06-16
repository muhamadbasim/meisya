# Hermes Compatibility Notes

Hermes skills are on-demand knowledge documents. Hermes scans skill directories,
shows installed skills as slash commands, and loads full skill content only when
needed.

## Layout

This pack follows the documented Hermes skill layout:

```text
skills/
└── agency/
    └── agency-frontend-developer/
        └── SKILL.md
```

Each skill has frontmatter with:

- `name`
- `description`
- `version`
- `platforms`
- `metadata.hermes.category`
- `metadata.hermes.tags`

## Install Location

Hermes' primary skill directory is:

```text
~/.hermes/skills/
```

The installer copies this pack to:

```text
~/.hermes/skills/agency/
```

## Usage

```text
/agency-code-reviewer
Review this pull request.
```

```bash
hermes -s agency-code-reviewer
```

## Excluded Runtime Data

Hermes configuration and profile data live under `~/.hermes/`, but this pack
does not include personal runtime state:

- `.env`
- `auth.json`
- `sessions/`
- `logs/`
- `state.db`
- `memories/`

Those files are machine/user specific and should not be distributed as a skill
pack.

