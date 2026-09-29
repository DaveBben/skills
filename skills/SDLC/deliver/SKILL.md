---
name: deliver
description: "Use this skill before touching any file on a request to add, change, fix or remove behaviour in code that exists, or to turn an idea, a PRD or an epic into stories. Use it on: 'add X', 'fix the bug where X', 'X is broken', 'refactor X', 'build story X', 'I have an idea', 'break this epic down', 'write the acceptance criteria', 'work through this epic', 'what should I pick up next', 'pick up where we left off', 'write the PR description'. Use it even when the change looks small. Maps the stories, then takes each one through agreed criteria, failing tests, a build, a review and a pull request into main."
license: MIT
compatibility: any-agent
metadata:
  version: "17.0.0"
---
# Deliver

Take a request from its outcome to merged pull requests. Every behaviour change starts as failing tests committed before any code, and the user agrees each story's criteria before anything leaves the machine.

## Words used here

* **Tracker:** the project tracker the `Backlog:` line of `AGENTS.md` names, reached by the methods listed under it. An epic per feature, its stories and spikes as child issues with blocking links, each issue's comments as its log. The **slug** is the epic's key, or the issue's key for a one-story request.
* **Feature header:** the epic's description, in the named lines [references/epic.md](references/epic.md) gives. A one-story request has none; its issue's description stands in.
* **Story:** a change a person outside the system can observe, in one workflow step and one variation.
* **Criterion:** one Given/When/Then statement of what a person sees. It **records a product choice** when it holds a number, a rule a person could argue with, or what happens at a boundary the requirements leave open, or when it touches a data shape, a trust boundary, an interface another team calls, a value a person sees, personal or health data, or a record lost or half stored.
* **Red commit:** the commit holding a story's failing tests and stubs only, made before any code, by the red-commit command `AGENTS.md` records when it records one.
* **Check command:** the one command `AGENTS.md` names that runs every check.
* **Feature acceptance test:** the one test the user writes for a feature's outcome, in a `feature-acceptance` directory the agent never edits, marked strictly expected-to-fail until the feature is whole.
* **ADR:** an architecture decision record under `docs/adr/`, holding a decision, its reasons and the alternatives rejected.
* **Parked:** a question written on a story's issue as a comment starting `Parked:`. The story keeps going up to the step that needs the answer. **The waiting question** is the oldest parked question only the user can answer that the loop cannot move past; a `Parked: ask <person>` question is not one, and neither are criteria still being built on.
* **[scripts/story.sh](scripts/story.sh):** the git steps of a story. Run it with no arguments for its usage.

## Talking to the user

Sort every question, including each one a subagent returns, before it reaches the user:

* **A fact the agent can reach** (what a table holds, whether a secret exists, what a route returns, what CI runs): look it up in a read-only subagent given the one question and the paths, and use the answer. Ask only when no tool reaches it, and say where it looked.
* **A fact only a named person knows:** write `Parked: ask <person>: <question>` on the story, tell the user once whom to ask, and work on what the answer does not block. After one failed run against another team's system, do the same with that team's owner.
* **A technical choice a `git revert` undoes, that no person sees and no later story inherits:** decide it and list it among the choices decided alone.
* **A repository setting** (criteria per story, stories at once): use the default here and record it in `AGENTS.md`, else on the feature header.
* **The loop's own next step** (write criteria, run a review, start the next ready story, push a story the user confirmed): take it.
* **Product intent, or a choice expensive to reverse:** ask the user.

Then ask:

* **One question per message:** ask only the waiting question, and hold every other until it is answered. Open with one line naming the repository and the story or feature in plain words. Use the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion), recommended option first, each option with its consequence in one sentence.
* **An answer that fits no option** ("yes" to an either/or) gets the question again, naming the options.
* **Never restate a question.** It lives on its story as a `Parked:` comment. When a subagent returns nothing the user must act on, send nothing.
* **A command the user must run** reports every step's result in one run. When the harness blocks a command that reads a secret or health data, or that force-pushes, say so and ask whether the user wants to run it.
* **Where things stand.** Open with the `Outcome:` line and one clause per repository saying its part. Then one line per open story (key, what it does in plain words, and building, in review, or which question it is parked on), each `Parked: ask <person>` with whom to ask, what threatens the `Target:` date, and the waiting question.
* **Overload.** When the user says they are overloaded, send one message: where things stand without the waiting question, opening with "Nothing needs you now" when no question waits for the user. Ask the waiting question in the reply to their next message.

The message that reports an opened or merged pull request also carries whether the last merged story deployed and what its `Success` signal showed, and the splits, new stories and choices the loop decided alone. A signal that moved the wrong way past its noise band goes in the next message, whatever it reports.

## Subagents

