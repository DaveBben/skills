#!/usr/bin/env bash
# PostToolUse on Edit|Write|MultiEdit. Runs deps_check when the edit touched
# the manifest (deps_file).
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_lib.sh"
. "$root/.claude/hooks/_slots.sh"

file="$(read_json_field file_path)"
case "$file" in /*) ;; *) file="$root/$file" ;; esac
file="$(physical "$file")"
wt="$(clone_worktree "$(dirname "$file")")" || exit 0
[ "$file" = "$wt/$deps_file" ] && [ -f "$file" ] || exit 0
cd "$wt"

if ! output="$(deps_check 2>&1)"; then
  echo "$deps_file no longer matches the lockfile:" >&2
  echo "$output" >&2
  echo "Change dependencies with $deps_fix, never by editing $deps_file by" >&2
  echo "hand. If this edit was intentional and not a dependency change," >&2
  echo "regenerate the lockfile." >&2
  exit 2
fi
exit 0
