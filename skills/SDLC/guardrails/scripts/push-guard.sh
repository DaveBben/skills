#!/usr/bin/env bash
# PreToolUse on Bash. Holds a story branch on this machine until the user has
# confirmed its criteria: `git push`, `gh pr create` and `glab mr create` for a
# story branch with a red commit recorded exit 2 until `story.sh confirm` has
# set branch.<branch>.criteriaConfirmed. A pull request's title must also carry
# the branch's [<issueKey>].
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

input="$(cat)"
cmd="$(printf '%s' "$input" | read_json_field command)"
case "$cmd" in *"git push"*|*"gh pr create"*|*"glab mr create"*) ;; *) exit 0 ;; esac

# The branch is a story/* token in the command when there is one, else the
# branch of the directory the command runs in: the session's cwd, or the target
# of a leading `cd <dir> &&`.
dir="$(printf '%s' "$input" | read_json_field cwd)"; dir="${dir:-$root}"
to="$(printf '%s' "$cmd" | sed -En 's/^[[:space:]]*cd[[:space:]]+([^;&|[:space:]]+)[[:space:]]*&&.*/\1/p' | head -1)"
if [ -n "$to" ]; then case "$to" in /*) dir="$to" ;; *) dir="$dir/$to" ;; esac; fi
branch="$(printf '%s' "$cmd" | grep -Eo 'story/[^[:space:]:"'"'"']+' | head -1 || true)"
[ -n "$branch" ] || branch="$(git -C "$dir" branch --show-current 2>/dev/null || true)"
# A story branch is story/* or one `story.sh adopt` marked.
case "$branch" in story/*) ;; *) [ "$(git -C "$dir" config --get "branch.$branch.story" 2>/dev/null || true)" = true ] || exit 0 ;; esac

# The trivial and no-behaviour-change paths record no red commit, so their
# branches pass.
wt="$(git -C "$dir" worktree list --porcelain 2>/dev/null \
  | awk -v b="branch refs/heads/$branch" '/^worktree /{w=substr($0,10)} $0==b{print w}')"
[ -n "$wt" ] && [ -n "$(git -C "$wt" config --get-all "branch.$branch.redCommit" || true)" ] || exit 0

problems=()
[ "$(git -C "$wt" config --get "branch.$branch.criteriaConfirmed" || true)" = true ] \
  || problems+=("The user has not confirmed this story's criteria. Show them, and run story.sh confirm once they agree.")
case "$cmd" in
  *"gh pr create"*|*"glab mr create"*)
    key="$(git -C "$wt" config --get "branch.$branch.issueKey" || true)"
    if [ -n "$key" ]; then
      case "$cmd" in *"[$key]"*) ;; *) problems+=("The title does not carry [$key].") ;; esac
    fi ;;
esac

[ ${#problems[@]} -eq 0 ] && exit 0
echo "$branch cannot leave this machine yet:" >&2
printf '  %s\n' "${problems[@]}" >&2
exit 2
