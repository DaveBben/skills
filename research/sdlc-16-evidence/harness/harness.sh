#!/usr/bin/env bash
# harness.sh: build the guardrails harness once on a fresh llama.cpp base checkout (run id llama-harness-0)
set -uo pipefail
. $HOME/projects/sdlc-experiment/env.sh
id=llama-harness-0; d=$X/runs/$id
repo=$("$X/prep.sh" llama "$id" | tail -1) || exit 1
mkdir -p "$d/log"; cd "$repo"
prompt='/SDLC:guardrails Get this repository ready for agents: write AGENTS.md and set up the checks, the agent hooks, the commit gate and one check command, running every setup stage.

---
Working conditions:
- This checkout has no git remote and no issue tracker.
- I am away until you finish and cannot answer questions. Make every decision yourself, taking your recommended option, and list the ones you made in your final message.
- Do not push and do not open a pull request. Finish with everything committed to git on main, with no uncommitted changes.'
flags=(--model claude-opus-5-5 --effort high --setting-sources project,local --strict-mcp-config
       --permission-mode auto --disallowedTools AskUserQuestion "Bash(git push:*)" "Bash(gh:*)"
       --output-format stream-json --verbose --max-budget-usd 60 --plugin-dir $HOME/projects/skills/plugins/SDLC)
date +%s > "$d/start"
claude -p "$prompt" "${flags[@]}" > "$d/log/turn1.jsonl" 2> "$d/log/turn1.err"
sid=$(grep -m1 '"session_id"' "$d/log/turn1.jsonl" | python3 -c 'import json,sys;print(json.loads(sys.stdin.readline())["session_id"])')
for n in 2 3; do
  [ -z "$(git status --porcelain)" ] && tail -c 400 "$d/log/turn$((n-1)).jsonl" | grep -vq '?' && break
  claude -p "I am still away and cannot answer. Decide anything open yourself, taking your recommended option, and keep going until every setup stage is done and committed on main. If everything is already finished and committed, reply DONE." --resume "$sid" "${flags[@]}" > "$d/log/turn$n.jsonl" 2> "$d/log/turn$n.err"
done
date +%s > "$d/end"; echo "finished $id"
