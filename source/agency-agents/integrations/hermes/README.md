# Hermes Integration

Converts Agency agents into Hermes Agent skills. Each source agent becomes one
Hermes-native `SKILL.md` file with the `agency-` prefix to avoid collisions with
built-in skills.

## Install

```bash
./scripts/convert.sh --tool hermes
./scripts/install.sh --tool hermes
```

This copies generated skills to:

```text
~/.hermes/skills/agency/<agency-agent-slug>/SKILL.md
```

## Usage

Start a new Hermes session and load a skill by slash command:

```text
/agency-frontend-developer
Review this React component for performance and accessibility.
```

Or preload a skill when starting Hermes:

```bash
hermes -s agency-code-reviewer
hermes chat -s agency-code-reviewer -q "Review the current git diff."
```

## Regenerate

After modifying source agents:

```bash
./scripts/convert.sh --tool hermes
./scripts/install.sh --tool hermes
```

## Notes

Generated Hermes skills include a short wrapper that keeps Hermes system,
developer, user, security, and tool-use instructions higher priority than the
imported Agency role prompt.
