# sourced by run.sh and loop.sh after t, arm are set: the claude flags for this arm
flags=(--model claude-opus-5-5 --effort high --setting-sources project,local --strict-mcp-config
       --permission-mode auto --disallowedTools AskUserQuestion "Bash(git push:*)" "Bash(gh:*)"
       --output-format stream-json --verbose --include-hook-events --max-budget-usd 60)
case "$arm" in
  sdlc|sdlc16) flags+=(--plugin-dir $HOME/projects/skills/plugins/SDLC) ;;
  writing) flags+=(--plugin-dir $X/plugins/writing-only) ;;
esac
