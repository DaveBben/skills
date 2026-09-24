---
name: execute
description: "Use this skill on every request to write, add, remove, change, implement or fix code in a system that already exists, be it a feature, a bug, a chore, a refactor or a complaint about existing behavior, before touching any file. Use it on: 'I want to add X', 'implement X', 'fix the bug where X', 'wire X to Y', 'build story X', 'work through this epic', 'pick up where we left off', 'implement this prd', 'here is the prd, start building'. Use it even when the change looks small enough to just do. Runs one named story, or a whole epic with `next-story` choosing each story. Agree the outcome, the architecture decisions, a module map and every story's acceptance criteria with the user up front, then run each story unattended from failing tests to a merged pull request. Pause only for a new story, a forced decision, a product decision, or the merge. Do not use it to stand up a project that does not exist yet (`greenfield`), for throwaway exploration (`spike`), or for repo tooling (`harness`)."
license: MIT
compatibility: any-agent
metadata:
  version: "10.0.0"
---
# Execute

Two modes. **One story:** the user names it, and the loop runs that story and stops after its log commit. **An epic:** the loop runs every story in the feature, choosing each next one with `next-story`.

Two phases. **With the user, once per feature:** Orient -> Define -> Decide -> Map -> Record. **Unattended, per story:** Branch -> Table -> Red -> Build -> Review -> Verify -> Pull request -> Merge -> Log, then `next-story` picks the next one.

## Principles

* **Working software over documentation.** No documents beyond the feature log, ADRs, `AGENTS.md`, and any file `AGENTS.md` says to keep current; those are rewritten in the log commit.
* **Executable specifications.** Never write implementation code first. Two levels of acceptance test. Every criterion of a story has one, the agent writes it, and the story is complete when all of them pass. every feature has one, the user writes it, and the feature is complete when it passes.
* **Smallest valuable increment.** One vertical story proving the riskiest assumption.
* **Fixed authorship.** The agent proposes; the user confirms once, up front: the outcome, each architecture decision, the module map, and every story with its criteria. After that the agent runs each story alone. The pull request is where the user sees the story.
* **No fixed order.** `next-story` chooses the next story from what is ready when the last one merges. A bug, a finding or a forced decision can add a story. Adding one is a pause, never a silent change.

## Communication

Load [references/writing.md](references/writing.md) now.

* **Challenge bad ideas.** Offer the simpler alternative, then defer to the user's product vision.
* **Say when an instruction does not parse.** Name any story, criterion or constraint that is ambiguous, contradicts `AGENTS.md`, or asks for what the code cannot do, and stop the turn there. Never proceed on a guess.
* **One decision per turn** in the first phase. Put one choice to the user and wait.

## When to Pause

A pause stops the loop, states the question in one message, and waits. The loop resumes where it stopped. Pause on these and nothing else:

* **A new story is needed:** a bug in shipped work, a split after the builder fails twice, or a `Learned` fact that changes what gets built. Propose the story and what blocks it.
* **A decision is forced:** a `Deferred:` item this story needs, or an architecture decision not in the feature header. Section 1 runs for it.
* **A product decision a test row exposes** that no PRD or ADR records: a timezone, whether refunds count, what a limit is.
* **A criterion cannot be written as a test,** or contradicts `AGENTS.md`.
* **The merge.** The user merges every pull request.
* **The feature acceptance test passes with stories remaining.** The remaining stories may not be needed; the user cuts or keeps them.
* **The user writes the code.** When they have said they will implement this story themselves, the red commit lands and the loop waits for their diff.

## Orient

