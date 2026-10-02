#!/usr/bin/env bash
# loop.sh <task> <arm> <rep>: resume the run's session until status.py says done (at most 4 sessions in all)
set -uo pipefail
. $HOME/projects/sdlc-experiment/env.sh
t=$1 arm=$2 rep=$3 id=$1-$2-$3; . $X/tasks/$t/task.env
d=$X/runs/$id; repo=$d/repo; sid=$(cat "$d/session")
. $X/flags.sh
follow="I am still away and cannot answer. Decide anything open yourself, taking your recommended option, and keep going until the work is finished and committed locally (no push, no pull request). If you need my confirmation of what a person can do once this merges: $CONFIRM If everything is already finished and committed, reply DONE."
for n in 2 3 4; do
  [ -f "$d/log/turn$n.jsonl" ] && continue
  s=$(python3 $X/status.py "$d" "$BASE" "$d/log/turn$((n-1)).jsonl"); echo "turn$((n-1)): $s" >> "$d/status.log"
  [ "$s" = done ] && break
  cd "$repo" && claude -p "$follow" --resume "$sid" "${flags[@]}" > "$d/log/turn$n.jsonl" 2> "$d/log/turn$n.err"
done
[ -f "$d/log/turn4.jsonl" ] && echo "turn4: $(python3 $X/status.py "$d" "$BASE" "$d/log/turn4.jsonl")" >> "$d/status.log"
date +%s > "$d/end"
echo "finished $id"
