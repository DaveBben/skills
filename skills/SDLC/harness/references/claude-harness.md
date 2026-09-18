# Claude Code harness

Load when the harness is Claude Code. Everything here lives in `.claude/`. The commands are project-specific and live in one file the hooks share.

## Layout

```
.claude/
  settings.json          permissions and hook wiring
  hooks/
    _slots.sh            every project-specific command, defined once
    fast-check.sh        edit time
    turn-end-check.sh    turn end
    deps-guard.sh        edit time, manifest only
    session-start.sh     environment sanity
    bash-guard.sh        pre-execution hard blocks
    tests-guard.sh       edit time, accepted tests only
  rules/                 path-scoped instructions
```

## Fill the slots first

`.claude/hooks/_slots.sh` holds every command the hooks run. Nothing else in `.claude/hooks/` names a tool.

Take what the project already uses. A team already on a formatter and a linter gets those wired.

Two rules for the split. `fast_fix` and `fast_check` run on every edit, so anything needing more than the one file goes in `turn_end`. `turn_end` fires once a turn, so anything needing the network or minutes goes in the commit-time gate instead.

If a project has no usable per-file checker, leave `fast_check` returning 0 and wire `turn_end` only.

**Python / uv:**

```bash
matches()    { case "$1" in *.py) return 0 ;; *) return 1 ;; esac; }
pathspec=('*.py')
fast_fix()   { ruff check --fix "$1" >/dev/null 2>&1 || true
               ruff format "$1"     >/dev/null 2>&1 || true; }
fast_check() { ruff check "$1"; }
turn_end()   { uv run mypy src; }
deps_file='pyproject.toml'
deps_check() { uv lock --check; }
deps_fix='uv add / uv remove'
env_check()  {
  command -v uv >/dev/null 2>&1 || { echo "NOTE: uv is not on PATH."; return; }
  [ -d .venv ] || { echo "NOTE: .venv is missing, run 'uv sync'."; return; }
  uv sync --check >/dev/null 2>&1 || echo "NOTE: .venv is out of sync with uv.lock, run 'uv sync'."
}
```

The block above is the shape. Fill the same slots for the language in front of you. Three findings that are not obvious:

- **A lockfile guard must not be a dry run.** Where the package manager offers one, it frequently suppresses the frozen-lockfile check, so the guard passes on drifted input. Use the flag that resolves the lockfile without installing, plus the flag that keeps it off the network.
- **Verifying the dependency cache is not verifying the manifest.** Where the two commands look interchangeable, pick the one that compares the manifest against the source tree, not the one that checksums downloaded modules and hits the network on a miss.
- **Some languages have no per-file semantic check.** Where the single-file invocation fails on any reference to a sibling in the same package, the fast layer is formatting only and the semantic check moves to `turn_end`.

## settings.json

Merge into an existing file rather than replacing it.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "deny": [
      "Read(./.env*)", "Edit(./.env*)", "Write(./.env*)",
      "Edit(./uv.lock)", "Write(./uv.lock)",
      "Edit(./tests/feature-acceptance/**)", "Write(./tests/feature-acceptance/**)",
      "Edit(./.git/**)", "Write(./.git/**)"
    ]
  },
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash-guard.sh"}]
    }, {
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/tests-guard.sh"}]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/fast-check.sh"},
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/deps-guard.sh"}
      ]
    }],
    "Stop": [{
      "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/turn-end-check.sh"}]
    }],
    "SessionStart": [{
      "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"}]
    }]
  }
}
```

Replace `uv.lock` in the deny list with the project's own lockfile, and `tests/feature-acceptance/` with the same directory inside the project's test tree; that directory holds the user's feature acceptance tests and stays denied for the life of the repo. Add `rm` and `mv` on it to `bash-guard.sh`, since the deny list does not see the shell. Add an `allow` list for the project's routine tool invocations, so ordinary checks do not prompt.

**Exit codes differ by event.** On `PreToolUse` and `PostToolUse`, exit 2 blocks and feeds stderr to the agent. On `Stop`, exit 2 blocks the stop and feeds stderr back. On `SessionStart`, stderr goes to the user only and **stdout** is what reaches the agent, so that hook reports on stdout and never exits non-zero.

## Shared preamble

Every hook needs the edited path out of the JSON on stdin. Never assume `python3` is installed; on a TypeScript or Go machine its absence is a silent no-op that disables the loop.

```bash
# .claude/hooks/_slots.sh, above the slot definitions
read_json_field() {
  local field="$1" body
  body="$(cat)"
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$body" | jq -r --arg f "$field" '.tool_input[$f] // .[$f] // ""' 2>/dev/null
  else
    printf '%s' "$body" | sed -n "s/.*\"$field\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" | head -1
  fi
}
```

## Edit time

`.claude/hooks/fast-check.sh`, `chmod +x`.

```bash
#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

