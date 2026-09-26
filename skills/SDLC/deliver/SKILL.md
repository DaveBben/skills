---
name: deliver
description: "Use this skill before touching any file on every request to add, change, remove or fix behaviour in a system that already has an application, to pick the next story, or to describe a branch for review. Use it on: 'add X', 'implement X', 'fix the bug where X', 'X is broken', 'refactor X', 'add tests for X', 'build story X', 'work through this epic', 'implement this prd', 'pick up where we left off', 'what should I pick up next', 'what is ready', 'open a pull request', 'write the PR description', 'write the MR body'. Use it even when the change looks small. Sizes each request, then runs each story through criteria, setup, build and review subagents to a pull request into main, pausing for the user to confirm criteria and asking each question as it arises. For an epic it picks each ready story until all are merged or cut. Not for a repository with no application (`architecture`), planning without building (`define-work`), throwaway code (`spike`), checks or rules (`guardrails`), or AGENTS.md (`orient`)."
license: MIT
compatibility: any-agent
metadata:
  version: "13.2.0"
---
# Deliver

Load [references/writing.md](references/writing.md) before the first reply.

Two phases. **With the user, once per feature:** Orient -> Define -> Architecture -> Record. **Per story:** Criteria -> the user confirms -> Setup and red commit -> Build -> Review -> Verify -> Log -> Pull request, then the user merges. For an epic the loop runs until every story is merged or cut, starting each ready story as soon as its blockers merge. Every story merges into main.

## Principles

* **Working software over documentation.** No documents beyond the feature log, ADRs, `AGENTS.md`, and any file `AGENTS.md` says to keep current; those are rewritten in the log commit.
* **Executable specifications.** Never write implementation code first. Two levels of acceptance test. Every criterion of a story has one, the agent writes it, and the story is complete when all of them pass. Every feature has one, the user writes it, and the feature is complete when it passes.
* **Detail just in time.** The agent proposes and the user confirms, up front, the outcome, the story list, the architecture tables and the decisions the first story needs. Each story's criteria are written when that story starts, using what the earlier stories taught, and the user confirms them before any test is written.
* **Park, never stop.** A question about one story parks that story, and the loop moves to another ready story (section "When to Park and When to Ask").
* **The user accepts running software.** Every pull request says how to try the story on its branch.
* **Small releases.** Each story merges into main and can deploy. A story that exposes half a feature ships behind a flag.

## Subagents

* **Every step and every skill the loop runs goes to a subagent** that returns its result and its questions. This session asks the user those questions and reissues the subagent with the answers. `define-work` and `architecture` run in this session, since they are conversations with the user.
* **Inside the per-story loop, this session holds the feature header, the log's entries and what each subagent returns.** It never reads a diff, a test file, source, an ADR or the PRD; the subagents read those and return the lines it needs.
* **Where the agent cannot start subagents,** run each step inline, one story at a time, without asking; run the review in a fresh session where the harness allows one; say so once.

## Communication

* **Challenge bad ideas.** Offer the simpler alternative, then defer to the user's product vision.
* **Say when an instruction does not parse.** Name any story, criterion or constraint that is ambiguous, contradicts `AGENTS.md`, or asks for what the code cannot do, and park that story. Never proceed on a guess.

Every message to the user, whether a pull request is ready or the loop is waiting, carries in one place: every question still waiting for an answer; whether the last merged story deployed and what its signal showed, whose answer becomes its `Observed` line; every fifth merged story, which pause or check has cost time without catching anything, handed to the `guardrails` skill; and the splits, new stories and rules the loop decided alone.

## Before sizing

These three requests skip sizing.

**Describe an existing branch.** When the request is only for a pull request description, of a branch built here or elsewhere, load [references/pull-request.md](references/pull-request.md). A subagent reads the branch's diff against its target, the commits, and any ticket the branch name or commits cite, and returns the description's lines. Write the description and stop.

**What should I pick up next.** When several features are open, ask which one. A subagent runs the first section of [references/tracker.md](references/tracker.md) to find where the stories live, then [references/next.md](references/next.md) as a request from the user, and returns the report.

