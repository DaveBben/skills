#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

input="$(cat)"
cmd="$(printf '%s' "$input" | read_json_field command)"
case "$cmd" in *"gh pr create"*|*"glab mr create"*) ;; *) exit 0 ;; esac

# The branch is --head when given, else the branch of the directory the
# command runs in: the session's cwd, or the target of a leading `cd <dir> &&`.
dir="$(printf '%s' "$input" | read_json_field cwd)"; dir="${dir:-$root}"
to="$(printf '%s' "$cmd" | sed -En 's/^[[:space:]]*cd[[:space:]]+([^;&|[:space:]]+)[[:space:]]*&&.*/\1/p' | head -1)"
if [ -n "$to" ]; then case "$to" in /*) dir="$to" ;; *) dir="$dir/$to" ;; esac; fi
branch="$(printf '%s' "$cmd" | sed -En 's/.*(--head|-H)[= ]+([^[:space:]]+).*/\2/p' | head -1)"
branch="${branch//[\"\']/}"
[ -n "$branch" ] || branch="$(git -C "$dir" branch --show-current 2>/dev/null || true)"
case "$branch" in story/*) ;; *) exit 0 ;; esac

# Only a story that went through the full loop has a red commit recorded; the
# trivial and no-behaviour-change paths open their pull requests without one.
wt="$(git -C "$dir" worktree list --porcelain 2>/dev/null \
  | awk -v b="branch refs/heads/$branch" '/^worktree /{w=substr($0,10)} $0==b{print w}')"
[ -n "$wt" ] && [ -n "$(git -C "$wt" config --get-all "branch.$branch.redCommit" || true)" ] || exit 0
gd="$(git -C "$wt" rev-parse --path-format=absolute --git-dir)"

problems=()
ex="$gd/exceptions.txt"
if [ ! -f "$ex" ]; then
  problems+=("exceptions.txt is missing from $gd: verify has not run on this branch.")
# The AGENTS.md rewrite is the story's last commit and lands after verify, so it
# does not count.
elif [ "$(stat -c %Y "$ex" 2>/dev/null || stat -f %m "$ex")" -lt \
       "$(git -C "$wt" log -1 --format=%ct -- . ':(exclude)AGENTS.md' ':(exclude)CLAUDE.md')" ]; then
  problems+=("exceptions.txt is older than the branch's last code commit: run verify again.")
fi
if grep -Eq '^Security:[[:space:]]*pending' "$gd/done-block.md" 2>/dev/null; then
  problems+=("done-block.md says Security: pending: run the security review first.")
fi
if grep -Eq '^Refuted:[[:space:]]*pending' "$gd/done-block.md" 2>/dev/null; then
  problems+=("done-block.md says Refuted: pending: run the refute step first.")
fi
key="$(git -C "$wt" config --get "branch.$branch.issueKey" || true)"
if [ -n "$key" ]; then
  case "$cmd" in *"[$key]"*) ;; *) problems+=("The title does not carry [$key].") ;; esac
fi
file="$(printf '%s' "$cmd" | sed -En 's/.*(--body-file|-F)[= ]+([^[:space:]]+).*/\2/p' | head -1)"
file="${file//[\"\']/}"
if [ -n "$file" ]; then
  case "$file" in /*) ;; *) file="$dir/$file" ;; esac
  head -1 "$file" 2>/dev/null | grep -q '^Read code:' || problems+=("The body file's first line is not 'Read code:'.")
elif ! printf '%s\n' "$cmd" | grep -Eq "^[[:space:]]*Read code:|(--body|-b|--description|-d)[= ]+[\"']?Read code:"; then
  problems+=("The body does not start with a 'Read code:' line.")
fi

[ ${#problems[@]} -eq 0 ] && exit 0
echo "The pull request for $branch cannot open yet. Write its description by deliver's" >&2
echo "references/pull-request.md, after review and verify:" >&2
printf '  %s\n' "${problems[@]}" >&2
exit 2
