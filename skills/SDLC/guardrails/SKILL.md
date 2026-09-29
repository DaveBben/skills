---
name: guardrails
description: "Use this skill when a repository's AGENTS.md or CLAUDE.md must be written, checked or rewritten, when its automated checks must be set up or repaired, or when one rule or recurring mistake must be enforced. Use it on: 'write AGENTS.md', 'set up CLAUDE.md', 'get this repo ready for agents', 'orient yourself', 'set up guardrails', 'add hooks', 'set up the commit gate', 'we have no linting', 'add a rule', 'always do X', 'never do Y', 'the agent keeps making this mistake', 'ban this pattern'. Writes AGENTS.md, one tool per check slot, the agent hooks and one check command, and puts each rule where a program can enforce it."
license: MIT
compatibility: any-agent
metadata:
  version: "3.0.1"
---
# Guardrails

A check is a program that passes or fails a change: a formatter, a linter, a type checker, a dependency contract, a test runner, a Semgrep rule. A rule a program checks is followed every time. A rule an agent reads is followed when the agent remembers it. `AGENTS.md` holds what no program can check.

## Pick the path

* **Write, check or rewrite `AGENTS.md`,** or orient in a repository: "AGENTS.md" below.
* **Set up or repair the checks,** hooks, deny list, commit gate or CI: [references/setup.md](references/setup.md). The hook scripts and checks ship in `scripts/`.
* **Enforce one rule,** stop a recurring mistake, or audit instruction files for rules a check could hold: [references/rules.md](references/rules.md).

## What never bends

* **The failure message is the prompt.** Every check says what is forbidden and what to do instead, never a bare rule identifier.
* **Watch every check fail once.** Introduce the violation, confirm the non-zero exit and the message, remove it.
* **Feedback arrives at the edit,** on the developer's machine. CI is the backstop.
* **Silencing a check is not passing it.** Disabling a rule, loosening a config, weakening an assertion or skipping a test to reach green is not a fix. This sentence goes into `AGENTS.md` verbatim.
* **A blocking check needs an escape.** Wire the retry limit before the checks.

## Where a rule lives

Put every rule as high on this ladder as it will go.

| Rung | Where | Use when |
|---|---|---|
| 1. Deterministic | A linter setting, a Semgrep rule, a type check, a dependency contract, a test, a hook | A program can decide pass or fail from the code, the config or the command |
| 2. Scoped agent rule | A rule file loaded only for matching paths (`.claude/rules/*.md` with `paths:`, `.cursor/rules/*.mdc` with `globs:`), or a nested `AGENTS.md` | It needs judgment and applies to some paths |
| 3. Agent instructions | One line in `AGENTS.md` | It needs judgment and applies everywhere |

## AGENTS.md

`AGENTS.md` at the repository root is the one file every session reads first, with `CLAUDE.md` a symlink to it. Rewrite it in place, never append. It holds no feature list, priorities or architecture tables; those live in stories, tests, ADRs and snapshots.

**Orienting.** With neither `AGENTS.md` nor a real `CLAUDE.md`, report what the repository shows (the README's purpose, the stack, the commands) and offer to write it. With one, read it whole, run the review below, and report in one message: the purpose, the commands, the constraints and every finding. Rewrite nothing unless a finding is accepted.

**Interview.** Ask only what the conversation and the repository leave open, in one message of drafts to correct. Stop when every line could be proven false by a stranger.

* **Purpose:** what a person does with this that they could not before; an actor and an observable result.
* **Users,** and what they do with the output.
* **Not doing:** what a reader would expect it to do that it never will, each checkable.
* **Nouns:** the three to five domain terms the code, tables and tests must use.
* **Boundaries:** each system it reads, writes or runs inside, by name and address, and who writes the data in each store it reads.
* **Backlog:** the tracker, the project, and how an agent reaches it in order of preference (an MCP server, a CLI, an HTTP API). It must hold epics, stories and spikes, link them, and hold descriptions and comments. Leave it out when there is none; the first story that needs one connects it.
* **Constraints:** what must stay true for every change, each naming its enforcer (a test asserting its number, a commit-gate check, an ADR) or saying no tool can see it.

```text
# <product name>

## Project Identity
Purpose:    <one sentence: actor, observable result>
Users:      <who, and what they do with the output>
Not doing:  <one checkable statement per line>
Nouns:      <term: one-line meaning>

## Tech Stack and Codebase Map
<language and version, framework, package manager, top-level directories with one-line purposes>
Boundaries: <system: address, read, write or host; who writes the data>
Backlog:    <tracker, project, access methods in order>
  Types:    <issue types>   Criteria: <field>   Blocks: <link type and checked direction>   Status: <names>
Architecture: <path of the latest snapshot under docs/architecture/snapshots/; omitted until one exists>

## Operational Commands
<exact commands: install, test, lint, format, run, deploy; the check command, which runs every check; the red-commit command, which commits failing tests before any code>

## Critical Constraints
<one checkable statement per line, each ending with its enforcer, or a rule no tool can see>

## Pointers to Deeper Docs
<path — purpose, only for files that exist>
```

* **Charter from the interview, the rest from the repository:** versions from the manifest, the package manager from the lockfile, commands from the task runner. Run each safe command once before listing it. When there is no manifest or task runner, leave the line out and say what was not found.
* **Never write** improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable or modern; write what is observed. Leave a section out rather than fill it with "Users: our users".
* **Write the mechanism** in a constraint: "never hold a worker longer than one HTTP round trip; the pool has 5 and a full pool returns 502 to every user", not "keep the pool safe". Give each project-local name one sentence saying what it is.
* **Cap it at 100 lines and 8 KB,** with the `agents-md-size` commit check from `setup.md`. A module's conventions go in a nested file; a file type's rule goes in a path-scoped rule.
* **Symlink `CLAUDE.md` to it,** and any other conventional name the repository carries, and commit them together.

**An instructions file that already exists** (`AGENTS.md`, a real `CLAUDE.md`, or both): read each whole, show one table mapping each line to its section, to a check (rung 1 or 2), or to "dropped, cannot be checked", and ask once whether to adopt this format. On yes, carry every kept line over and replace a real `CLAUDE.md` with the symlink; a line sent to a check stays until `rules.md` lands that check, only for rows the user accepts. On no, touch nothing.

**Review:** quote the line for each finding: requirements leaking in (a feature list, a priority, a schema); a statement that cannot fail; a boundary the code no longer touches, or one it touches that is missing; a constraint with no enforcer; a command that does not run; over 100 lines.
