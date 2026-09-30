---
name: architecture
description: "Use this skill when a choice costs more than a day to reverse, when a system's shape must be decided or mapped, when a decision or an accepted risk must be recorded, when an idea must be tried, compared or tested with throwaway code before it is built for real, or when work is asked for in a repository with no application yet. Use it on: 'how should this be structured', 'should I use X or Y', 'let's build this' in an empty repo, 'note this decision', 'record the why', 'write an ADR', 'snapshot the architecture', 'do a spike', 'let's prove this works first', 'try a few approaches and see', 'test whether X improves Y', 'find the best model for this', 'experiment with', 'prototype', 'mock this up', 'a demo', 'is X feasible', 'see how this would fit or integrate', 'what would it take to move to X', 'template project'. Load it before asking what the user means. Runs spikes, maps the system, records decisions with the user's reasons."
license: MIT
metadata:
  version: "3.1.0"
---
# Architecture

Decide architecture in this order: prove each unknown with a spike, take a broad starting shape, record each decision, prove the shape with a walking skeleton (the thinnest end-to-end version a real person can use, built first), and change it by refactoring as stories teach more.

## Where things are written

* **The shape:** a dated snapshot under `docs/architecture/snapshots/`, by [references/snapshot.md](references/snapshot.md), with one `Architecture:` line in `AGENTS.md` pointing at the latest. The user owns a one-page summary, `docs/architecture/summary.md`, by the same reference.
* **Each decision:** an ADR (architecture decision record) under `docs/adr/`, by [references/adr.md](references/adr.md).
* **Each rule:** a test or a dependency contract, which the `guardrails` skill writes.
* **The feature:** the feature header is the epic's description on the tracker that the `Backlog:` line of `AGENTS.md` names. When a feature is open, write to it `Decided:` (one ADR path per line), `Deferred:` (one open item per line, with what will force it), and each number on `Constraints:`. With no feature header, ask the user for the outcome in one sentence and the steps a person takes.
* **Commit** a plan's ADRs, snapshot and `AGENTS.md` change on `story/{slug}/0-plan` (the slug is the epic's key) with a pull request the user merges before the first story, or on main in a repository with no remote. A single decision commits by `adr.md`.

## Asking

