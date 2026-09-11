---
name: orient
description: "Use this skill whenever an agent needs to orient itself in a repository, or a repository needs the two files every agent session reads first written or revised: CONTEXT.md, the one-page product charter (what the product is, for whom, why, and what it is not), and AGENTS.md, the agent instructions file (stack, commands, hard constraints, pointers), with CLAUDE.md symlinked to it. Use it on: 'orient yourself', 'orient yourself with this repo', 'familiarize yourself with this codebase', 'get to know this repo', 'setup claude in this repo', 'set up claude for this project', 'get this repo ready for ai agents', 'make this repo agent ready', 'setup initial context', 'create repo context', 'write the charter', 'create a charter', 'project charter', 'write CONTEXT.md', 'what is this project for', 'document the vision', 'define what this product is', 'what's in and out of scope for this project', 'set the boundaries', 'update the context file', 'write AGENTS.md', 'write CLAUDE.md', 'set up CLAUDE.md', 'create an agents file', 'streamline my CLAUDE.md', and when a project has no CONTEXT.md or no AGENTS.md. Use it on the bare words 'charter' or 'orient' alone. When both files exist and are sound, orienting means reading them and reporting; otherwise interview the user, write CONTEXT.md under thirty lines with fixed sections and no requirements, metrics or priorities, then write AGENTS.md in five sections and symlink CLAUDE.md to it; when an instructions file already exists, show the mapping and ask once before rewriting. Finish by offering `harness` for the checks and hooks. Do not use it for linting, hooks, commit gates or guardrails; that is `harness`. Do not use it to specify a feature or a change; that is `agile`."
license: MIT
compatibility: any-agent
metadata:
  version: "2.0.0"
---
# Orient

Write the two files every session reads before it does anything: `CONTEXT.md`, the product's one-page charter, and `AGENTS.md`, the agent's instructions, with `CLAUDE.md` a symlink to it. Both live at the repository root and are rewritten in place, never appended to.

A charter is not a requirements document. It holds no feature list, no priorities, no metrics, no architecture. Those live in slices, tests and ADRs. A charter that grows past thirty lines is carrying something that belongs elsewhere.

## Interview

Ask only what the conversation and the repository do not already answer. Batch the questions into one message. Stop when every section below can be filled with a sentence a stranger could prove false.

* **Purpose.** What does a person do with this that they could not do before? One sentence naming the person and the observable result.
* **Users.** Who uses it, and what do they do with the output? When the answer is "me", say what the user does with it.
* **Not doing.** What would a reader expect this product to do that it never will? Each as a checkable statement.
* **Nouns.** The three to five domain terms the code, tables and tests must use. Never invent synonyms.
* **Boundaries.** The systems this product reads from, writes to, or runs inside, each by name and address. Include the backlog when one exists outside the repository ("Backlog: Jira project TAG"); the change loop reads it from here.
* **Constraints.** What must stay true for every slice: where data may live, what it may cost, what it runs on, who must be able to use it. Each as a checkable statement, and each naming where it is enforced: a Budget row (a test asserting the constraint's number, proposed for every change that touches it), a check in the repository's commit gate, or an ADR. A constraint with no enforcer is a wish; leave it out and say so.

## Rules

* **Name an actor and an observable outcome** in Purpose. "Tags articles" fails. "Each morning Dave opens one feed and reads only what the tagger judged relevant" passes.
* **Ban unfalsifiable words:** improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable, modern. Replace each with the thing observed.
* **Write non-goals as statements.** "No backfill of articles older than the first run" can be checked. "Keep it simple" cannot.
* **Refuse to fill a section with furniture.** An empty section is better than "Users: our users". Leave it out and say so.
* **Record what is imposed.** When the user supplies a technology or a constraint, put it under Boundaries and name who imposed it.

## CONTEXT.md

```text
# <product name>

Purpose:    <one sentence: actor, observable result>
Users:      <who, and what they do with the output>
Not doing:  <one checkable statement per line>
Nouns:      <term: one-line meaning, three to five lines>
Boundaries: <system: address or path, and whether read, write or host>
Constraints: <one checkable statement per line, each ending with its enforcer>
```

Under thirty lines. Rewrite it in place whenever a slice changes the shape: a new noun, a new boundary, a non-goal that became a goal. Commit the rewrite with the slice that caused it.

## AGENTS.md

Load [references/agents-md-format.md](references/agents-md-format.md) now. It carries the five sections, in order, with a good and a bad example of each: Project Identity, Tech Stack and Codebase Map, Operational Commands, Critical Constraints, Pointers to Deeper Docs.

* **Write `AGENTS.md`, then symlink `CLAUDE.md` to it.** One file, every tool reads it. Symlink any other conventional name the repository already carries the same way.
* **Fill it from the repository, not the interview.** Language and versions from the manifest, the package manager from the lockfile, the layout from the top-level directories, the commands from the task runner, the scripts directory or the package manifest. Run each safe command once (test, lint, format) before listing it; a command that does not run is not listed.
* **Identity is `CONTEXT.md` compressed.** One to three sentences from Purpose and Users. Pointers name `CONTEXT.md`, `docs/adr/` and `docs/tasks/` when they exist, and nothing that does not.
* **Critical Constraints hold only what no check enforces.** A constraint the commit gate or a Budget row enforces stays in `CONTEXT.md` with its enforcer. What remains is the rule a tool cannot see: never commit credentials, every migration reversible, nothing edited under `vendor/`.
* **Cap it at 100 lines.** Every line costs context on every turn. A module's conventions belong in a nested instructions file in that module; a rule for one file type belongs in a path-scoped rule. The `harness` skill wires those.
* **Commit both files together** with the symlink.

### When an instructions file already exists

`AGENTS.md`, `CLAUDE.md`, or both, as real files. Read every one whole before proposing anything.

* **Show the mapping.** One table: each existing line or block, the section it lands in, or "no section" with where it goes instead (a nested file, a path-scoped rule, a rule in the harness, or dropped). Name the lines that duplicate `CONTEXT.md`.
* **Ask once** whether to adopt the five-section format. One question, then wait.
* **On yes:** rewrite `AGENTS.md` in the format, carrying every line the mapping kept; replace the real `CLAUDE.md` with the symlink. When only `CLAUDE.md` exists, its content becomes `AGENTS.md` and the symlink takes its place.
* **On no:** touch neither file. Write `CONTEXT.md` only, and say the instructions file was left as found.

## Orienting in a repository that has both files

Read `CONTEXT.md` and `AGENTS.md` whole, run the Review below on `CONTEXT.md`, and report in one message: the purpose in one line, the commands, the constraints, and every finding. Rewrite nothing unless a finding is accepted. When the root instructions file names no check command, offer the `harness` skill once.

## Review

When a `CONTEXT.md` already exists, read it whole and report, quoting the line for each finding:

* **Requirements leaking in.** A numbered list, a priority, a metric, a schema or an endpoint. Say which file it belongs in.
* **Statements that cannot fail.** Every banned word, every purpose with no actor.
* **Stale boundaries.** A system named that the code no longer touches, or one the code touches that is not named.
* **Unenforced constraints.** A constraint with no Budget row, commit-gate check or ADR behind it.
* **Length.** Over thirty lines is a finding on its own.
