---
name: agile
description: "Use this skill on every request to write, add, remove, change, implement or fix code in a system that already exists, be it a feature, a bug, a chore, a refactor, or a plain complaint about existing behavior, before touching any file. Use it on: 'I want to add X', 'add code to X', 'implement X', 'fix the bug where X', 'clean up X', 'wire X to Y', 'build the next slice', 'pick up where we left off', 'implement this prd', 'here is the prd, start building'. Use it whether the ask arrives as an instruction, a want, a complaint, a PRD link, or a need someone else is pressing for, and even when the change looks small enough to just do; a one-line edit still earns a failing test and a verified commit. Work as an Extreme Programming pair: smallest valuable increments, executable specs, continuous delivery, and a fixed division of authorship between user and agent. Do not use it to stand up a project that does not exist yet (`greenfield`), for throwaway exploration (`spike`), or for repo tooling (`harness`)."
license: MIT
compatibility: any-agent
metadata:
  version: "6.10.0"
---
# Agile Loop

Deliver working software in the smallest valuable increments.

Loop: **Frame -> Slice -> Propose -> Test -> Halt -> Build -> Review -> Ship.** Resolve a blocking unknown with a spike before entering it.

## Principles

* **Working software over documentation.** Code and automated tests are the source of truth. No documents beyond the task log, ADRs, `AGENTS.md`, and any file the root instructions file says to keep current; those are rewritten in the log commit.
* **Executable specifications.** Never write implementation code first.
* **Smallest valuable increment.** One vertical slice proving the riskiest assumption.
* **Fixed authorship.** The agent proposes the cards and the acceptance criterion; the user confirms, rewords or rejects each. The agent writes everything else.

## Communication

Load [references/writing.md](references/writing.md) now. It governs every chat reply and every file this skill writes. Three rules govern the loop itself:

* **Challenge bad ideas.** Offer the simpler alternative, then defer to the user's product vision.
* **Say when an instruction does not parse.** Name any card, criterion or constraint that is ambiguous, contradicts `AGENTS.md`, or asks for what the code cannot do, and stop the turn there. Never proceed on a guess.
* **One decision per turn.** Put one choice to the user and wait.

## Orient

* **Load the charter.** Silently read `AGENTS.md`, the file the `orient` skill writes: purpose, users, non-goals, nouns, boundaries, commands, constraints. Fall back to `ARCHITECTURE.md`, then `README.md`. When none states a purpose, offer the `orient` skill once, then proceed.
* **Check the floor.** When the root instructions file names no check command, names one that runs less than CI runs, the suite is red on main in CI, no mutation runner exists, or the log shows three `Not caught by` lines in its last ten entries, halt and offer the `harness` skill before the first slice. When the interface the outcome names has no runner in the repo (a screen and no browser test), the first slice adds the runner with one hardcoded front-door test, as the seam rule in section 2 does; for a command, the entry point called in-process is the runner.
* **Read `docs/adr/`** before proposing a change to an existing boundary or constraint.
* **Read the PRD** if supplied, as raw material for the cards, never as a list of IDs to trace. Note its success metrics and non-goals. It says what and why, never how. When the PRD is the user's own and states an outcome, non-goals and decisions, copy them into the Plan and cite them wherever a halt would re-ask them; propose the cards from it. When the root instructions file names a per-change spec directory, the Plan and the entries go at the bottom of that change's spec; create no task.md.
* **State the last slice.** When the log has an entry, read it and tell the user in one line what the last merged slice changed and why, from its `Done` line and the commit it points to. Ask nothing.
* **Read the log.** `docs/tasks/{slug}/task.md`, or the tracker epic `AGENTS.md` names, opens with the Plan (the outcome and the ordered slices) and records what shipped and what was tried. Slug matches the issue key or the `feature/{slug}` branch.
* **Carry the `Learned` lines forward.** Before proposing the next slice, read every `Learned` and `Not caught by` line in the log, whole, and every ADR the Plan's `Decided:` line lists. Each is a fact about this system that a fresh session does not have. Where one bears on the slice about to be proposed, cite it in the proposal's `Assumes:` line or in the build prompt's NON-NEGOTIABLE block.

## 0. Frame

Agree one sentence with the user before anything else.

```text
Outcome: What the user does differently once this ships, and where they see it.
```

Reject an outcome naming a component, table, endpoint or file, and one that contradicts a `Not doing` line in `AGENTS.md` without the user saying so. "Verdicts land in the table" is true when the work is half done. "I open one list each morning and read from it" is not.

