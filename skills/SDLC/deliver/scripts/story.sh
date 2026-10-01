#!/usr/bin/env bash
# Usage: story.sh start <slug> <key> <short-name> | adopt <key> | red [hash...] | unred | rebase | confirm | verify '<check command>' | close <branch> | status [--local] | self-test
#
# The git steps of a story, run from any worktree of the repository.
#   start   cuts story/<slug>/<key>-<short-name> from the latest main into a
#           worktree beside the repository and prints its path
#   adopt   makes the branch checked out here a story branch for <key>, for
#           work that already has a branch or an open pull request
#   red     records HEAD, or each hash given, as a red commit: its test files
#           and the tests that existed at the base are then accepted tests, and
#           the guard refuses a commit that changes them
#   unred   clears this branch's red commits, after the user agreed a test was wrong
#   rebase  rebases the story branch on the latest main and re-records every
#           red commit under its new hash, matched by commit message
#   confirm records that the user confirmed the story; the guard refuses a
#           push or pull request for the branch until then
#   verify  rebases as above, fails when a test file changed since its red
#           commit, or since the base when no red commit touched it, then runs the check command, given as one string,
#           through sh -c and exits with its status
#   close   removes the branch's worktree, its records and the branch, after a
#           merge or a cut
#   status  prints one line per story worktree: branch, path, and where it
#           stands; it closes a branch whose pull request has merged. Run it
#           from the main checkout. --local skips the pull request check.
# MAIN names the branch start cuts from (default main); start records it as the
# branch's base, and rebase and verify reuse that base.
set -euo pipefail
main="${MAIN:-main}"
die() { echo "$*" >&2; exit 1; }

repo() { dirname "$(git rev-parse --path-format=absolute --git-common-dir)"; }
base() {  # $1: branch name, default $main
  local m="${1:-$main}"
  if git remote get-url origin >/dev/null 2>&1; then
    git fetch -q origin "$m" && echo "origin/$m"
  else
    echo "$m"
  fi
}
do_rebase() {
  local b="$1" old onto h pid match c used=" "
  old="$(git config --get-all "branch.$b.redCommit" || true)"
  onto="$(base "$(git config --get "branch.$b.base" || echo "$main")")"
  [ -z "$(git status --porcelain --untracked-files=no)" ] || die "The worktree has uncommitted changes. Commit or undo them, then run this again."
  git rebase -q "$onto" || die "The rebase stopped on a conflict. Resolve it, run 'git rebase --continue', then run story.sh rebase again."
  local new=()
  # Matched by patch, not message: a red commit rewritten with the same message is not the red commit.
  for h in $old; do
    pid="$(git show "$h" | git patch-id --stable | cut -d' ' -f1)"
    match=""
    for c in $(git rev-list "$onto..HEAD"); do
      case "$used" in *" $c "*) continue ;; esac
      [ "$(git show "$c" | git patch-id --stable | cut -d' ' -f1)" = "$pid" ] && { match="$c"; break; }
    done
    [ -n "$match" ] || die "Red commit $h has no commit with the same changes after the rebase: an accepted test changed. The guard is unchanged."
    used="$used$match "; new+=("$match")
  done
  git config --unset-all "branch.$b.redCommit" || true
  for c in ${new[@]+"${new[@]}"}; do git config --add "branch.$b.redCommit" "$c"; echo "$c"; done
}
# ponytail: a test file is a path under test/, tests/, spec/ or __tests__/, or
# named test_*, *_test.*, *.test.* or *.spec.*; set TESTS to a grep -E pattern
# when the project names tests differently.
test_pat() { echo "${TESTS:-(^|/)(tests?|specs?|__tests__)/|(^|/)test_[^/]*$|_test\.[^/]*$|\.(test|spec)\.[^/]*$}"; }
reds_newest_first() {  # $1 branch: its recorded red commits, newest first
  local c left; set -- " $(echo $(git config --get-all "branch.$1.redCommit" || true)) "
  left="$(echo $1 | wc -w | tr -d ' ')"
  for c in $(git rev-list HEAD); do
    [ "$left" -gt 0 ] || break
    case "$1" in *" $c "*) echo "$c"; left=$((left - 1)) ;; esac
  done
}
is_story() { case "$1" in story/*) return 0 ;; esac; [ "$(git config --get "branch.$1.story" || true)" = true ]; }
story_branch() {
  local b; b="$(git branch --show-current)"
  is_story "$b" && echo "$b" || die "Run this in a story worktree; the current branch is '$b'. Run story.sh adopt <key> to make it one."
}
pr_state() {  # prints MERGED, OPEN, CLOSED or nothing, from gh or glab
  local s
  if command -v gh >/dev/null && s="$(gh pr view "$1" --json state -q .state </dev/null 2>/dev/null)"; then echo "$s"; return; fi
  if command -v glab >/dev/null && s="$(glab mr view "$1" -F json </dev/null 2>/dev/null | sed -n 's/.*"state": *"\([a-z]*\)".*/\1/p' | head -1)"; then
    case "$s" in merged) echo MERGED ;; opened) echo OPEN ;; closed) echo CLOSED ;; esac
  fi
}

