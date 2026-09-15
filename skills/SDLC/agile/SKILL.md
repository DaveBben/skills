---
name: agile
description: "Use this skill on every request to write, add, remove, change, implement or fix code in a system that already exists, be it a feature, a bug, a chore, a refactor, or a plain complaint about existing behavior, before touching any file. Use it on: 'I want to add X', 'add code to X', 'implement X', 'fix the bug where X', 'clean up X', 'wire X to Y', 'build the next slice', 'pick up where we left off', 'implement this prd', 'here is the prd, start building'. Use it whether the ask arrives as an instruction, a want, a complaint, a PRD link, or a need someone else is pressing for, and even when the change looks small enough to just do; a one-line edit still earns a failing test and a verified commit. Work as an Extreme Programming pair: smallest valuable increments, executable specs, continuous delivery, and a fixed division of authorship between user and agent. Do not use it to stand up a project that does not exist yet (`greenfield`), for throwaway exploration (`spike`), or for repo tooling (`harness`)."
license: MIT
compatibility: any-agent
metadata:
  version: "4.6.1"
---
# Agile Loop

Deliver working software in the smallest valuable increments.

Loop: **Frame -> Slice -> Propose -> Test -> Halt -> Build -> Review -> Ship.** Resolve a blocking unknown with a spike before entering it.

## Principles

* **Working software over documentation.** Code and automated tests are the source of truth. No documents beyond the task log, ADRs, `AGENTS.md`, and any file the root instructions file says to keep current; those are rewritten in the log commit.
* **Executable specifications.** Never write implementation code first.
* **Smallest valuable increment.** One vertical slice proving the riskiest assumption.
* **Fixed authorship.** The user writes the cards and the acceptance criterion. The agent writes everything else.

## Communication

* **No filler.** No acknowledgments, no wrap-ups. Stop when the answer or code is complete.
* **Answer first.** Lead with the core answer or the hard blocker.
* **No analogies.** Describe systems literally.
* **Challenge bad ideas.** Offer the simpler alternative, then defer to the user's product vision.
* **Say when an instruction does not parse.** Name any card, criterion or constraint that is ambiguous, contradicts `AGENTS.md`, or asks for what the code cannot do, and stop the turn there. Never proceed on a guess.
* **One decision per turn.** Put one choice to the user and wait.

## Orient

* **Load the charter.** Silently read `AGENTS.md`, the file the `orient` skill writes: purpose, users, non-goals, nouns, boundaries, commands, constraints. Fall back to `ARCHITECTURE.md`, then `README.md`. When none states a purpose, offer the `orient` skill once, then proceed.
* **Check the floor.** When the root instructions file names no check command, names one that runs less than CI runs, the suite is red on main in CI, no mutation runner exists, or the log shows three `Not caught by` lines in its last ten entries, halt and offer the `harness` skill before the first slice. When the interface the outcome names has no runner in the repo (a screen and no browser test), the first slice adds the runner with one hardcoded front-door test, as the seam rule in section 2 does; for a command, the entry point called in-process is the runner.
* **Read `docs/adr/`** before proposing a change to an existing boundary or constraint.
* **Read the PRD** if supplied, as raw material for the user's cards, never as a list of IDs to trace. Note its success metrics and non-goals. It says what and why, never how. When the PRD is the user's own and states an outcome, non-goals and decisions, copy them into the Plan and cite them wherever a halt would re-ask them; ask only for the cards. When the root instructions file names a per-change spec directory, the Plan and the entries go at the bottom of that change's spec; create no task.md.
* **Recall before reading.** When the log has an entry, ask the user for one sentence from memory: what the last slice changed and why. Then read the log and name the gap, if any.
* **Read the log.** `docs/tasks/{slug}/task.md`, or the tracker epic `AGENTS.md` names, opens with the Plan (the outcome and the ordered slices) and records what shipped and what was tried. Slug matches the issue key or the `feature/{slug}` branch.

## 0. Frame

Agree one sentence with the user before anything else.

```text
Outcome: What the user does differently once this ships, and where they see it.
```

Reject an outcome naming a component, table, endpoint or file, and one that contradicts a `Not doing` line in `AGENTS.md` without the user saying so. "Verdicts land in the table" is true when the work is half done. "I open one list each morning and read from it" is not.

Choose the slug: the issue key when `AGENTS.md` names a tracker, else a kebab-case name for the outcome. Create the branch `feature/{slug}` from main.

Then play the planning game. Two roles, never swapped.

