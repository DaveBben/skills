#!/usr/bin/env bash
# Sourced by every hook. Every project-specific command lives here, defined once.

read_json_field() {
  local field="$1" body
  body="$(cat)"
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$body" | jq -r --arg f "$field" '.tool_input[$f] // .[$f] // ""' 2>/dev/null
  else
    printf '%s' "$body" | sed -n "s/.*\"$field\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" | head -1
  fi
}

# Prints the top of the worktree holding <path> when that worktree belongs to
# this clone, and fails otherwise. A session can hold other repositories, and
# deliver's story worktrees sit outside the project directory.
clone_worktree() {
  local dir="$1" wt
  while [ ! -d "$dir" ]; do dir="$(dirname "$dir")"; done
  wt="$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)" || return 1
  [ "$(git -C "$wt" rev-parse --path-format=absolute --git-common-dir)" = \
    "$(git -C "$root" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" ] || return 1
  echo "$wt"
}

# EDIT: every line below. This is the Python / uv example; fill the same slots
# for the project's own language and tools.
matches()    { case "$1" in *.py) return 0 ;; *) return 1 ;; esac; }
# Test files, relative to the worktree; `*` matches across `/`. Keep them the
# same as the test globs of the red-commit-scope and accepted-tests hooks.
is_test()    { case "$1" in tests/*|*/tests/*|test_*.py|*/test_*.py) return 0 ;; *) return 1 ;; esac; }
pathspec=('*.py')
fast_fix()   { ruff check --fix "$1" >/dev/null 2>&1 || true
               ruff format "$1"     >/dev/null 2>&1 || true; }
fast_check() { ruff check "$1"; }
turn_end()   { uv run mypy src; }
deps_file='pyproject.toml'
deps_check() { uv lock --check; }
deps_fix='uv add / uv remove'
env_check()  {
  command -v uv >/dev/null 2>&1 || { echo "NOTE: uv is not on PATH."; return; }
  [ -d .venv ] || { echo "NOTE: .venv is missing, run 'uv sync'."; return; }
  uv sync --check >/dev/null 2>&1 || echo "NOTE: .venv is out of sync with uv.lock, run 'uv sync'."
}
main_branch='main'
main_ok=('AGENTS.md' 'CLAUDE.md' 'docs/adr/*')
acceptance_dir='tests/feature-acceptance/'