**Pick up where we left off.** Run Orient. When several features are open, ask which one. Read the feature header and `Deferred:`, and list the story worktrees (`git worktree list`) and the open story pull requests. Skip Define and Architecture. Restart each story worktree at the step its state shows:

| State | Restart at |
|---|---|
| A pull request is open | Section 8, watching it |
| A parked question | Ask it again |
| A log commit and no pull request | Section 7, the pull request |
| A red commit and no log commit | Section 5, with a NON-NEGOTIABLE block a setup subagent rebuilds from the red commit |
| No red commit | Section 4, setup |
| A spike branch | The spike subagent (section 0) |

Then continue at section 3.

## Orient

Every other request runs Orient first.

* **Load the charter.** Silently read `AGENTS.md`, the file the `orient` skill writes: purpose, users, non-goals, nouns, boundaries, commands, constraints. Fall back to `ARCHITECTURE.md`, then `README.md`. When none states a purpose, offer the `orient` skill once, then proceed.
* **Check the floor.** When `AGENTS.md` names no check command, names one that runs less than CI runs, the suite is red on main in CI, or the log shows three `Not caught by` lines in its last ten entries, halt and offer the `guardrails` skill before the first story. When it records no red-commit command, say that failing tests cannot be committed and start no story until `guardrails` adds it. When only the mutation runner is missing, offer `guardrails` once; when the user declines, continue, and the review applies each mutation by hand. When the interface the outcome names has no runner in the repo (a screen and no browser test), the first story adds the runner with one hardcoded acceptance test, hardcoding the rest; for a command, the entry point called in-process is the runner.
* **A PRD** goes to `define-work` as raw material; close-out checks its success metrics. When `AGENTS.md` names a per-change spec directory, the feature header and the entries go at the bottom of that change's spec; create no file under `docs/delivery/`.
* **State the last story.** When the log has an entry, tell the user in one line what the last merged story changed and why, from its `Done` line. Ask nothing.
* **Find where the stories live.** Load [references/tracker.md](references/tracker.md) and run its first section. It reads the `Backlog:` line of `AGENTS.md`, or finds a tracker and records one. On a tracker the epic is the log; otherwise the log is `docs/delivery/{slug}.md`. The slug is the epic's key or the `story/{slug}/` branch prefix. A log at the old path `docs/features/{slug}/feature.md` is read the same way and moved to the new path with `git mv` in the next log commit.

## Size the request

When the request names a story in an open feature, run that story (section 4) and stop after its merge. When it names an epic or hands over a PRD, it is several stories. Otherwise, write the request's outcome in one sentence and list the steps a person takes, and size it from those, never by whether it is called a bug, a chore or a feature. Write no criteria until the size is known, so a request that turns out to be several stories gets its criteria one story at a time.

| Size | Test | Path |
|---|---|---|
| No behaviour change | A refactor, a dependency bump, a rename, or tests added for behaviour that already exists: nothing a person sees or a caller receives changes | Section "Change without new behaviour". No criteria and no red commit. |
| Trivial | Nobody is harmed and nothing a person reads is wrong before a `git revert` lands: copy, layout, colour, a log line nobody operates from, a dev-only tool | One criterion from `story` in its trivial mode, confirmed by the user. Then one subagent commits one acceptance test red with the red-commit command `AGENTS.md` records, makes it pass, runs the check command and commits, on a story branch with a pull request. No test plan, build subagent, review subagent or Done block. |
| One story | One change a person can see, in one workflow step and one variation, with nothing unknown that changes what gets built | Section 4. Skip the feature header, the `architecture` skill and the feature acceptance test. The log entry goes in `docs/delivery/{slug}.md` under a slug for the change, with no header. |
| Several stories | More than one step or variation, an unknown whose answer changes what gets built, or a PRD or epic | Section 0 onward. The loop runs every story, choosing each next one by section 3. |

