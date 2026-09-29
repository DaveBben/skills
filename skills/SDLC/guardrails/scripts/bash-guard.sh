#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

input="$(cat)"
cmd="$(printf '%s' "$input" | read_json_field command)"

# Strip quoted segments, then cut each command at its heredoc marker and drop
# the body that follows, so a commit message that merely mentions a blocked
# phrase passes. Cutting at the marker, not the line, keeps the flags before it:
# `git commit --no-verify -F - <<EOF` must still be seen.
scan="$(printf '%s' "$cmd" | sed -e "s/'[^']*'//g" -e 's/"[^"]*"//g' -e '/<</{s/<<.*//;q;}')"

case "$scan" in
  # EDIT: this repository's own direct-install command. Shipping a block for a
  # package manager the project does not use is blocklist creep.
  *"<direct install>"*)
    echo "Install dependencies with $deps_fix. A direct install desyncs the" >&2
    echo "environment from the lockfile." >&2
    exit 2 ;;
  *--no-verify*)
    echo "The pre-commit gate is the quality gate. To skip one hook, use" >&2
    echo "SKIP=<hook id> git commit; the red commit uses SKIP=tests,e2e," >&2
    echo "which red-commit-scope allows only for tests and stubs." >&2
    echo "Never --no-verify." >&2
    exit 2 ;;
esac
# rm and mv through the shell get past the deny list and the accepted-test
# guard, which see only the edit tool. Block them on the feature acceptance
# directory, and on each story's accepted tests: by absolute path in any story
# worktree, and by relative path in the worktree the command runs in (the
# session's cwd, or the target of a leading `cd <dir> &&`). The commit gate's
# accepted-tests hook catches what this misses, such as a path after `cd tests`.
if printf '%s' "$scan" | grep -Eq '(^|[;&|(]|[[:space:]])(git[[:space:]]+)?(rm|mv)[[:space:]]'; then
  here="$(printf '%s' "$input" | read_json_field cwd)"; here="${here:-$root}"
  to="$(printf '%s' "$cmd" | sed -En 's/^[[:space:]]*cd[[:space:]]+([^;&|[:space:]]+)[[:space:]]*&&.*/\1/p' | head -1)"
  if [ -n "$to" ]; then case "$to" in /*) here="$to" ;; *) here="$here/$to" ;; esac; fi
  here="$(clone_worktree "$here" || true)"
  guarded="$(
    echo "$acceptance_dir"
    git -C "$root" worktree list --porcelain | awk '/^worktree /{w=substr($0,10)} /^branch /{print substr($0,19) "\t" w}' \
      | while IFS=$'\t' read -r b wt; do
        reds="$( { git -C "$wt" config --get-all "branch.$b.redCommit"
                   [ "$wt" = "$here" ] && git -C "$wt" config --get-all agile.redCommit; } 2>/dev/null || true)"
        for red in $reds; do
          git -C "$wt" diff-tree --root --no-commit-id --name-only -r "$red" 2>/dev/null
        done | while IFS= read -r f; do
          is_test "$f" || continue
          echo "$wt/$f"
          [ "$wt" = "$here" ] && echo "$f"
        done
      done)"
  while IFS= read -r path; do
    [ -n "$path" ] || continue
    case "$cmd" in
      *"$path"*)
        echo "$path is an accepted test or one of the user's feature acceptance tests." >&2
        echo "Do not remove or move it. If it is wrong, stop and say so; the user changes" >&2
        echo "it, or deliver clears the guard once the user agrees." >&2
        exit 2 ;;
    esac
  done <<< "$guarded"
fi
# `-n` is --no-verify's short form. Match it as a whole word anywhere in a git
# commit command: padding with spaces catches it at either end, and requiring
# `git` before `commit` leaves `grep -n commit` alone.
case "$scan" in
  *git*commit*)
    case " $scan " in
      *" -n "*)
        echo "-n is --no-verify. Use SKIP=<hook id> git commit; the red commit uses SKIP=tests,e2e." >&2
        exit 2 ;;
    esac ;;
esac
exit 0
