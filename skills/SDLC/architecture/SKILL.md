---
name: architecture
description: "Use this skill when the shape of a system must be decided, when any decision must survive the conversation, or when work is asked for in a repository with no application yet. Use it on: planning a new application, 'let's build this' in an empty repo, 'how should this be structured', 'should I use X for storage', 'capture, snapshot or map the architecture', and any choice costing more than a day to reverse: a library, a data shape, a trust or consistency boundary. Use it on: 'adr', 'write an adr', 'record the why', 'we will accept that risk', 'let's go with X instead of Y'. Spikes each untried crossing first, asks the load, response-time, downtime and data-volume numbers, maps processes, modules and flows, and puts each expensive decision to the user in turn, recording each as an ADR with the user's reasons and the rejected alternatives. Not for reviewing an existing ADR (`reviewing`), drafting stories (`define`), throwaway code (`spike`), orienting in a repository (`orient`), or building (`deliver`)."
license: MIT
compatibility: any-agent
metadata:
  version: "2.4.0"
---
# Architecture

Architecture here is the set of decisions that are expensive to reverse, and the shape they give the system: which processes run, which modules own what, and how they talk. Decide it in this order: find out what is unknown with spikes, take a broad starting shape, record each decision, prove the shape with a walking skeleton, and change it by refactoring as stories teach more. The walking skeleton is the thinnest end-to-end version of the outcome a real person can use, built as the first story.

The shape goes into a dated snapshot under `docs/architecture/snapshots/`, written by [references/snapshot.md](references/snapshot.md), and `AGENTS.md` holds one line pointing at the latest snapshot. Each decision goes into an ADR (architecture decision record) under `docs/adr/`, and each rule into a test or a dependency contract.

Everything here is agreed with the user. Propose, then wait. The user makes every decision section 5 lists.

**Where things are written.** Planning a system or a new application needs the tracker the `Backlog:` line of `AGENTS.md` names; with no such line, halt and run the `orient` skill, which helps the user connect one. Recording one decision and deciding one open item need no tracker: with none, or with no feature open, the ADR goes under `docs/adr/architecture/` and nothing else is written. The slug is the epic's key. The feature header is the epic's description, which `define` writes. This skill adds `Decided:` (one ADR path per line) and `Deferred:` (one item per line, with the number, story or spike that will force it), and appends its numbers to `define`'s `Constraints:` line. When the work spans repositories, `docs/adr/` lives in the first repository on the `Repositories:` line. Commit the ADRs, the snapshot, and any `AGENTS.md` change, on a branch `story/{slug}/0-plan` and open its pull request, which the user merges before the first story; in a repository with no remote, commit them on main. With nothing to commit before the first story, open no plan branch.

## 1. Pick the path

