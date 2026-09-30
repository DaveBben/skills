#!/usr/bin/env bash
# Stop and SubagentStop. Runs turn_end on the main checkout and on the story
# worktree the agent works in, only when files under pathspec changed. Blocks
# the stop on a failure, three times per session at most, then lets it through
# and says so.
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_lib.sh"
. "$root/.claude/hooks/_slots.sh"

input="$(cat)"
sid="$(printf '%s' "$input" | read_json_field session_id)"
cwd="$(printf '%s' "$input" | read_json_field cwd)"
counter="${TMPDIR:-/tmp}/claude-turn-end-${sid:-unknown}"
count="$(cat "$counter" 2>/dev/null || true)"
case "$count" in ''|*[!0-9]*) count=0 ;; esac

# The main checkout, and the worktree the agent is working in when that is a
# story worktree of this clone outside the project directory.
dirs=("$(git -C "$root" rev-parse --show-toplevel)")
if wt="$(clone_worktree "${cwd:-$root}")" && [ "$wt" != "${dirs[0]}" ]; then dirs+=("$wt"); fi

failed=""
for d in "${dirs[@]}"; do
  cd "$d"
  # The array stays quoted. Unquoted, bash expands the pattern against the repo
  # root before git sees it, and the check silently stops firing.
  changed="$(git status --porcelain -- "${pathspec[@]}" 2>/dev/null || true)"
  [ -z "$changed" ] && continue
  output="$(turn_end 2>&1)" || failed="$failed$d:"$'\n'"$output"$'\n'
done

if [ -n "$failed" ]; then
  if [ "$count" -ge 3 ]; then
    rm -f "$counter"
    echo "turn-end: still failing after 3 blocked stops, letting the stop through." >&2
    exit 0
  fi
  echo $((count + 1)) > "$counter"
  echo "The turn-end check failed. Fix these before finishing:" >&2
  printf '%s' "$failed" >&2
  exit 2
fi

rm -f "$counter"
exit 0
