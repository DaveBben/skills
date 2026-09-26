---
name: architecture
description: "Use this skill when the shape of a system must be decided, when any decision must survive the conversation, or when work is asked for in a repository with no application yet. Use it on: planning a new application, 'let's build this' in an empty repository, 'how should this be structured', 'should I use X for storage', 'map this codebase's architecture', and any choice costing more than a day to reverse: a library, a data shape, a trust or consistency boundary. Use it on: 'adr', 'write an adr', 'record the why', 'we will accept that risk', 'let's go with X instead of Y'. Spikes each untried crossing first, asks the load, response-time, downtime and data-volume numbers, maps processes, modules and flows, and puts each expensive decision to the user one at a time, recording each as an ADR with the user's reasons and the rejected alternatives. Not for reviewing an existing ADR (`reviewing`), drafting stories (`define-work`), throwaway code (`spike`), orienting in a repository (`orient`), or building (`deliver`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.2.0"
---
# Architecture

Load [references/writing.md](references/writing.md) before the first reply.

Architecture here is the set of decisions that are expensive to reverse, and the shape they give the system: which processes run, which modules own what, and how they talk. Decide it in this order: find out what is unknown with spikes, take a broad starting shape, record each decision, prove the shape with a walking skeleton, and change it by refactoring as stories teach more. The walking skeleton is the thinnest end-to-end version of the outcome a real person can use, built as the first story.

Nothing goes into a separate design document. The tables go into `AGENTS.md`, each decision into an ADR (architecture decision record) under `docs/adr/`, and each rule into a test or a dependency contract.

Everything here is agreed with the user. Propose, then wait. The user makes every decision section 5 lists.

**Where things are written.** The slug is the short kebab-case name `define-work` gave the work, or the epic's key on a tracker. The feature log is `docs/delivery/{slug}.md`; its `## Feature` block at the top is the feature header, which `define-work` writes. This skill adds `Decided:` (one ADR path per line) and `Deferred:` (one item per line, with the number, story or spike that will force it), and appends its numbers to `define-work`'s `Constraints:` line. On a tracker the feature header is the epic's description. When the work spans repositories, the feature log and `docs/adr/` live in the first repository on the `Repositories:` line. Commit the feature log, the ADRs and the tables on a branch `story/{slug}/0-plan` and open its pull request, which the user merges before the first story; in a repository with no remote, commit them on main.

## 1. Pick the path

