#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

cmd="$(read_json_field command)"

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
# The holdout directory (~/.holdout/ by default) holds the user's hidden
# scenarios. Only its `run` command may name it, alone, with no pipe, chain or
# redirect. This stops accidents; anything that runs code can still read it.
# The raw command is matched, since quoting the path must not hide it.
case "$cmd" in
  *.holdout*)
    first="${cmd%% *}"
    case "$cmd" in *[\;\|\&\`\<\>]*|*'$('*) first="" ;; esac
    case "$first" in
      *.holdout/*/run) ;;
      *)
        echo "The holdout directory holds the user's hidden scenarios. Do not read," >&2
        echo "list or copy it. The only command that may name it is its run command," >&2
        echo "on its own: <holdout dir>/run --done <numbers> --diff <file>." >&2
        exit 2 ;;
    esac ;;
esac
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
