#!/bin/sh
# SubagentStart: a subagent sees none of the main session's SessionStart output,
# so hand it writing.md as additionalContext. JSON-escape backslashes, quotes
# and newlines here, since jq and python3 may not be installed.
f="$(dirname "$0")/writing.md"
printf '{"hookSpecificOutput":{"hookEventName":"SubagentStart","additionalContext":"'
sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/	/\\t/g' "$f" | awk '{printf "%s\\n", $0}'
printf '"}}\n'