file="$(read_json_field file_path)"

# This repo only. A session can hold other working directories.
case "$file" in "$root"/*) ;; *) exit 0 ;; esac
# A source file that still exists. An edit may have been a deletion.
matches "$file" || exit 0
[ -f "$file" ] || exit 0

cd "$root"
fast_fix "$file"

set +e
output="$(fast_check "$file" 2>&1)"; code=$?
set -e

if [ "$code" -eq 1 ]; then
  echo "Issues in $file that need a real fix (not auto-fixable):" >&2
  echo "$output" >&2
  exit 2
elif [ "$code" -ne 0 ]; then
  # Fail open: the checker itself broke. Blocking here would stop every edit.
  echo "fast-check: the checker failed to run (exit $code), not a finding:" >&2
  echo "$output" >&2
fi
exit 0
```

Check what exit codes your checker actually uses before relying on the `-eq 1` test. Some return 1 for findings and something else for their own failure; others use 1 for both, in which case drop the fail-open branch and accept that a broken tool blocks.

Where the package manager wraps the tool, call the resolved binary from `fast_fix` instead and fall back to the wrapper before the environment is built. The wrapper revalidates the environment on every invocation, and this hook fires on every edit.

## Turn end

`.claude/hooks/turn-end-check.sh`. Fires once, when the agent believes it is finished.

```bash
#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

sid="$(read_json_field session_id)"
counter="${TMPDIR:-/tmp}/claude-turn-end-${sid:-unknown}"
count="$(cat "$counter" 2>/dev/null || true)"
case "$count" in ''|*[!0-9]*) count=0 ;; esac

cd "$root"

# The array stays quoted. Unquoted, bash expands the pattern against the repo
# root before git sees it, and the check silently stops firing.
changed="$(git status --porcelain -- "${pathspec[@]}" 2>/dev/null || true)"
[ -z "$changed" ] && exit 0

if ! output="$(turn_end 2>&1)"; then
  if [ "$count" -ge 3 ]; then
    rm -f "$counter"
    echo "turn-end: still failing after 3 blocked stops, letting the stop through." >&2
    exit 0
  fi
  echo $((count + 1)) > "$counter"
  echo "The turn-end check failed. Fix these before finishing:" >&2
  echo "$output" >&2
  exit 2
fi

rm -f "$counter"
exit 0
```

`pathspec` is an array and stays quoted at the call site. Unquoted, `git status --porcelain -- $(...)` returns empty on a repo with any root-level source file, and the turn-end check silently stops running.

Do not replace the retry counter with a check-once guard: that verifies before the fix is made and never re-checks after.

## Dependency guard

`.claude/hooks/deps-guard.sh`. Edit time, manifest only.

```bash
#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

file="$(read_json_field file_path)"
case "$file" in "$root/$deps_file"|"$deps_file") ;; *) exit 0 ;; esac
[ -f "$file" ] || exit 0
cd "$root"

if ! output="$(deps_check 2>&1)"; then
  echo "$deps_file no longer matches the lockfile:" >&2
  echo "$output" >&2
  echo "Change dependencies with $deps_fix, never by editing $deps_file by" >&2
  echo "hand. If this edit was intentional and not a dependency change," >&2
  echo "regenerate the lockfile." >&2
  exit 2
fi
exit 0
```

## Session start

`.claude/hooks/session-start.sh`. Reports rather than blocks: an unbuilt environment or a stale lockfile makes every later check fail for the wrong reason.

```bash
#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"
cd "$root"

# stdout, not stderr: on SessionStart only stdout reaches the agent.
env_check

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  dirty="$(git status --short)"
  [ -n "$dirty" ] && { echo "Uncommitted changes at session start:"; echo "$dirty"; }
fi
exit 0
```

Every message `env_check` prints must name the command that fixes it.

## Hard blocks

`.claude/hooks/bash-guard.sh`, wired to `PreToolUse` on `Bash`. Exit 2 cancels the command before it runs.

```bash
#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"

cmd="$(read_json_field command)"

# Strip quoted segments, then cut each command at its heredoc marker and drop
# the body that follows, so a commit message that merely mentions a blocked
# phrase passes. Cutting at the marker, not the line, keeps the flags before it:
# `git commit --no-verify -F - <<EOF` must still be seen.
scan="$(printf '%s' "$cmd" | sed -e "s/'[^']*'//g" -e 's/"[^"]*"//g' -e '/<</{s/<<.*//;q;}')"

