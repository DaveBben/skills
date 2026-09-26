---
name: guardrails
description: "Use this skill when a repository's automated checks must be set up or repaired, or when one rule, convention or recurring mistake must be enforced. Use it on: 'set up guardrails', 'add hooks for the agent', 'set up the commit gate', 'we have no linting', 'add a mutation runner', 'set up CI checks', 'add a rule', 'always do X', 'never do Y', 'the agent keeps making this mistake', 'enforce this convention', 'ban this pattern', 'write a semgrep rule', 'which of these instructions could be lint rules', 'audit CLAUDE.md for rules a check could enforce'. Sets up one tool per check slot, the agent hooks, a deny list and one check command. Places each rule in the first place that holds: a deterministic check, then a path-scoped agent rule, then one line in AGENTS.md. Not for writing, streamlining or getting a repository ready with AGENTS.md (`orient`), a repository with no application (`architecture`), a failing CI run or a cleanup of product code (`deliver`), or reviewing an existing check setup (`reviewing`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Guardrails

A check is a program that passes or fails a change: a formatter, a linter, a type checker, a dependency contract, a test runner, a Semgrep rule. A rule a program checks is followed every time. A rule an agent reads is followed when the agent remembers it.

## 1. Pick the path

Load only the files the path lists. A one-rule request reads only what its row lists.

| Request | Load |
|---|---|
| Set up or repair the repository's checks, hooks, deny list, commit gate or CI | [references/setup.md](references/setup.md), then [references/toolchain.md](references/toolchain.md) before writing any config, then [references/claude-guardrails.md](references/claude-guardrails.md) when the agent harness is Claude Code |
| Enforce one rule, stop a recurring mistake, or audit the instruction files for rules a check could enforce | [references/rules.md](references/rules.md), then [references/semgrep.md](references/semgrep.md) only when the rule needs a Semgrep pattern |
| The `story` skill hands over its `Interpreted` line: each place a story's input reaches a query, a shell, a template or a parser | [references/rules.md](references/rules.md), section "Defend where input becomes instructions" |
| A dependency direction, a hook or a deny-list entry arrives as one rule | [references/rules.md](references/rules.md) to classify it, then the Contracts, Loop or Guards section of [references/setup.md](references/setup.md), and [references/claude-guardrails.md](references/claude-guardrails.md) for a hook or deny-list entry on Claude Code, to write only that entry |

## 2. What never bends

* **The failure message is the prompt.** Every check states what is forbidden and what to do instead, never a bare rule identifier such as `rule R2011 violated`.
* **Watch every check fail once.** Introduce the violation, confirm the non-zero exit and the message, remove it.
* **Feedback arrives on the developer's machine**, at the moment of the edit. CI is the backstop and never the first place a rule fires.
* **Silencing a check is not passing it.** Disabling a rule, loosening a config, weakening an assertion, or skipping a test to reach green is not a fix. This sentence goes into `AGENTS.md` verbatim.
* **A blocking check needs an escape.** Wire the loop safety before the checks.

## 3. Where a rule lives

Put every rule as far up this ladder as it will go.

| Rung | Where the rule lives | Use when |
| --- | --- | --- |
| 1. Deterministic | A linter setting, a Semgrep rule, a type check, a dependency contract, a test | A program can decide pass or fail from the code, the config or the command alone |
| 2. Scoped agent rule | A rule file the agent loads only for matching paths (`.claude/rules/*.md` with `paths:`, `.cursor/rules/*.mdc` with `globs:`, `.github/instructions/*.instructions.md` with `applyTo:`), or a nested `AGENTS.md` in one module's directory | It needs judgment, and it applies to some paths, one kind of file or one module |
| 3. Agent instructions | One line in `AGENTS.md` | It needs judgment, and it applies everywhere |

Use the rule-file format of the agent this repository already configures. When the repository configures none, and the agent in use has no path-scoped format, the rule goes to rung 3.

## What this skill does not do

Writing the whole `AGENTS.md` is `orient`. A repository with no application yet is `architecture`. Deciding the modules and the flows between them is `architecture`; this skill encodes what `architecture` wrote. Building product code is `deliver`.
