---
name: deliver
description: "Use this skill before touching any file on every request to add, change, remove or fix behaviour in a system that already has an application, to pick the next story, or to describe a branch for review. Use it on: 'add X', 'implement X', 'fix the bug where X', 'X is broken', 'refactor X', 'add tests for X', 'build story X', 'work through this epic', 'implement this prd', 'pick up where we left off', 'what should I pick up next', 'what is ready', 'open a pull request', 'write the PR description', 'write the MR body'. Use it even when the change looks small. Sizes each request, then runs each story through criteria, setup, build and review subagents to a pull request into main, pausing for the user to confirm criteria and asking each question as it arises. For an epic it picks each ready story until all are merged or cut. Not for a repository with no application (`architecture`), planning without building (`define`), throwaway code (`spike`), checks or rules (`guardrails`), or AGENTS.md (`orient`)."
license: MIT
compatibility: any-agent
metadata:
  version: "14.3.0"
---
# Deliver

Load [references/writing.md](references/writing.md) before the first reply.

Two phases. **With the user, once per feature:** Orient -> Define -> Architecture -> Record. **Per story:** Criteria -> the user confirms -> Setup and red commit -> Build -> Review -> Verify -> Log -> Pull request, then the user merges. For an epic the loop runs until every story is merged or cut, starting each ready story as soon as its blockers merge. Every story merges into main.

## Principles

* **Working software over documentation.** No documents beyond the tracker's issues, ADRs, `AGENTS.md`, and any file `AGENTS.md` says to keep current.
* **Executable specifications.** Never write implementation code first. Two levels of acceptance test. Every criterion of a story has one, the agent writes it, and the story is complete when all of them pass. Every feature has one, the user writes it, and the feature is complete when it passes.

## Subagents

* **Every step and every skill the loop runs goes to a subagent** that returns its result and its questions in at most ten lines. Give it the feature header lines it needs by name, and grep results in place of whole files. This session asks the user those questions and reissues the subagent with the answers. `define` and `architecture` run in this session, since they are conversations with the user.
* **Inside the per-story loop, this session holds the feature header, the last ten log comments and what each subagent returns.** It never reads a diff, a test file, source, an ADR or the PRD; the subagents read those and return the lines it needs.
* **The holdout is the user's alone.** Only the verify subagent gets the feature header's `Holdout:` line. Nothing reads the holdout directory, and no holdout result reaches a builder.
* **Where the agent cannot start subagents,** run each step inline, one story at a time, without asking; run the review in a fresh session where the harness allows one; say so once.

## Communication

* **Challenge bad ideas.** Offer the simpler alternative, then defer to the user's product vision.
* **Say when an instruction does not parse.** Name any story, criterion or constraint that is ambiguous, contradicts `AGENTS.md`, or asks for what the code cannot do, and park that story. Never proceed on a guess.

Every message to the user, whether a pull request is ready or the loop is waiting, carries in one place: every question still waiting for an answer; whether the last merged story deployed and what its signal showed, whose answer becomes its `Observed` line; when it moved the wrong way past the `Success` line's noise band, the code that emits the signal, for the user to read; every fifth merged story, which pause or check has cost time without catching anything, and how often reading code changed anything, handed to the `guardrails` skill; and the splits, new stories and rules the loop decided alone.

## Before sizing

These three requests skip sizing.

**Describe an existing branch.** When the request is only for a pull request description, of a branch built here or elsewhere, load [references/pull-request.md](references/pull-request.md). A subagent reads the branch's diff against its target, the commits, and any ticket the branch name or commits cite, and returns the description's lines. Write the description and stop.

**What should I pick up next.** When several features are open, ask which one. A subagent finds where the stories live, as Orient does, runs [references/next.md](references/next.md) as a request from the user, and returns the report.

**Pick up where we left off.** Load [references/resume.md](references/resume.md).

## Orient

Every other request runs Orient first.