case "$scan" in
  # Substitute this repository's own direct-install commands. Shipping a block
  # for a package manager the project does not use is blocklist creep.
  *"<direct install>"*)
    echo "Install dependencies with $deps_fix. A direct install desyncs the" >&2
    echo "environment from the lockfile." >&2
    exit 2 ;;
  *--no-verify*)
    echo "The pre-commit gate is the quality gate. To skip one hook that needs" >&2
    echo "the network, use SKIP=<hook> git commit. Never --no-verify." >&2
    exit 2 ;;
esac
# `-n` is --no-verify's short form. Match it as a whole word anywhere in a git
# commit command: padding with spaces catches it at either end, and requiring
# `git` before `commit` leaves `grep -n commit` alone.
case "$scan" in
  *git*commit*)
    case " $scan " in
      *" -n "*)
        echo "-n is --no-verify. Use SKIP=<hook> git commit to skip one hook." >&2
        exit 2 ;;
    esac ;;
esac
exit 0
```

Match the install command at a shell boundary, so a wrapper whose name ends in the same token still passes.

## Accepted-test guard

`.claude/hooks/tests-guard.sh`, wired to `PreToolUse` on `Edit|Write|MultiEdit`. Exit 2 cancels the edit. It fires only while `agile` has recorded a red commit, and only for the files that commit touched. Hooks fire for subagents too, so the builder is bound by it.

```bash
#!/usr/bin/env bash
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-.}"
. "$root/.claude/hooks/_slots.sh"
cd "$root"

red="$(git config --get agile.redCommit 2>/dev/null || true)"
[ -n "$red" ] || exit 0
git cat-file -e "$red^{commit}" 2>/dev/null || exit 0

file="$(read_json_field file_path)"
case "$file" in "$root"/*) file="${file#"$root"/}" ;; esac

if git diff --name-only "$red^" "$red" | grep -qxF "$file"; then
  echo "$file is an accepted test from red commit $red. It is the contract;" >&2
  echo "the build makes it pass, never changes it. Add a new test file for a" >&2
  echo "case the table missed. If the contract itself is wrong, stop and say so:" >&2
  echo "the user re-accepts the row, then runs 'git config --unset agile.redCommit'." >&2
  exit 2
fi
exit 0
```

`agile` sets the config at the red commit and unsets it at the merge. A deletion through the shell is not caught; `bash-guard.sh` may add `rm` on those paths as its third hard block. A rename in the refactor that a test names is the case that trips this guard legitimately: the user clears it, the refactor commits, and the review diff still reports the change.

## Path-scoped rules

`.claude/rules/*.md` take path frontmatter, so an instruction loads only for the files it governs. The frontmatter uses gitignore semantics, where `*` matches inside one path segment: `"*.py"` alone matches root-level files and nothing under `src/`. Ship both patterns.

```markdown
---
paths: ["*.py", "**/*.py"]
---
<the instruction, and the files it governs>
```

An instruction that has to hold for the whole conversation goes in the repository's agent instructions file instead, which loads every session.