Choose the slug: the issue key when `AGENTS.md` names a tracker, else a kebab-case name for the outcome. Create the branch `feature/{slug}` from main. Every slice gets its own branch `slice/{slug}/{n}-{short-name}` from the feature branch, and merges back into it; the feature branch merges into main when the Plan's slice list is empty. The prefixes differ because git stores refs as paths, so `feature/{slug}` and `feature/{slug}/1-x` cannot both exist.

Then propose the cards.

* **The agent proposes the cards from the request:** one line each, a title naming something the user will be able to do, every card the request needs and no more, in a proposed order with the riskiest first. Split any card that crosses more than one seam or workflow step. No estimates.
* **The user cuts, adds, rewords and reorders.** A card not changed is accepted. One turn.
* **A card is a title.** The conversation and the criterion wait until it is picked in section 3.
* **Rework the list after every slice:** add, split, reorder, and put each change to the user the same way.

Write the result as the Plan at the top of the log, creating the file if absent. Commit the log, and keep it after the last slice ships. Rewrite the Plan and no other section. Keep it under twenty lines.

```text
# {slug}

## Plan
Outcome:   <the sentence above>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <checkable non-goals, one per line>
Decided:   <one line per architecture decision: the ADR file, or the file in the code that already settles it>
Deferred:  <one line per deferred decision, and the slice that will force it>
Slices:    <the accepted cards, one line each, in order; the first is next>
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

Architecture decisions are put to the user one per message, with the alternatives and the tradeoff, and the agent waits. Each answer is written with the `adr` skill before the next decision is asked and before any code that depends on it: `docs/adr/architecture/` when it outlives the feature, `docs/adr/{slug}/` when it does not. The user may answer "defer"; a deferred decision goes on the Plan under `Deferred:` with the slice that will force it.

* **Before the first slice.** Load [references/decisions.md](references/decisions.md). Walk its "before the first slice" list for this system's kind. For each item the outcome touches, state in the Plan under `Decided:` what the code already settles, with the file that settles it, and put the rest to the user one at a time. No proposal until every item is decided, deferred, or stated as settled.
* **At every slice pick.** Before the first halt, read `Deferred:` and the "when a slice forces it" list. When this slice is the first to need one (the first cache, the first queue, the first second service, the first payment call), put that decision to the user, then write the ADR, then propose.
* **Ask before any smaller choice a later slice inherits:** a port, address or schedule, a file or wire format, a name that becomes a domain noun. One message, alternatives and tradeoff, then wait.
* **Decide everything below that line alone,** and list each one under `Decided alone:` in the review's Done block, with what was chosen, why, and the tradeoff.
* **Suggest an architectural change only when the current design obstructs the implementation.**

The `adr` skill still fires on its own triggers mid-slice: an accepted hazard, a rejected alternative, knowledge that cost time to acquire. An assumption a recorded decision depends on goes in that ADR's `What it doesn't buy` section.

## 2. Slice

Cut across the system's layers, never along them. Every slice ends with a person able to do one thing they could not do before, observed through the interface they actually use.

* **Choose the first slice for risk.** The thinnest path touching every layer and reaching a real deploy. Observable is mandatory; valuable is not. Skip it when that pathway exists and is proven.
* **Hardcode everything the skeleton does not test.** Count the seams the criterion crosses: database, model, queue, third-party API, container, host. When more than one is unmeasured, the first slice fakes all but one. A served feed holding one hardcoded article is a slice. A feed fed by real verdicts from a real database in a real container is three.
* **The skeleton is a slice like any other.** The user's card stays the feature's outcome in the Plan. The skeleton gets its own one-sentence criterion in section 3, naming what the user will observe (a fake entry in the real reader).
* **Cross whatever boundary the value chain crosses** in the first slice: repo, service, team, or an orchestration layer that does not exist yet. A cron line, a hardcoded query and a bookmark is valid.
* **The user picks every later slice** from the cards. The agent argues for the card that kills the largest unknown, and flags any spike or constraint card it adds.
* **Split further** by workflow step, happy path before error path, one rule before its variants, hardcoding before generalising.
* **Never name a slice** after a layer, component, table or team.
* **Give a constraint its own slice** when no feature slice can carry it: a throughput floor, a memory ceiling, a data-residency rule. Its acceptance criterion is the number. Spike first when the number is unknown.
* **Give a slice its signal.** When the slice changes behaviour no test can observe after deploy (a rate, a failure mode, a path taken), the same slice emits the event that makes it observable, and a `Metric` row asserts the event fires.
* **Defer infrastructure** not required to pass this slice's test to a later slice.
* **Pin untested legacy before changing it.** When the code the slice touches has no test of its current behaviour, write characterization tests asserting what it does today, bugs included, and commit them before the red commit. They are scaffolding: the review deletes any the accepted rows make redundant.
* **Introduce the seam first.** When legacy code offers no point to test through, the first slice adds the seam (an injected dependency, an extracted function, a wrapper) and changes no behaviour. Where the old path resists a seam, build the slice beside it and route to the new path, rather than editing in place.
* **Treat a bug as a card** with negative value. A bug in the slice under way is fixed now, no card. A bug in shipped work is a card the user orders against the others, and may decline to fix. Its outcome and criterion are the reproduction; its table is two rows: the failing test at the level the report describes, written before reading the code, then a unit test isolating the fault. The halts of section 3 still run. Then grep every caller of the function about to change and fix at the point they all route through.

