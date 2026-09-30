#!/usr/bin/env bash
# Usage: story.sh start <slug> <key> <short-name> | adopt <key> | red [hash...] | unred | confirm | rebase | verify '<check command>' | kill '<test command>' | close <branch> | status [--local] | next [step] | self-test
#
# The git steps of a story, run from any worktree of the repository.
#   start   cuts story/<slug>/<key>-<short-name> from the latest main into a
#           worktree beside the repository, records <key> as the branch's
#           issueKey for the commit hook that tags messages, and prints its path
#   adopt   makes the branch checked out here a story branch for <key>, for
#           work that already has a branch or an open pull request
#   red     records HEAD, or each hash given, in the accepted-test guard, and
#           refuses a commit whose test table leaves a Killed by cell empty
#   unred   clears the guard's record of every red commit on this branch
#   confirm records that the user confirmed the story's criteria; the push
#           guard refuses a push or pull request for the branch until then
#   rebase  rebases the current story branch on the latest main and re-records
#           every red commit under its new hash, matched by commit message
#   verify  rebases as above, fails when a file a red commit touched has changed
#           since that commit, then runs the check command, given as one string,
#           through sh -c and exits with its status
#   kill    applies each row's competitor patch, attack/mutants/<row>.patch in
#           the git directory, runs the test command through sh -c, restores
#           the tree, and prints killed, SURVIVED, REFUSED, DID NOT APPLY or
#           MISSING per row. A patch may change only lines the story wrote,
#           and no test file. Exits 1 unless every row is killed or skipped
#   close   removes the branch's worktree, its guard keys and the branch, after
#           a merge or a cut
#   status  prints one line per story worktree: branch, path, and the next step.
#           It runs close on a branch whose pull request has merged. Run it
#           from the main checkout. --local skips the pull request check.
#   next    prints the rules of the current story's next step, from
#           references/steps/<step>.md; with a step name, prints that step.
#           next open also records that the story's pull request is open
# MAIN names the branch start cuts from (default main); start records it as the
# branch's base, and rebase, verify and kill reuse that base.
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
  local b="$1" old onto h msg match c
  old="$(git config --get-all "branch.$b.redCommit" || true)"
  onto="$(base "$(git config --get "branch.$b.base" || echo "$main")")"
  git rebase -q "$onto" || die "The rebase stopped on a conflict. Resolve it, run 'git rebase --continue', then run story.sh rebase again."
  local new=()
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
rows() {  # commits, newest first: "<row>\t<Killed by>\t<1 when it characterizes existing behaviour>" per index row, newest wins
  local h
  for h in "$@"; do git log -1 --format=%B "$h"; done | awk -F'|' '
    /^\| *[0-9]+ *\|/ {
      n = $2; k = $6; gsub(/^[ \t]+|[ \t]+$/, "", n); gsub(/^[ \t]+|[ \t]+$/, "", k)
      if (!(n in seen)) { seen[n] = 1; print n "\t" k "\t" ($0 ~ /characteri[sz]es existing behaviou?r/) }
    }'
}
vacuous() {  # rows on stdin: prints the numbers whose Killed by names no competitor
  awk -F'\t' '{ k = tolower($2) } k == "" || k ~ /^(none|n\/?a|-+|\?+|tbd|todo|stub|missing|not implemented|any (change|mutation|mutant|wrong implementation))$/ { print $1 }'
}
story_lines() {  # "<file>\t<line>" for each line of HEAD the story wrote since its base, and each place it deleted
  local m onto
  m="$(git config --get "branch.$1.base" || echo "$main")"
  onto="$m"; git rev-parse -q --verify "origin/$m" >/dev/null && onto="origin/$m"
  git -c core.quotePath=false diff -U0 "$(git merge-base "$onto" HEAD)" HEAD | awk '
    /^\+\+\+ b\// { f = substr($0, 7); next }
    /^\+\+\+ / { f = ""; next }
    /^@@ / && f != "" {
      split($3, a, ","); s = substr(a[1], 2) + 0; c = (a[2] == "") ? 1 : a[2] + 0
      if (c == 0) { print f "\t" s; print f "\t" (s + 1) }
      for (i = 0; i < c; i++) print f "\t" (s + i)
    }'
}
refuse_patch() {  # $1 patch, $2 story lines: prints why the patch is refused, or nothing
  printf '%s\n' "$2" | PAT="$(test_pat)" awk '
    function refuse(m) { print m; bad = 1; exit }
    NR == FNR { split($0, t, "\t"); ok[t[1] "\t" t[2]] = 1; next }
    !inhunk && /^--- / {
      if ($0 !~ /^--- a\//) refuse("creates a file")
      f = substr($0, 7); if (f ~ ENVIRON["PAT"]) refuse("edits the test file " f)
      next
    }
    !inhunk && /^@@ / {
      split($0, h, " "); split(substr(h[2], 2), o, ","); split(substr(h[3], 2), w, ",")
      l = o[1] + 0; oc = (o[2] == "") ? 1 : o[2] + 0; nc = (w[2] == "") ? 1 : w[2] + 0; inhunk = 1; next
    }
    !inhunk { next }
    /^-/ { if (!ok[f "\t" l]) refuse("changes " f ":" l ", a line the story did not write"); l++; oc--; n++ }
    /^\+/ { if (!ok[f "\t" l] && !ok[f "\t" (l - 1)]) refuse("inserts at " f ":" l ", outside the lines the story wrote"); nc--; n++ }
    /^ / || $0 == "" { l++; oc--; nc-- }
    oc <= 0 && nc <= 0 { inhunk = 0 }
    END { if (!bad && !n) print "changes nothing" }
  ' - "$1"
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

steps="$(dirname "$0")/../references/steps"
state() {  # $1 branch, $2 worktree: prints "<where it stands>\t<step>" from local files
  local b="$1" wt="$2" db gd
  db="$(git -C "$wt" rev-parse --path-format=absolute --git-dir)/done-block.md"
  gd="$(dirname "$db")"
  if [ -f "$db" ] && [ ! -f "$gd/security.md" ] && grep -qs '^Security: *needed' "$db" "$gd/card.md"; then
    printf 'reviewed, security needed and not run: run the security agent\tsecurity'
  elif [ -f "$db" ] && grep -q 'pending refute' "$db"; then
    printf 'reviewed, not refuted: run the refute agent on findings.md and security.md\trefute'
  elif [ -f "$db" ]; then
    if [ "$(git -C "$wt" config --get "branch.$b.prOpened" || true)" = true ]; then
      printf 'pull request open: watch it\topen'
    elif [ "$(git -C "$wt" config --get "branch.$b.criteriaConfirmed" || true)" = true ]; then
      printf 'reviewed and confirmed: verify, log and open the pull request\tconfirm'
    else
      printf 'reviewed: act on the review, verify, then show the criteria for confirmation\tverdicts'
    fi
  elif [ -f "$gd/refactor.md" ]; then
    printf 'refactored and not reviewed: review\treview'
  elif git -C "$wt" grep -q 'TODO(user)' -- . 2>/dev/null; then
    printf "waits for the user's turn: offer the core or sketch at its TODO(user) marker\tbuild"
  elif [ -n "$(git -C "$wt" config --get-all "branch.$b.redCommit" || true)" ]; then
    printf 'red commit and no review: build\tbuild'
  else
    printf 'no red commit: set up\tsetup'
  fi
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
    bad="$(rows "$c" | vacuous)"
    [ -z "$bad" ] || die "Red commit $c: row $(echo $bad) names no competitor in Killed by. Name the wrong implementation each row's fixture rejects, amend the message, and run story.sh red again."
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
  [ -z "$changed" ] || die "FAIL accepted tests changed since their red commit:$changed"
  echo "accepted tests unchanged"
  # One string through sh -c, so &&, pipes, variables and globs in the check
  # command work whatever shell the caller runs.
  sh -c "$*"
  ;;
kill)
  [ $# -eq 2 ] || die "Usage: story.sh kill '<command that runs the story's tests>'"
  b="$(story_branch)"; cmd="$2"
  git diff --quiet && git diff --cached --quiet || die "Commit or undo the worktree's changes first; kill applies each patch to HEAD."
  dir="$(git rev-parse --path-format=absolute --git-dir)/attack/mutants"
  table="$(rows $(reds_newest_first "$b") | sort -n)"
  [ -n "$table" ] || die "No red commit's message holds a test table, so no row names a competitor."
  sh -c "$cmd" </dev/null >/dev/null 2>&1 || die "The test command fails on the built code, so no competitor can be judged: $cmd"
  lines="$(story_lines "$b")"; status=0
  trap 'exit 130' INT TERM
  while IFS=$'\t' read -r n k c; do
    p="$dir/$n.patch"
    if [ "$c" = 1 ]; then echo "skipped $n: characterizes existing behaviour"; continue; fi
    if [ ! -s "$p" ]; then echo "MISSING $n: no $p for '$k'"; status=1; continue; fi
    why="$(refuse_patch "$p" "$lines")"
    if [ -n "$why" ]; then echo "REFUSED $n: the patch $why"; status=1; continue; fi
    git apply "$p" 2>/dev/null || { echo "DID NOT APPLY $n: $p"; status=1; continue; }
    trap 'git apply -R "$p"' EXIT
    if sh -c "$cmd" </dev/null >/dev/null 2>&1; then echo "SURVIVED $n: $k"; status=1; else echo "killed $n: $k"; fi
    git apply -R "$p"; trap - EXIT
  done <<< "$table"
  exit "$status"
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
  git -C "$r" config --unset-all agile.redCommit || true
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
      *) at="$(state "$b" "$wt" | cut -f1)" ;;
    esac
    printf '%s\t%s\t%s\n' "$b" "$wt" "$at"
  done
  ;;
next)
  step="${2:-}"
  if [ -z "$step" ]; then
    b="$(story_branch)"; wt="$(git rev-parse --show-toplevel)"
    pr="$(pr_state "$b" || true)"
    case "$pr" in
      MERGED|OPEN|CLOSED) at="pull request $(echo "$pr" | tr 'A-Z' 'a-z')"; step=open ;;
      *) st="$(state "$b" "$wt")"; at="${st%%$'\t'*}"; step="${st##*$'\t'}" ;;
    esac
    echo "Story $b: $at."
  fi
  [ -f "$steps/$step.md" ] || die "No step '$step'. Steps: $(cd "$steps" && ls | sed 's/\.md$//' | tr '\n' ' ')"
  if [ "$step" = open ]; then
    b="$(git branch --show-current 2>/dev/null || true)"
    ! is_story "$b" 2>/dev/null || git config "branch.$b.prOpened" true
  fi
  cat "$steps/$step.md"
  ;;