* **Load the charter.** Silently read `AGENTS.md`, the file the `orient` skill writes: purpose, users, non-goals, nouns, boundaries, commands, constraints. Fall back to `ARCHITECTURE.md`, then `README.md`. When none states a purpose, offer the `orient` skill once, then proceed.
* **Check the floor.** When `AGENTS.md` names no check command, names one that runs less than CI runs, the suite is red on main in CI, no mutation runner exists, or the log shows three `Not caught by` lines in its last ten entries, halt and offer the `harness` skill before the first story. When the interface the outcome names has no runner in the repo (a screen and no browser test), the first story adds the runner with one hardcoded acceptance test, hardcoding the rest; for a command, the entry point called in-process is the runner.
* **Read `docs/adr/`** before proposing a change to an existing boundary or constraint.
* **Read the PRD** if supplied, as raw material for the stories, never as a list of IDs to trace. Note its success metrics and non-goals. When the PRD is the user's own and states an outcome, non-goals and decisions, copy them into the feature header and cite them wherever a pause would re-ask them. When `AGENTS.md` names a per-change spec directory, the feature header and the entries go at the bottom of that change's spec; create no feature.md.
* **State the last story.** When the log has an entry, read it and tell the user in one line what the last merged story changed and why, from its `Done` line and the commit it points to. Ask nothing.
* **Read the log:** `docs/features/{slug}/feature.md`, or the tracker epic `AGENTS.md` names (load [references/tracker.md](references/tracker.md) then). Slug matches the issue key or the `feature/{slug}` branch.
* **Carry the `Learned` lines forward.** Before starting the next story, read every `Learned` and `Not caught by` line in the log, whole, and every ADR the feature header's `Decided:` line lists. Where one bears on the story, cite it in the pull request's `Assumes:` line or in the build prompt's NON-NEGOTIABLE block. Where one changes what gets built, pause.

## 0. Define

Run the `feature` skill with the user before anything else. It returns the outcome, the problem, the non-goals, and the stories and spikes with what blocks each. It writes each story with the `story` skill, which holds every rule for acceptance criteria. A criterion that cannot be written as a test goes back to `story`. In one-story mode, run only `story` on the named story when the feature header already exists. A project that does not exist yet goes to `greenfield`.

Choose the slug: the issue key when `AGENTS.md` names a tracker, else a kebab-case name for the outcome. Create the branch `feature/{slug}` from main. Every story gets its own branch `story/{slug}/{n}-{short-name}` from the feature branch, and merges back into it; the feature branch merges into main when the feature header's story list is empty. The prefixes differ because git stores refs as paths, so `feature/{slug}` and `feature/{slug}/1-x` cannot both exist.

| Unknown is about | Settled by |
|---|---|
| Whether it is possible | `spike` |
| Whether anyone wants the output | story, then observe it in use |
| Whether the layers connect | walking skeleton story: the thinnest path through every layer, everything else hardcoded |
| Which of two approaches | `spike` both, timeboxed |
| What the existing system actually does | read the data, not the code |

### Spike only when blocked

* **At PRD read:** an assumption whose falsity changes *what* gets built, not *how*.
* **In the loop:** the acceptance criterion or a test row cannot be written for want of a fact about the world: a throughput number, a library's real behaviour, what an API returns.

Do not spike when a story answers it as fast, when the question is a product decision (pause), or when there is no falsifiable answer.

Run the `spike` skill. It writes its findings into this slug's log as the spike entry of section 9. The code is deleted, not offered for keeping; record the deletion in the log. When an edit-time hook blocks a spike edit, work in a directory outside the hook's paths, such as the session scratchpad.

## 1. Decide

Architecture decisions are put to the user one per message, with the alternatives and the tradeoff, and the agent waits. Each answer is written with the `adr` skill before the next decision is asked and before any code that depends on it: `docs/adr/architecture/` when it outlives the feature, `docs/adr/{slug}/` when it does not. The user may answer "defer"; a deferred decision goes on the feature header under `Deferred:` with the story that will force it.

* **Before the first story.** Read [references/decisions.md](references/decisions.md) before proposing any story; it lists, per kind of system, the decisions that are expensive to reverse. Walk its "before the first story" list for this system's kind. For each item the outcome touches, state in chat what the code already settles, with the file that settles it, and put the rest to the user one at a time; `Decided:` in the feature header lists only the ADRs. No stories until every item is decided, deferred, or stated as settled.
* **At every story start.** Read `Deferred:` and the "when a story forces it" list. When this story is the first to need one (the first cache, the first queue, the first second service, the first payment call), pause, put that decision to the user, write the ADR, then continue.
* **Ask before any smaller choice a later story inherits,** at the same moment: a port, address or schedule, a file or wire format, a name that becomes a domain noun. One message, alternatives and tradeoff, then wait.
* **Decide everything below that line alone,** and list each one under `Decided alone:` in the review's Done block, with what was chosen, why, and the tradeoff.
* **Suggest an architectural change only when the current design obstructs the implementation.**

