---
name: agile
description: "Use this skill on every request to write, add, remove, change, implement or fix code in a system that already exists, before touching any file. Use it on: 'I want to add X', 'add code to X', 'implement X', 'fix the bug where X', 'build the next slice', 'pick up where we left off', 'implement this prd', 'here is the prd, start building'. Use it whether the ask arrives as an instruction, a want, a complaint, a PRD link, or a need someone else is pressing for, and even when the change looks small enough to just do; a one-line edit still earns a failing test and a verified commit. Work as an Extreme Programming pair: smallest valuable increments, executable specs, continuous delivery, and a fixed division of authorship between user and agent. Do not use it to stand up a project that does not exist yet (`greenfield`), for throwaway exploration (`spike`), or for repo tooling (`harness`)."
license: MIT
compatibility: any-agent
metadata:
  version: "4.0.0"
---
# Agile Loop

Deliver working software in the smallest valuable increments. Generation is cheap. Judgment, redoing non-code work, and discovering the output is unwanted are not. Every rule here protects one of those three.

Loop: **Frame -> Slice -> Propose -> Test -> Halt -> Build -> Review -> Ship.** Resolve a blocking unknown with a spike before entering it.

## Principles

* **Working software over documentation.** Code and automated tests are the source of truth. Generate no Markdown specs, design docs or architecture maps unless asked.
* **Executable specifications.** Never write implementation code first.
* **Smallest valuable increment.** One vertical slice proving the riskiest assumption.
* **Fixed authorship.** The user writes the acceptance criterion. The agent writes everything else. Green must not mean the implementation matches itself.

## Communication

* **No filler.** No acknowledgments, no wrap-ups. Stop when the answer or code is complete.
* **Answer first.** Lead with the core answer or the hard blocker.
* **No analogies.** Describe systems literally.
* **Challenge bad ideas.** Offer the simpler alternative, then defer to the user's product vision.

## Orient

* **Load the charter.** Silently read `CONTEXT.md`, the file the `charter` skill writes: purpose, users, non-goals, nouns, boundaries, constraints. Fall back to `ARCHITECTURE.md`, then `README.md`. When none states a purpose, offer the `charter` skill once, then proceed.
* **Read `docs/adr/`** before proposing a change to an existing boundary or constraint.
* **Read the PRD** if supplied. Extract requirements, success metrics, non-goals. It says what and why, never how.
* **Read the log.** `docs/tasks/{slug}/task.md`, or the tracker epic `CONTEXT.md` names, opens with the Plan (the outcome and the ordered slices) and records what shipped and what was tried. Slug matches the issue key or the `feature/{slug}` branch.

## 0. Frame

Agree one sentence with the user before anything else.

```text
Outcome: What the user does differently once this ships, and where they see it.
```

Reject an outcome naming a component, table, endpoint or file, and one that contradicts a `Not doing` line in `CONTEXT.md` without the user saying so. "Verdicts land in the table" is true when the work is half done. "I open one list each morning and read from it" is not.

Choose the slug: the issue key when `CONTEXT.md` names a tracker, else a kebab-case name for the outcome. Create the branch `feature/{slug}` from main.

Then rank the unknowns. Tag each with what settles it. After the walking skeleton, the slice that resolves the largest unknown most cheaply goes first.

Then play the planning game: name every slice you can see now, one line each, ordered. Titles only, no detail. This is the release plan. It tells the next session that slice 1 is one of six, not the whole feature. Split, add and reorder it after every slice.

Write the result as the Plan at the top of the log, creating the file if absent. The Plan is the only section that is rewritten. Keep it under twenty lines.

```text
# {slug}
Committed so every developer and session reads the same plan. Delete this file when
the last slice ships, after each Learned and A1 line has become a test, an ADR, or
a line in CONTEXT.md. Anything left in it after that is a scar nobody will find.

## Plan
Outcome:   <the sentence above>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <checkable non-goals, one per line>
Slices:    <every slice nameable now, one line each, ordered; the first is next>
```

The log defaults to `docs/tasks/{slug}/task.md`. When `CONTEXT.md` Boundaries names a tracker ("Backlog: Jira project TAG"), the Plan is the epic, each slice is a story under it, a spike is a spike issue, and log entries are resolution comments. Use whatever tracker tool the session has. The slug is the issue key.

| Unknown is about | Settled by |
|---|---|
| Whether it is possible | `spike` |
| Whether anyone wants the output | slice, then observe it in use |
| Whether the layers connect | walking skeleton slice |
| Which of two approaches | `spike` both, timeboxed |
| What the existing system actually does | read the data, not the code |

