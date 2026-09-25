---
name: deliver
description: "Use this skill before touching any file on every request to add, change, remove or fix behaviour in a system that already has an application: a feature, a bug, a chore, a refactor, or a complaint about how it behaves. Use it on: 'I want to add a feature', 'add X', 'implement X', 'fix the bug where X', 'X is broken', 'wire X to Y', 'refactor X', 'build story X', 'work through this epic', 'implement this prd', 'pick up where we left off'. Use it even when the change looks small enough to just do. Sizes each request as no behaviour change, trivial, one story or several, then runs it: agrees the outcome, first decisions, module map and stories, then runs each story unattended through setup, build and review subagents to a pull request into main, and for an epic keeps going until every story is merged or cut. Not for a project with no application (`greenfield`), throwaway code (`spike`), checks, hooks or rules (`guardrails`, `make-rule`), or AGENTS.md (`orient`)."
license: MIT
compatibility: any-agent
metadata:
  version: "11.0.0"
---
# Deliver

## Size the request first

When the request names a story in an open feature, run that story (section 4) and stop after its merge. When it names an epic or hands over a PRD, it is several stories. Otherwise, write the request's outcome in one sentence and list the steps a person takes, and size it from those, never by whether it is called a bug, a chore or a feature. Write no criteria until the size is known, so a request that turns out to be several stories gets its criteria one story at a time.

| Size | Test | Path |
|---|---|---|
| No behaviour change | A refactor, a dependency bump, a rename: nothing a person sees or a caller receives changes | Section "Change without new behaviour". No criteria and no red commit. |
| Trivial | Nobody is harmed and nothing a person reads is wrong before a `git revert` lands: copy, layout, colour, a log line nobody operates from, a dev-only tool | One criterion from `story`, then one acceptance test committed red, the check command and the commit, on a story branch with a pull request. No test plan, build subagent or review subagent. |
| One story | One change a person can see, in one workflow step and one variation, with nothing unknown that changes what gets built | Section 4. Skip the feature header, the decision walk, the map and the feature acceptance test. The log entry goes in `docs/delivery/{slug}.md` under a slug for the change, with no header. |
| Several stories | More than one step or variation, an unknown whose answer changes what gets built, or a PRD or epic | Section 0 onward. The loop runs every story, choosing each next one with `next-story`. |

A bug is sized like any request. Its outcome is the behaviour the person should have seen, and its first criterion is the reproduction, which `story` writes.

Say the size and the reason in the first message. The user can move the request to another size. When a one-story request's criteria cross more than one step or variation, or exceed the number of criteria per story `AGENTS.md` states, it is several stories: run `story-map` on it. When `AGENTS.md` states no number, ask the user once and record it under its constraints as "A story has at most <n> acceptance criteria."

## Change without new behaviour

For a refactor or any change that alters no behaviour. Cut `story/{slug}/0-{short-name}` from main and run the full suite, which must be green. When the code to change has no test of its current behaviour, commit characterization tests first. Make the change as a mechanical tool run where one exists: the language's refactoring tool, a codemod or a script. Run the full suite again, green, with no existing test changed except for a rename the tool made. Run the `review-build` skill in a subagent, whose correctness pass checks that no test changed its assertion. Write a log entry with a `Done` line, then open a pull request whose criteria section says "No behaviour change" and lists the tests that prove it. The user merges.

Two phases. **With the user, once per feature:** Orient -> Define -> Decide -> Map -> Record. **Per story, unattended:** Setup -> Red -> Build -> Review -> Verify -> Log -> Pull request, then the user merges. Setup, build and review each run in a subagent. For an epic the loop runs until every story is merged or cut, starting each ready story as soon as its blockers merge. Every story merges into main.

## Principles

* **Working software over documentation.** No documents beyond the feature log, ADRs, `AGENTS.md`, and any file `AGENTS.md` says to keep current; those are rewritten in the log commit.
* **Executable specifications.** Never write implementation code first. Two levels of acceptance test. Every criterion of a story has one, the agent writes it, and the story is complete when all of them pass. Every feature has one, the user writes it, and the feature is complete when it passes.
* **Detail just in time.** The agent proposes and the user confirms, up front, the outcome, the decisions the first story needs, the module map and the story list. Each story's criteria are written when that story starts, using what the earlier stories taught, and the user sees them in its pull request.
* **Park, never stop.** A question about one story parks that story, and the loop moves to another ready story. The loop waits for the user only when nothing else can move, and then asks every parked question in one message.
* **Keep the main session small.** The main session holds the feature header, the log, and what each subagent returns. It never reads a full diff. Where the agent cannot start subagents, run each step inline and say so once.
* **The user accepts running software.** Every pull request says how to try the story on its branch.
* **Small releases.** Each story merges into main and can deploy. A story that exposes half a feature ships behind a flag.

