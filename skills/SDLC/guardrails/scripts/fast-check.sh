#!/usr/bin/env bash
# PostToolUse on Edit|Write|MultiEdit. Runs fast_fix, then fast_check, on the
# edited file; blocks on findings and fails open when the checker breaks.
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_lib.sh"
. "$root/.claude/hooks/_slots.sh"

file="$(read_json_field file_path)"

case "$file" in /*) ;; *) file="$root/$file" ;; esac
# This clone only, in whichever worktree holds the file.
wt="$(clone_worktree "$(dirname "$file")")" || exit 0
# A source file that still exists. An edit may have been a deletion.
matches "$file" || exit 0
[ -f "$file" ] || exit 0

cd "$wt"
fast_fix "$file"

set +e
output="$(fast_check "$file" 2>&1)"; code=$?
set -e

if [ "$code" -eq 1 ]; then
  echo "Issues in $file that need a real fix (not auto-fixable):" >&2
  echo "$output" >&2
  exit 2
elif [ "$code" -ne 0 ]; then
  # Fail open: the checker itself broke. Blocking here would stop every edit.
  echo "fast-check: the checker failed to run (exit $code), not a finding:" >&2
  echo "$output" >&2
fi
exit 0