### Spike only when blocked

A spike answers one question with throwaway code. Two triggers:

* **At PRD read:** an assumption whose falsity changes *what* gets built, not *how*.
* **In the loop:** you cannot write the acceptance criterion or a test row because you lack a fact about the world: a throughput number, a library's real behaviour, what an API returns.

Do not spike when a slice answers it as fast, when the question is a product decision (ask the user), or when there is no falsifiable answer. "Look into the queue library" is not a spike. "The library sustains 1,000 messages/second on this hardware" is.

State the question and the finish line, get agreement, run the `spike` skill. Override two things. Findings go to the log, not `SPIKE_FINDINGS.md`, as the spike entry in section 7: the spike's Outcome and Approach become `Learned`, its Quirks and Dead ends become sub-lines under `Learned`, its Open questions become `Biggest unknown now`. The code is deleted, not offered for keeping; record in the log that you deleted it. When an edit-time hook blocks a spike edit, work in a directory outside the hook's paths, such as the session scratchpad.

## 1. Decide

Run the `adr` skill immediately, not at the end of the feature, for:

* A choice that is expensive or irreversible.
* Knowledge that was expensive to acquire: a measurement, a scar, a cost.
* An accepted hazard or an explicitly rejected alternative.

Below that threshold, ask before any choice a later slice inherits: a new dependency, a port, address or schedule, a file or wire format, a schema, a name that becomes a domain noun. Put the alternatives and the tradeoff to the user in one message and wait. Everything below that line is the agent's to decide, and every such decision is listed under `Decided alone:` in the review's Done block, with what was chosen, why, and the tradeoff. Suggest an architectural change only when the current design obstructs the implementation.

Record assumptions in the task log, each with a kill condition:

```text
- A1: <estimate, with the arithmetic behind it> | kills it: <the observation, and when>
```

When one dies, append the actual next to the estimate. An assumption a recorded decision depends on goes in that ADR's `Assumes` line instead.

## 2. Slice

Cut across the system's layers, never along them. Every slice ends with a person able to do one thing they could not do before, observed through the interface they actually use.

* **Choose the first slice for risk.** The thinnest path touching every layer and reaching a real deploy. Observable is mandatory; valuable is not. Skip it when that pathway exists and is proven.
* **Hardcode everything the skeleton does not test.** Count the seams the user's criterion crosses: database, model, queue, third-party API, container, host. When more than one is unmeasured, the first slice fakes all but one. A served feed holding one hardcoded article is a slice. A feed fed by real verdicts from a real database in a real container is three.
* **The skeleton is a slice like any other.** The user's story stays the feature's criterion in the Plan. The skeleton gets its own one-sentence criterion in section 3, naming what the user will observe (a fake entry in the real reader).
* **Cross whatever boundary the value chain crosses** in the first slice: repo, service, team, or an orchestration layer that does not exist yet. A cron line, a hardcoded query and a bookmark is valid.
* **Choose every later slice for value,** or for unknown killed per hour while an assumption is live.
* **Split further** by workflow step, happy path before error path, one rule before its variants, hardcoding before generalising.
* **Never name a slice** after a layer, component, table or team.
* **Give a constraint its own slice** when no feature slice can carry it: a throughput floor, a memory ceiling, a data-residency rule. Its acceptance criterion is the number. Spike first when the number is unknown.
* **Defer infrastructure** not required to pass this slice's test to a later slice.
* **Treat a bug as a slice** whose outcome is the reproduction. Write the failing test at the level the report describes, before reading the code. Then grep every caller of the function about to change and fix at the point they all route through.

## 3. Propose and Halt

Two halts, in this order. No code, no tests, until both have passed.

**First halt: the criterion.** Output the top of the proposal and stop.

```text
Slice:      Short name.
Outcome:    What a person can do afterwards that they could not before, and where they see it.
Chosen for: Risk, value, or unknown killed. One sentence.
Covers:     PRD requirement IDs, or "none" for a walking skeleton, or "no PRD".
Acceptance: USER-WRITTEN. Blank until the user writes it.
```

The user writes the acceptance criterion. Do not draft it and invite approval. Approval of a generated criterion is not authorship, and the failure it prevents is exactly this: the agent defines correct, implements against its own definition, and reports green.

* **Reject** any criterion containing improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable or modern. Each hides the measurement.
* **Exactly one.** A second criterion means two slices, or a mislabelled integration test that belongs in the table.
* **Promote into it** anything encoding an ADR. How a recorded decision was interpreted must not be discovered by reading generated code.

