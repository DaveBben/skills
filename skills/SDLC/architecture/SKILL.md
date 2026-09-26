---
name: architecture
description: "Use this skill when the shape of a system must be decided, when any decision must survive the conversation, or when work is asked for in a repository with no application yet. Use it on: planning a new application, 'let's build this' in an empty repository, 'how should this be structured', 'should I use X for storage', 'map this codebase's architecture', and any choice costing more than a day to reverse: a library, a data shape, a trust or consistency boundary. Use it on: 'adr', 'write an adr', 'record the why', 'we will accept that risk', 'let's go with X instead of Y'. Spikes each untried crossing first, asks the load, response-time, downtime and data-volume numbers, maps processes, modules and flows, and puts each expensive decision to the user one at a time, recording each as an ADR with the user's reasons and the rejected alternatives. Not for reviewing an existing ADR (`reviewing`), drafting stories (`define-work`), throwaway code (`spike`), orienting in a repository (`orient`), or building (`deliver`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.5.0"
---
# Architecture

Load [references/writing.md](references/writing.md) before the first reply, unless it is already loaded this session.

Architecture here is the set of decisions that are expensive to reverse, and the shape they give the system: which processes run, which modules own what, and how they talk. Decide it in this order: find out what is unknown with spikes, take a broad starting shape, record each decision, prove the shape with a walking skeleton, and change it by refactoring as stories teach more. The walking skeleton is the thinnest end-to-end version of the outcome a real person can use, built as the first story.

Nothing goes into a separate design document. The tables go into `AGENTS.md`, each decision into an ADR (architecture decision record) under `docs/adr/`, and each rule into a test or a dependency contract.

Everything here is agreed with the user. Propose, then wait. The user makes every decision section 5 lists.

**Where things are written.** The slug is the short kebab-case name `define-work` gave the work, or the epic's key on a tracker. The feature log is `docs/delivery/{slug}.md`; its `## Feature` block at the top is the feature header, which `define-work` writes. This skill adds `Decided:` (one ADR path per line) and `Deferred:` (one item per line, with the number, story or spike that will force it), and appends its numbers to `define-work`'s `Constraints:` line. On a tracker the feature header is the epic's description. When the work spans repositories, the feature log and `docs/adr/` live in the first repository on the `Repositories:` line. Commit the feature log, the ADRs and the tables on a branch `story/{slug}/0-plan` and open its pull request, which the user merges before the first story; in a repository with no remote, commit them on main.

## 1. Pick the path

* **Record one decision already made** (an accepted risk, "X instead of Y", "record the why", a spike's decision rows): load [references/adr.md](references/adr.md) and do nothing else.
* **Decide one open item** ("Postgres or SQLite?", or one decision a story forced): run section 5 for that item alone, then record the answer by [references/adr.md](references/adr.md).
* **Map an existing codebase** ("map this codebase's architecture"): load [references/plan.md](references/plan.md), run its section 4 from the code, write the tables by its section 6, and stop.
* **Plan a system** (a feature of several stories, "how should this be structured"): load [references/plan.md](references/plan.md) and run sections 2 to 6. Run alone, end by running `deliver`.
* **A new application**, or work asked for in a repository with no application yet: this skill owns the path end to end. Once `define-work` has written the shared understanding, decide the repositories first: how many, the name of each, and the directory each lives in, written on `Repositories:` as `new: <name> <directory>`. Run `git init -b main` in the first one's directory, move the feature log there if `define-work` wrote it elsewhere, commit it, and record the repositories decision by [references/adr.md](references/adr.md). Then load [references/plan.md](references/plan.md) and run sections 2 to 7.

Inputs: the shared understanding `define-work` wrote, with its outcome, the steps a person takes, the walking-skeleton story and the `Repositories:` line. When none exists, run `define-work` first. In an existing application with no walking skeleton, the crossings are the ones this work's stories make. Before proposing a change to an existing boundary, read `AGENTS.md` and list the titles in `docs/adr/`, skipping any ADR with a `Superseded by:` line; open one only when its Decision names a module, flow or store this work touches.

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
* **Turn each answer a story could break into a constraint** on the feature header's `Constraints:` line, so the `story` skill writes it as a criterion on every story that could break it. "Writing the same sample twice stores one row", "an upload without the credential is refused" and "a row with no unit is refused" are each a criterion with a test.
* **Ask whether each third-party service's sandbox can be tested against,** for every flow whose To runs on a machine marked `external:` in the Processes table (section 4 of the plan reference): at the volume the numbers need, and in each failure mode the user names with its number ("429 after 100 requests a minute", "the webhook arrives twice", "no answer for 30 s"). When it cannot, record an ADR standing a twin in for it: a fake of the service kept under `tests/twins/<service>/`, whose contract suite runs against the twin in every check and against the sandbox or recorded real responses on a schedule. Its Detector is that suite, and its rows come from recorded real exchanges, never from the documentation alone. The twin is criteria on the first story that crosses the flow.
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
* **An assumption a recorded decision depends on** goes in that ADR's Decision paragraph.