state() {  # $1 branch: where the story stands, from its git config
  if [ "$(git config --get "branch.$1.criteriaConfirmed" || true)" = true ]; then echo "confirmed: verify and open the pull request"
  elif [ -n "$(git config --get-all "branch.$1.redCommit" || true)" ]; then echo "red commit recorded: build, review, then confirm"
  else echo "no red commit: write the failing tests"; fi
}

case "${1:-}" in
start)
  [ $# -eq 4 ] || die "Usage: story.sh start <slug> <key> <short-name>"
  r="$(repo)"
  wt="$(dirname "$r")/$(basename "$r")-$3"
  git worktree add -q -b "story/$2/$3-$4" "$wt" "$(base)" >&2
  git config "branch.story/$2/$3-$4.issueKey" "$3"
  git config "branch.story/$2/$3-$4.base" "$main"
  echo "$wt"
  ;;
adopt)
  [ $# -eq 2 ] || die "Usage: story.sh adopt <key>"
  b="$(git branch --show-current)"
  [ -n "$b" ] && [ "$b" != "$main" ] || die "Check out the story's own branch first; adopt refuses '$b'."
  git config "branch.$b.story" true
  git config "branch.$b.issueKey" "$2"
  echo "$b"
  ;;
red)
  b="$(story_branch)"; shift
  [ $# -gt 0 ] || set -- HEAD
  for h in "$@"; do
    c="$(git rev-parse "$h")"
    git config --get-all "branch.$b.redCommit" "^$c\$" >/dev/null || git config --add "branch.$b.redCommit" "$c"
    echo "$c"
  done
  ;;
unred)
  b="$(story_branch)"
  git config --unset-all "branch.$b.redCommit" || true
  ;;
rebase)
  do_rebase "$(story_branch)"
  ;;
confirm)
  b="$(story_branch)"
  git config "branch.$b.criteriaConfirmed" true
  echo "criteria confirmed on $b"
  ;;
verify)
  [ $# -ge 2 ] || die "Usage: story.sh verify '<check command>'"
  shift
  b="$(story_branch)"
  do_rebase "$b" | sed 's/^/red: /'
  changed=""
  nl='
'
  seen="$nl"
  # Each test file is compared with the newest red commit that touched it, so a
  # corrected row committed as a later red commit passes.
  pat="$(test_pat)"
  for h in $(reds_newest_first "$b"); do
    # Read one path per line, so a path with a space stays one path.
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      case "$seen" in *"$nl$f$nl"*) continue ;; esac
      seen="$seen$f$nl"
      git diff --quiet "$h" HEAD -- "$f" 2>/dev/null || changed="$changed '$f'"
    done < <(git -c core.quotePath=false diff-tree --no-commit-id --name-only -r "$h" | grep -E "$pat" || true)
  done
  # Tests that existed before the story, and that no red commit changed, match the base.
  if [ -n "$(git config --get-all "branch.$b.redCommit" || true)" ]; then
    mb="$(git merge-base "$(base "$(git config --get "branch.$b.base" || echo "$main")")" HEAD)"
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      case "$seen" in *"$nl$f$nl"*) continue ;; esac
      git diff --quiet "$mb" HEAD -- "$f" 2>/dev/null || changed="$changed '$f'"
    done < <(git -c core.quotePath=false ls-tree -r --name-only "$mb" | grep -E "$pat" || true)
  fi
  [ -z "$changed" ] || die "FAIL accepted tests changed since their red commit or the base:$changed"
  echo "accepted tests unchanged"
  # One string through sh -c, so &&, pipes, variables and globs in the check
  # command work whatever shell the caller runs.
  sh -c "$*"
  ;;
close)
  [ $# -eq 2 ] || die "Usage: story.sh close <branch>"
  r="$(repo)"
  wt="$(git -C "$r" worktree list --porcelain | awk -v b="branch refs/heads/$2" '/^worktree /{w=substr($0,10)} $0==b{print w}')"
  [ -z "$wt" ] || git -C "$r" worktree remove "$wt"
  git -C "$r" config --unset-all "branch.$2.redCommit" || true
  git -C "$r" config --unset-all "branch.$2.criteriaConfirmed" || true
  git -C "$r" config --unset-all "branch.$2.story" || true
  git -C "$r" config --unset-all "branch.$2.base" || true
  git -C "$r" branch -q -D "$2"
  ;;
status)
  r="$(repo)"; me="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"; local_only="${2:-}"
  [ -n "$local_only" ] || command -v gh >/dev/null || command -v glab >/dev/null || echo "Neither gh nor glab is installed, so pull request state is not checked." >&2
  git -C "$r" worktree list --porcelain \
    | awk '/^worktree /{w=substr($0,10)} /^branch refs\/heads\//{print substr($0,19) "\t" w}' \
    | while IFS=$'\t' read -r b wt; do
    (cd "$wt" && is_story "$b") || continue
    pr=""; [ -n "$local_only" ] || pr="$(cd "$wt" && pr_state "$b" || true)"
    case "$pr" in
      MERGED) "$me" close "$b" && at="merged; worktree, branch and guard removed" ;;
      CLOSED) at="pull request closed without merging: ask the user to reopen it or cut the story" ;;
      OPEN) at="pull request open: watch it" ;;
      *) at="$(state "$b")" ;;
    esac
    printf '%s\t%s\t%s\n' "$b" "$wt" "$at"
  done
  ;;
