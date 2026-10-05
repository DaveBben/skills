---
name: guardrails
description: "Use this skill when the user wants a rule their AI agent must follow in a codebase, asks what rules, checks or hooks a repository already enforces or whether anything stops a mistake from landing, wants a rule turned into a lint, semgrep or hook check, or a repository needs its default checks set up. Use it on: 'make a rule for X', 'add a rule', 'always do X', 'never do Y', 'ban this pattern', 'the agent keeps making this mistake', 'set up guardrails', 'what rules are in my repo', 'do I have guardrails in place', 'can this be a semgrep rule', 'write a lint rule for X', 'we have no linting', 'add a commit gate', 'run the tests when claude finishes', 'which of our CLAUDE.md rules could be checks', and the bare word 'guardrails'. Load it before searching the repository. Puts each rule where it is followed most: a deterministic check first, a path-scoped rule file second, a line in AGENTS.md last. Writing AGENTS.md as a whole is the `orient` skill."
license: MIT
metadata:
  version: "5.0.0"
---
# Guardrails

A rule a program checks is followed every time. A rule an agent reads is followed when the agent remembers it. Put every rule as high on this ladder as it will go.

| Rung | Where | Use when |
|---|---|---|
| 1. Check | A compiler or linter setting, a Semgrep rule, a script or a test, run by `./check` | A program can decide pass or fail from the code, the config or a command |
| 2. Path-scoped rule | `.claude/rules/<topic>.md` with `paths:` frontmatter, plus one equivalent (below) for each other agent whose instructions file or directory exists, such as `.cursor/` or `.github/copilot-instructions.md` | It needs judgment and applies to some paths |
| 3. Agent instructions | One line under Constraints in the root `AGENTS.md` | It needs judgment and applies everywhere |

Rung 2 equivalents for other agents:

* **Cursor:** `.cursor/rules/<topic>.mdc` with `globs:`.
* **GitHub Copilot:** `.github/instructions/<topic>.instructions.md` with `applyTo:`.
* **Agents with no path-scoped format, such as Codex:** a nested `AGENTS.md` in that directory.

`./check` is the repository's check command, `./check --full` adds the slow tests, and `./check --scheduled` runs off the gates on CI's schedule. [references/defaults.md](references/defaults.md) sets up all three.

## Routing

* **A request to set up checks, hooks or linting,** such as 'we have no linting' or 'run the tests when claude finishes': set them up by [references/defaults.md](references/defaults.md).
* **'What rules or guardrails do I have':** list the steps `./check` runs, the hooks in `.claude/settings.json`, and the files under `.claude/rules/`, then offer the two choices below.
* **'Which CLAUDE.md rules could be checks':** "Scan the instructions" below.
* **The bare word 'guardrails':** offer two choices in one message, set up the default checks or scan the instructions, using the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion).

## Add one rule

No executable `./check` at the repository root: set it up by [references/defaults.md](references/defaults.md) first.

1. **Restate the rule** as something a stranger could check, with one real violation from this codebase, or say none exists today.
2. **Pick the rung.** Try rung 1, cheapest first, and stop at the first that holds; else rung 2 when it applies to some paths; else rung 3.
   * **Language or compiler setting.**
   * **A rule the linter already ships,** at error severity.
   * **A Semgrep rule** over source.
   * **A script** for a fact about files, config or commands.
   * **A test** for a fact about behaviour.
3. **Agree it:** show the user the restated rule, the rung and tool chosen, and the violation it catches. Continue on their yes.
4. **Semgrep rule:** launch a fresh subagent (in Claude Code, the Agent tool) with the absolute path of [references/semgrep.md](references/semgrep.md), the branch, the restated rule, and the violation's file and line, or, when none exists, a short snippet that would violate it.
   * **No subagent available:** read the brief and do its task yourself.
   * **It returns `Semgrep missing`:** ask the user to install it and wait.
   * **It returns `Not expressible`:** go to the next rung-1 option, a script and then a test.
5. **The failure message is the prompt:** it says what is forbidden and what to do instead, never a bare rule identifier.
6. **Watch it fail once:** introduce the violation, confirm `./check` exits non-zero with the message, then remove the violation.
7. **Existing violations:** the user picks one of these.
   * A cleanup first, as its own change.
   * A ratchet, which fails only when a file gains a finding: copy [scripts/ratchet.py](scripts/ratchet.py) into the repository, commit its baseline JSON, and pipe the tool's findings to it from `./check`, one `<rule><TAB><file>` line each, such as `semgrep --config .semgrep/ --json | jq -r '.results[] | "\(.check_id)\t\(.path)"' | python3 tools/ratchet.py .ratchet.json`. Semgrep's `--baseline-commit` cannot do this job: it aborts when the tree has unstaged changes, which it always has at turn end.
8. **Rung 2:** write one file per topic, holding the glob, one imperative sentence and the reason.
   * **Claude Code globs:** `*` matches within one path segment and `**` across directories, so write `"**/*.py"` to match at every depth.
9. **Rung 3:** write one line stating what happens and what breaks when the rule is broken.
10. **Report** the step 6 failing output.
11. Never leave `./check` failing.

## Scan the instructions

Read `AGENTS.md`, every `CLAUDE.md`, `.claude/rules/`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.github/instructions/` and `CONTRIBUTING.md`. List only the lines a program could decide.

```text
| # | File:line | Instruction | Check that would hold it | Violations today |
```

* **Already enforced:** introduce one violation; when `./check` fails on it, write "already enforced by <check>" and remove the violation.
* **Selection:** the user picks rows by number.
* **Each pick:** add it by "Add one rule", then delete the original line from the agent instruction files (`AGENTS.md`, `CLAUDE.md`, the rule directories), since the check now holds it. Leave `CONTRIBUTING.md` as it is: human contributors read it.