## 3. Propose and Halt

Start the slice on its own branch, `slice/{slug}/{n}-{short-name}`, cut from `feature/{slug}` after rebasing the feature branch on main. Then two halts, in this order. No code, no tests, until both have passed.

**First halt: the criterion.** Output the top of the proposal and stop.

```text
Slice:      Short name.
Outcome:    What a person can do afterwards that they could not before, and where they see it.
Chosen for: Risk, value, or unknown killed. One sentence.
Card:       The user's card, verbatim, or "walking skeleton".
Assumes:    One line per fact the slice rests on that was read from a document or not checked, with how to check it. Omit when every fact was read from the code.
Acceptance: Given <a concrete starting state>, when <a concrete action>, then <what the person sees>, in the domain's nouns with real values. Agent-proposed; the user confirms, rewords or rejects it.
```

The user strikes or confirms each `Assumes` line. A fact found wrong after the build is a `Decided alone` line in the review; a fact stated here is checked before it.

**Skip the table, the build subagent and the review subagent** when nobody is harmed and nothing a person reads is wrong before a `git revert` lands: copy, layout, a log line nobody operates from, a dev-only tool. Such a slice is the criterion, one acceptance test committed red, the check command, and the commit. Say so in the proposal.

Propose the criterion as one Given/When/Then sentence and stop. The user confirms it, rewords it, or rejects it, and a rejected one is re-proposed from what they said.

* **Never propose** a criterion containing improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable or modern. Each hides the measurement.
* **Exactly one.** A second criterion means two slices, or a mislabelled integration test that belongs in the table.
* **Promote into it** anything encoding an ADR. How a recorded decision was interpreted must not be discovered by reading generated code.

**Second halt: the rows.** With the criterion in hand, run the `test-table` skill. It proposes an index table (number, title, Level, Generator, Killed by) and one block per test with Given, When, Then and Prevents, where Killed by is the one-line mutation that must turn the row red. Put any product decision a row exposed before the table, one question. Output the table and the rest of the proposal, then stop. The user cuts rows and adds rows; a row not cut is accepted. One turn, not a row-by-row approval.

```text
Tests:      The table. Agent-proposed, user-accepted.
Not now:    What a reader would expect here that is deferred, and to which slice. Omit when empty.
```

Revise and re-propose on any rejected line.

## 4. Test and Halt

* **Write every accepted row as a failing test,** acceptance test first, new rows in a new test file.
* **Run the tests.** A row that passes before the build, or fails for a reason other than the missing behaviour, means the code is not what you believe; read it before going on.
* **Delete or rewrite every existing test that asserts behaviour this slice removes,** in the same commit and listed in its message.
* **Commit the red tests as their own commit,** with the criterion and the accepted table verbatim in the message. Where the harness installed the test guard, record the hash with `git config agile.redCommit <hash>`; the guard refuses edits to those files until the merge clears it.
* **Then stop.** Write no implementation until the user says go, and change no accepted row without saying so.

When a turn-end hook blocks the red run because the tests name symbols that do not exist yet, add the symbols as stubs whose only body raises. The types pass and the tests still fail on behaviour.

## 5. Build

Issue one instruction to a subagent using [references/build-prompt.md](references/build-prompt.md). The builder makes the accepted rows pass and may add tests for cases the table missed, listing each one and why. It never rewrites an accepted row.

**When the user says they will write the code themselves,** issue no build prompt. The accepted rows are already red; the user writes the code until they are green. Then run the `give-feedback` skill on their diff before section 6.

Run the tests and the check command yourself, in this session, after the builder returns; the builder's report is a claim, not a result. The check command is the one the root instructions file names; the `harness` skill commits one, and when none exists, run the linter, the type checker and the build. A red check is a red slice.