* **Load the charter.** Silently read `AGENTS.md`, the file the `orient` skill writes: purpose, users, non-goals, nouns, boundaries, commands, constraints. Fall back to `ARCHITECTURE.md`, then `README.md`. When none states a purpose, offer the `orient` skill once, then proceed.
* **Check the floor.** When `AGENTS.md` names no check command, names one that runs less than CI runs, the suite is red on main in CI, or the log comments of the feature's last ten closed stories show three `Not caught by` lines, halt and offer the `guardrails` skill before the first story. When it records no red-commit command, say that failing tests cannot be committed and start no story until `guardrails` adds it. When only the mutation runner is missing, offer `guardrails` once; when the user declines, continue, and the review applies each mutation by hand. When `CODEOWNERS` has an `# owner reads:` section, the user reads code only when a signal fires (section 7), and a missing mutation runner halts the loop instead. When the interface the outcome names has no runner in the repo (a screen and no browser test), the first story adds the runner with one hardcoded acceptance test, hardcoding the rest; for a command, the entry point called in-process is the runner.
* **A PRD** goes to `define` as raw material; close-out checks its success metrics.
* **State the last story.** When the feature has a closed story, tell the user in one line what the last merged story changed and why, from its log comment's `Done` line. Ask nothing.
* **Find the tracker.** Load [references/tracker.md](references/tracker.md) and run its first section; with no tracker set up, it halts and helps the user connect one. The slug is the epic's key, or the issue's key for a one-story request.

## Size the request

When the request names a story in an open feature, run that story (section 4) and stop after its merge. When it names an epic or hands over a PRD, it is several stories. Otherwise, write the request's outcome in one sentence and list the steps a person takes, and size it from those, never by whether it is called a bug, a chore or a feature. Write no criteria until the size is known, so a request that turns out to be several stories gets its criteria one story at a time.

| Size | Test | Path |
|---|---|---|
| No behaviour change | A refactor, a dependency bump, a rename, or tests added for behaviour that already exists: nothing a person sees or a caller receives changes | One subagent runs [references/no-behaviour-change.md](references/no-behaviour-change.md). No criteria and no red commit. Open its pull request by [references/pull-request.md](references/pull-request.md); it is the record, linked to an issue when one exists. |
| Trivial | Nobody is harmed and nothing a person reads is wrong before a `git revert` lands: copy, layout, colour, a log line nobody operates from, a dev-only tool | One criterion from `define` in its trivial mode, confirmed by the user. Then one subagent commits one acceptance test red with the red-commit command `AGENTS.md` records, makes it pass, runs the check command and commits, on a story branch with a pull request. No test plan, build subagent, review subagent or Done block. The pull request is the record, linked to an issue when one exists. |
| One story | One change a person can see, in one workflow step and one variation, with nothing unknown that changes what gets built | Section 4 of [references/loop.md](references/loop.md). One issue with no epic, whose comments are its log. Skip the feature header, the `architecture` skill and the feature acceptance test. |
| Several stories | More than one step or variation, an unknown whose answer changes what gets built, or a PRD or epic | Section 0 onward of [references/loop.md](references/loop.md). The loop runs every story, choosing each next one by its section 3. |

A bug is sized like any request. Its outcome is the behaviour the person should have seen, and its first criterion is the reproduction, which `define` writes. A flaky test is a bug whose reproduction is the test failing on repeated runs of unchanged code. A red CI run is a bug report, and its failing step's output is the report.

Say the size and the reason in the first message. The user can move the request to another size. When a one-story request's criteria cross more than one step or variation, or exceed the number of criteria per story `AGENTS.md` states, it is several stories: split it by the split rule in section "When to Park and When to Ask". When `AGENTS.md` states no number, ask the user once and record it under its constraints as "A story has at most <n> acceptance criteria."

## 0 to 6. The loop

Sections 0 to 6 (Define, Architecture, Record, Pick, Set up, Build, Review and Verify) are in [references/loop.md](references/loop.md). Load it for a request sized as one story or several.