self-test)
  t="$(cd "$(mktemp -d)" && pwd -P)"; trap 'rm -rf "$t"' EXIT
  me="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  git init -q -b main "$t/app" && cd "$t/app"
  git -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
  wt="$("$me" start pay PAY-1 refunds)"
  [ "$wt" = "$t/app-PAY-1" ] || die "FAIL start path: $wt"
  [ "$(git config branch.story/pay/PAY-1-refunds.issueKey)" = PAY-1 ] || die "FAIL start did not record the issue key"
  [ "$(git config branch.story/pay/PAY-1-refunds.base)" = main ] || die "FAIL start did not record the base"
  "$me" status 2>/dev/null | grep -q "no red commit" || die "FAIL status before the red commit"
  cd "$wt"
  "$me" next | grep -q "^# Step: set up" || die "FAIL next before the red commit"
  "$me" next verify | grep -q "^# Step: verify" || die "FAIL next with a step name"
  if "$me" next nosuch >/dev/null 2>&1; then die "FAIL next accepted an unknown step"; fi
  mkdir -p tests && echo x > test_a && echo x > "tests/my test.py" && echo stub > app_a && git add -A && git -c user.name=t -c user.email=t@t commit -q -m "red: refunds"
  red="$("$me" red)"
  "$me" red >/dev/null && [ "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit | wc -l)" -eq 1 ] \
    || die "FAIL red recorded one commit twice"
  (cd "$t/app" && "$me" status --local) | grep -q "red commit and no review" || die "FAIL status --local after the red commit"
  "$me" next | grep -q "^# Step: build" || die "FAIL next after the red commit"
  echo "# TODO(user): row 1" > app_a
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "user's turn" || die "FAIL status misses a waiting user's turn"
  echo stub > app_a
  touch "$(git rev-parse --git-dir)/refactor.md"
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "refactored and not reviewed" || die "FAIL status after the refactor"
  rm "$(git rev-parse --git-dir)/refactor.md"
  printf 'DONE\nFindings:    pending refute\n' > "$(git rev-parse --git-dir)/done-block.md"
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "not refuted" || die "FAIL status before the refute"
  "$me" next | grep -q "^# Step: refute" || die "FAIL next before the refute"
  printf 'Security: needed: auth\n' > "$(git rev-parse --git-dir)/card.md"
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "security needed" || die "FAIL status misses a pending security review"
  "$me" next | grep -q "^# Step: security review" || die "FAIL next before the security review"
  touch "$(git rev-parse --git-dir)/security.md"
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "not refuted" || die "FAIL status after the security review"
  rm "$(git rev-parse --git-dir)/card.md" "$(git rev-parse --git-dir)/security.md"
  echo "DONE" > "$(git rev-parse --git-dir)/done-block.md"
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "show the criteria" || die "FAIL status with a review and no confirmation"
  "$me" next | grep -q "^# Step: act on the review" || die "FAIL next after the refute"
  "$me" confirm >/dev/null
  (cd "$t/app" && "$me" status 2>/dev/null) | grep -q "reviewed and confirmed" || die "FAIL status after confirm"
  "$me" next open >/dev/null
  (cd "$t/app" && "$me" status --local) | grep -q "pull request open" || die "FAIL status --local after the pull request opened"
  "$me" next | grep -q "^# Step: pull request open" || die "FAIL next with no code host after the pull request opened"
  rm "$(git rev-parse --git-dir)/done-block.md"
  cd "$t/app" && echo y > other && git add other && git -c user.name=t -c user.email=t@t commit -q -m main-moves
  cd "$wt" && moved="$("$me" rebase)"
  [ "$moved" != "$red" ] && [ "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit)" = "$moved" ] \
    || die "FAIL rebase did not re-record the red commit"
  echo built > app_a && git -c user.name=t -c user.email=t@t commit -q -am "build fills the stub"
  "$me" verify true | grep -q "accepted tests unchanged" || die "FAIL verify on unchanged tests"
  if "$me" verify false >/dev/null 2>&1; then die "FAIL verify ignored the check command's status"; fi
  "$me" verify 'true && echo "a b" | grep -q "a b"' >/dev/null || die "FAIL verify of a check command with && and a pipe"
  if "$me" verify 'true && false' >/dev/null 2>&1; then die "FAIL verify ignored the status of a compound check command"; fi
  echo z > test_a && git -c user.name=t -c user.email=t@t commit -q -am "edit accepted test"
  if "$me" verify true >/dev/null 2>&1; then die "FAIL verify passed an edited accepted test"; fi
  "$me" red >/dev/null && "$me" verify true >/dev/null || die "FAIL verify after a corrected row's red commit"
  echo y > "tests/my test.py" && git -c user.name=t -c user.email=t@t commit -q -am "edit a test whose path has a space"
  if "$me" verify true >/dev/null 2>&1; then die "FAIL verify missed an edited test whose path has a space"; fi
  "$me" red >/dev/null
  "$me" unred && [ -z "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit || true)" ] || die "FAIL unred"
  "$me" red "$red" >/dev/null && [ "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit)" = "$red" ] || die "FAIL red <hash>"
  cd "$t/app" && git worktree add -q -b feature/old "$t/app-old" main && cd "$t/app-old"
  "$me" red >/dev/null 2>&1 && die "FAIL red on a branch that is not a story"
  "$me" adopt PAY-2 >/dev/null && "$me" red >/dev/null || die "FAIL adopt"
  st="$(cd "$t/app" && "$me" status 2>/dev/null)"; case "$st" in *feature/old*) ;; *) die "FAIL status misses an adopted branch" ;; esac
  cd "$t/app" && "$me" close feature/old && [ -z "$(git config --get branch.feature/old.story || true)" ] || die "FAIL close of an adopted branch"
  cd "$t/app" && "$me" close story/pay/PAY-1-refunds
  [ ! -d "$wt" ] && ! git rev-parse -q --verify story/pay/PAY-1-refunds >/dev/null \
    && [ -z "$(git config --get-all branch.story/pay/PAY-1-refunds.redCommit || true)" ] \
    && [ -z "$(git config --get branch.story/pay/PAY-1-refunds.criteriaConfirmed || true)" ] \
    || die "FAIL close left the worktree, branch or guard key"
  k="$("$me" start pay PAY-3 price)" && cd "$k"
  commit() { git -c user.name=t -c user.email=t@t commit -q "$@"; }
  mkdir -p tests && echo '[ "$(sh price.sh 3 5)" = 15 ]' > tests/t.sh && echo 'exit 1' > price.sh && git add -A
  commit -m "red: price" -m "| 1 | total | Unit | Requirement | none |"
  if "$me" red >/dev/null 2>&1; then die "FAIL red accepted a row with no competitor"; fi
  table='| # | Test | Level | Generator | Killed by |