* **The user writes the cards:** one line each, in their words, naming something they want to do, as many as they can see now and no more. When the user has no cards yet, ask for them; never write them.
* **The agent estimates each card in one word** (hours, a day, more), splits any card over a day into cards the user re-words, and proposes a risk-first order.
* **The user sets the final order.**
* **A card is a title.** The conversation and the criterion wait until it is picked in section 3.
* **Rework this release plan after every slice,** with the same roles: add, split, reorder.

Write the result as the Plan at the top of the log, creating the file if absent. Commit the log, and keep it after the last slice ships. Rewrite the Plan and no other section. Keep it under twenty lines.

```text
# {slug}

## Plan
Outcome:   <the sentence above>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <checkable non-goals, one per line>
Slices:    <user-written cards, one line each, agent estimate beside each, user-ordered; the first is next>
```

The log defaults to `docs/tasks/{slug}/task.md`. When `AGENTS.md` Boundaries names a tracker ("Backlog: Jira project TAG"), the Plan is the epic, each slice is a story under it, a spike is a spike issue, and log entries are resolution comments. Use whatever tracker tool the session has. The slug is the issue key.

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

Run the `spike` skill. It writes its findings into this slug's log as the spike entry of section 7. The code is deleted, not offered for keeping; record in the log that you deleted it. When an edit-time hook blocks a spike edit, work in a directory outside the hook's paths, such as the session scratchpad.

## 1. Decide

Run the `adr` skill immediately, not at the end of the feature, for:

* A choice that is expensive or irreversible.
* Knowledge that was expensive to acquire: a measurement, a scar, a cost.
* An accepted hazard or an explicitly rejected alternative.

Below that threshold:

* **Ask before any choice a later slice inherits:** a new dependency, a port, address or schedule, a file or wire format, a schema, a name that becomes a domain noun. Put the alternatives and the tradeoff to the user in one message and wait.
* **Decide everything below that line alone,** and list each one under `Decided alone:` in the review's Done block, with what was chosen, why, and the tradeoff.
* **Suggest an architectural change only when the current design obstructs the implementation.**

An assumption a recorded decision depends on goes in that ADR's `Assumes` line.

## 2. Slice

Cut across the system's layers, never along them. Every slice ends with a person able to do one thing they could not do before, observed through the interface they actually use.

* **Choose the first slice for risk.** The thinnest path touching every layer and reaching a real deploy. Observable is mandatory; valuable is not. Skip it when that pathway exists and is proven.
* **Hardcode everything the skeleton does not test.** Count the seams the user's criterion crosses: database, model, queue, third-party API, container, host. When more than one is unmeasured, the first slice fakes all but one. A served feed holding one hardcoded article is a slice. A feed fed by real verdicts from a real database in a real container is three.
* **The skeleton is a slice like any other.** The user's story stays the feature's criterion in the Plan. The skeleton gets its own one-sentence criterion in section 3, naming what the user will observe (a fake entry in the real reader).
* **Cross whatever boundary the value chain crosses** in the first slice: repo, service, team, or an orchestration layer that does not exist yet. A cron line, a hardcoded query and a bookmark is valid.
* **The user picks every later slice** from the cards, by value. The agent argues for the card that kills the largest unknown per hour, and adds only spike and constraint slices itself, flagged for the user.
* **Split further** by workflow step, happy path before error path, one rule before its variants, hardcoding before generalising.
* **Never name a slice** after a layer, component, table or team.
* **Give a constraint its own slice** when no feature slice can carry it: a throughput floor, a memory ceiling, a data-residency rule. Its acceptance criterion is the number. Spike first when the number is unknown.
* **Give a slice its signal.** When the slice changes behaviour no test can observe after deploy (a rate, a failure mode, a path taken), the same slice emits the event that makes it observable, and a `Metric` row asserts the event fires.
* **Defer infrastructure** not required to pass this slice's test to a later slice.
* **Pin untested legacy before changing it.** When the code the slice touches has no test of its current behaviour, write characterization tests asserting what it does today, bugs included, and commit them before the red commit. They are scaffolding: the review deletes any the accepted rows make redundant.
* **Introduce the seam first.** When legacy code offers no point to test through, the first slice adds the seam (an injected dependency, an extracted function, a wrapper) and changes no behaviour. Where the old path resists a seam, build the slice beside it and route to the new path, rather than editing in place.
* **Treat a bug as a card** with negative value. A bug in the slice under way is fixed now, no card. A bug in shipped work is a card the user writes and orders against the others, and may decline to fix. Its outcome and criterion are the reproduction; its table is two rows: the failing test at the level the report describes, written before reading the code, then a unit test isolating the fault. The halts of section 3 still run. Then grep every caller of the function about to change and fix at the point they all route through.

## 3. Propose and Halt

Two halts, in this order. No code, no tests, until both have passed.

**First halt: the criterion and the class.** Output the top of the proposal and stop.

