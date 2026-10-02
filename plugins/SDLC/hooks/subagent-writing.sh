#!/bin/sh
# SubagentStart: a subagent sees none of the main session's SessionStart output,
# so hand it writing.md as additionalContext. Skip the SDLC agents, whose return
# goes only to the session (agent_type in the hook input names them). JSON-escape
# backslashes, quotes and newlines here, since jq and python3 may not be installed.
# Run with --self-test to check the filter and the output shape.
if [ "$1" = --self-test ]; then
  fail=0
  for t in SDLC:test-author SDLC:review SDLC:verify; do
    out=$(printf '{"hook_event_name":"SubagentStart","agent_type":"%s"}' "$t" | "$0")
    [ -z "$out" ] || { echo "FAIL: $t got output"; fail=1; }
  done
  for t in general-purpose Explore; do
    out=$(printf '{"hook_event_name":"SubagentStart", "agent_type": "%s"}' "$t" | "$0")
    case "$out" in '{"hookSpecificOutput":{"hookEventName":"SubagentStart","additionalContext":"# Writing rules\n'*'"}}') ;;
      *) echo "FAIL: $t got no writing rules"; fail=1 ;; esac
  done
  [ $fail = 0 ] && echo "self-test passed"
  exit $fail
fi
type=$(tr -d '\n' | sed -n 's/.*"agent_type" *: *"\([^"]*\)".*/\1/p')
case "$type" in SDLC:test-author|SDLC:review|SDLC:verify) exit 0 ;; esac
f="$(dirname "$0")/writing.md"
printf '{"hookSpecificOutput":{"hookEventName":"SubagentStart","additionalContext":"'
sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/	/\\t/g' "$f" | awk '{printf "%s\\n", $0}'
printf '"}}\n'