## Communication

Load [references/writing.md](references/writing.md) now.

* **Challenge bad ideas.** Offer the simpler alternative, then defer to the user's product vision.
* **Say when an instruction does not parse.** Name any story, criterion or constraint that is ambiguous, contradicts `AGENTS.md`, or asks for what the code cannot do, and park that story. Never proceed on a guess.

## When to Park and When to Ask

A parked story waits for one answer while the loop works on other ready stories. Park a story on these and nothing else:

* **An accepted row is wrong:** the builder reports a row it cannot satisfy, and the reason holds against the code. Queue the row, the reason and the corrected row. Once the user re-accepts it, clear the story's red-commit guard, land the corrected row as a new red commit, and re-add every red commit of this story to the guard.
* **This story removes behaviour a feature acceptance test asserts.** The user edits or retires that test, since the agent cannot touch it.
* **A decision is forced:** a `Deferred:` item this story needs, or an architecture decision not in the feature header. Section 1 runs for it.
* **A product decision a test row exposes** that no PRD or ADR records: a timezone, whether refunds count, what a limit is.
* **A criterion cannot be written as a test,** or contradicts `AGENTS.md`.
* **The live PRD contradicts a line of the feature header.** Re-read the PRD at every story's setup.
* **The feature acceptance test passes.** Verify reports it on its own (section 7). The user removes its expected-to-fail marker. With stories remaining, they may not be needed, and the user cuts or keeps them.
* **The user writes the code.** When they have said they will implement this story themselves, the red commit lands and the story waits for their diff.

Decide these without asking, and list each in the next message to the user:

* **A split.** When a story's criteria cross more than one workflow step or variation, or the builder fails twice on sound rows, split it with the `story-map` skill's splitting patterns, add the new stories to `Stories:`, and carry on.
* **A new story.** A bug in shipped work, or a `Learned` or `Observed` fact that changes what gets built, becomes a new story with its blockers on `Stories:`. The user can cut it.

Every message to the user, whether a pull request is ready or the loop is waiting, carries in one place: the parked questions; whether the last merged story deployed and what its signal showed, whose answer becomes its `Observed` line; every fifth merged story, which pause or check has cost time without catching anything, handed to the `make-rule` skill; and the splits, new stories and rules the loop decided alone.

The loop waits for the user only when no story is ready, no build is running, and a merge or a parked answer is what everything left needs.

## Orient

* **Load the charter.** Silently read `AGENTS.md`, the file the `orient` skill writes: purpose, users, non-goals, nouns, boundaries, commands, constraints. Fall back to `ARCHITECTURE.md`, then `README.md`. When none states a purpose, offer the `orient` skill once, then proceed.
* **Check the floor.** When `AGENTS.md` names no check command, names one that runs less than CI runs, the suite is red on main in CI, or the log shows three `Not caught by` lines in its last ten entries, halt and offer the `guardrails` skill before the first story. When only the mutation runner is missing, offer `guardrails` once. When the user declines, continue, and the review applies each mutation by hand. When the interface the outcome names has no runner in the repo (a screen and no browser test), the first story adds the runner with one hardcoded acceptance test, hardcoding the rest; for a command, the entry point called in-process is the runner.
* **Read `docs/adr/`** before proposing a change to an existing boundary or constraint.
* **Read the PRD** if supplied, as raw material for the stories, never as a list of IDs to trace. Note its success metrics and non-goals. Close-out checks the metrics. When the PRD is the user's own and states an outcome, non-goals and decisions, copy them into the feature header with the PRD section each came from, and cite them wherever a question would re-ask them. When `AGENTS.md` names a per-change spec directory, the feature header and the entries go at the bottom of that change's spec; create no file under `docs/delivery/`.
* **State the last story.** When the log has an entry, read it and tell the user in one line what the last merged story changed and why, from its `Done` line and the commit it points to. Ask nothing.
* **Find where the stories live.** Load [references/tracker.md](references/tracker.md) and run its first section. It reads the `Backlog:` line of `AGENTS.md`, or finds a tracker and records one. On a tracker the epic is the log; otherwise the log is `docs/delivery/{slug}.md`. The slug is the epic's key or the `story/{slug}/` branch prefix. A log at the old path `docs/features/{slug}/feature.md` is read the same way and moved to the new path with `git mv` in the next log commit.
* **Carry the `Learned` lines forward.** Before starting the next story, read every `Learned`, `Not caught by` and `Observed` line in the log, whole, and every ADR the feature header's `Decided:` line lists. Where one bears on the story, cite it in the pull request's `Assumes:` line or in the build prompt's NON-NEGOTIABLE block. Where one changes what gets built, add or change the story and say so in the next message.

