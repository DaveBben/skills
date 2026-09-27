#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

file="$(read_json_field file_path)"
case "$file" in /*) ;; *) file="$root/$file" ;; esac

# The file may sit in any worktree of this clone; find the nearest existing directory.
dir="$(dirname "$file")"
while [ ! -d "$dir" ]; do dir="$(dirname "$dir")"; done
wt="$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)" || exit 0

# Another repository the session can reach is out of scope.
[ "$(git -C "$wt" rev-parse --path-format=absolute --git-common-dir)" = \
  "$(git -C "$root" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" ] || exit 0

branch="$(git -C "$wt" branch --show-current 2>/dev/null || true)"
[ "$branch" = "$main_branch" ] || exit 0

rel="${file#"$wt"/}"
for ok in "${main_ok[@]}"; do
  case "$rel" in $ok) exit 0 ;; esac
done

echo "$rel is on $main_branch, and edits on $main_branch are blocked." >&2
echo "A request that adds, changes, removes or fixes behaviour runs the deliver" >&2
echo "skill, which cuts a story branch in its own worktree; edit there. Any other" >&2
echo "change (a check, a chore, a spike) goes on a branch you create first." >&2
echo "Only these paths change on $main_branch: ${main_ok[*]}" >&2
exit 2