Setup, build, review, refute and the description each run in a subagent given one prompt file from `references/`, the feature header lines it names, and paths in place of file contents. It returns at most ten lines. This session reads the tracker and `AGENTS.md` itself, and never a diff, a test or source. Where the harness has no subagents, run each step inline, one story at a time, and say so once.

## Start

* **Read `AGENTS.md`** in each repository the work touches, and find the tracker by section 1 of [references/tracker.md](references/tracker.md). When there is no check command, use what CI runs, else the test command the README gives; when there is no red-commit command, commit red tests with plain `git commit`. Record both as decided alone. When the user declines red commits, the tests land in the build's first commit and `story.sh red` records that commit. Mention once that the `guardrails` skill sets these up properly; ask nothing.
* **Resume** when `story.sh status`, run from each main checkout, prints a story, or a story carries a `Parked:` comment: read those comments and the epic's open pull requests, send where things stand, and restart each story at the step its line prints. Take the slug from a printed branch name (`story/<slug>/...`); with none, search the tracker for the user's open epics.
* **Find work already begun.** Look up each story's issue key among open branches and pull requests on the code host; skip this when the host is unreachable. A pull request the user authored is theirs: add a worktree for its branch (`git worktree add <path> <branch>`), run `story.sh adopt <key>` there, and skip `story.sh start` for that story. When the branch is checked out in a checkout the agent did not create, park `Parked: switch <checkout> off <branch>` for the user. An adopted story has no red commit: the setup subagent keeps its existing tests as characterization rows, commits the new failing rows, and runs `story.sh red` on that commit. Another person's: the story waits for it. Never touch uncommitted changes in a checkout the agent did not create. Say each in one line.
* **For several stories, clear the way once.** Ask one question: may the loop push branches named `story/{slug}/*` and adopted ones, rebase them with `--force-with-lease`, open and update their pull requests, and write to the epic's issues, for this feature. Record the answer on the header's `Context:` line. Anything wider (other pull requests, other branches) is asked when it comes up, naming exactly what it covers. Check from the repository and CI config that each repository on `Repositories:` deploys to production from main by a command in the repository, and that the feature acceptance test can run without manual steps; tell the user each gap once, as a story or as a risk.

## Size the request

Write the outcome in one sentence and the steps a person takes, and size from those, whatever the request calls itself.

| Size | Test | Path |
|---|---|---|
| No behaviour change | A refactor, a dependency bump, a rename, or tests for behaviour that exists | Cut `story/{slug}/0-<name>`, commit characterization tests first where none pin the code, change it by a tool or codemod where one exists, run the suite green with no assertion changed, and open the pull request by [references/pull-request.md](references/pull-request.md). |
| Trivial | Nobody is harmed before a `git revert` lands: copy, layout, a dev-only tool | One outcome criterion, shown to the user; one red test, the fix, the check command, a pull request. |
| One story | One step and one variation, nothing unknown | "Each story" below, on one issue whose comments are its log. |
| Several stories | More than one step or variation, an unknown that changes what gets built, a PRD or an epic | [references/epic.md](references/epic.md) for the feature header, the story map and the feature acceptance test, then "Each story" for every story. |

