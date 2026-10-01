#!/usr/bin/env bash
# PreToolUse on Edit|Write|MultiEdit. Refuses edits on main_branch except the
# paths in main_ok.
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_lib.sh"
. "$root/.claude/hooks/_slots.sh"

file="$(read_json_field file_path)"
case "$file" in /*) ;; *) file="$root/$file" ;; esac
file="$(physical "$file")"

wt="$(clone_worktree "$(dirname "$file")")" || exit 0

branch="$(git -C "$wt" branch --show-current 2>/dev/null || true)"
[ "$branch" = "$main_branch" ] || exit 0

rel="${file#"$wt"/}"
for ok in "${main_ok[@]}"; do
  case "$rel" in $ok) exit 0 ;; esac
done

echo "$rel is on $main_branch, and edits on $main_branch are blocked." >&2
echo "Cut a branch first and edit there: a story's branch (deliver's story.sh start" >&2
echo "cuts one in its own worktree), or a branch you create for a check, a chore or" >&2
echo "a spike." >&2
echo "Only these paths change on $main_branch: ${main_ok[*]}" >&2
exit 2
