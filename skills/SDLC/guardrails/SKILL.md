---
name: guardrails
description: "Use this skill when the user wants a rule their AI agent must follow in a codebase, when a repository needs its default checks set up, or when instruction files must be scanned for rules a program could check. Use it on: 'add a rule', 'always do X', 'never do Y', 'the agent keeps making this mistake', 'ban this pattern', 'make it a rule it cant ignore', 'set up guardrails', 'get this repo ready for agents', 'we have no linting', 'run the tests when claude finishes', 'which of our CLAUDE.md rules could be checks', and the bare word 'guardrails'. Puts each rule where it is followed most: a deterministic check first, a path-scoped rule file second, a line in AGENTS.md last. Writing AGENTS.md as a whole is the `orient` skill."
license: MIT
metadata:
  version: "5.0.0"
---
# Guardrails
# Guardrails

A rule a program checks is followed every time. A rule an agent reads is followed when the agent remembers it. Put every rule as high on this ladder as it will go.

| Rung | Where | Use when |
|---|---|---|
| 1. Check | A compiler or linter setting, a Semgrep rule, a script or a test, run by `./check` | A program can decide pass or fail from the code, the config or a command |
| 2. Path-scoped rule | `.claude/rules/<topic>.md` with `paths:` frontmatter, plus one equivalent per other agent the repository serves (below) | It needs judgment and applies to some paths |
| 3. Agent instructions | One line under Constraints in the root `AGENTS.md` | It needs judgment and applies everywhere |

Rung 2 equivalents for other agents:

* **Cursor:** `.cursor/rules/<topic>.mdc` with `globs:`.
* **GitHub Copilot:** `.github/instructions/<topic>.instructions.md` with `applyTo:`.
* **Agents with no path-scoped format, such as Codex:** a nested `AGENTS.md` in that directory.

`./check` is the repository's check command, and `./check --full` adds the slow tests. [references/defaults.md](references/defaults.md) sets up both.

## With no request

Offer two choices in one message, using the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion).

1. **Set up the default checks:** by [references/defaults.md](references/defaults.md).
2. **Scan the instructions** for rules a check could hold: "Scan the instructions" below.

## Add one rule

1. **Restate the rule** as something a stranger could check, with one real violation from this codebase, or say none exists today.
2. **Try rung 1, cheapest first,** and stop at the first that holds:
   * **Language or compiler setting.**
   * **A rule the linter already ships,** at error severity.
   * **A Semgrep rule** over source.
   * **A script** for a fact about files, config or commands.
   * **A test** for a fact about behaviour.
3. **Semgrep rule:** launch a fresh subagent (in Claude Code, the Agent tool) with the path of [references/semgrep.md](references/semgrep.md), the restated rule and the violation's file and line.
   * **No subagent available:** read the brief and do its task yourself.
   * **It returns `Semgrep missing`:** ask the user to install it and wait.
4. **The failure message is the prompt:** it says what is forbidden and what to do instead, never a bare rule identifier.
5. **Watch it fail once:** introduce the violation, confirm `./check` exits non-zero with the message, then remove the violation.
6. **Existing violations:** the user picks one of these. Never leave `./check` failing.
   * New code only (Semgrep's `--baseline-commit <sha>`).
   * A cleanup first, as its own change.
   * A ratchet by [scripts/ratchet.py](scripts/ratchet.py) with a committed baseline.
7. **Rung 2:** write one file per topic, holding the glob, one imperative sentence and the reason.
   * **Claude Code globs:** `*` matches within one path segment and `**` across directories, so write `"**/*.py"` to match at every depth.
8. **Rung 3:** write one line stating what happens and what breaks when the rule is broken.
9. **Show the user** the rung, the file, the exact text and the violation it catches, and write it on their yes.

## Scan the instructions

Read `AGENTS.md`, every `CLAUDE.md`, `.claude/rules/`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.github/instructions/` and `CONTRIBUTING.md`. List only the lines a program could decide.

```text
| # | File:line | Instruction | Check that would hold it | Violations today |
```

* **Already enforced:** write "already enforced by <check>" once one violation confirms it.
* **Selection:** the user picks rows by number.
* **Each pick:** add it by "Add one rule", then delete the original line, since the check now holds it.
