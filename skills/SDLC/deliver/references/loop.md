# The loop: sections 0 to 6

Load this when a request is sized as one story or several stories, or when resume restarts a story at one of these sections. Sections 7 and 8, the parking rules and the split rule are in `SKILL.md`.

## 0. Define

Run the `define-work` skill with the user before anything else. Criteria are written with the `story` skill when each story starts (section 4). A repository with no application yet belongs to the `architecture` skill, which hands back to this skill at section 2.

Choose the slug: the epic's key when the stories live on a tracker, else a kebab-case name for the outcome. Every story gets its own branch `story/{slug}/{n}-{short-name}` from main, and merges back into main. No feature branch exists.

### Spike only when blocked

* **At PRD read:** an assumption whose falsity changes *what* gets built, not *how*.
* **In the loop:** the acceptance criterion or a test row cannot be written for want of a fact about the world: a throughput number, a library's real behaviour, what an API returns.

Do not spike when a story answers it as fast, when the question is a product decision (park the story), or when there is no falsifiable answer. When the question is what the existing system actually does, read its data, not its code.

Frame the spike's question, finish line and timebox with the user. Then run the `spike` skill in a subagent with that frame, the feature's slug and the spike's number on `Stories:`; it commits its findings where the `spike` skill says and returns what its subagent mode lists. Put its decision table to the user and run the `architecture` skill to record each row marked `record`. When the spike reports that its findings contradict a decided ADR, park the stories that depend on it and run the `architecture` skill's path for deciding one open item; the new ADR names the old one on its `Supersedes:` line and replaces its path on `Decided:`. When a spike is done is defined in [next.md](next.md).

## 1. Architecture

For a request sized as several stories, or a project with no application yet, run the `architecture` skill with the user after Define. No story starts until every item it needs is decided, deferred, waiting on a spike, or settled by the code.

* **At every story start,** read `Deferred:`. A choice swappable behind an interface, or affecting one story, waits until a story needs it. When this story is the first to need one (the first cache, the first queue, the first second service, the first payment call), or an item waits on a spike that is done, park the story and run the `architecture` skill's path for deciding one open item.
* **A decision the build needs that nobody recorded** parks the story the same way.

## 2. Record

Load [feature-header.md](feature-header.md). It holds the rules the record keeps, the feature header's format, the plan branch, the feature acceptance test the user writes, and close-out. Write the header where Orient found the stories live.

## 3. Pick the next story

A subagent runs [next.md](next.md) at every pick and returns its report: which stories are ready, in rank order, and what blocks the rest.

## 4. Set up the story

Take the story the user named, the request sized above, or each story section 3 picks. Cut `story/{slug}/{n}-{short-name}` from main, where `{n}` is the story's number on `Stories:` or its issue key, in its own worktree (`git worktree add` is one way), so stories can run side by side, and run the check command there. Run the section 1 check for a forced decision. When the story changes more than one repository, load [cross-repo.md](cross-repo.md).

**Criteria.** Issue one instruction to a criteria subagent, given its own `Stories:` line, the feature header's `Outcome:`, `Not doing:`, `Constraints:`, `Context:` and `Decided:` lines, `AGENTS.md` and the worktree path. It runs the `story` skill without writing to the tracker. It greps the log for unpinned `Learned`, `Not caught by` and `Observed` lines, skipping spike `Dead ends` and pinned `Decided alone` lines. It reads each ADR on `Decided:` by its title, Decision and Detector lines, and opens one in full only when its Decision names a module, flow or store the story touches. It reads the live PRD. It returns the criteria, the card text, the lines that bear on the story as `Assumes:` lines and NON-NEGOTIABLE facts, any contradiction with the PRD, and every question it could not decide. Where a returned line changes what gets built, add or change the story and say so. Show the user the criteria in full and park the story until the user confirms or edits them. On a tracker, put them in the story's criteria field under "PROPOSED, NOT AGREED" until then, with no comment. When the user rejects them outright, reissue the criteria subagent with the objection; after a second rejection, put the story's outcome line back to the user. Where the stories live on a tracker, write the returned card text to the story's issue once confirmed.

