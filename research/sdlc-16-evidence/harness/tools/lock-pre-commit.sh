#!/usr/bin/env bash
# pre-commit: refuse a commit that changes a file the recorded red commit touched.
b=$(git branch --show-current); red=$(git config --get "branch.$b.redCommit") || exit 0
files=$(git diff-tree --no-commit-id --name-only -r "$red")
changed=$(git diff --cached --name-only -- $files)
[ -z "$changed" ] && exit 0
echo "Refused: these accepted test files changed after the red commit $red: $changed" >&2
echo "The accepted tests are locked. A test you cannot satisfy for a reason that holds against the code is a stop: report the test and the reason instead of changing it." >&2
exit 1