The `adr` skill still fires on its own triggers mid-story. An assumption a recorded decision depends on goes in that ADR's `What it doesn't buy` section.

## 2. Map

Propose the shape of this feature's code in one table, and stop. The user edits it in one turn; a row not changed is accepted.

```text
| Module | Owns | Depends on | Pattern |
|---|---|---|---|
| <name, in the domain's nouns> | <the one thing it is responsible for> | <modules it may import, or "nothing"> | <only where one is chosen: composite, queue, hexagonal, ...> |
```

* **Only the modules the outcome touches.** Existing ones are stated from the code, with the directory. New ones are proposed.
* **Dependencies point one way.** A cycle in the table is a finding, not a row.
* **Contract first at a shared boundary.** Where a module on the map is called by another team, another service or another repository, write the executable contract (OpenAPI, Protobuf, strict interface types) and assert it in a test before any code sits behind it.
* **Pattern is optional.** Fill it where the user has a preference or a decision in section 1 fixes it. Leave it blank otherwise; the builder picks the simplest thing that passes the tests.
* **Write it into `AGENTS.md`** under the codebase map, in the log commit of the first story. Until then it lives only in the chat and the first build prompt. Where the `harness` skill has wired contracts, add each "depends on" line there, so a reversed dependency fails the build.
* **Every build prompt cites it:** the module this story's code lives in, its pattern, and its allowed dependencies, under NON-NEGOTIABLE.

This is not a design document. It has no sequence diagrams, no schemas, no endpoints; those come out of the tests, story by story.

## 3. Record

* **Promote into a criterion anything encoding an ADR,** so how a recorded decision was interpreted is never discovered by reading generated code.
* **Defer infrastructure** not required to pass a story's test to a later story. Logging, retries and error handling enter when a story pulls them, after a run showed the need. When the user can name the moment they wanted a thing, it is story-pulled; when they can only say it is good practice, it is speculation.
* **Skip the first-story skeleton** when that pathway through every layer already exists and is proven.
* **A bug in the story under way is fixed now,** with no new story. A bug in shipped work is a pause: propose the story and its place. Its table is two rows, the failing test at the level the report describes, written before reading the code, then a unit test isolating the fault. Then grep every caller of the function about to change and fix at the point they all route through.

Write the result as the feature header at the top of the log, creating the file if absent. Commit the log, and keep it after the last story ships. The file has exactly one `## feature header` heading, above the first dated entry; rewrite it in place and never append a second. Keep it to one screen.

```text
# {slug}

## Feature
Outcome:   <the sentence from section 0>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <one checkable non-goal per line>
Decided:   <one ADR path per line>
Deferred:  <decision, and the story that forces it; omit when none>
feature acceptance test: <path, or "after story 1" when the interface the outcome names has no test runner yet>
Stories:    <remaining stories and spikes, numbered, each with its criteria and its blockers; "none" when done>
```

Nothing else goes in the feature header. What the code already settles is stated in chat when the decisions are walked and lives in the code; the map lives in `AGENTS.md`; pins go beside the `Learned` line they pin.

The log defaults to `docs/features/{slug}/feature.md`. When `AGENTS.md` Boundaries names a tracker ("Backlog: Jira project TAG"), load [references/tracker.md](references/tracker.md). Stories already on the board are read as the proposed stories.

### The feature acceptance test

The outcome sentence gets one acceptance test of its own, and the user writes it.

* **The agent names, the user writes.** State the file, the runner, and the Given/When/Then the test must assert: the outcome sentence in concrete values, through the interface the user actually uses. The user writes the body. When the user asks the agent to write it, write it; the lock below still applies once it is committed.
* **It lives in a `feature-acceptance` directory inside the repo's test tree,** the directory the harness denies to the agent. When the harness has no such deny, offer the `harness` skill to add it before the commit.
* **It is marked expected-to-fail, strictly,** in the framework's own way (pytest `xfail(strict=True)`, jest `test.failing`, or the nearest equivalent), so the suite stays green while it fails and goes red the moment it passes. That flip is the close-out signal. The user removes the marker at close-out; the agent never touches the file.
* **Commit it on its own on `feature/{slug}`** before the first story. When the interface the outcome names has no test runner yet, the first story adds the runner, and the user writes the feature acceptance test after that story merges; the feature header says "after story 1" until then.
* **Locked from the agent forever.** The red-commit guard clears at each merge; this file is denied for good. The agent never edits, moves, deletes, skips or re-marks it, in any phase, and no subagent does either. A wrong feature acceptance test is the user's to change. Before it is committed, run the `give-feedback` skill on it once.

