#!/usr/bin/env bash
# prep.sh <task> <run-id>: fresh checkout of the task's base commit with no remote,
# no later history, dependencies installed. Prints the repo path.
set -euo pipefail
. $HOME/projects/sdlc-experiment/env.sh
t=$1 id=$2; . $X/tasks/$t/task.env
d=$X/runs/$id; rm -rf "$d"; mkdir -p "$d"; cd "$d"
if [ -n "${CLONE_FROM:-}" ]; then  # a prepared checkout with state outside git (the guardrails harness)
  cp -cR "$X/runs/$CLONE_FROM/repo" repo && cd repo && git reset -q --hard "$BASE" && git clean -fdq -e .venv -e node_modules -e build -e models
else
  git init -q -b main repo && cd repo
  git fetch -q "$X/cache/${KIND:-$t}.git" "$BASE" && git reset -q --hard FETCH_HEAD
fi
git config user.name "Experiment User"; git config user.email "exp@example.com"
sh -c "$SETUP"
git status --porcelain | head -5
echo "$d/repo"