self-test)
  t="$(cd "$(mktemp -d)" && pwd -P)"; trap 'rm -rf "$t"' EXIT
  me="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  commit() { git -c user.name=t -c user.email=t@t commit -q "$@"; }
  git init -q -b main "$t/app" && cd "$t/app" && echo old > old_test.go && git add -A && commit -m init
  wt="$("$me" start pay PAY-1 refunds)"
  [ "$wt" = "$t/app-PAY-1" ] || die "FAIL start path: $wt"
  [ "$(git config branch.story/pay/PAY-1-refunds.issueKey)" = PAY-1 ] || die "FAIL start did not record the issue key"
  [ "$(git config branch.story/pay/PAY-1-refunds.base)" = main ] || die "FAIL start did not record the base"
  "$me" status --local | grep -q "no red commit" || die "FAIL status before the red commit"
  cd "$wt"
  mkdir -p tests && echo x > test_a && echo x > "tests/my test.py" && echo stub > app_a && git add -A && commit -m "red: refunds"
  red="$("$me" red)"
  "$me" red >/dev/null && [ "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit | wc -l)" -eq 1 ] \
    || die "FAIL red recorded one commit twice"
  (cd "$t/app" && "$me" status --local) | grep -q "red commit recorded" || die "FAIL status after the red commit"
  "$me" confirm >/dev/null
  (cd "$t/app" && "$me" status --local) | grep -q "confirmed" || die "FAIL status after confirm"
  cd "$t/app" && echo y > other && git add other && commit -m main-moves
  cd "$wt" && moved="$("$me" rebase)"
  [ "$moved" != "$red" ] && [ "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit)" = "$moved" ] \
    || die "FAIL rebase did not re-record the red commit"
  echo built > app_a && commit -am "build fills the stub"
  "$me" verify true | grep -q "accepted tests unchanged" || die "FAIL verify on unchanged tests"
  if "$me" verify false >/dev/null 2>&1; then die "FAIL verify ignored the check command's status"; fi
  "$me" verify 'true && echo "a b" | grep -q "a b"' >/dev/null || die "FAIL verify of a check command with && and a pipe"
  echo z > test_a && commit -am "edit accepted test"
  if "$me" verify true >/dev/null 2>&1; then die "FAIL verify passed an edited accepted test"; fi
  "$me" red >/dev/null && "$me" verify true >/dev/null || die "FAIL verify after a corrected test's red commit"
  echo y > "tests/my test.py" && commit -am "edit a test whose path has a space"
  if "$me" verify true >/dev/null 2>&1; then die "FAIL verify missed an edited test whose path has a space"; fi
  "$me" red >/dev/null
  echo changed > old_test.go && commit -am "edit a test that existed before the story"
  if "$me" verify true >/dev/null 2>&1; then die "FAIL verify missed an edited pre-existing test"; fi
  git -c user.name=t -c user.email=t@t revert --no-edit HEAD >/dev/null && "$me" verify true >/dev/null || die "FAIL verify after the pre-existing test was restored"
  echo dirty > app_a
  out="$("$me" verify true 2>&1 || true)"; case "$out" in *"uncommitted changes"*) ;; *) die "FAIL verify did not name uncommitted changes: $out" ;; esac
  git checkout -q -- app_a
  h="$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit | tail -1)"; m="$(git log -1 --format=%B "$h")"
  git reset -q --soft "$h~1" && echo pass > test_a && git add -A && commit -m "$m"
  if "$me" verify true >/dev/null 2>&1; then die "FAIL verify accepted a red commit rewritten with the same message"; fi
  git reset -q --hard "$h"
  "$me" unred && [ -z "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit || true)" ] || die "FAIL unred"
  "$me" red "$red" >/dev/null && [ "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit)" = "$red" ] || die "FAIL red <hash>"
  cd "$t/app" && git worktree add -q -b feature/old "$t/app-old" main && cd "$t/app-old"
  "$me" red >/dev/null 2>&1 && die "FAIL red on a branch that is not a story"
  "$me" adopt PAY-2 >/dev/null && "$me" red >/dev/null || die "FAIL adopt"
  st="$(cd "$t/app" && "$me" status --local)"; case "$st" in *feature/old*) ;; *) die "FAIL status misses an adopted branch" ;; esac
  cd "$t/app" && "$me" close feature/old && [ -z "$(git config --get branch.feature/old.story || true)" ] || die "FAIL close of an adopted branch"
  "$me" close story/pay/PAY-1-refunds
  [ ! -d "$wt" ] && ! git rev-parse -q --verify story/pay/PAY-1-refunds >/dev/null \
    && [ -z "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit || true)" ] \
    && [ -z "$(git config --get branch.story/pay/PAY-1-refunds.criteriaConfirmed || true)" ] \
    || die "FAIL close left the worktree, branch or records"
  echo "self-test passed"
  ;;
*) sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
