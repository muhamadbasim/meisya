#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_ROOT/skills/agency"
DEST_ROOT="${HERMES_SKILLS_DIR:-$HOME/.hermes/skills}"
DEST="$DEST_ROOT/agency"

if [[ ! -d "$SRC" ]]; then
  echo "Missing skills directory: $SRC" >&2
  exit 1
fi

mkdir -p "$DEST"

count=0
while IFS= read -r -d '' skill_dir; do
  name="$(basename "$skill_dir")"
  mkdir -p "$DEST/$name"
  cp "$skill_dir/SKILL.md" "$DEST/$name/SKILL.md"
  count=$((count + 1))
done < <(find "$SRC" -mindepth 1 -maxdepth 1 -type d -name 'agency-*' -print0 | sort -z)

echo "Installed $count Hermes Agency skills to $DEST"
echo "Start a new Hermes session if slash commands are not visible immediately."