## 4. Start the Story

Take the story the user named, or in epic mode the one `next-story` returns, and say which it is and why in one line. Rebase `feature/{slug}` on main, cut `story/{slug}/{n}-{short-name}` from it, and run the check command on the tree. Run the section 1 check for a forced decision, and the Orient rule for `Learned` lines.

* **Pin untested legacy before changing it.** When the code the story touches has no test of its current behaviour, write characterization tests asserting what it does today, bugs included, and commit them before the red commit. They are scaffolding: the review deletes any the accepted rows make redundant.
* **Introduce the seam first.** When legacy code offers no point to test through, this story adds the seam (an injected dependency, an extracted function, a wrapper) and changes no behaviour, and the story's behaviour becomes the next story. Where the old path resists a seam, build beside it and route to the new path, rather than editing in place.
* **Write the story header** for the pull request description, not for the user:

```text
Story:      <the story's title>
Criteria:   <the story's Given/When/Then criteria, verbatim>
Assumes:    <one line per fact the story rests on that was read from a document or not checked, with how it was checked before the build; omit when every fact was read from the code>
```

* **Generate the table.** Run the `test-table` skill against the story's criteria and the code. Apply its cut rules in this session; the accepted table is the one the review holds the build to. A row that exposes a product decision no PRD or ADR records is a pause. Skip the table, the build subagent and the review subagent only when nobody is harmed and nothing a person reads is wrong before a `git revert` lands: copy, layout, a log line nobody operates from, a dev-only tool. Such a story is one acceptance test committed red, the check command, and the commit; say so in the pull request description.

```text
Tests:      The table.
Not now:    What a reader would expect here that is deferred, and to which story. Omit when empty.
```

## 5. Red

* **Write every accepted row as a failing test,** acceptance test first, new rows in a new test file.
* **Run the tests.** A row that passes before the build, or fails for a reason other than the missing behaviour, means the code does not do what the story assumes; read it before going on.
* **Delete or rewrite every existing test that asserts behaviour this story removes,** in the same commit and listed in its message.
* **Commit the red tests as their own commit,** with the criteria and the accepted table verbatim in the message. Where the harness installed the test guard, record the hash with `git config agile.redCommit <hash>`; the guard refuses edits to those files until the merge clears it. Change no accepted row after this commit.

When a turn-end hook blocks the red run because the tests name symbols that do not exist yet, add the symbols as stubs whose only body raises. The types pass and the tests still fail on behaviour.

## 6. Build

Read [references/build-prompt.md](references/build-prompt.md) once the red commit has landed; it holds the prompt's format. Issue one instruction to a subagent from it. The builder makes the accepted rows pass and may add tests for cases the table missed, listing each one and why. It never rewrites an accepted row.

Run the tests and the check command in this session after the builder returns. The check command is the one `AGENTS.md` names; the `harness` skill commits one, and when none exists, run the linter, the type checker and the tests. A red check is a red story.

When the builder reports red on any row, or touched anything outside its paths, do not debug the attempt. Reset the tree to the red commit and reissue the prompt with the one new fact under NON-NEGOTIABLE. Twice, then the story is too big: pause and propose the split as new stories.

**When the user has said they will write the code themselves,** issue no build prompt. The accepted rows are already red; the user writes the code until they are green. Then run the `give-feedback` skill on their diff before section 7.

## 7. Review and Verify

Run the `review` skill in a subagent in the worktree, given the diff, the red commit, the check command and the build prompt's NON-NEGOTIABLE block, and nothing from this session's chat. Correctness, subtraction, scars, then refactor while green. Commit before the refactor and again after it.

Then verify the whole feature, not the story. Rebase the story branch on `feature/{slug}`, run the full suite and the check command, and run the story's acceptance tests through the interface each names (the one the user actually uses: the screen, the API, the command), against the running system where its Level says so. Every earlier acceptance test runs here too, and the feature acceptance test runs under its expected-to-fail marker. A red anywhere is a red story: reset to the red commit and reissue the build, as in section 6.