Everything here is agreed with the user. Look up any fact the code, the data or the tracker holds, and use it. Put a fact only a named person knows on the epic for that person. Ask one question per message. A set of drafts for the user to correct (the Numbers, the Map tables, an ADR's three answers) goes in one message. Open each message with one line naming the repository and the feature, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion).

## Pick the path

* **Record a decision already made:** [references/adr.md](references/adr.md), nothing else.
* **Decide one open item:** draft the numbers it turns on ("Numbers" below), then "Decide" for that item, then record it.
* **Find something out by building throwaway code:** [references/spike.md](references/spike.md).
* **Capture the current architecture:** read the code, then write the snapshot by `snapshot.md`, with no questions until it is drafted. List what the code settles (each language, store and check on a caller) with its file, report drift from any earlier snapshot, and move any architecture tables out of `AGENTS.md`. When the summary does not exist, draft it and ask the user to rewrite it. Commit on its own branch with a pull request, then stop.
* **Plan a system:** "Crossings" through "Record" below.
* **A new application:** decide the repositories first (how many, each name and directory; on the feature header's `Repositories:` line as `new: <name>`, or in chat until a tracker exists), run `git init -b main` in the first (`scaffold.sh` keeps that repository), and record that decision. Run "Crossings" through "Decide", then "Stand up a repository", then "Record".

## Crossings

A crossing is a place the walking skeleton's outcome passes from one running piece into another: a database, a third-party API, a host, a device, a queue, another repository. List each one, ask which someone has already made work in this stack, and spike each untried one before going on, framed with the user as a question that can fail ("the app can read Health data while the phone is locked").

## Numbers

Skip what `AGENTS.md` records. Draft the rest from `AGENTS.md`, the code and the tracker, and put the drafts to the user in one message to correct, writing "unknown" where nothing settles one: people or requests at once; how long a response may take and for what share; downtime allowed per month; data now and its growth; which data is sensitive, where it may live, and whether it must be encrypted at rest and in transit. Write each as a constraint with its enforcer, a test asserting the number: in `AGENTS.md` when it holds for the whole system, else on the feature header. An unknown number defers what depends on it and never blocks the walking skeleton.

## Map

Propose three tables, only for what the outcome touches, and let the user edit them in one turn.

```text
| Process | Repository | Machine | Copies | Started by |
| Module | Process | Owns |
| From -> To | What crosses | How (and whether From waits) | When To fails, what the person sees | Who else reaches To, and how To checks the caller |
```

* **A module owns one thing.** An Owns cell that needs "and" is two modules or a flow. State existing modules from the code, with their directory.
* **Flows point one way.** A cycle is a finding. When To must call back, From defines a port that To depends on.
* **Name a pattern only where a flow needs one:** a port when To must be faked or swapped, a queue when From must not wait.
* **Copies times connections** stays under the limit of what they connect to.
* **Ask who else reaches To** for every flow that crosses a machine, and how To checks the caller. Each answer is a decision below.
* **Contract first** where another team, service or repository calls To: an executable contract (OpenAPI, Protobuf, strict types) asserted in a test before code sits behind it.

## Decide

List what the outcome touches and cannot cheaply reverse: the repositories and the language and platform of each; every flow crossing a process, machine or repository; per store, what makes a record unique, the rules the data always keeps (preferring database constraints), retention and deletion, backup and a proved restore, and how the schema changes; the trust and consistency boundaries; each choice a number or the sensitive-data answer forces.

Read the latest snapshot `AGENTS.md` points at and the titles under `docs/adr/`, skipping superseded ones, and state what the code and those records already settle, with the file. Put each other item to the user one per message: the problem, the constraints, and the alternatives with their tradeoff, marking none as recommended. Ask which the user would pick, and wait. "Not sure" or "you pick" is an answer: give the recommendation and its reason, and record it. Once they answer, say in one sentence whether the agent would have picked differently and why, and in the same message any tradeoff, alternative or untested hazard the answer missed. Record each answer before the next question and before any code that depends on it.

* **A third-party service** the tests cannot use at the volume or failure modes needed gets an ADR for a twin: a fake under `tests/twins/<service>/` whose contract suite runs against the twin in every check and against recorded real responses on a schedule.
* **Data the system cannot regenerate** puts a restore criterion on the story that first stores it.
* **A smaller choice a later story inherits** (a port, a schedule, a file format, a name that becomes a domain noun): ask, unless the ranked qualities in the summary pick one; then decide it and name the quality.
* **A choice nothing inherits and nobody sees:** decide alone and list it.

Each item ends Decided (an ADR on `Decided:`), Deferred (on `Deferred:` with what will force it; propose this for each item the first story does not touch), waiting on a spike, or settled by the code. No story that needs an item starts before then.

## Stand up a repository

Once a new repository's language is decided, run [scripts/scaffold.sh](scripts/scaffold.sh) `<template> <name> <directory> <test command>`. It clones the template, strips its history, renames `example_project`, runs the tests and commits each step. The Python template is `https://github.com/DaveBben/claude-ready-python-codebase`, tested with `uv run pytest`. With no template for the language, run the platform's own generator (`cargo new`, `npm init`) and add one passing test. Then replace the README with the project name and one sentence, delete docs that describe the template, remove sample modules and the dependencies only they used, keeping anything ambiguous, and run the tests again, then commit. Rewrite the `new:` line to the remote URL or path. Then run the `guardrails` skill for `AGENTS.md` and the checks, before "Record" points `AGENTS.md` at the snapshot.

## Record

Write the agreed shape as a snapshot headed "planned, not yet built", draft the summary when there is none and ask the user to rewrite it, and point `AGENTS.md` at the snapshot. Hand the in-process flows to the `guardrails` skill as dependency contracts, with the directories the user reads on every change (who may do what, secrets, money, health or personal data, migrations, deploys) as `# owner reads: data` lines for `CODEOWNERS`. A story that changes a process, a store, a module or a flow writes a new snapshot in its last commit. A spike's findings that contradict a decided ADR get a new ADR naming the old one on `Supersedes:`. Then `deliver` builds, starting at the walking skeleton.