## 0. Define

Run the `story-map` skill with the user before anything else. It retrieves or writes the shared understanding (outcome, problem, non-goals, success signal, constraints every story keeps) and drafts the steps a person takes, with candidate stories and spikes under each, their blockers, and the walking skeleton marked. Criteria are written with the `story` skill when each story starts (section 4). A project that does not exist yet goes to `greenfield`.

Choose the slug: the epic's key when the stories live on a tracker, else a kebab-case name for the outcome. Every story gets its own branch `story/{slug}/{n}-{short-name}` from main, and merges back into main. No feature branch exists.

### Spike only when blocked

* **At PRD read:** an assumption whose falsity changes *what* gets built, not *how*.
* **In the loop:** the acceptance criterion or a test row cannot be written for want of a fact about the world: a throughput number, a library's real behaviour, what an API returns.

Do not spike when a story answers it as fast, when the question is a product decision (park the story), or when there is no falsifiable answer. When the question is what the existing system actually does, read its data, not its code.

Run the `spike` skill. Its findings go into this slug's log as the spike entry of section 8, committed on `story/{slug}/{n}-spike-{short-name}` from main and opened as a pull request the user merges. A spike is done when that pull request merges. The spike code never enters that branch: it is deleted, and the log records the deletion. When an edit-time hook blocks a spike edit, work in a directory outside the hook's paths, such as the session scratchpad.

## 1. Decide

Architecture decisions are put to the user one per message, with the alternatives and the tradeoff, and the agent waits. Each answer is written with the `adr` skill before the next decision is asked and before any code that depends on it: `docs/adr/architecture/` when it outlives the feature, `docs/adr/{slug}/` when it does not. The user may answer "defer"; a deferred decision goes on the feature header under `Deferred:` with the story that will force it.

* **Before the first story.** List the decisions this system cannot cheaply reverse: any choice that touches the data's shape, the system's trust or consistency boundaries, or the hardware or platform target. For each one the outcome touches, state in chat what the code already settles, with the file that settles it. Put the rest to the user one at a time, and propose "defer" for each one the first story does not touch; the check at every story start raises it when a story needs it. `Decided:` in the feature header lists only ADR paths and PRD sections that record a decision. No stories until every item is decided, deferred, or stated as settled.
* **At every story start.** Read `Deferred:`. A choice swappable behind an interface, or affecting one story, waits until a story needs it. When this story is the first to need one (the first cache, the first queue, the first second service, the first payment call), park the story, put that decision to the user, write the ADR once answered, then continue.
* **Ask before any smaller choice a later story inherits,** at the same moment: a port, address or schedule, a file or wire format, a name that becomes a domain noun. One message, alternatives and tradeoff, then wait.
* **Decide everything below that line alone,** and list each one for the review to carry into `Decided alone:`, with what was chosen, why, and the tradeoff.
* **Suggest an architectural change only when the current design obstructs the implementation.**

An assumption a recorded decision depends on goes in that ADR's `What it doesn't buy` section.

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
* **Write it into `AGENTS.md`** under the codebase map, in the log commit of the first story. Until then it lives only in the chat and the first build prompt. Where the `guardrails` skill has wired contracts, add each "depends on" line there, so a reversed dependency fails the build.

This is not a design document. It has no sequence diagrams, no schemas, no endpoints; those come out of the tests, story by story.

## 3. Record

* **Promote into a criterion anything encoding an ADR,** so how a recorded decision was interpreted is never discovered by reading generated code.
* **Defer infrastructure** not required to pass a story's test to a later story. Logging, retries and error handling enter when a story pulls them, after a run showed the need. When the user can name the moment they wanted a thing, it is story-pulled; when they can only say it is good practice, it is speculation.
* **A bug in the story under way is fixed now,** with no new story. A bug in shipped work becomes a new story on `Stories:`, listed in the next message. Its table is two rows, the failing test at the level the report describes, written before reading the code, then a unit test isolating the fault. Then grep every caller of the function about to change and fix at the point they all route through.

Write the result as the feature header at the top of the log, creating the file if absent. Commit the log as the first commit on the first story's branch, and keep it after the last story ships. The file has at most one `## Feature` heading, above the first dated entry; rewrite it in place and never append a second. Keep it to one screen.