The review returns its Done block: Correctness, Subtraction, Scars, Refactor, Decided alone, Gate. Never open a pull request without the block.

## 8. Pull Request and Merge

Open the pull request from the story branch into `feature/{slug}`, and write its description with the `merge-request` skill, which holds the format. Its `Why` comes from the feature header, its criteria are the story's verbatim, its `Assumes` comes from the story header, and the accepted table, `Not now:` and the review's Done block go in the collapsed section. Apply the writing rules in [references/writing.md](references/writing.md).

Tag the pull request, its tests and its commits with the story's issue key when a tracker exists, e.g. `[PAY-1420]`. Where the repo has no remote, the same description is the merge commit message and the user merges locally.

Then wait for the merge. The agent never merges. When the harness can poll the pull request's state, poll it and continue on merged. When it cannot, end the turn with the pull request link and resume when the user says it is merged. After the merge: delete the story branch, clear the red-commit guard, and go to section 9.

## 9. Log and Next

* **Make the last commit the log,** on `feature/{slug}`: rewrite the feature header in place (drop the shipped story), append the entry below, and rewrite `AGENTS.md` if the story added a noun, crossed a new boundary, turned a non-goal into a goal, or is the first story (the map). One commit. A split or new story the story exposed is a pause before this commit.
* **Flag** only when the feature, once merged to main, exposes user-visible behaviour a later feature completes, or when backing it out needs more than a `git revert`. Name the story that removes the flag in the feature header's `Stories:` list.
* **Deploy from main, by a command in the repo.** A `deploy` script or task target, committed with the story that first needs it. Never from the working tree, never from a branch, never by commands that live only in chat.
* **Exercise the rollback once** before anything a `git revert` cannot undo: a backfill, a migration, a bulk send.
* **Then run `next-story`** and start the story it returns at section 4, without asking. In one-story mode, stop here. When nothing is ready, pause and show its report.
* **Close out** when the feature header's story list is empty: ask the user to remove the feature acceptance test's expected-to-fail marker, run the suite, and go no further while it is red; then promote every `Learned` line to a test, an ADR or an `AGENTS.md` line, write the pin beside each, rebase `feature/{slug}` on main and run the check command, then open the pull request into main with the feature header and every entry's `Done` and `Observed` lines as its body. The user merges it. Prompt the user to observe each signal once deployed. Delete the feature branch, close the epic, keep the log file.

```text
## <date> — <story name>
- Done: <what shipped, one line>
- Learned: **<mechanism, one sentence>**; <the test, ADR or AGENTS.md line that pins it, or "not pinned">
- Not caught by: <bugs only: the gap, and the rule, row or hook now closing it>
- Observed: <seen <date>, what was seen, one line; appended when seen>
```

Every line is optional except `Done`. One line per finding; repeat `Learned`. Nothing else goes in the entry. A finding that needs more than a line is an ADR: write it, leave the path. A `Learned` line marked "not pinned" is promoted or dropped at close-out; none survives the feature. `Not caught by` is mandatory for a bug: name the gap in the harness or the test table and close it in the same story, or hand it to the `harness` skill. Never edit or delete an entry beyond appending its `Observed` line. A spike's entry is titled `spike: <the question>`; the `spike` skill writes it, and its every line is a `Learned` line.

## Working in a Team

* **One slug, one feature branch, one log file. One story, one story branch, one session.** Two stories never share a branch. Parallel work is parallel slugs, each with its own feature header; the shared backlog is the tracker `AGENTS.md` names.
* **Rebase the story branch on `feature/{slug}` before the red commit and again before the review,** and the feature branch on main before each story starts and before its own merge. Run the check command on the rebased tree.
* **Edit `AGENTS.md` and `docs/adr/architecture/` only in the log commit, after the rebase.** An architecture ADR is written the moment the decision is made, as `adr` says; in the first phase that is its own commit on `feature/{slug}`, and mid-story it rides the log commit.
* **The red-commit guard is local git config**, per clone. It never travels with the branch.
* **The harness is the repo's, not the developer's.** Hooks, rules, contracts and the check command are committed; nothing the loop depends on lives in one person's settings.

## When the Loop Is Not Working

When a feature header is precise about internals and silent about the user's day, or the suite is green and the user is still unhappy, read [references/failure-modes.md](references/failure-modes.md).
