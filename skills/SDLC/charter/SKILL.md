---
name: charter
description: "Use this skill whenever a project needs its one-page product charter written or revised: what the product is, for whom, why, and what it is not. Use it on: 'write the charter', 'create a charter', 'project charter', 'write CONTEXT.md', 'what is this project for', 'document the vision', 'define what this product is', 'what's in and out of scope for this project', 'set the boundaries', 'update the context file', and when a new project has no CONTEXT.md. Use it on the bare word 'charter' alone. Interview the user, then write CONTEXT.md at the repository root, under thirty lines, with fixed sections and no requirements, metrics or priorities; those belong in slices and tests. Do not use it to specify a feature or a change; that is `agile`."
license: MIT
compatibility: any-agent
metadata:
  version: "1.1.0"
---
# Charter

Write the product's one-page charter to `CONTEXT.md` at the repository root. It is the file every session reads first to learn what the product is, who it serves, and where its edges are. It is rewritten in place, never appended to.

A charter is not a requirements document. It holds no feature list, no priorities, no metrics, no architecture. Those live in slices, tests and ADRs. A charter that grows past thirty lines is carrying something that belongs elsewhere.

## Interview

Ask only what the conversation and the repository do not already answer. Batch the questions into one message. Stop when every section below can be filled with a sentence a stranger could prove false.

* **Purpose.** What does a person do with this that they could not do before? One sentence naming the person and the observable result.
* **Users.** Who uses it, and what do they do with the output? When the answer is "me", say what the user does with it.
* **Not doing.** What would a reader expect this product to do that it never will? Each as a checkable statement.
* **Nouns.** The three to five domain terms the code, tables and tests must use. Never invent synonyms.
* **Boundaries.** The systems this product reads from, writes to, or runs inside, each by name and address.
* **Constraints.** What must stay true for every slice: where data may live, what it may cost, what it runs on, who must be able to use it. Each as a checkable statement, and each naming where it is enforced: a Budget row in the test table, a harness check, or an ADR. A constraint with no enforcer is a wish; leave it out and say so.

## Rules

* **Name an actor and an observable outcome** in Purpose. "Tags articles" fails. "Each morning Dave opens one feed and reads only what the tagger judged relevant" passes.
* **Ban unfalsifiable words:** improve, better, seamless, robust, intuitive, flexible, scalable, modern. Replace each with the thing observed.
* **Write non-goals as statements.** "No backfill of articles older than the first run" can be checked. "Keep it simple" cannot.
* **Refuse to fill a section with furniture.** An empty section is better than "Users: our users". Leave it out and say so.
* **Record what is imposed.** When the user supplies a technology or a constraint, put it under Boundaries and name who imposed it.

## Output

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

## Review

When a `CONTEXT.md` already exists, read it whole and report, quoting the line for each finding:

* **Requirements leaking in.** A numbered list, a priority, a metric, a schema or an endpoint. Say which file it belongs in.
* **Statements that cannot fail.** Every banned word, every purpose with no actor.
* **Stale boundaries.** A system named that the code no longer touches, or one the code touches that is not named.
* **Unenforced constraints.** A constraint with no Budget row, harness check or ADR behind it.
* **Length.** Over thirty lines is a finding on its own.
