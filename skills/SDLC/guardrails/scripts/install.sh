#!/usr/bin/env bash
# Usage: install.sh [repository] | --self-test
#
# Installs the Claude Code hooks into <repository> (default: the current
# directory): copies each hook script beside this file into .claude/hooks/,
# makes it executable, merges settings.json into .claude/settings.json, and
# prints every line the agent must edit for this project. A hook script that
# holds `# EDIT` lines is copied only when it is not there yet, so a re-run
# keeps the project's edits; every other one, _lib.sh included, is overwritten,
# so a re-run brings the shared functions up to date. Safe to run twice.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
hooks=(_lib.sh _slots.sh fast-check.sh deps-guard.sh turn-end-check.sh session-start.sh
       bash-guard.sh main-guard.sh tests-guard.sh push-guard.sh)

# The shipped settings win on a shared key; the deny list and each hook event's
# list are unions, with exact duplicates dropped.
merge='def union: reduce .[] as $x ([]; if any(.[]; . == $x) then . else . + [$x] end);
  .[0] as $a | .[1] as $b | ($a * $b)
  | .permissions.deny = (($a.permissions.deny // []) + ($b.permissions.deny // []) | union)
  | .hooks = reduce (($b.hooks // {}) | keys[]) as $e (($a.hooks // {});
      .[$e] = ((.[$e] // []) + $b.hooks[$e] | union))'

install() {
  local repo="$1" dest settings f
  dest="$repo/.claude/hooks"; settings="$repo/.claude/settings.json"
  mkdir -p "$dest"
  for f in "${hooks[@]}"; do
    if [ -f "$dest/$f" ] && grep -q '# EDIT' "$here/$f"; then
      echo "kept $dest/$f (it holds this project's edits)"
    else
      cp "$here/$f" "$dest/$f"
    fi
    chmod +x "$dest/$f"
  done
  if [ ! -f "$settings" ]; then
    cp "$here/settings.json" "$settings"
  elif command -v jq >/dev/null 2>&1; then
    jq -s "$merge" "$settings" "$here/settings.json" > "$settings.tmp" && mv "$settings.tmp" "$settings"
  else
    echo "jq is missing, so $settings was not merged. Merge $here/settings.json into it by hand:"
    echo "  add its permissions.deny entries, and append each of its hooks events' lists."
  fi
  echo
  echo "Edit these lines for this project (the comment above each says how):"
  grep -Hn '# EDIT' "$dest"/*.sh || true
  grep -Hn 'uv.lock\|tests/feature-acceptance' "$settings" \
    | sed 's/$/   <- replace with the project'"'"'s lockfile and feature acceptance directory/' || true
}

self_test() {
  local d; d="$(mktemp -d /tmp/guardrails-install-XXXXXX)"
  trap 'rm -rf "$d"' RETURN
  git -C "$d" init -q
  mkdir -p "$d/.claude"
  printf '%s\n' '{"model":"x","permissions":{"deny":["Read(./secret)"],"allow":["Bash(ls)"]},' \
    '"hooks":{"Stop":[{"hooks":[{"type":"command","command":"mine.sh"}]}]}}' > "$d/.claude/settings.json"
  install "$d" >/dev/null
  echo 'fast_check() { mine; }' >> "$d/.claude/hooks/_slots.sh"
  install "$d" >/dev/null
  local s="$d/.claude/settings.json"
  for f in "${hooks[@]}"; do [ -x "$d/.claude/hooks/$f" ] || { echo "FAIL: $f not installed"; return 1; }; done
  grep -q 'fast_check() { mine; }' "$d/.claude/hooks/_slots.sh" || { echo "FAIL: re-run overwrote _slots.sh"; return 1; }
  [ "$(jq -r '.model' "$s")" = x ] || { echo "FAIL: lost an existing key"; return 1; }
  [ "$(jq -r '.permissions.allow[0]' "$s")" = 'Bash(ls)' ] || { echo "FAIL: lost the allow list"; return 1; }
  jq -e '.permissions.deny | index("Read(./secret)") and index("ScheduleWakeup") and index("Skill(loop)")' "$s" >/dev/null \
    || { echo "FAIL: deny lists not unioned"; return 1; }
  [ "$(jq '.hooks.Stop | length' "$s")" = 2 ] || { echo "FAIL: Stop hooks not unioned once"; return 1; }
  [ "$(jq '.hooks.PreToolUse | length' "$s")" = 2 ] || { echo "FAIL: a re-run duplicated hooks"; return 1; }
  [ "$(jq '.permissions.deny | length' "$s")" = "$(jq '.permissions.deny | length + 1' "$here/settings.json")" ] \
    || { echo "FAIL: a re-run duplicated deny entries"; return 1; }
  install "$d" | grep -q '_slots.sh:.*# EDIT' || { echo "FAIL: EDIT lines not printed"; return 1; }
  hook_self_test "$d" || return 1
  # An install from before _lib.sh: its _slots.sh defines the shared functions
  # of that time, not physical(), and holds `# EDIT`, so a re-run keeps it.
  local o="$d/old"; mkdir -p "$o/.claude/hooks"; git -C "$o" init -q
  { cat "$here/_lib.sh"; sed 1d "$here/_slots.sh"; } | sed '/^physical()/,/^}/d' > "$o/.claude/hooks/_slots.sh"
  echo '# stale' > "$o/.claude/hooks/_lib.sh"
  install "$o" >/dev/null
  grep -q '^physical()' "$o/.claude/hooks/_slots.sh" && { echo "FAIL: the old-style _slots.sh was replaced"; return 1; }
  cmp -s "$o/.claude/hooks/_lib.sh" "$here/_lib.sh" || { echo "FAIL: a re-run did not overwrite _lib.sh"; return 1; }
  hook_self_test "$o" || { echo "FAIL: the guards above broke over an old-style _slots.sh"; return 1; }
  echo "install self-test passed"
}

# The installed guards, run on a repository reached through a symlink (on
# macOS /tmp is one too), where git prints the resolved path.
hook_self_test() {
  local d="$1" l="$1/via-link" h="$1/.claude/hooks" f got red
  ln -s "$d" "$l"
  echo 'deps_check() { echo drifted; return 1; }' >> "$h/_slots.sh"
  git -C "$d" symbolic-ref HEAD refs/heads/main
  git -C "$d" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
  run() { local rc=0
    printf '{"tool_input":{"file_path":"%s"}}' "$2" | CLAUDE_PROJECT_DIR="$l" "$h/$1" >/dev/null 2>&1 || rc=$?
    echo "$rc"; }
  for f in "main-guard.sh $l/AGENTS.md 0" "main-guard.sh AGENTS.md 0" "main-guard.sh $l/CLAUDE.md 0" \
           "main-guard.sh $l/docs/adr/0001-x.md 0" "main-guard.sh $l/docs/architecture/snapshots/x.md 0" \
           "main-guard.sh $l/src/x.py 2" "main-guard.sh $d/src/x.py 2"; do
    set -- $f; got="$(run "$1" "$2")"
    [ "$got" = "$3" ] || { echo "FAIL: $1 on $2 exited $got, want $3"; return 1; }
  done
  git -C "$d" checkout -q -b story/x
  mkdir -p "$d/tests"; echo 'def test_a(): assert 0' > "$d/tests/test_a.py"
  printf '# owner reads: checks\n.pre-commit-config.yaml @me\n\n' > "$d/CODEOWNERS"
  touch "$d/pyproject.toml"
  git -C "$d" add tests CODEOWNERS
  git -C "$d" -c user.name=t -c user.email=t@t commit -q -m red
  red="$(git -C "$d" rev-parse HEAD)"; git -C "$d" config branch.story/x.redCommit "$red"
  for f in "tests-guard.sh $l/tests/test_a.py 2" "tests-guard.sh $l/.pre-commit-config.yaml 2" \
           "tests-guard.sh $l/tests/test_b.py 0" "tests-guard.sh $l/src/x.py 0" \
           "deps-guard.sh $l/pyproject.toml 2" "deps-guard.sh $l/src/x.py 0"; do
    set -- $f; got="$(run "$1" "$2")"
    [ "$got" = "$3" ] || { echo "FAIL: $1 on $2 exited $got, want $3"; return 1; }
  done
}

if [ "${1:-}" = --self-test ]; then self_test; else install "${1:-.}"; fi
