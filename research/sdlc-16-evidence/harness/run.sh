#!/usr/bin/env bash
# run.sh <task> <arm> <rep>: one run; arms/<arm>.txt is appended to the working conditions
set -uo pipefail
. $HOME/projects/sdlc-experiment/env.sh
t=$1 arm=$2 rep=$3 id=$1-$2-$3; . $X/tasks/$t/task.env
d=$X/runs/$id
repo=$("$X/prep.sh" "$t" "$id" | tail -1) || { echo "prep failed $id"; exit 1; }
mkdir -p "$d/log"; cd "$repo"
[ "$arm" = carefullock ] && cp "$X/tools/lock-pre-commit.sh" .git/hooks/pre-commit
cond=$'\n\n---\nWorking conditions:\n- This checkout has no git remote and no issue tracker. This message is the issue; call it TASK-1.\n- I am away until you finish and cannot answer questions. Make every decision yourself and list the ones you made in your final message.\n- Do not push and do not open a pull request. Finish with the change committed to git in this repository (any branch), with no uncommitted changes.'
prompt="$(cat $X/tasks/$t/story.md)$cond"
[ -s "$X/arms/$arm.txt" ] && prompt="$prompt"$'\n'"$(cat $X/arms/$arm.txt)"
. $X/flags.sh
case "$arm" in sdlc|sdlc16) prompt="/SDLC:deliver $prompt" ;; esac
printf '%s' "$prompt" > "$d/prompt.txt"
date +%s > "$d/start"
claude -p "$prompt" "${flags[@]}" > "$d/log/turn1.jsonl" 2> "$d/log/turn1.err"
grep -m1 '"session_id"' "$d/log/turn1.jsonl" | python3 -c 'import json,sys;print(json.loads(sys.stdin.readline())["session_id"])' > "$d/session"
exec $X/loop.sh "$t" "$arm" "$rep"
