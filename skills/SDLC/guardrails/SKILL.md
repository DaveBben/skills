---
name: guardrails
description: "Use this skill when the user wants a rule their AI agent must follow in a codebase, when a repository needs its default checks set up, or when instruction files must be scanned for rules a program could check. Use it on: 'add a rule', 'always do X', 'never do Y', 'the agent keeps making this mistake', 'ban this pattern', 'make it a rule it cant ignore', 'set up guardrails', 'get this repo ready for agents', 'we have no linting', 'run the tests when claude finishes', 'which of our CLAUDE.md rules could be checks', and the bare word 'guardrails'. Puts each rule where it is followed most: a deterministic check first, a path-scoped rule file second, a line in AGENTS.md last. Writing AGENTS.md as a whole is the `orient` skill."
license: MIT
metadata:
  version: "5.0.0"
---
# Guardrails

A rule a program checks is followed every time. A rule an agent reads is followed when the agent remembers it. Put every rule as high on this ladder as it will go:

| Rung | Where | Use when |
|---|---|---|
| 1. Check | A compiler or linter setting, a Semgrep rule, a script or a test, run by `./check` | A program can decide pass or fail from the code, the config or a command |
| 2. Path-scoped rule | `.claude/rules/<topic>.md` with `paths:` frontmatter, plus the same rule for each other agent the repository serves: `.cursor/rules/<topic>.mdc` with `globs:`, `.github/instructions/<topic>.instructions.md` with `applyTo:`, and for agents with no path-scoped format, such as Codex, a nested `AGENTS.md` in that directory | It needs judgment and applies to some paths |
| 3. Agent instructions | One line under Constraints in the root `AGENTS.md` | It needs judgment and applies everywhere |

`./check` is the repository's check command, and `./check --full` adds the slow tests; [references/defaults.md](references/defaults.md) sets both up.

## With no request

Offer two choices in one message, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion):

1. **Set up the default checks:** by [references/defaults.md](references/defaults.md).
2. **Scan the instructions** for rules a check could hold: "Scan the instructions" below.

## Add one rule

1. **Restate it as something a stranger could check,** with one real violation from this codebase, or say none exists today.
2. **Try rung 1, cheapest first,** and stop at the first that holds: a language or compiler setting; a rule the linter already ships, at error severity; a Semgrep rule over source; a script for a fact about files, config or commands; a test for a fact about behaviour. For a Semgrep rule, launch a fresh subagent (in Claude Code, the Agent tool) with the path of [references/semgrep.md](references/semgrep.md), the restated rule and the violation's file and line; where the harness cannot launch one, read the brief and do its task yourself. When it returns `Semgrep missing`, ask the user to install it and wait.
   * **The failure message is the prompt.** It says what is forbidden and what to do instead, never a bare rule identifier.
   * **Watch it fail once.** Introduce the violation, confirm `./check` exits non-zero with the message, and remove it.
   * **Existing violations:** the user picks new code only (Semgrep's `--baseline-commit <sha>`), a cleanup first as its own change, or a ratchet by [scripts/ratchet.py](scripts/ratchet.py) with a committed baseline. Never leave `./check` failing.
3. **Rung 2** is one file per topic: the glob, one imperative sentence and the reason. In Claude Code, `*` matches within one path segment and `**` across directories, so write `"**/*.py"` to match at every depth.
4. **Rung 3** is one line, stating what happens and what breaks when it is broken.
5. **Show the user the rung, the file, the exact text and the violation it catches,** and write it on their yes.

## Scan the instructions

Read `AGENTS.md`, every `CLAUDE.md`, `.claude/rules/`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.github/instructions/` and `CONTRIBUTING.md`. List only the lines a program could decide:

```text
| # | File:line | Instruction | Check that would hold it | Violations today |
```

A line a check already enforces gets "already enforced by <check>" once one violation confirms it. The user picks rows by number. Add each by "Add one rule", then delete the original line, since the check now holds it.