* **Record one decision already made** (an accepted risk, "X instead of Y", "record the why", a spike's decision rows): load [references/adr.md](references/adr.md) and do nothing else.
* **Decide one open item** ("Postgres or SQLite?", or one decision a story forced): run section 5 for that item alone, then record the answer by [references/adr.md](references/adr.md).
* **Map an existing codebase** ("map this codebase's architecture"): run section 4 from the code, write the tables by section 6, and stop.
* **Plan a system** (a feature of several stories, "how should this be structured"): run sections 2 to 6. Run alone, end by running `deliver`.
* **A new application**, or work asked for in a repository with no application yet: this skill owns the path end to end. Once `define-work` has written the shared understanding, decide the repositories first: how many, the name of each, and the directory each lives in, written on `Repositories:` as `new: <name> <directory>`. Run `git init -b main` in the first one's directory, move the feature log there if `define-work` wrote it elsewhere, commit it, and record the repositories decision by [references/adr.md](references/adr.md). Then run sections 2 to 7.

Inputs: the shared understanding `define-work` wrote, with its outcome, the steps a person takes, the walking-skeleton story and the `Repositories:` line. When none exists, run `define-work` first. In an existing application with no walking skeleton, the crossings are the ones this work's stories make. Read `AGENTS.md` and every file in `docs/adr/` before proposing a change to an existing boundary.

## 2. Crossings and exploration

A crossing is a place the walking skeleton's outcome passes from one running piece into another: a database, a third-party API, a host, a device, a queue, another repository.

* **List every crossing** the walking skeleton makes.
* **Ask which crossings someone has already made work** in this stack. The user decides which count as tried.
* **Run a spike on each untried crossing before section 3.** Frame its falsifiable question, finish line and timebox with the user, such as "the app can read Health data while the phone is locked". Then run the `spike` skill in a subagent with that frame, the feature's slug and the spike's number on `Stories:`. It commits its findings where the plan is committed and returns its verdict and its decision table; put the table to the user and record each row marked `record`. Sections 3 to 5 use the findings.

## 3. Numbers and sensitive data

Skip any answer `AGENTS.md` already records. Ask the rest in one message:

* How many people or requests at once.
* How long a response may take, and for what share of requests.
* How much downtime is acceptable, per month.
* How much data there is now, and how fast it grows.
* Which data is sensitive (health, personal, financial, credentials), where it may be stored, and whether it must be encrypted on disk and on the wire. Sensitive data in a log line or an error message counts as stored.

Write each answer as a constraint with its enforcer: under Critical Constraints in `AGENTS.md` when it holds for the whole system, or on the feature header's `Constraints:` line when it holds for one feature. Before `AGENTS.md` exists, write every number on the feature header. The enforcer is a Budget row: a test asserting the number, which the `story` skill proposes for every change that touches it. Accept "unknown" and write it as unknown. An unknown number defers every decision that depends on it and never blocks the walking skeleton.

## 4. Map

Propose three tables, only for what the outcome touches, and stop. The user edits them in one turn; a row not changed is accepted.

```text
| Process | Repository | Machine | Copies | Started by |
|---|---|---|---|---|
| <name> | <a repository from the Repositories: line, or "-" for a service someone else runs> | <the machine it runs on, or "external: <address>"> | <1, one per <thing>, or n threads> | <boot, a request, a schedule, an event> |

| Module | Process | Owns |
|---|---|---|
| <name, in the domain's nouns> | <a process from the first table> | <the one thing it is responsible for> |

| From -> To | What crosses | How | When To fails | Who else reaches To |
|---|---|---|---|---|
| <caller> -> <callee> | <the data sent, and the data returned> | <in-process call, HTTP, queue, file or event, and whether From waits for the answer> | <what the person sees when To is down or slow, or "-" for an in-process call> | <who else can send to To, and how To checks the caller is From; "-" for an in-process call> |
```

* **Ask who else reaches To** for every flow that crosses a machine, a database included: the local network, the internet, another app on the device. Then ask how To checks the caller: a credential, a certificate, or where it sits on the network. For a database, also ask which account From uses and what that account may do. "Only the home network can reach it" is an answer the user may choose; record it as an accepted risk. Each answer is a section 5 decision, and its test sends the call without the check and expects a refusal.

* **Copies times connections is a number to check.** The copies of each process times the connections each holds must stay under the limit of whatever it connects to. A scheduled process running beside request traffic can hold locks the requests wait on.
* **A module owns one thing.** When its Owns cell needs "and", a list or an arrow, it is two modules or a flow. State existing modules from the code, with their directory. Propose new ones.
* **Map only what the outcome touches.** Leave out files, libraries, story numbers, behaviour details and deletions. The build decides files and libraries. A schema change is a decision for section 5.
* **Flows point one way.** From depends on To. A cycle is a finding, not a row. When To must call back into From, From defines a port, and the port is its own module that To depends on.
* **A flow that crosses a process, a machine or a repository is a decision.** Its How and When To fails cells go to section 5 unless the code or an ADR already settles them.
* **Name a pattern only for a flow that needs one.** Use a port when To must be faked in tests or swapped. Use a queue when From must not wait for To. Write the pattern in the flow's How cell with the one rule it enforces, e.g. "port: listener imports the display port, never display.py". Never walk the user through a pattern catalogue. The builder picks the simplest thing that passes the tests for every other flow.
* **The walking skeleton crosses every flow with real code.** It hardcodes data, never a crossing. A module the walking skeleton does not reach stays off the map until the story that needs it.
* **Contract first at a shared boundary.** Where To is called by another team, another service or another repository, write the executable contract (OpenAPI, Protobuf, strict interface types) and assert it in a test before any code sits behind it.

This is not a design document. It has no sequence diagrams, no schemas, no endpoints; those come out of the tests, story by story.

## 5. Decide

List the decisions this system cannot cheaply reverse:

* how many repositories the system has, and the name of each new one, unless section 1 already recorded it
* the platform and language of each repository, and the hardware it runs on
* every flow the map marks as crossing a process, a machine or a repository
* the shape of the data, as five questions:
  * what makes a record unique (the key the source gives it, such as a sample's ID), and what writing the same record twice does
  * each rule the data must always keep (a required field, an allowed range, a unit, a time zone), and whether the database or the code enforces it; prefer a database constraint, since it holds for every writer
  * how long data is kept, and how it is deleted
  * how it is backed up, and how a restore is proved
  * how the schema changes, and whether each change can be undone
* the system's trust boundaries (the Who else reaches To answers from section 4) and consistency boundaries
* each choice a number or a sensitive-data answer from section 3 forces, such as a connection pool, a read replica, failover or encryption

For each one the outcome touches, state in chat what the code already settles, with the file that settles it. Put the rest to the user one per message, with the alternatives and the tradeoff, and wait. Record each answer by [references/adr.md](references/adr.md) before the next decision is asked and before any code that depends on it.

* **Turn each answer a story could break into a constraint** on the feature header's `Constraints:` line, so the `story` skill writes it as a criterion on every story that could break it. "Writing the same sample twice stores one row", "an upload without the credential is refused" and "a row with no unit is refused" are each a criterion with a test.
* **Prove the restore.** When the system stores data it cannot regenerate, the story that first stores it carries a criterion: restore the latest backup into an empty store and find every row.

Every item ends in one of four states:

| State | Written where |
|---|---|
| Decided | An ADR, listed on the feature header's `Decided:` line |
| Deferred | The feature header's `Deferred:` line, with the number or the story that will force it. Propose "defer" for each item the first story does not touch. |
| Waiting on spike N | The feature header's `Deferred:` line as "waits on spike N", for a spike the `deliver` loop runs. Decide it once the spike is done: its findings merged, or on a tracker its resolution comment written. |
| Settled by the code | Stated in chat with the file that settles it |

No story that needs an item starts until the item is in one of the four states.

* **Ask before any smaller choice a later story inherits:** a port, an address or a schedule, a file or wire format, a name that becomes a domain noun. One message, alternatives and tradeoff, then wait.
* **Decide alone** any choice no later story inherits and no person using the system would see, and list each in chat with what was chosen, why, and the tradeoff.
* **Suggest an architectural change only when the current design obstructs the implementation.**
* **An assumption a recorded decision depends on** goes in that ADR's `What it doesn't buy` section.

## 6. Record and revise

* **Write the tables into `AGENTS.md`** under a `### Architecture` heading inside Tech Stack and Codebase Map. Before `AGENTS.md` exists, write them into the feature log below the feature header; the `orient` skill moves them, and the numbers, into `AGENTS.md` when it writes that file. Commit them with the plan. Each repository's `AGENTS.md` holds the rows whose Repository cell names it.
* **A flow inside one process leaves the Flows table** once the `guardrails` skill has written its dependency contract ("From may import To"), so a reversed dependency fails the build. Hand the in-process flows to `guardrails` in a subagent once the tables are recorded. `AGENTS.md` stays under its 100-line cap this way.
* **Rewrite the tables in the last commit of any story's branch** that changes a process, a module's name or Owns cell, or a flow.
* **Read an older module map** with a Depends on column as flows, and rewrite it in this format in the next commit that touches it.

## 7. A new application: stand up and hand on

Once each new repository's language is decided and every other item the walking skeleton needs is in one of the four states, run the `greenfield` skill once per repository marked `new:` on `Repositories:`. It takes the name and directory from that line, rewrites the line to the remote URL or local path, and returns here. Then return to `deliver` when it called this skill, or run it; it starts at the walking skeleton.

## What this skill does not do

Writing the outcome, the steps and the candidate stories is `define-work`. Answering one unknown with throwaway code is `spike`. Standing up a repository from a template is `greenfield`. Encoding the flows as contracts is `guardrails`. Building the stories is `deliver`.