```text
Slice:      Short name.
Outcome:    What a person can do afterwards that they could not before, and where they see it.
Chosen for: Risk, value, or unknown killed. One sentence.
Card:       The user's card, verbatim, or "walking skeleton".
Class:      low | normal | high, proposed with the reason. It stands unless the user changes it.
Acceptance: USER-WRITTEN. Blank until the user writes it.
```

Set the class by what a wrong change costs, never by the slice's size. It decides how much of the loop runs; both halts run at every class.

| Class | Defines it | Runs |
|---|---|---|
| `low` | Nobody is harmed and nothing a person reads is wrong before a `git revert` lands: copy, layout, a log line nobody operates from, a dev-only tool | Criterion, one acceptance test committed red, check command, commit. No table, no build subagent, no review subagent. |
| `normal` | Everything else | Sections 3 to 7 as written, with the written explain-back in section 6 |
| `high` | Money, auth, data loss, a migration, a public contract, anything a revert cannot undo | Everything, plus the second reviewer and the live walkthrough in section 6, and the rollback in section 7 rehearsed; when the repository has one maintainer, the second reviewer's rows are the walkthrough agenda and the user answers them in the description |

The user writes the acceptance criterion. Never draft it and invite approval; approval is not authorship.

* **Reject** any criterion containing improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable or modern. Each hides the measurement.
* **Exactly one.** A second criterion means two slices, or a mislabelled integration test that belongs in the table.
* **Promote into it** anything encoding an ADR. How a recorded decision was interpreted must not be discovered by reading generated code.

**Second halt: the rows.** With the criterion in hand, run the `test-table` skill. It proposes one row per test with the columns Test, Level, Generator, Prevents and Killed by, where Killed by is the one-line mutation that must turn the row red. Put any product decision a row exposed before the table, one question. Output the table and the rest of the proposal, then stop. The user writes one line naming the failure they most fear from this change; the agent names the row that catches it or adds one, or, when no test level can observe it, names the section 7 signal that does, under `Not now:`. Then the user cuts rows and adds rows; a row not cut is accepted. One turn, not a row-by-row approval.

```text
Tests:      The table. Agent-proposed, user-accepted.
Not now:    What a reader would expect here that is deferred, and to which slice. Omit when empty.
```

Revise and re-propose on any rejected line.

## 4. Test and Halt

* **Write every accepted row as a failing test,** acceptance test first, new rows in a new test file.
* **Predict each failure before running it:** the assertion, the error type, the value. Run the tests and print prediction and actual side by side, one line per row. A test that fails differently than predicted means the code is not what you believe; read it before going on.
* **Delete or rewrite every existing test that asserts behaviour this slice removes,** in the same commit and listed in its message.
* **Commit the red tests as their own commit,** with the criterion and the accepted table verbatim in the message. Where the harness installed the test guard, record the hash with `git config agile.redCommit <hash>`; the guard refuses edits to those files until the merge clears it.
* **Then stop.** Write no implementation until the user says go, and change no accepted row without saying so.

When a turn-end hook blocks the red run because the tests name symbols that do not exist yet, add the symbols as stubs whose only body raises. The types pass and the tests still fail on behaviour.

## 5. Build

Issue one instruction to a subagent using [references/build-prompt.md](references/build-prompt.md). The builder makes the accepted rows pass and may add tests for cases the table missed, listing each one and why. It never rewrites an accepted row.

**One function is the user's.** On every `normal` and `high` slice, the builder leaves one function unwritten: the one the acceptance row's `Killed by` mutation lands in, or, when that is glue, the first function the acceptance test calls. The builder writes its signature and a one-line contract, and a body that only raises. It makes every other row green and returns with the acceptance row red. The user writes the body until the row is green, then section 6 runs. A slice that adds no function skips this and says so. When the user asks for the whole slice, run the `pair-programming` skill from its hand-over step instead.

Run the tests and the check command yourself, in this session, after the builder returns; the builder's report is a claim, not a result. The check command is the one the root instructions file names; the `harness` skill commits one, and when none exists, run the linter, the type checker and the build. A red check is a red slice.

When the builder reports red on any row but the acceptance row, or touched anything outside its paths, do not debug the attempt. Reset the tree to the red commit and reissue the prompt with the one new fact under NON-NEGOTIABLE. Twice, then the slice is too big: return to section 2 and split it.

## 6. Review

Run the `review` skill in a subagent in the worktree, given the diff, the red commit, the check command and the build prompt's NON-NEGOTIABLE block, and nothing from this session's chat; the context that wrote the tests does not review them. Correctness, subtraction, scars, then refactor while green. Commit before the refactor and again after it.