A bug is sized like any request. Its outcome is the behaviour the person should have seen, and its first criterion is the reproduction, which `story` writes. A flaky test is a bug whose reproduction is the test failing on repeated runs of unchanged code. A red CI run is a bug report, and its failing step's output is the report.

Say the size and the reason in the first message. The user can move the request to another size. When a one-story request's criteria cross more than one step or variation, or exceed the number of criteria per story `AGENTS.md` states, it is several stories: split it by the split rule in section "When to Park and When to Ask". When `AGENTS.md` states no number, ask the user once and record it under its constraints as "A story has at most <n> acceptance criteria."

## Change without new behaviour

For a refactor or any change that alters no behaviour. The slug is a short kebab-case name for the change. Run the whole path in one subagent, which returns the log entry's `Done` line and the pull request description's lines. It cuts `story/{slug}/0-{short-name}` from main and runs the full suite, which must be green. To add tests for existing behaviour, it runs the `story` skill's route for existing behaviour; the new tests pass on the current code, and nothing else changes. When the code to change has no test of its current behaviour, it commits characterization tests first. It makes the change as a mechanical tool run where one exists: the language's refactoring tool, a codemod or a script. It runs the full suite again, green, with no existing test changed except for a rename the tool made, and runs the `reviewing` skill on the code built, whose correctness pass checks that no test changed its assertion. It writes the log entry by [references/log.md](references/log.md). Open the pull request by [references/pull-request.md](references/pull-request.md), with a criteria section that says "No behaviour change" and lists the tests that prove it. The user merges.

## 0. Define

Run the `define-work` skill with the user before anything else. It retrieves or writes the shared understanding (outcome, problem, non-goals, success signal, constraints every story keeps, the repositories the work changes) and drafts the steps a person takes, with candidate stories and spikes under each, their blockers, and the walking skeleton marked. Criteria are written with the `story` skill when each story starts (section 4). A repository with no application yet belongs to the `architecture` skill, which runs `define-work`, decides each repository's language, runs `greenfield` once per new repository, and then hands back to this skill at section 2.

Choose the slug: the epic's key when the stories live on a tracker, else a kebab-case name for the outcome. Every story gets its own branch `story/{slug}/{n}-{short-name}` from main, and merges back into main. No feature branch exists.

### Spike only when blocked

* **At PRD read:** an assumption whose falsity changes *what* gets built, not *how*.
* **In the loop:** the acceptance criterion or a test row cannot be written for want of a fact about the world: a throughput number, a library's real behaviour, what an API returns.

Do not spike when a story answers it as fast, when the question is a product decision (park the story), or when there is no falsifiable answer. When the question is what the existing system actually does, read its data, not its code.

Frame the spike's question, finish line and timebox with the user. Then run the `spike` skill in a subagent with that frame, the feature's slug and the spike's number on `Stories:`; it commits its findings where the `spike` skill says and returns what its subagent mode lists. Put its decision table to the user and run the `architecture` skill to record each row marked `record`. When the spike reports that its findings contradict a decided ADR, park the stories that depend on it and run the `architecture` skill's path for deciding one open item; the new ADR names the old one on its `Supersedes:` line and replaces its path on `Decided:`. When a spike is done is defined in [references/next.md](references/next.md).

## 1. Architecture

For a request sized as several stories, or a project with no application yet, run the `architecture` skill with the user after Define. It lists the crossings the walking skeleton makes and spikes the untried ones, asks the load, response-time, downtime and data-volume numbers, maps processes, modules and flows, and walks each expensive decision to one of four states: decided, deferred, waiting on a spike, or settled by the code. No story starts until every item it needs is in one of those states.

* **At every story start,** read `Deferred:`. A choice swappable behind an interface, or affecting one story, waits until a story needs it. When this story is the first to need one (the first cache, the first queue, the first second service, the first payment call), or an item waits on a spike that is done, park the story and run the `architecture` skill's path for deciding one open item.
* **A decision the build needs that nobody recorded** parks the story the same way.

## 2. Record