**Second halt: the rows.** With the criterion in hand, run the `test-table` skill. It proposes one row per test with the columns Test, Level, Generator, Prevents and Killed by, where Killed by is the one-line mutation that must turn the row red. Output the table and the rest of the proposal, then stop until the user accepts or cuts every row.

```text
Tests:      The table. Agent-proposed, user-accepted.
Not now:    What a reader would expect here that is deferred, and to which slice.
```

Revise and re-propose on any rejected line.

## 4. Test and Halt

Write every accepted row as a failing test, acceptance test first. Run them. Output the test names and the red run, then stop. Write no implementation until the user says go. The failing tests are the specification, and the only artifact a person reads in one pass. Change no accepted row without saying so.

When a turn-end hook blocks the red run because the tests name symbols that do not exist yet, add the symbols as stubs whose only body raises. The types pass and the tests still fail on behaviour.

## 5. Build

Issue one instruction to a subagent using [references/build-prompt.md](references/build-prompt.md). The builder makes the accepted rows pass and may add tests for cases the table missed, listing each one and why. It never rewrites an accepted row.

Run the check command the root instructions file names, alongside the tests. The `harness` skill commits one; when none exists, run the linter, the type checker and the build. A red check is a red slice.

## 6. Review

Run the `review` skill: correctness, subtraction, scars, then refactor while green. Commit before the refactor and again after it.

A green gate is not a finished slice. Before reporting done, print the review's Done block: Correctness, Subtraction, Scars, Refactor, Decided alone, Gate. `Decided alone` lists every choice made below the ask-first line in section 1, with what was chosen, why, and the tradeoff. A slice reported without the block is unreviewed. Do not run on into the next slice.

## 7. Ship and Log

* **Commit at every green row,** not once per slice. A commit is the unit a person reviews.
* **Flag** only when the slice exposes user-visible behaviour later slices complete, or when backing it out needs more than a `git revert`. Name the slice that removes the flag under `Not now:`.
* **Tag tests and commits** with the requirement ID, e.g. `[PAY-1420]`.
* **Make the last commit the log.** After the Done block prints: rewrite the Plan at the top of the log (drop the shipped slice, split or add what the slice exposed, reorder by the biggest unknown now), append the entry below, and rewrite `CONTEXT.md` if the slice added a noun, crossed a new boundary, or turned a non-goal into a goal. One commit.
* **Merge to main.** One slice, one merge. A branch that outlives its slice is a queue of unreviewed work. Delete the branch.
* **Deploy from main, by a command in the repo.** A `deploy` script or task target, committed with the slice that first needs it. Never from the working tree, never from a branch, never by commands that live only in chat.
* **Exercise the rollback once** before anything a `git revert` cannot undo: a backfill, a migration, a bulk send.
* **Prompt the user to observe** the behaviour in reality: UI, API or telemetry.
* **Close out** when the Plan's slice list is empty: promote every `Learned` and `A1` line to a test, an ADR or a `CONTEXT.md` line, then delete the log or close the epic.

```text
## <date> — <slice name>
- Done: <what shipped, one line>
- Learned: <what the work exposed that was not known before>
- Built and did not need: <usually an abstraction for a case that never arrived>
- Biggest unknown now: <the reason the Plan was reordered, if it was>
```

Omit empty lines. Never edit or delete an entry. Log a spike the same way, titled `spike: <the question>`, with the field mapping from section 0. `Learned` is mandatory for a spike.

Then ask whether this solved the immediate problem or another slice is required.

## Standing Up a New Domain

Only when a slice opens a genuinely new domain inside an existing system:

* **Establish the ubiquitous language.** Ask the user for the three to five core nouns. Use those exact terms for types, tables and variables. Never invent synonyms.
* **Contract-first at shared boundaries.** Define the executable contract (OpenAPI, Protobuf, strict interface types) and assert it in a test before implementing behind it.
* **Defer explicitly.** Ask which constraints are irreversible, ADR those now, and state that every other decision waits until a test needs it.

To stand up a project that does not exist yet, stop and use `greenfield`.

## Where Things Belong

| Thing | When it enters |
|---|---|
| Library choice, environment facts | The build prompt, before generation |
| Logging, retries, error handling | Pulled by a slice, after a run showed the need |
| Naming, deletion, de-duplication | Refactor, while green |

If the user can name the moment they wanted it, it is slice-pulled. If they can only say it is good practice, it is speculation.

When a plan is precise about internals and silent about the user's day, or the suite is green and the user is still unhappy, read [references/failure-modes.md](references/failure-modes.md).
