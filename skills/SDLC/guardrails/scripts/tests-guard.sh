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

# The check paths are the lines under `# owner reads: checks` in CODEOWNERS, up
# to the first blank line: a path, a directory ending in `/`, or a glob.
for owners in "$wt/CODEOWNERS" "$wt/.github/CODEOWNERS" "$wt/docs/CODEOWNERS"; do
  [ -f "$owners" ] || continue
  while read -r pattern _; do
    pattern="${pattern#/}"
    case "$pattern" in
      */) case "$rel" in "$pattern"*) hit=1 ;; *) hit= ;; esac ;;
      *) case "$rel" in $pattern) hit=1 ;; *) hit= ;; esac ;;
    esac
    if [ -n "$hit" ]; then
      echo "$rel is a check path, and a story is mid-build. The checks judge the" >&2
      echo "build, so they do not change during it. Make the code pass. If a check" >&2
      echo "itself is wrong, stop and say so; the guardrails skill changes checks." >&2
      exit 2
    fi
  done < <(awk '/^# owner reads: checks/{f=1; next} f && /^[[:space:]]*$/{exit} f && !/^#/' "$owners")
  break
done

# Stubs in a red commit are for the build to fill in; only its tests are the contract.
is_test "$rel" || exit 0
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