Load [references/feature-header.md](references/feature-header.md). It holds the rules the record keeps, the feature header's format, the plan branch, and the feature acceptance test the user writes. Write the header where [references/tracker.md](references/tracker.md) puts the stories.

## 3. Pick the next story

A subagent runs [references/next.md](references/next.md) at every pick and returns its report: which stories are ready, in rank order, and what blocks the rest.

## 4. Set up the story

Take the story the user named, the request sized above, or each story section 3 picks. Cut `story/{slug}/{n}-{short-name}` from main, where `{n}` is the story's number on `Stories:` or its issue key, in its own worktree (`git worktree add` is one way), so stories can run side by side, and run the check command there. Run the section 1 check for a forced decision.

**A story that spans repositories.** Cut a branch with the same name in each repository the story changes, taken from the feature header's `Repositories:` line; for a one-story request with no header, from the request, or ask. Open one pull request per repository. Order them by parallel change (Martin Fowler, "ParallelChange", https://martinfowler.com/bliki/ParallelChange.html), which splits an incompatible interface change into expand, migrate and contract:

1. **Expand.** The pull request in the repository being called goes first. Its contract test lands first. The new form sits beside the old one, so existing callers keep working, and it merges and deploys on its own.
2. **Migrate.** The pull request in the calling repository merges after the first has merged.
3. **Contract.** When an old form exists, removing it is a later story on `Stories:`, blocked by the story that migrated the last caller.

Each pull request links the others. Setup, build, review and verify run once per repository, in expand-then-migrate order. The feature log, the ADRs and the feature acceptance test live in the first repository on `Repositories:`. The log commit goes on that repository's branch, which merges after every other pull request of the story. When the first repository's own change is the expand step, or the story does not change the first repository, the log goes in a log-only pull request there after the others merge. The story is done when all of its pull requests have merged, in every repository.

**Criteria.** Issue one instruction to a criteria subagent, given the story, the feature header, `AGENTS.md` and the worktree path. It runs the `story` skill without writing to the tracker. It reads every `Learned`, `Not caught by` and `Observed` line in the log, every ADR on `Decided:`, and the live PRD. It returns the criteria, the card text, the lines that bear on the story as `Assumes:` lines and NON-NEGOTIABLE facts, any contradiction with the PRD, and every question it could not decide. Where a returned line changes what gets built, add or change the story and say so. When this story, merged to main, exposes behaviour a later story completes, or backing it out needs more than a `git revert`, the criteria include a flag: with the flag off, the person sees today's behaviour, and the story that completes the behaviour carries a criterion that removes the flag. Acceptance tests turn the flag on explicitly, and the flag-off criterion's test turns it off. Show the user the criteria in full and park the story until the user confirms or edits them. When the user rejects them outright, reissue the criteria subagent with the objection; after a second rejection, put the story's outcome line back to the user. Where the stories live on a tracker, write the returned card text to the story's issue once confirmed.

**Setup and red commit.** Then issue one instruction to a setup subagent, given the confirmed criteria, the same inputs and [references/setup.md](references/setup.md). It runs every step there through the red commit and returns what that reference lists. A criterion that cannot be written as a test goes back to `story`, and the user confirms the rewritten criteria.

## 5. Build

Read [references/build-prompt.md](references/build-prompt.md) once the red commit has landed; it holds the prompt's format. Fill it from what the setup subagent returned, and issue one instruction to a subagent from it. The builder makes the accepted rows pass and may add tests for cases the table missed, listing each one and why. It never rewrites an accepted row.

Run the tests and the check command after the builder returns, and read only their summary. The check command is the one `AGENTS.md` names; the `guardrails` skill commits one, and when none exists, run the linter, the type checker and the tests. A red check is a red story.

When the builder returns a question about a choice a person would see, ask the user as soon as control returns and park the story. Once answered, reissue the prompt on the branch as it stands, with the answer under NON-NEGOTIABLE. A builder that stopped to ask is not reset, even with rows still red.

