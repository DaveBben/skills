#!/usr/bin/env bash
# Usage: story.sh start <slug> <key> <short-name> | red | rebase | close <branch> | status | self-test
#
# The git steps of a story, run from any worktree of the repository.
#   start   cuts story/<slug>/<key>-<short-name> from the latest main into a
#           worktree beside the repository, records <key> as the branch's
#           issueKey for the commit hook that tags messages, and prints its path
#   red     records HEAD, the red commit just made, in the accepted-test guard
#   rebase  rebases the current story branch on the latest main and re-records
#           every red commit under its new hash, matched by commit message
#   close   removes the branch's worktree, its guard keys and the branch, after
#           a merge or a cut
#   status  prints one line per story worktree: branch, path, and where the loop
#           restarts. It runs close on a branch whose pull request has merged.
#           Run it from the main checkout.
# MAIN overrides the main branch name (default main).
set -euo pipefail
main="${MAIN:-main}"
die() { echo "$*" >&2; exit 1; }

repo() { dirname "$(git rev-parse --path-format=absolute --git-common-dir)"; }
base() {
  if git remote get-url origin >/dev/null 2>&1; then
    git fetch -q origin "$main" && echo "origin/$main"
  else
    echo "$main"
  fi
}
story_branch() {
  local b; b="$(git branch --show-current)"
  case "$b" in story/*) echo "$b" ;; *) die "Run this in a story worktree; the current branch is '$b'." ;; esac
}

case "${1:-}" in
start)
  [ $# -eq 4 ] || die "Usage: story.sh start <slug> <key> <short-name>"
  r="$(repo)"
  wt="$(dirname "$r")/$(basename "$r")-$3"
  git worktree add -q -b "story/$2/$3-$4" "$wt" "$(base)" >&2
  git config "branch.story/$2/$3-$4.issueKey" "$3"
  echo "$wt"
  ;;
red)
  b="$(story_branch)"
  git config --add "branch.$b.redCommit" "$(git rev-parse HEAD)"
  git rev-parse HEAD
  ;;
rebase)
  b="$(story_branch)"
  old="$(git config --get-all "branch.$b.redCommit" || true)"
  onto="$(base)"
  git rebase -q "$onto" || die "The rebase stopped on a conflict. Resolve it, run 'git rebase --continue', then run story.sh rebase again."
  new=()
  for h in $old; do
    msg="$(git log -1 --format=%B "$h")"
    match=""
    for c in $(git rev-list "$onto..HEAD"); do
      [ "$(git log -1 --format=%B "$c")" = "$msg" ] && { match="$c"; break; }
    done
    [ -n "$match" ] || die "Red commit $h has no commit with its message after the rebase. The guard is unchanged."
    new+=("$match")
  done
  git config --unset-all "branch.$b.redCommit" || true
  for c in ${new[@]+"${new[@]}"}; do git config --add "branch.$b.redCommit" "$c"; echo "$c"; done
  ;;
close)
  [ $# -eq 2 ] || die "Usage: story.sh close <branch>"
  r="$(repo)"
  wt="$(git -C "$r" worktree list --porcelain | awk -v b="branch refs/heads/$2" '/^worktree /{w=substr($0,10)} $0==b{print w}')"
  [ -z "$wt" ] || git -C "$r" worktree remove "$wt"
  git -C "$r" config --unset-all "branch.$2.redCommit" || true
  git -C "$r" config --unset-all agile.redCommit || true
  git -C "$r" branch -q -D "$2"
  ;;
status)
  r="$(repo)"; me="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  command -v gh >/dev/null || echo "gh is not installed, so pull request state is not checked." >&2
  git -C "$r" worktree list --porcelain \
    | awk '/^worktree /{w=substr($0,10)} /^branch refs\/heads\/story\//{print substr($0,19) "\t" w}' \
    | while IFS=$'\t' read -r b wt; do
    pr="$(cd "$wt" && gh pr view "$b" --json state -q .state </dev/null 2>/dev/null || true)"
    case "$pr" in
      MERGED) "$me" close "$b" && at="merged; worktree, branch and guard removed" ;;
      CLOSED) at="pull request closed without merging: ask the user to reopen it or cut the story" ;;
      OPEN) at="pull request open: SKILL.md section 8, watch it" ;;
      *)
        db="$(git -C "$wt" rev-parse --path-format=absolute --git-dir)/done-block.md"
        if grep -Eq '^(Security|Refuted):[[:space:]]*pending' "$db" 2>/dev/null; then
          at="Done block with security or refute pending: loop.md section 6"
        elif [ -f "$db" ]; then
          at="Done block and no pull request: SKILL.md section 7"
        elif [ -n "$(git -C "$wt" config --get-all "branch.$b.redCommit" || true)" ]; then
          at="red commit and no Done block: loop.md section 5"
        else
          at="no red commit: loop.md section 4, setup"
        fi ;;
    esac
    printf '%s\t%s\t%s\n' "$b" "$wt" "$at"
  done
  ;;
self-test)
  t="$(cd "$(mktemp -d)" && pwd -P)"; trap 'rm -rf "$t"' EXIT
  me="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  git init -q -b main "$t/app" && cd "$t/app"
  git -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
  wt="$("$me" start pay PAY-1 refunds)"
  [ "$wt" = "$t/app-PAY-1" ] || die "FAIL start path: $wt"
  [ "$(git config branch.story/pay/PAY-1-refunds.issueKey)" = PAY-1 ] || die "FAIL start did not record the issue key"
  "$me" status 2>/dev/null | grep -q "no red commit" || die "FAIL status before the red commit"
  cd "$wt"
  echo x > test_a && git add test_a && git -c user.name=t -c user.email=t@t commit -q -m "red: refunds"
  red="$("$me" red)"
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "red commit and no Done block" || die "FAIL status after the red commit"
  echo "Refuted:     pending" > "$(git rev-parse --git-dir)/done-block.md"
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "loop.md section 6" || die "FAIL status with a pending Done block"
  echo "Refuted:     none" > "$(git rev-parse --git-dir)/done-block.md"
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "section 7" || die "FAIL status with a Done block"
  rm "$(git rev-parse --git-dir)/done-block.md"
  cd "$t/app" && echo y > other && git add other && git -c user.name=t -c user.email=t@t commit -q -m main-moves
  cd "$wt" && moved="$("$me" rebase)"
  [ "$moved" != "$red" ] && [ "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit)" = "$moved" ] \
    || die "FAIL rebase did not re-record the red commit"
  cd "$t/app" && "$me" close story/pay/PAY-1-refunds
  [ ! -d "$wt" ] && ! git rev-parse -q --verify story/pay/PAY-1-refunds >/dev/null \
    && [ -z "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit || true)" ] \
    || die "FAIL close left the worktree, branch or guard key"
  echo "self-test passed"
  ;;
*) sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
