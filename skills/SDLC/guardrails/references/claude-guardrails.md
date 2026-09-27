# Claude Code guardrails

Everything here lives in `.claude/`. The files ship with this skill in its `scripts/` directory. Copy each hook script into `.claude/hooks/` and `chmod +x` it, and merge `scripts/settings.json` into `.claude/settings.json`. Edit only the lines marked `# EDIT` and the settings entries named below; never rewrite a script.

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
    main-guard.sh        edit time, no edits on main
    pr-guard.sh          pre-execution, story pull requests
  rules/                 path-scoped instructions
```

## Fill the slots first

`_slots.sh` holds every command the hooks run; nothing else in `.claude/hooks/` names a tool. It starts with `read_json_field`, which reads the hook's JSON input with `jq` or `sed`: never assume `python3` is installed, since on a TypeScript or Go machine its absence silently disables the loop. Its `# EDIT` lines are the Python / uv example; fill the same slots for the project's language, taking what the project already uses. Three findings that are not obvious:

- **A lockfile guard must not be a dry run.** Where the package manager offers one, it frequently suppresses the frozen-lockfile check, so the guard passes on drifted input. Use the flag that resolves the lockfile without installing, plus the flag that keeps it off the network.
- **Verifying the dependency cache is not verifying the manifest.** Where the two commands look interchangeable, pick the one that compares the manifest against the source tree, not the one that checksums downloaded modules and hits the network on a miss.
- **Some languages have no per-file semantic check.** Where the single-file invocation fails on any reference to a sibling in the same package, the fast layer is formatting only and the semantic check moves to `turn_end`.

## settings.json

Merge into an existing file rather than replacing it. Replace `uv.lock` in the deny list with the project's own lockfile, and `tests/feature-acceptance/` with the same directory inside the project's test tree; that directory holds the user's feature acceptance tests and stays denied for the life of the repo. Set `acceptance_dir` in `_slots.sh` to that directory; `bash-guard.sh` blocks `rm` and `mv` on it, since the deny list does not see the shell. The `~/.holdout/**` entries deny the user's hidden scenarios for `deliver`; keep them even when the user has none yet, and `bash-guard.sh` blocks shell commands naming that directory except its `run` command. Add an `allow` list for the project's routine tool invocations, so ordinary checks do not prompt.

**Exit codes differ by event.** On `PreToolUse` and `PostToolUse`, exit 2 blocks and feeds stderr to the agent. On `Stop`, exit 2 blocks the stop and feeds stderr back. On `SessionStart`, stderr goes to the user only and **stdout** is what reaches the agent, so that hook reports on stdout and never exits non-zero.

## Edit time: fast-check.sh

Check what exit codes the checker actually uses before relying on the `-eq 1` test. Some return 1 for findings and something else for their own failure; others use 1 for both, in which case drop the fail-open branch and accept that a broken tool blocks.

Where the package manager wraps the tool, call the resolved binary from `fast_fix` instead and fall back to the wrapper before the environment is built. The wrapper revalidates the environment on every invocation, and this hook fires on every edit.

## Turn end: turn-end-check.sh

Do not replace the retry counter with a check-once guard: that verifies before the fix is made and never re-checks after. The hook exits early on a clean tree, so `deliver`'s red commit, made before its turn ends, passes it with failing tests committed.

## Dependency guard and session start

`deps-guard.sh` runs at edit time on the manifest only. `session-start.sh` reports rather than blocks, and prints at most the change count and 20 lines of `git status`, since its output loads into every session.

## Hard blocks: bash-guard.sh

Wired to `PreToolUse` on `Bash`; exit 2 cancels the command before it runs. Edit its `<direct install>` line to the repository's own direct-install command, matched at a shell boundary, so a wrapper whose name ends in the same token still passes.

## Accepted-test guard: tests-guard.sh

Wired to `PreToolUse` on `Edit|Write|MultiEdit`. Exit 2 cancels the edit. It fires only while `deliver` has recorded a red commit for the branch the edited file's worktree is on, and only for the files those commits touched and the check paths, the lines under `# owner reads: checks` in `CODEOWNERS`. The key `branch.<branch>.redCommit` is per branch, so stories running in separate worktrees each keep their own guard, and multi-valued, because a corrected row adds a second red commit. It also reads the older single key `agile.redCommit`. Hooks fire for subagents too, so the builder is bound by it.

`deliver` adds the branch's key at each red commit and unsets it at the merge. `bash-guard.sh` blocks `rm` and `mv` naming a file a recorded red commit touched, and the commit gate's `accepted-tests` hook refuses a commit that changes or deletes an accepted test by any route. A rename in the refactor that a test names is the case that trips this guard legitimately: `deliver` clears it once the user agrees, the refactor commits, and the review diff still reports the change.

## Pull request guard: pr-guard.sh

Wired to `PreToolUse` on `Bash`. Exit 2 cancels `gh pr create` or `glab mr create` for a `story/*` branch with a red commit recorded, until verify has written `exceptions.txt` after the branch's last commit, `done-block.md` has no `Security: pending` line, the title carries the branch's `[<issueKey>]`, and the body starts with `Read code:`. It finds the branch from `--head`, a leading `cd <dir> &&`, or the session's working directory. A story on the trivial or no-behaviour-change path records no red commit, so the guard lets its pull request through.

## Main guard and prompt reminder: main-guard.sh

Wired to `PreToolUse` on `Edit|Write|MultiEdit`, ahead of `tests-guard.sh`. Exit 2 cancels any edit on `main_branch` in any worktree of this clone, except the paths in `main_ok`, and tells the agent to run `deliver`, which edits only in a story worktree. Set both in `_slots.sh`. Add to `main_ok` only files other skills write on main.

`settings.json` also wires `UserPromptSubmit` to an `echo`. Its stdout reaches the agent with every prompt, so the instruction to run `deliver` arrives even when the request's wording does not match the skill's description.

## Path-scoped rules

`.claude/rules/*.md` take path frontmatter, so an instruction loads only for the files it governs. The frontmatter uses gitignore semantics, where `*` matches inside one path segment: `"*.py"` alone matches root-level files and nothing under `src/`. Ship both patterns.

```markdown
---
paths: ["*.py", "**/*.py"]
---
<the instruction, and the files it governs>
```