A bug is sized like any request; its first criterion is the reproduction. A red CI run is a bug report. These stop early: a request only to break work down runs `epic.md` to the confirmed map; a request only for criteria runs sections 1 and 2 of [references/criteria.md](references/criteria.md) in a subagent with no worktree and shows the card; a request only for a pull request description runs `pull-request.md` on that branch; "what next" runs the pick section of `epic.md`. When a decision that costs more than a day to reverse is open (a library, a data shape, a trust boundary, a new repository), or a fact nobody can supply without building (a library's real behaviour, a throughput number), run the `architecture` skill with the user before the story that needs it.

A story's product-choice criteria stay within the number `AGENTS.md` states. When it states none, use 8 and record "A story has at most 8 acceptance criteria that record a product choice."

## Each story

1. **Set up.** In each repository the story changes, run `story.sh start {slug} {key} {short-name}` (the short name is two or three words of its title), finding each clone from `Repositories:` and cloning one that is missing. For an epic's first story, the user's feature acceptance test is committed on the branch first, or the story parks. A subagent with [references/criteria.md](references/criteria.md) writes the criteria, the test table, the failing tests and the red commit, and writes the card to `card.md` in the worktree's git directory, and returns its path, the criteria and its questions. When it proposes a split instead, run `story.sh close` on the branch and split. When the story changes more than one repository, the called repository's pull request merges first.
2. **Show the criteria** in one message: each criterion that records a product choice, in the user's terms, then the number of other criteria, which stay on the card, accepted unless the user cuts them. On the tracker, write them under "PROPOSED, NOT AGREED" and add `Parked: criteria`. Do not wait.
3. **Build.** A subagent with [references/build.md](references/build.md). Skip it when no row is red. A question about something a person sees is parked. A red row or a touch outside its paths: reset to the latest red commit and reissue with the one new fact. Red twice on sound rows is a split. When the user writes the code, wait for their diff instead.
4. **Review.** In each repository's worktree, delete any old `done-block.md` from its git directory, then a fresh subagent with [references/review.md](references/review.md), given the card, the interfaces its criteria name, the branch, the red commit, the check command, the story's permitted paths and the header's `Decided:` line, and nothing from this chat. Read the `Findings:` and `Questions:` rows of `done-block.md`; a question about behaviour no criterion states parks the story as a product decision. A blocking finding that no red attack test already shows goes to a second fresh subagent with [references/refute.md](references/refute.md). Each confirmed finding, and each `unsettled` one's settling test, becomes a red row: the setup subagent adds a test that fails on it as a new red commit (`story.sh red`), then build and review run again. A second round of confirmed blocking findings on one story is a split, or a question to the user.
5. **Verify.** Run `story.sh verify <check command>` in the worktree. A red result is a red story. Run the feature acceptance test last and report its failure message when it changed. When it passes, park the story: the user removes its expected-to-fail marker.
6. **Confirm and open.** A subagent drafts the description by [references/pull-request.md](references/pull-request.md), with any installed skill for writing in the user's voice. Then one message: the criteria changes since step 2 and why, the review's result, and the description, which goes out as shown unless the user edits it. One question: do you confirm these criteria? On yes, run `story.sh confirm`, write the confirmed card to the issue in place of the proposed one, delete `Parked: criteria`, push, and open the pull request with the issue key in the title, e.g. `[PAY-1420]`. The push guard, where `guardrails` installed it, refuses the push until `confirm` has run. An edit is a wrong row (below).
7. **Log.** Write this comment on the issue:

```text
- Done: <what shipped, one line>
- Learned: **<mechanism, one sentence>**; <the test, ADR or AGENTS.md line that pins it, or "not pinned">
- Not caught by: <bugs only: the gap, and the rule or row now closing it>
- Proposed refactor: <files>; <the duplication it removes>; open
- Observed: <seen <date>, <signal> = <value>; appended when seen>
```

Every line but `Done` is optional; a finding that needs more than a line is an ADR.

8. **Review comments.** One refute subagent per pull request checks every new reviewer comment that claims how the code behaves against the code. A confirmed defect becomes a red row as in step 4. Then draft the reply with any installed skill for writing in the user's voice, run the refute subagent on every claim in it about how code, a service or data behaves, given every repository the text names, and show the user the reply. The user posts it, or says to.

## Park, and decide alone

Park a story on: its criteria before the push; a builder question about what a person sees; a wrong row; a product decision a test row exposes that no PRD or ADR records; a criterion that cannot be written as a test; a `Deferred:` decision the story needs, decided with the `architecture` skill; the feature acceptance test not yet written, for the first story; a change to behaviour that test asserts, since only the user edits it; that test passing.

A **wrong row** is one the builder cannot satisfy for a reason that holds against the code, or one the user edits. Once the user accepts the correction, run `story.sh unred`, commit the corrected test as a new red commit, and run `story.sh red <hash>` for it and for every earlier red commit of the story.

Decide these alone and list them in the next pull request message: a split, by the patterns in `epic.md`, closing the original as `cut: split into <keys>`; a new story for a bug in shipped work or a `Learned` fact that changes what gets built; a rebase conflict resolved outside test files.

## Merge and next

* **Stories at once.** Set up the next ready story when a pull request opens, up to the number `AGENTS.md` states, else 1. A story counts from setup until its pull request opens. Branch only from main: a story whose blocker is unmerged, or waits on another person's branch, waits for that merge.
* **Watch this feature's open pull requests** for merges, failing checks, review comments and conflicts with main, rebasing a story branch under the grant. The agent never merges. A poll set up in this session stops with the session: say so when starting it; a later session resumes from `story.sh status` and the epic. Watching other pull requests needs the user to name them; "all my open pull requests" names them, and acting on any of them beyond reading is asked, naming exactly which. Outside this feature, rebase with plain git and park any pull request that conflicts; conflicts are resolved alone only on story branches. On merge, run `story.sh close <branch>` unless `status` already closed it, and set the story Done with its log comment as the resolution. When nothing is ready and nothing is building, say which blocker frees the most and wait.
* **Deploy from main** by a command committed in the repository, and exercise the rollback once before anything a revert cannot undo.
* **Stop** after the merge for a request that was not an epic. For an epic, close out by `epic.md` when every child is done or cut.
* **In a team,** each story has its own branch and worktree per repository and writes only its own comments.