When the builder reports red on any row but the acceptance row, or touched anything outside its paths, do not debug the attempt. Reset the tree to the red commit and reissue the prompt with the one new fact under NON-NEGOTIABLE. Twice, then the slice is too big: return to section 2 and split it.

## 6. Review

Run the `review` skill in a subagent in the worktree, given the diff, the red commit, the check command and the build prompt's NON-NEGOTIABLE block, and nothing from this session's chat; the context that wrote the tests does not review them. Correctness, subtraction, scars, then refactor while green. Commit before the refactor and again after it.

**Merge description.** The agent writes it: the criterion, what changed in one paragraph, and one line per new function or branch saying what it is for. The Done block follows it. It is the merge request's body.

Before reporting done, print the review's Done block: Correctness, Subtraction, Scars, Refactor, Decided alone, Gate. `Decided alone` lists every choice made below the ask-first line in section 1, with what was chosen, why, and the tradeoff. Never report a slice without the block, and never run on into the next slice.

## 7. Ship and Log

* **Flag** only when the feature, once merged to main, exposes user-visible behaviour a later feature completes, or when backing it out needs more than a `git revert`. Name the slice that removes the flag under `Not now:`.
* **Tag tests and commits** with the card's issue key when a tracker exists, e.g. `[PAY-1420]`.
* **Make the last commit the log.** After the Done block prints: rewrite the Plan at the top of the log (drop the shipped card; propose any split or new card the slice exposed, which the user accepts, rewords, reorders or cuts), append the entry below, and rewrite `AGENTS.md` if the slice added a noun, crossed a new boundary, or turned a non-goal into a goal. One commit.
* **Call out what the slice touches.** When the diff touches authentication, authorization, secrets, money, health or personal data, a migration, a public contract, or anything a `git revert` cannot undo, say so in one line above the Done block: what it touches and the file. The user decides what extra review it gets.
* **The user merges the slice into `feature/{slug}`.** Present the description, the Done block and the diff. The agent never merges. One slice, one merge. Delete the slice branch after the merge and clear the red-commit guard.
* **Deploy from main, by a command in the repo.** A `deploy` script or task target, committed with the slice that first needs it. Never from the working tree, never from a branch, never by commands that live only in chat.
* **Exercise the rollback once** before anything a `git revert` cannot undo: a backfill, a migration, a bulk send.
* **Name the signal before merging:** the screen, the endpoint or the event the user will read to know the slice worked. Prompt the user to observe it once the code is deployed: after the feature merges to main, or earlier when the repo deploys feature branches.
* **Close out** when the Plan's slice list is empty: promote every `Learned` line to a test, an ADR or an `AGENTS.md` line, write the pin beside each, rebase `feature/{slug}` on main and run the check command, then open the merge request into main with the Plan and every entry's `Done` line as its body. The user merges it. Delete the feature branch, close the epic, keep the log file.

```text
## <date> — <slice name>
- Done: <what shipped, one line>
- Observed: <the section 7 signal, seen or not; appended once the slice is deployed>
- Accepted: <red commit hash; its message holds the criterion and the table>
- Learned: <one finding, bold headline, then the test, ADR ID or AGENTS.md line that pins it>
- Not caught by: <bugs only: why no test, check or review stopped it, and the rule, row or hook now added>
```

Omit empty lines. One line per finding; repeat the field. The entry fits on one screen. A `Learned` line states the mechanism ("the pool has 5 workers and each LLM call holds one for the full round trip"), never a label alone ("pool exhaustion"). A finding that needs more than a line is an ADR: write it, leave the ID. The reason the Plan was reordered goes in the Plan, not the entry. `Not caught by` is mandatory for a bug: name the gap in the harness or the test table and close it in the same slice, or hand it to the `harness` skill. Never edit or delete an entry beyond appending its `Observed` line. A spike's entry is titled `spike: <the question>`; the `spike` skill writes it. `Learned` is mandatory for a spike.

The next slice starts fresh from the log.

## Working in a Team

Other people and other agents change main while a slice is in flight.

* **One slug, one feature branch, one log file. One slice, one slice branch, one session.** Two slices never share a branch. Parallel work is parallel slugs, each with its own Plan; the shared backlog is the tracker `AGENTS.md` names.
* **Rebase the slice branch on `feature/{slug}` before the red commit and again before the review,** and the feature branch on main before each slice starts and before its own merge. Run the check command on the rebased tree.
* **Open a merge request from the slice branch into `feature/{slug}` when the repo has a remote.** The merge description is its body. The user merges, after any reviewer the repo requires.
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
