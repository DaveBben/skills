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
branch="$(git -C "$wt" branch --show-current 2>/dev/null || true)"

reds="$( { [ -n "$branch" ] && git -C "$wt" config --get-all "branch.$branch.redCommit"; git -C "$wt" config --get-all agile.redCommit; } 2>/dev/null || true)"
[ -n "$reds" ] || exit 0
rel="${file#"$wt"/}"

for red in $reds; do
  git -C "$wt" cat-file -e "$red^{commit}" 2>/dev/null || continue
  if git -C "$wt" diff --name-only "$red^" "$red" | grep -qxF "$rel"; then
    echo "$rel is an accepted test from red commit $red. It is the contract;" >&2
    echo "the build makes it pass, never changes it. Add a new test file for a" >&2
    echo "case the table missed. If the contract itself is wrong, stop and say so:" >&2
    echo "once the user re-accepts the row, deliver clears this guard and lands the corrected row." >&2
    exit 2
  fi
done
exit 0