* **Record one decision already made** (an accepted risk, "X instead of Y", "record the why", a spike's decision rows): load [references/adr.md](references/adr.md) and do nothing else.
* **Decide one open item** ("Postgres or SQLite?", or one decision a story forced): run section 5 for that item alone, then record the answer by [references/adr.md](references/adr.md).
* **Capture the current architecture** ("capture", "snapshot" or "map this codebase's architecture"): no tracker needed, and no questions until the snapshot is drafted. Load [references/plan.md](references/plan.md) and run its section 4 from the code, for the whole system rather than one outcome, then write the snapshot by [references/snapshot.md](references/snapshot.md):
  * **Processes:** every entry point that starts one: a server, a worker, a scheduled job, a command.
  * **Modules:** the top-level packages or directories, each with the one thing it owns.
  * **Flows:** calls across modules, and every call to a database, queue, file store or other service. Fill "Who else reaches To" from what the code shows (the address it listens on, the check on the caller, the credential it uses), and write "unknown" where the code does not show it.

  When an earlier snapshot exists, or `AGENTS.md` still holds architecture tables, report the drift: each fact the code contradicts, each process, store or flow the code has and the earlier record lacks, and each the record has and the code lacks. Move any tables out of `AGENTS.md` into the snapshot. List in chat what the code settles (each repository's language and platform, each data store, each check on a caller), with the file that settles it, and each "unknown" as one question. Commit the snapshot and the `AGENTS.md` pointer on their own branch with a pull request. Record any settled item as an ADR only when the user gives the reasons, by [references/adr.md](references/adr.md). Then stop.
* **Plan a system** (a feature of several stories, "how should this be structured"): load [references/plan.md](references/plan.md) and run sections 2 to 6. Run alone, end by running `deliver`.
* **A new application**, or work asked for in a repository with no application yet: this skill owns the path end to end. Once `define` has written the shared understanding, decide the repositories first: how many, the name of each, and the directory each lives in, written on `Repositories:` as `new: <name> <directory>`. Run `git init -b main` in the first one's directory and record the repositories decision there by [references/adr.md](references/adr.md). Then load [references/plan.md](references/plan.md) and run sections 2 to 7.

Inputs: the shared understanding `define` wrote, with its outcome, the steps a person takes, the walking-skeleton story and the `Repositories:` line. When none exists, run `define` first. In an existing application with no walking skeleton, the crossings are the ones this work's stories make. Before proposing a change to an existing boundary, read `AGENTS.md` and the latest snapshot it points at, and list the titles in `docs/adr/`, skipping any ADR with a `Superseded by:` line; open one only when its Decision names a module, flow or store this work touches.

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
* the system's trust boundaries (the Who else reaches To answers from section 4 of the plan reference) and consistency boundaries
* each choice a number or a sensitive-data answer from section 3 of the plan reference forces, such as a connection pool, a read replica, failover or encryption

For each one the outcome touches, state in chat what the code already settles, with the file that settles it. Put the rest to the user one per message, with the alternatives and the tradeoff, and wait. Record each answer by [references/adr.md](references/adr.md) before the next decision is asked and before any code that depends on it.

* **A data rule that holds for every feature** (sensitive data, retention, backup) goes in one ADR under `docs/adr/architecture/` and one Critical Constraints line, never on a feature header. Record the five data-shape answers as one ADR per store.
* **Turn each answer a story could break into a constraint** on the feature header's `Constraints:` line, so the `define` skill writes it as a criterion on every story that could break it. "Writing the same sample twice stores one row", "an upload without the credential is refused" and "a row with no unit is refused" are each a criterion with a test.
* **Ask whether each third-party service's sandbox can be tested against,** for every flow whose To runs on a machine marked `external:` in the Processes table (section 4 of the plan reference): at the volume the numbers need, and in each failure mode the user names with its number ("429 after 100 requests a minute", "the webhook arrives twice", "no answer for 30 s"). When it cannot, record an ADR standing a twin in for it: a fake of the service kept under `tests/twins/<service>/`, whose contract suite runs against the twin in every check and against the sandbox or recorded real responses on a schedule. Its Detector is that suite, and its rows come from recorded real exchanges, never from the documentation alone. The twin is criteria on the first story that crosses the flow.
* **Prove the restore.** When the system stores data it cannot regenerate, the story that first stores it carries a criterion: restore the latest backup into an empty store and find every row.

Every item ends in one of four states:

| State | Written where |
|---|---|
| Decided | An ADR, listed on the feature header's `Decided:` line |
| Deferred | The feature header's `Deferred:` line, with the number or the story that will force it. Propose "defer" for each item the first story does not touch. |
| Waiting on spike N | The feature header's `Deferred:` line as "waits on spike N", for a spike the `deliver` loop runs. Decide it once the spike is done: its resolution comment, the findings, is written. |
| Settled by the code | Stated in chat with the file that settles it |

No story that needs an item starts until the item is in one of the four states.

* **Ask before any smaller choice a later story inherits:** a port, an address or a schedule, a file or wire format, a name that becomes a domain noun. One message, alternatives and tradeoff, then wait.
* **Decide alone** any choice no later story inherits and no person using the system would see, and list each in chat with what was chosen, why, and the tradeoff.
* **Suggest an architectural change only when the current design obstructs the implementation.**
* **An assumption a recorded decision depends on** goes in that ADR's Decision paragraph.