For a `high` slice, dispatch a second reviewer on a different model with one lens named in its prompt: security, concurrency, or the boundary the slice crosses. Its output is test rows, not edits. Merge them into the table, mark each in scope or deferred under `Not now:`, and write the in-scope rows red before the slice ships.

**Explain-back.** Before the merge, the user accounts for the change in their own words, written before they read the builder's report or the review's Done block.

* `low`: nothing.
* `normal`: the user writes the merge description in their own words: what changed, and one line per new function or branch saying what it is for. A fresh subagent, given only the diff and that text, lists every place the account and the diff disagree, and every function the account does not mention, as questions. The user answers them in the description or changes the code. The description is the merge request's body. Do not draft it, and do not answer the questions for the user; when asked, point at the diff. The review returns its Done block; print it only after the description exists.
* `high`: the same, then a live walkthrough with another person, function by function, with the subagent's questions as the agenda.

Before reporting done, print the review's Done block: Correctness, Subtraction, Scars, Refactor, Decided alone, Gate. `Decided alone` lists every choice made below the ask-first line in section 1, with what was chosen, why, and the tradeoff. Never report a slice without the block, and never run on into the next slice.

## 7. Ship and Log

* **Flag** only when the slice exposes user-visible behaviour later slices complete, or when backing it out needs more than a `git revert`. Name the slice that removes the flag under `Not now:`.
* **Tag tests and commits** with the card's issue key when a tracker exists, e.g. `[PAY-1420]`.
* **Make the last commit the log.** After the Done block prints: rewrite the Plan at the top of the log (drop the shipped card; put any split or new card the slice exposed to the user, who words and orders it; never add a feature card alone), append the entry below, and rewrite `AGENTS.md` if the slice added a noun, crossed a new boundary, or turned a non-goal into a goal. One commit.
* **The user merges.** Present the answered description, the Done block and the diff. The agent never merges to main. One slice, one merge. Delete the branch after the merge and clear the red-commit guard.
* **Deploy from main, by a command in the repo.** A `deploy` script or task target, committed with the slice that first needs it. Never from the working tree, never from a branch, never by commands that live only in chat.
* **Exercise the rollback once** before anything a `git revert` cannot undo: a backfill, a migration, a bulk send.
* **Name the signal before merging:** the screen, the endpoint or the event the user will read to know the slice worked. Then prompt the user to observe it in reality.
* **Close out** when the Plan's slice list is empty: promote every `Learned` line to a test, an ADR or an `AGENTS.md` line, write the pin beside each, then close the epic. Keep the file.

```text
## <date> — <slice name>
- Done: <what shipped, one line>
- By hand: <the function the user wrote, or "none: no new function">
- Observed: <the section 7 signal, seen or not; the next session appends this line before its first slice>
- Accepted: <red commit hash; its message holds the criterion and the table>
- Learned: <one finding, bold headline, then the test, ADR ID or AGENTS.md line that pins it>
- Decided: <one choice from Decided alone, with its tradeoff, or a bare ADR ID>
- Not caught by: <bugs only: why no test, check or review stopped it, and the rule, row or hook now added>
```

Omit empty lines. One line per finding and per decision; repeat the field. The entry fits on one screen. A finding that needs more than a line is an ADR: write it, leave the ID. The reason the Plan was reordered goes in the Plan, not the entry. `Not caught by` is mandatory for a bug: name the gap in the harness or the test table and close it in the same slice, or hand it to the `harness` skill. Never edit or delete an entry beyond appending its `Observed` line. A spike's entry is titled `spike: <the question>`; the `spike` skill writes it. `Learned` is mandatory for a spike.

Then ask whether this solved the immediate problem or another slice is required. Either way, end the session here. The next slice starts fresh from the log.

## Working in a Team

Other people and other agents change main while a slice is in flight.

* **One slug, one branch, one session, one log file.** Two slices never share a branch or a log. Parallel work is parallel slugs, each with its own Plan; the shared backlog is the tracker `AGENTS.md` names.
* **Rebase on main before the red commit and again before the review.** Run the check command on the rebased tree.
* **Open a merge request when the repo has a remote.** The explain-back description is its body; the Done block follows it. The user merges, after any reviewer the repo requires.
* **Edit `AGENTS.md` and `docs/adr/architecture/` only in the log commit, after the rebase.** They are the shared files, and a stale rewrite erases someone else's slice. Write an architecture ADR the moment the decision is made, as `adr` says, and commit it there.
* **The red-commit guard is local git config**, per clone. It never travels with the branch.
* **The harness is the repo's, not the developer's.** Hooks, rules, contracts and the check command are committed; nothing the loop depends on lives in one person's settings.

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
