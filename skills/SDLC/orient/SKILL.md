---
name: orient
description: "Use this skill whenever an agent needs to orient itself in a repository, or a repository needs the one file every session reads first: AGENTS.md, with CLAUDE.md symlinked to it, holding the product charter (purpose, users, non-goals, nouns) and the agent instructions (stack, commands, hard constraints, pointers). Use it on: 'orient yourself', 'familiarize yourself with this codebase', 'setup claude in this repo', 'get this repo ready for ai agents', 'setup initial context', 'create repo context', 'write the charter', 'what is this project for', 'what's in and out of scope', 'write AGENTS.md', 'set up CLAUDE.md', 'streamline my CLAUDE.md', on the bare words 'charter' or 'orient', and when a project has no AGENTS.md. When the file exists and is sound, read it and report; otherwise interview for the charter, fill the rest from the repository, and ask once before rewriting an existing file. Not for linting, hooks or guardrails; that is `harness`. Not for a feature or a change; that is `agile`."
license: MIT
compatibility: any-agent
metadata:
  version: "3.2.0"
---
# Orient

Write the one file every session reads before it does anything: `AGENTS.md` at the repository root, with `CLAUDE.md` a symlink to it. It is rewritten in place, never appended to. The first and fourth sections are the product's charter; the rest are the agent's instructions.

The charter holds no feature list, no priorities, no metrics, no architecture. Those live in stories, tests and ADRs.

## Interview

Ask only what the conversation and the repository do not already answer. Batch the questions into one message. Stop when every item below can be filled with a sentence a stranger could prove false.

* **Purpose.** What does a person do with this that they could not do before? One sentence naming the person and the observable result.
* **Users.** Who uses it, and what do they do with the output? When the answer is "me", say what the user does with it.
* **Not doing.** What would a reader expect this product to do that it never will? Each as a checkable statement.
* **Nouns.** The three to five domain terms the code, tables and tests must use. Never invent synonyms.
* **Boundaries.** The systems this product reads from, writes to, or runs inside, each by name and address, and for each store it reads, who writes the data: this product, a person through its own screens, or something outside. A reviewer cannot get that from the source, and it decides how far a value is trusted. Include the backlog when one exists outside the repository ("Backlog: Jira project TAG"); the change loop reads it from here.
* **Constraints.** What must stay true for every story: where data may live, what it may cost, what it runs on, who must be able to use it. Each as a checkable statement, and each naming where it is enforced: a Budget row (a test asserting the constraint's number, proposed for every change that touches it), a check in the repository's commit gate, or an ADR. Leave out a constraint with no enforcer, and say so.

## Rules

* **Name an actor and an observable outcome** in Purpose. "Tags articles" fails. "Each morning Dave opens one feed and reads only what the tagger judged relevant" passes.
* **Ban unfalsifiable words:** improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable, modern. Replace each with the thing observed.
* **Write non-goals as statements.** "No backfill of articles older than the first run" can be checked. "Keep it simple" cannot.
* **Refuse to fill a section with furniture.** An empty line is better than "Users: our users". Leave it out and say so.
* **Mechanism before label.** A constraint or non-goal states what physically happens and what breaks when it is violated. "Keep the pool safe" is a label. "Never hold a plugin-runner worker for longer than one HTTP round trip; the pool has 5 and a full pool returns 502 to every user" is the mechanism.
* **Resolve every pointer.** No project-local abbreviation, test ID, or config key without one sentence saying what it is, in this file. Industry-standard terms need no definition. The reader has no other file open. Never invent a mechanism: when the cause of a constraint is not known, write "cause not established".
* **Record what is imposed.** When the user supplies a technology or a constraint, put it under Boundaries and name who imposed it.

## AGENTS.md

Load [references/agents-md-format.md](references/agents-md-format.md) now. It carries the five sections, in order, with a good and a bad example of each.

```text
# <product name>

## Project Identity
Purpose:    <one sentence: actor, observable result>
Users:      <who, and what they do with the output>
Not doing:  <one checkable statement per line>
Nouns:      <term: one-line meaning, three to five lines>

## Tech Stack and Codebase Map
<language and version, framework, package manager, top-level directories with one-line purposes>
Boundaries: <system: address or path, and whether read, write or host; who writes the data in each store; the backlog when external>

## Operational Commands
<exact commands: install, test, lint, format, run, deploy; the check command the harness names>

## Critical Constraints
<one checkable statement per line, each ending with its enforcer, or a rule no tool can see>

## Pointers to Deeper Docs
<path — purpose, one per line, only files that exist: docs/adr/, docs/features/, specs>
```

* **Charter from the interview, the rest from the repository.** Language and versions from the manifest, the package manager from the lockfile, the layout from the top-level directories, the commands from the task runner, the scripts directory or the package manifest. Run each safe command once (test, lint, format) before listing it; a command that does not run is not listed.
* **Critical Constraints end with their enforcer.** A Budget row, a commit-gate check, or an ADR. A rule no tool can see is the other kind that belongs here: never commit credentials, every migration reversible, nothing edited under `vendor/`. Vague guidance belongs nowhere.
* **Cap it at 100 lines,** the charter sections under thirty of them. A module's conventions belong in a nested instructions file in that module; a rule for one file type belongs in a path-scoped rule. The `harness` skill wires those.
* **Symlink `CLAUDE.md` to it,** and symlink any other conventional name the repository already carries the same way.
* **Commit the file and the symlink together.** Rewrite in place whenever a story changes the shape: a new noun, a new boundary, a non-goal that became a goal. Commit that rewrite with the story that caused it.

### When an instructions file already exists

`AGENTS.md`, `CLAUDE.md`, a `CONTEXT.md` from an earlier version of this skill, or any of them, as real files. Read every one whole before proposing anything.

* **Show the mapping.** One table: each existing line or block, the section it lands in, or "no section" with where it goes instead (a nested file, a path-scoped rule, a rule in the harness, or dropped). Name duplicated lines once.
* **Ask once** whether to adopt the five-section format. One question, then wait.
* **On yes:** write `AGENTS.md` in the format, carrying every line the mapping kept; replace the real `CLAUDE.md` with the symlink; delete a `CONTEXT.md` whose lines moved. When only `CLAUDE.md` exists, its content becomes `AGENTS.md` and the symlink takes its place.
* **On no:** touch nothing, and say the file was left as found.

## Orienting in a repository that has the file

Read `AGENTS.md` whole, run the Review below, and report in one message: the purpose in one line, the commands, the constraints, and every finding. Rewrite nothing unless a finding is accepted. When Operational Commands names no check command, offer the `harness` skill once.

## Review

When an `AGENTS.md` already exists, read it whole and report, quoting the line for each finding:

* **Requirements leaking in.** A numbered feature list, a priority, a metric, a schema or an endpoint. Say which file it belongs in.
* **Statements that cannot fail.** Every banned word, every purpose with no actor.
* **Stale boundaries.** A system named that the code no longer touches, or one the code touches that is not named.
* **Unenforced constraints.** A constraint with no Budget row, commit-gate check or ADR behind it, and no claim that a tool cannot see it.
* **Commands that do not run.** Run each safe one.
* **Length.** Over 100 lines, or charter sections over thirty, is a finding on its own.
