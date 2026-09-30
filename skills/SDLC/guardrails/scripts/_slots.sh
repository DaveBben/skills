#!/usr/bin/env bash
# Sourced by every hook after _lib.sh, which holds the shared functions. Every
# project-specific command lives here, defined once.

# EDIT: every line below. This is the Python / uv example; fill the same slots
# for the project's own language and tools.
matches()    { case "$1" in *.py) return 0 ;; *) return 1 ;; esac; }
# Test files, relative to the worktree; `*` matches across `/`. Keep them the
# same as the test globs of the red-commit-scope and accepted-tests hooks.
is_test()    { case "$1" in tests/*|*/tests/*|test_*.py|*/test_*.py) return 0 ;; *) return 1 ;; esac; }
pathspec=('*.py')
fast_fix()   { ruff check --fix "$1" >/dev/null 2>&1 || true
               ruff format "$1"     >/dev/null 2>&1 || true; }
# fast-check.sh reads exit 1 as "found problems" and any other non-zero exit
# as "could not run". Check the checker's exit codes, and map them here when
# they differ.
fast_check() { ruff check "$1"; }
# Every turn-end slot: types, contracts, rules, complexity, and tests when the
# suite finishes in under five seconds. Fail when any fails; turn-end-check.sh
# runs only this.
turn_end()   { local rc=0
               uv run mypy src || rc=1
               # One line each for contracts, rules, complexity and fast tests.
               return $rc; }
deps_file='pyproject.toml'
# A lockfile check that resolves without installing and stays offline; a dry
# run often skips the frozen-lockfile check. Of two dependency checks, pick the
# one that compares the manifest with the source, not the one that checksums
# downloads.
deps_check() { uv lock --check; }
deps_fix='uv add / uv remove'
env_check()  {
  command -v uv >/dev/null 2>&1 || { echo "NOTE: uv is not on PATH."; return; }
  [ -d .venv ] || { echo "NOTE: .venv is missing, run 'uv sync'."; return; }
  uv sync --check >/dev/null 2>&1 || echo "NOTE: .venv is out of sync with uv.lock, run 'uv sync'."
}
main_branch='main'
main_ok=('AGENTS.md' 'CLAUDE.md' 'docs/adr/*' 'docs/architecture/*')
acceptance_dir='tests/feature-acceptance/'