```text
# {slug}

## Feature
Outcome:   <the sentence from section 0>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <one checkable non-goal per line>
Success:   <the signal that shows the outcome happened>
Constraints: <one line per rule every story must keep true>
Context:   <one line per fact every story needs: environment, variables, URLs, test accounts, commands, and where each credential lives, never its value>
Steps:     <the steps the person takes, in order>
Decided:   <one ADR path per line, or a PRD path and section when the PRD records the decision and its rejected alternative>
Deferred:  <decision, and the story that forces it; omit when none>
feature acceptance test: <path, or "after story 1" when the interface the outcome names has no test runner yet>
Stories:    <every story and spike, each with its number, title, outcome line, "Blocked by:", and "[walking skeleton]" where marked. A cut story stays as "<n>. cut: <reason>". Numbers never change. This line is written once and edited only to add or cut a story: a story is done when its log entry exists, and a spike when its findings pull request has merged>
```

Nothing else goes in the feature header. What the code already settles is stated in chat when the decisions are walked and lives in the code; the map lives in `AGENTS.md`; pins go beside the `Learned` line they pin.

The feature header goes where [references/tracker.md](references/tracker.md) put the stories: the epic's description on a tracker, the top of `docs/delivery/{slug}.md` otherwise. Stories already on the board are read as the proposed stories.

### The feature acceptance test

The outcome sentence gets one acceptance test of its own, and the user writes it.

* **The agent names, the user writes.** State the file, the runner, and the Given/When/Then the test must assert: the outcome sentence in concrete values, through the interface the user actually uses. The user writes the body. When the user asks the agent to write it, write it; the lock below still applies once it is committed.
* **It lives in a `feature-acceptance` directory inside the repo's test tree,** the directory the harness denies to the agent. When the harness has no such deny, offer the `guardrails` skill to add it before the commit.
* **It is marked expected-to-fail, strictly,** in the framework's own way (pytest `xfail(strict=True)`, jest `test.failing`, or the nearest equivalent), so the suite stays green while it fails and goes red the moment it passes. That flip is the close-out signal. The user removes the marker at close-out; the agent never touches the file.
* **Commit it on its own on the first story's branch,** after the log and before the red commit. When the interface the outcome names has no test runner yet, the first story adds the runner, and the user writes the feature acceptance test after that story merges; the feature header says "after story 1" until then.
* **Locked from the agent for good,** unlike the red-commit guard, which clears at each merge. No subagent edits, moves, deletes, skips or re-marks it either. A wrong feature acceptance test is the user's to change. Before it is committed, run the `give-feedback` skill on it once.

## 4. Set Up the Story

Take the story the user named, the request sized above, or in epic mode each story `next-story` returns. Cut `story/{slug}/{n}-{short-name}` from main in its own worktree (`git worktree add` is one way), so stories can run side by side, and run the check command there. Run the section 1 check for a forced decision.

Issue one instruction to a setup subagent, given the story, the feature header, every `Learned` and `Observed` line, `AGENTS.md` and the worktree path. It runs the `story` skill for the criteria and the steps below through the red commit (section 5), and returns the criteria, the accepted table, the red commit's hash and anything it could not decide. Anything it could not decide parks the story. A criterion that cannot be written as a test goes back to `story`.