**Setup and red commit.** Then issue one instruction to a setup subagent, given the confirmed criteria, the `Assumes:` and NON-NEGOTIABLE lines, the ADR titles and the PRD path the criteria subagent returned, the worktree path and [setup.md](setup.md). It runs every step there through the red commit and returns what that reference lists. A criterion that cannot be written as a test goes back to `story`, and the user confirms the rewritten criteria.

## 5. Build

Read [build-prompt.md](build-prompt.md) once the red commit has landed; it holds the prompt's format. Fill it from what the setup subagent returned, and issue one instruction to a subagent from it. The builder makes the accepted rows pass and may add tests for cases the table missed, listing each one and why. It never rewrites an accepted row.

Run the tests and the check command `AGENTS.md` names after the builder returns, and read only their summary. A red check is a red story.

When the builder returns a question about a choice a person would see, ask the user as soon as control returns and park the story. Once answered, reissue the prompt on the branch as it stands, with the answer under NON-NEGOTIABLE. A builder that stopped to ask is not reset, even with rows still red.

When the builder reports a row it cannot satisfy, it cites the file and line that stop it; a subagent checks that reason against the code. When the reason holds, park the story for a wrong row. When the builder reports red on any row, or touched anything outside its paths, do not debug the attempt. Reset the tree to the latest red commit and reissue the prompt with the one new fact under NON-NEGOTIABLE. Twice red on sound rows is a split.

**When the user has said they will write the code themselves,** issue no build prompt. The accepted rows are already red; the user writes the code until they are green. Then run the `reviewing` skill in a subagent on their branch, as work the user made. It returns the feedback points and a `Changed:` line per new function, module or branch, with what it is for and its file. Section 6 then runs only its verify step, whose passing rows fill the criteria table, and the pull request carries the feedback points in place of the Done block.

## 6. Review and Verify

Run the `reviewing` skill in a subagent on the story branch, for code the agent built, given the branch name, the red commit's hash, the check command, the build prompt's NON-NEGOTIABLE block and the builder's list of choices, and nothing from this session's chat. It writes its Done block to `done-block.md` in the worktree's git directory (`git rev-parse --git-dir`) and returns only whether the review is done, its `Rules:` line and its `Proposed refactor:` lines. Hand each rule to the `guardrails` skill in a subagent.

**Security.** The review returns `Security: pending`. Run the `reviewing` skill's security review as its two subagents in turn: the first maps the attack surface into `attack-surface.md` in the shared git directory, updating the map from earlier stories; the second reviews the branch against it and appends its `Security:` line to `done-block.md`. Each blocking finding is a red story, reissued with a test that fails on that finding as one to add. Hand its `Rules:` line to `guardrails`.

**Attack.** Then a fresh subagent, given only the confirmed criteria, the interface each names and the story's diff, runs [attack-prompt.md](attack-prompt.md), on another model where the harness offers one. Its `Red` lines are a red story, reissued with each test as one to add; its `Unstated` lines park the story as a product decision.

Then verify the whole feature, not the story, in a subagent given the branch name, every red commit's hash and the path of [../scripts/read_by_exception.py](../scripts/read_by_exception.py). It rebases the story branch on main, re-records every red commit's new hash in the guard, and returns the latest. It runs that script from the repository root with `main` and the latest red commit, writes its output to `exceptions.txt` beside `done-block.md`, and returns the line count. It diffs the accepted test files against the red commit; any change is a red story. It runs the full suite and the check command, and the story's acceptance tests through the interface each names (the one the user actually uses: the screen, the API, the command), against the running system, with every earlier acceptance test. It runs the feature acceptance test last and returns its result and failure message on their own, and pass or fail for the rest. With a `Holdout:` line, it runs that command last, with `--done` and the merged story numbers plus this one, and `--diff` and a file holding the story's diff, and returns its line unchanged.

* **The holdout line names a failure or a leak:** park the story for the user. It is not a red story.
* **The feature acceptance test passes:** its strict marker turns it red. That parks the story, and is not a red story.
* **Its failure message changed since the last story:** say so.
* **Only the test-run time limit `AGENTS.md` states failed:** report it on its own and hand it to the `guardrails` skill. It is not a red story.
* **A red anywhere else is a red story:** reset to the latest red commit and reissue the build, as in section 5.

Never open a pull request without the review's Done block file, or the feedback points for code the user wrote. The trivial size needs neither.