|---|---|---|---|---|
| 1 | total | Unit | Requirement | ignores the quantity |
| 2 | total | Unit | Type | swaps the operands |
| 3 | total | Unit | Type | edits the test |
| 4 | total | Unit | Type | edits old code |
| 5 | total | Unit | Type | never written |
| 6 | old | Acceptance | Requirement | breaks other; characterizes existing behaviour |'
  commit --amend -m "red: price" -m "$table" && "$me" red >/dev/null || die "FAIL red refused a table that names every competitor"
  printf 'echo $(( $1 * $2 ))\n' > price.sh && commit -am build
  m="$(git rev-parse --git-dir)/attack/mutants" && mkdir -p "$m"
  printf 'echo $2\n' > price.sh && git diff > "$m/1.patch"
  printf 'echo $(( $2 * $1 ))\n' > price.sh && git diff > "$m/2.patch" && git checkout -q -- price.sh
  echo true > tests/t.sh && git diff > "$m/3.patch" && git checkout -q -- tests/t.sh
  echo z > other && git diff > "$m/4.patch" && git checkout -q -- other
  out="$("$me" kill 'sh tests/t.sh')" && die "FAIL kill exited 0 with a survivor"
  printf '%s\n' "$out" | grep -q '^killed 1:' || die "FAIL kill missed a killed competitor: $out"
  printf '%s\n' "$out" | grep -q '^SURVIVED 2: swaps the operands' || die "FAIL kill missed a survivor: $out"
  printf '%s\n' "$out" | grep -q '^REFUSED 3: the patch edits the test file tests/t.sh' || die "FAIL kill applied a patch to a test: $out"
  printf '%s\n' "$out" | grep -q '^REFUSED 4: the patch changes other:1' || die "FAIL kill applied a patch outside the story: $out"
  printf '%s\n' "$out" | grep -q '^MISSING 5:' || die "FAIL kill missed a row with no patch: $out"
  printf '%s\n' "$out" | grep -q '^skipped 6:' || die "FAIL kill did not skip a characterization row: $out"
  git diff --quiet || die "FAIL kill left a patch applied"
  echo "self-test passed"
  ;;
*) sed -n '2,34p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