* **Decide the flag.** When this story, merged to main, exposes behaviour a later story completes, or backing it out needs more than a `git revert`, `story` writes the flag as criteria: with the flag off, the person sees today's behaviour. The story that completes the behaviour carries a criterion that removes the flag. Acceptance tests turn the flag on explicitly, and the flag-off criterion's test turns it off.
* **Do the proposed refactors this story touches.** Make each one its own commit on the story branch before the red commit, with the full suite green before and after. Write the commit beside that `Proposed refactor` line in the log.
* **Pin untested legacy before changing it.** When the code the story touches has no test of its current behaviour, write characterization tests asserting what it does today, bugs included, and commit them before the red commit. They are scaffolding: the review deletes any the accepted rows make redundant.
* **Introduce the seam first.** When legacy code offers no point to test through, add the seam (an injected dependency, an extracted function, a wrapper) as its own commit on this story's branch before the red commit. It changes no behaviour, and the full suite stays green before and after. Where the old path resists a seam, build beside it and route to the new path, rather than editing in place.
* **Hand the story's `Crossings` line to the `make-rule` skill.** It writes each rule on this story's branch, and the pull request lists them for the user.
* **Note each fact the story rests on** that was read from a document or not checked, and check it before the build. These become the pull request's `Assumes` lines.
* **Generate the table.** Run the `test-plan` skill against the story's criteria and the code. Apply its cut rules in the setup subagent; the accepted table is the one the review holds the build to. A row that exposes a product decision no PRD or ADR records parks the story. Skip the table, the build subagent and the review subagent only for the trivial size in the sizing table, and say so in the pull request description.

## 5. Red

* **Write every accepted row as a failing test,** acceptance test first, new rows in a new test file.
* **Run the tests.** A row that passes before the build, or fails for a reason other than the missing behaviour, means the code does not do what the story assumes; read it before going on.
* **Delete or rewrite every existing test that asserts behaviour this story removes,** in the same commit and listed in its message.
* **Commit the red tests as their own commit,** with the criteria and the accepted table verbatim in the message. Where `guardrails` installed the accepted-test guard, record the hash on the story's branch with `git config --add branch.<branch>.redCommit <hash>`; the guard refuses edits to the files of every recorded red commit until the merge clears them with `git config --unset-all branch.<branch>.redCommit`. When the installed guard reads only the older single key `agile.redCommit`, offer `guardrails` to update it, and until then run one story at a time and record the hash under `agile.redCommit`. Change no accepted row after this commit, except through a parked wrong row.

When a turn-end hook blocks the red run because the tests name symbols that do not exist yet, add the symbols as stubs whose only body raises. The types pass and the tests still fail on behaviour.

## 6. Build

Read [references/build-prompt.md](references/build-prompt.md) once the red commit has landed; it holds the prompt's format. Issue one instruction to a subagent from it. The builder makes the accepted rows pass and may add tests for cases the table missed, listing each one and why. It never rewrites an accepted row.

Run the tests and the check command after the builder returns, and read only their summary. The check command is the one `AGENTS.md` names; the `guardrails` skill commits one, and when none exists, run the linter, the type checker and the tests. A red check is a red story.

When the builder reports a row it cannot satisfy, check its reason against the code. When the reason holds, park the story for a wrong row. When the builder reports red on any row, or touched anything outside its paths, do not debug the attempt. Reset the tree to the red commit and reissue the prompt with the one new fact under NON-NEGOTIABLE. Twice red on rows that are sound, and the story is too big: split it (section "When to Park and When to Ask").

**When the user has said they will write the code themselves,** issue no build prompt. The accepted rows are already red; the user writes the code until they are green. Then run the `give-feedback` skill on their diff before section 7.

## 7. Review and Verify

Run the `review-build` skill in a subagent on the story branch, given the diff, the red commit, the check command, the build prompt's NON-NEGOTIABLE block and the builder's list of choices, and nothing from this session's chat. Commit before the review's refactor and again after it.

Then verify the whole feature, not the story. Rebase the story branch on main, run the full suite and the check command, and run the story's acceptance tests through the interface each names (the one the user actually uses: the screen, the API, the command), against the running system. Every earlier acceptance test runs here too. Run the feature acceptance test last and report it on its own. When it passes, its strict marker turns it red: that parks the story for a passing feature acceptance test, and is not a red story. A red anywhere else is a red story: reset to the red commit and reissue the build, as in section 6. When the full run takes longer than the time limit `AGENTS.md` states, say so in the next message to the user, since every later story adds to it.

Never open a pull request without the review's Done block.

## 8. Log and Pull Request

* **Make the last commit on the story branch the log:** append the entry below, and rewrite `AGENTS.md` if the story added a noun, crossed a new boundary, turned a non-goal into a goal, or is the first story (the map). One commit. Copy each `Proposed refactor:` line from the review's Done block into the entry unchanged, marked "open". A split or new story the story exposed goes on `Stories:` in this commit and in the pull request description.
* **Open the pull request from the story branch into main,** and write its description with the `merge-request` skill, which holds the format. Its `Why` comes from the feature header, or, when the request has none, from the story's `Outcome` and `Why` lines. Its criteria are the story's verbatim, each with its acceptance test's Given/When/Then shown beneath it. Its `Try it` is the command, URL or screen that shows the outcome criterion on the story branch. Its `Assumes` comes from the facts noted at story start. It lists any rule `make-rule` wrote on the branch. The edge-case rows, what is deferred and the review's Done block go in the collapsed section.
* **Tag the pull request, its tests and its commits** with the story's issue key when the stories live on a tracker, e.g. `[PAY-1420]`. Where the repo has no remote, the same description is the merge commit message and the user merges locally.