When the builder reports a row it cannot satisfy, it cites the file and line that stop it; a subagent checks that reason against the code. When the reason holds, park the story for a wrong row. When the builder reports red on any row, or touched anything outside its paths, do not debug the attempt. Reset the tree to the latest red commit and reissue the prompt with the one new fact under NON-NEGOTIABLE. Twice red on sound rows is a split.

**When the user has said they will write the code themselves,** issue no build prompt. The accepted rows are already red; the user writes the code until they are green. Then run the `reviewing` skill in a subagent on their branch, as work the user made. It returns the feedback points and a `Changed:` line per new function, module or branch, with what it is for and its file. Section 6 then runs only its verify step, whose passing rows fill the criteria table, and the pull request carries the feedback points in place of the Done block.

## 6. Review and Verify

Run the `reviewing` skill in a subagent on the story branch, for code the agent built, given the branch name, the red commit's hash, the check command, the build prompt's NON-NEGOTIABLE block and the builder's list of choices, and nothing from this session's chat. It returns its Done block, whose lines fill the pull request's criteria table and What changed section. Hand each rule on its `Rules:` line to the `guardrails` skill in a subagent.

Then verify the whole feature, not the story, in a subagent given the branch name and every red commit's hash. It rebases the story branch on main, re-records every red commit's new hash in the guard, and returns the latest. It diffs the accepted test files against the red commit; any change is a red story. It runs the full suite and the check command, and the story's acceptance tests through the interface each names (the one the user actually uses: the screen, the API, the command), against the running system, with every earlier acceptance test. It runs the feature acceptance test last and returns its result and failure message on their own, and pass or fail for the rest.

* **The feature acceptance test passes:** its strict marker turns it red. That parks the story, and is not a red story.
* **Its failure message changed since the last story:** say so.
* **Only the test-run time limit `AGENTS.md` states failed:** report it on its own and hand it to the `guardrails` skill. It is not a red story.
* **A red anywhere else is a red story:** reset to the latest red commit and reissue the build, as in section 5.

Never open a pull request without the review's Done block, or the feedback points for code the user wrote. The trivial size needs neither.

## 7. Log and Pull Request

* **Make the last commit on the story branch the log.** Load [references/log.md](references/log.md) for the entry's format and rules.
* **Open the pull request from the story branch into main,** and write its description by [references/pull-request.md](references/pull-request.md). Its `Why` comes from the feature header, or, when the request has none, from the story's `Outcome` and `Why` lines. Its `Try it` is the command, URL or screen that shows the outcome criterion on the story branch. Its `Assumes` comes from the criteria and setup subagents. With a remote but no tool that opens pull requests, push the branch, print the description, and ask the user to open it and paste its link.
* **Tag the pull request, its tests and its commits** with the story's issue key when the stories live on a tracker, e.g. `[PAY-1420]`. Where the repo has no remote, the same description is the merge commit message and the user merges locally.

## 8. Merge, Next and Close Out

