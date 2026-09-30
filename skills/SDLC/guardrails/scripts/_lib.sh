#!/usr/bin/env bash
# Sourced by every hook before _slots.sh. The functions the hooks share, with no
# project-specific line; install.sh overwrites this file on every run, so a fix
# here reaches an existing install. An older _slots.sh that still defines some
# of them overrides them with its own copies, which is harmless.

# On PreToolUse, PostToolUse and Stop, a hook's exit 2 blocks and feeds its
# stderr to the agent; on SessionStart, only stdout reaches the agent.

# jq, else sed; keep python3 out of the hooks.
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

# Prints <path> with every symlinked directory in it resolved, the form
# `git rev-parse --show-toplevel` prints, so a path under a worktree can be cut
# to one relative to it. The last parts may not exist yet.
physical() {
  local p="$1" tail=""
  while [ ! -d "$p" ]; do tail="/$(basename "$p")$tail"; p="$(dirname "$p")"; done
  printf '%s%s\n' "$(cd "$p" && pwd -P)" "$tail"
}