```text
## <date> — <story name>
- Done: <what shipped, one line>
- Learned: **<mechanism, one sentence>**; <the test, ADR or AGENTS.md line that pins it, or "not pinned">
- Not caught by: <bugs only: the gap, and the rule, row or hook now closing it>
- Proposed refactor: <files>; <the duplication or confusion it removes>; <the commit that did it, or "open">
- Observed: <seen <date>, what was seen, one line; appended when seen>
```

Every line is optional except `Done`. One line per finding; repeat `Learned`. Nothing else goes in the entry. A finding that needs more than a line is an ADR: write it, leave the path. A `Learned` line marked "not pinned" is promoted or dropped at close-out; none survives the feature. `Not caught by` is mandatory for a bug: name the gap in the checks `guardrails` set up or in the test table and close it in the same story, or hand it to the `guardrails` skill. Never edit or delete an entry, except to append its `Observed` line, to write a pin beside a `Learned` or `Proposed refactor` line, or to delete an unpinned line at close-out with the user's agreement. A spike's entry is titled `spike: <the question>`; the `spike` skill writes it, and its every line is a `Learned` line. Its `Dead ends` lines stay as a record and need no pin. Its `Open questions` lines are closed by a story or by the user's decision before close-out. Its `Outcome`, `Approach used` and `Quirks and surprises` lines are promoted or dropped at close-out like a "not pinned" line, and its `Decided alone` lines stay as a record.

## 9. Merge, Next and Close Out

* **Move on while the pull request waits.** Run `next-story` as soon as a pull request opens, and set up every ready story whose blockers have all merged, each in its own worktree, up to the number of stories at once `AGENTS.md` states. When it states none, ask the user once and record it there.
* **A story whose blocker is still in review waits for that merge.** Watch the blocker's pull request, and set the story up from the updated main once it merges.
* **Watch every open pull request.** The agent never merges. When the harness can poll a pull request's state, poll it; on merge, delete the story's branch and worktree and clear its red-commit guard, then run `next-story`. When it cannot poll, end the turn with every open pull request's link and the parked questions, and resume when the user says which merged.
* **Deploy from main, by a command in the repo.** A `deploy` script or task target, committed with the story that first needs it. Never from the working tree, never from a branch, never by commands that live only in chat.
* **Exercise the rollback once** before anything a `git revert` cannot undo: a backfill, a migration, a bulk send.
* **Stop after the merge** when the request was trivial, one story, one named story, or a change without new behaviour. For an epic, keep going until every story in `Stories:` has a log entry or is cut. When nothing is ready and nothing is building, show `next-story`'s report with the parked questions and wait.
* **Close out** when every story in `Stories:` has a log entry or is cut. Confirm the feature acceptance test's marker is gone and the suite is green, and go no further while it is red. On one last branch from main, promote or drop each unpinned `Learned` line: turn it into a test, an ADR or an `AGENTS.md` line and write the pin beside it, or delete it with the user's agreement. Put each `Proposed refactor` line still marked "open" to the user: do it on this branch, or drop it. Then open the pull request. Ask the user whether the `Success` signal moved, and propose a follow-up story or a cut from the answer. Ask again which pause or check in this feature cost time without catching anything, and hand the answer to the `make-rule` skill to loosen or delete it. Prompt the user to observe each signal once deployed. Close the epic and keep the log file.

## Working in a Team

* **One slug, one log file. One story, one branch, one worktree.** Two stories never share a branch. Each story's log commit appends only its own entry, so when two pull requests both touch the log, rebase the later one and keep both entries. The shared backlog is the tracker on the `Backlog:` line of `AGENTS.md`.

## When the Loop Is Not Working

When every story shipped and nothing about the user's day changed, check whether the scope was chosen or inherited. A spike's boundary may have become the project's boundary, or the work that delivers the outcome may sit behind a repository edge with no story. The sign is a feature header precise about internals and silent about the user's day.
