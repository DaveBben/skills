#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"
cd "$root"

# stdout, not stderr: on SessionStart only stdout reaches the agent.
env_check

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  dirty="$(git status --short)"
  if [ -n "$dirty" ]; then
    # Twenty lines at most: this output loads into every session.
    echo "$(printf '%s\n' "$dirty" | wc -l | tr -d ' ') uncommitted changes at session start:"
    printf '%s\n' "$dirty" | head -20
  fi
fi
exit 0