* **Move on while the pull request waits.** Run section 3 as soon as a pull request opens, and set up every ready story whose blockers have all merged, each in its own worktree, up to the number of stories at once `AGENTS.md` states. When it states none, ask the user once and record it there.
* **A story whose blocker is still in review waits for that merge.** Watch the blocker's pull request, and set the story up from the updated main once it merges.
* **Watch every open pull request.** The agent never merges. When the harness can poll a pull request's state, poll it. On merge, delete the story's branch and worktree, clear its red-commit guard (`git config --unset-all` on the branch's key and on `agile.redCommit`), and on a tracker set the story Done with its log comment as the resolution; then run section 3. A pull request closed without merging: ask the user to reopen it or cut the story. On a cut, clean up the same way and mark it cut on `Stories:`; when an expand change already merged elsewhere, add a story to remove the new form. When it cannot poll, end the turn with every open pull request's link and the parked questions, and resume when the user says which merged.
* **Deploy from main, by a command in the repo.** A `deploy` script or task target, committed with the story that first needs it. Never from the working tree, never from a branch, never by commands that live only in chat.
* **Exercise the rollback once** before anything a `git revert` cannot undo: a backfill, a migration, a bulk send.
* **Stop after the merge** when the request was trivial, one story, one named story, or a change without new behaviour. For an epic, keep going until every story in `Stories:` is done or cut. When nothing is ready and nothing is building, show section 3's report with the parked questions and wait.
* **Close out** when every story in `Stories:` is done or cut. Confirm the feature acceptance test's marker is gone and the suite is green, and go no further while it is red. When it still fails with every story done, give the user its failure message and propose the story that would make it pass. On one last branch from main, promote or drop each unpinned `Learned` line: turn it into a test, an ADR or an `AGENTS.md` line and write the pin beside it, or delete it with the user's agreement. Put each `Proposed refactor` line still marked "open" to the user: do it on this branch, or drop it. Then open the pull request. Ask the user whether the `Success` signal moved, and propose a follow-up story or a cut from the answer. Ask again which pause or check in this feature cost time without catching anything, and hand the answer to the `guardrails` skill to loosen or delete it. Prompt the user to observe each signal once deployed. Close the epic and keep the log file.

## When to Park and When to Ask

A parked story waits for one answer while the loop works on other ready stories. Write each parked question, and criteria waiting for confirmation, as a comment on the story's issue, or as a `Parked: <story>: <question>` line at the end of the feature log, committed on main or on the plan branch before it merges, so a later session finds it. The loop waits for the user only when no story is ready, no build is running, and a merge or a parked answer is what everything left needs.

Park a story on these and nothing else:

* **Its criteria wait for confirmation.** Every story parks once, after `story` writes its criteria (section 4).
* **The builder asks a question** about a choice a person would see (section 5).
* **An accepted row is wrong:** the builder reports a row it cannot satisfy and the reason holds against the code, or a refactor renames a file an accepted test names. Queue the row, the reason and the corrected row. Once the user re-accepts it, clear the story's red-commit guard, land the corrected row as a new red commit, and re-add every red commit of this story to the guard.
* **This story removes behaviour a feature acceptance test asserts.** The user edits or retires that test, since the agent cannot touch it.
* **A decision is forced:** a `Deferred:` item this story needs, or an architecture decision not in the feature header. Section 1 runs for it.
* **A product decision a test row exposes** that no PRD or ADR records: a timezone, whether refunds count, what a limit is.
* **A criterion cannot be written as a test,** or contradicts `AGENTS.md`.
* **The live PRD contradicts a line of the feature header,** as the criteria subagent reports.
* **The feature acceptance test is not written yet,** unless the feature header says "after story 1". The first story's red commit waits for the user to write it.
* **The feature acceptance test passes.** Verify reports it on its own (section 6). The user removes its expected-to-fail marker. With stories remaining, they may not be needed, and the user cuts or keeps them.
* **The user writes the code.** When they have said they will implement this story themselves, the red commit lands and the story waits for their diff.

Decide these without asking, and list each in the next message to the user:

* **A split.** When a story's criteria cross more than one workflow step or variation, `story` reports it is several stories, or the builder is red twice on sound rows (counting every red in build and verify), run the `define-work` skill's splitting patterns in a subagent. Add the new stories to `Stories:`, mark the original `cut: split into <n>, <m>`, delete its branch and worktree, and carry on.
* **A new story.** A bug in shipped work, or a `Learned` or `Observed` fact that changes what gets built, becomes a new story with its blockers on `Stories:`. The user can cut it.

## Working in a Team

* **One slug, one log file. One story, one branch and one worktree per repository it changes.** Two stories never share a branch. Each story's log commit appends only its own entry, so when two pull requests both touch the log, rebase the later one and keep both entries. The shared backlog is the tracker on the `Backlog:` line of `AGENTS.md`.

## When the Loop Is Not Working

When every story shipped and nothing about the user's day changed, check whether the scope was chosen or inherited. A spike's boundary may have become the project's boundary, or the work that delivers the outcome may sit behind a repository edge with no story. The sign is a feature header precise about internals and silent about the user's day.