## 7. Log and Pull Request

* **Write the story's log comment.** Load [references/log.md](references/log.md) for the entry's format and rules.
* **Open the pull request from the story branch into main,** and have a subagent write its description by [references/pull-request.md](references/pull-request.md) from the Done block file and `exceptions.txt`. Its `Why` comes from the feature header, or, when the request has none, from the story's `Outcome` and `Why` lines. Its `Try it` is the command, URL or screen that shows the outcome criterion on the story branch. Its `Assumes` comes from the criteria and setup subagents. With a remote but no tool that opens pull requests, push the branch, print the description, and ask the user to open it and paste its link.
* **Tag the pull request, its tests and its commits** with the story's issue key, e.g. `[PAY-1420]`. Where `guardrails` installed its `issue-key` commit hook, the hook tags each commit on a branch `story.sh start` cut. Where the repo has no remote, the merge commit message is the description's Why, criteria table and Try it, and the user merges locally.

## 8. Merge and Next

* **Move on while the pull request waits.** Run section 3 as soon as a pull request opens, and set up every ready story whose blockers have all merged, each in its own worktree, up to the number of stories at once `AGENTS.md` states. When it states none, ask the user once and record it there.
* **A story whose blocker is still in review waits for that merge.** Watch the blocker's pull request, and set the story up from the updated main once it merges.
* **Watch every open pull request.** The agent never merges. When the harness can poll a pull request's state, poll it. On merge, run [scripts/story.sh](scripts/story.sh) `close <branch>`, which deletes the story's branch and worktree and clears its red-commit guard, and set the story Done with its log comment as the resolution; then run section 3. A pull request closed without merging: ask the user to reopen it or cut the story. On a cut, clean up the same way and close the issue as cut; when an expand change already merged elsewhere, add a story to remove the new form. When it cannot poll, end the turn with every open pull request's link and the parked questions, and resume when the user says which merged.
* **Deploy from main, by a command in the repo.** A `deploy` script or task target, committed with the story that first needs it. Never from the working tree, never from a branch, never by commands that live only in chat.
* **Exercise the rollback once** before anything a `git revert` cannot undo: a backfill, a migration, a bulk send.
* **Stop after the merge** when the request was trivial, one story, one named story, or a change without new behaviour. For an epic, keep going until every child issue is done or cut. When nothing is ready and nothing is building, show section 3's report with the parked questions and wait.
* **Close out** when every child issue is done or cut, by the close-out section of [references/feature-header.md](references/feature-header.md).

## When to Park and When to Ask

A parked story waits for one answer while the loop works on other ready stories. When a turn ends with a parked question unanswered, write it as a comment on the story's issue starting `Parked:`, so a later session finds it; for criteria waiting for confirmation, the comment says only `Parked: criteria`. Edit or delete it once answered where the tracker allows. The loop waits for the user only when no story is ready, no build is running, and a merge or a parked answer is what everything left needs.

Park a story on these and nothing else:

* **Its criteria wait for confirmation.** Every story parks once, after `define` writes its criteria (section 4).
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
* **The holdout line names a failure or a leak** (section 6). The user reads its report and hands over a bug report or changes the scenario.

Decide these without asking, and list each in the next message to the user:

* **A split.** When a story's criteria cross more than one workflow step or variation, `define` reports it is several stories, or the builder is red twice on sound rows (counting every red in build and verify), run the `define` skill's splitting patterns in a subagent. Create the new stories as children of the epic, close the original as `cut: split into <keys>`, run `story.sh close` on its branch, and carry on.
* **A new story.** A bug in shipped work, or a `Learned` or `Observed` fact that changes what gets built, becomes a new child issue with its blocking links. The user can cut it.

## Working in a Team

* **One epic per feature. One story, one branch and one worktree per repository it changes.** Two stories never share a branch. Each story writes only its own comments. The shared backlog is the tracker on the `Backlog:` line of `AGENTS.md`.
