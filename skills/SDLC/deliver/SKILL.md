---
name: deliver
description: "Use this skill before touching any file on a request to add, change, fix or remove behaviour in code that exists, or to build a story. Use it on: 'add X', 'fix the bug where X', 'X is broken', 'build story X', 'build the next story', 'refactor X', 'pick up where we left off', 'write the PR description'. Use it even when the change looks small. Builds each story from failing tests a fresh agent writes from the story alone, then the code, one fresh review and a pull request into main."
license: MIT
metadata:
  version: "21.0.0"
# Claude Code only: registered when the skill runs, for the rest of the session.
# scripts/guard.py says what it refuses. Without python3, it exits 0.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: 'f="${CLAUDE_PLUGIN_ROOT}/skills/deliver/scripts/guard.py"; [ -f "$f" ] && command -v python3 >/dev/null 2>&1 || exit 0; python3 "$f"'
---
# Deliver

Build one story at a time. A fresh agent that has seen no code for the change writes the story's cases as failing tests, and those tests are locked. This session writes the code. One fresh agent reviews it, the findings are fixed once, and the user confirms before anything is pushed.

## Words used here

* **Story:** what a person will be able to do once the change ships: an outcome, a `Not doing` list, numbered **cases** with concrete values, and a `Verify` line. The `story` skill writes it. A **feature** is several stories with one outcome; its `Order:` line lists them in build order, and it may have one **acceptance test** the user wrote for the whole feature.
* **Red commit:** a commit holding failing tests and stubs only, made before the code that passes them and recorded by `story.sh red`. Once one is recorded, its test files and every test that existed before the story are the **accepted tests**. A new test goes in a new test file.
* **Check command:** the one command that runs every check, as `AGENTS.md` names it; else what CI runs; else the test command the README gives.
* **[scripts/story.sh](scripts/story.sh):** the git steps of a story: start, red, confirm, verify, close, status. Run it with no arguments for its usage.
* **The guard:** [scripts/guard.py](scripts/guard.py), a hook on shell commands that refuses a merge, a push or pull request before the user confirms, and a commit that changes an accepted test.

## Start

Read `AGENTS.md` in each repository the work touches, for the check command and the red-commit command; when it names neither, use the definitions above and plain `git commit`, and say so once. Run `story.sh status` from the main checkout: a story it prints is picked up at the step its line names. When `AGENTS.md` has a `Backlog:` line, read and write the story's issue by [references/tracker.md](references/tracker.md): the story text on the issue, In Progress at the start, In Review when the pull request opens, the pull request's link as a comment.

## Size the request

| Size | Test | Path |
|---|---|---|
| No behaviour change | A refactor, a dependency bump, a rename, or tests for behaviour that exists | Cut a branch (`story.sh start`, or `git worktree add -b`). Where no test covers the code, commit tests that pin its current behaviour first. Make the change, run the check command, show the diff summary, and on the user's yes push and open the pull request. |
| Trivial | One sentence, an obvious test, and nobody harmed before a `git revert` lands | Show the one case. Cut a branch, commit one test that fails, then the fix, run the check command, and on the user's yes push and open the pull request. |
| One story | One workflow step and one variation | "Each story" below. |
| Several stories | More than one step or variation | The `story` skill splits it into a feature first, then "Each story" for each, in the feature's `Order:`. |

A bug's first case is its reproduction. A decision that costs more than a day to reverse (a library, a data shape, a trust boundary, a new repository) goes to the `architecture` skill before the story that needs it.

## Each story

1. **The story.** When the request has no numbered cases with concrete values, write them with the `story` skill and wait for the user's go.
2. **Branch.** From the main checkout, `story.sh start <slug> <key> <short-name>`: the slug is the feature's, the key the issue's or a short id of your own, the short name two or three words of the title. It prints the worktree's path; work there.
3. **Failing tests.** Launch the `test-author` agent, fresh, given the story's text, the worktree path, the path of `story.sh` and nothing from this chat. It commits the red commit, runs `story.sh red`, and returns the test list, `Changes existing:`, `At risk:` and `Questions:`. Show the user the test list and any `Changes existing:` line in one message; they edit it or say go. To apply their edit, run `story.sh unred`, have the `test-author` agent change the tests, and run `story.sh red` on its new commit. A question about a case is the user's to answer.
4. **Build.** Write the code in this session, in the worktree, until the red tests and the whole suite pass, committing as each case goes green.
   * Change only what the cases need. Add no config with one value, no interface with one implementation, no retry, cache or flag no case names, and no comment that restates the code.
   * Keep every test on `At risk:` passing: existing behaviour stays unless a case changes it.
   * A test you cannot satisfy for a reason that holds against the code is a stop: report the test and the reason to the user, and change nothing in it. The guard refuses a commit that changes an accepted test. Once the user agrees the test is wrong, run `story.sh unred`, have the `test-author` agent commit the corrected test as a new red commit, and run `story.sh red` for it and each earlier red commit.
5. **Review.** Launch the `review` agent, fresh, given the story, the branch, the merge target, the red commit's hash, the check command and the `Changes existing:` and `At risk:` lines, and nothing from this chat. When its `Security:` line says `needed`, then launch the `security` agent with the same inputs and what made it needed.
6. **Act on it once.** For each kept finding, have the `test-author` agent add a failing test in a new test file as a new red commit, then fix it here. For each weak test, run `story.sh unred`, have the `test-author` agent rewrite it, and run `story.sh red` on the rewrite and on each earlier red commit. Run the check command. Run no second review: a finding the fix does not settle goes to the user as a question with its evidence, and so does each row the review marked `question` (behaviour no case states).
7. **Verify.** In the worktree, `story.sh verify '<check command>'`: it rebases, fails when an accepted test changed, and runs the check command. When the feature has an acceptance test the user wrote, run it last and report its result.
8. **Confirm and open.** Send one message: the cases and any that changed since the user saw them, each kept finding and how it was settled, the choices made without the user, and a description of the pull request (what changed and why, and the `Verify` line). Ask for a yes. On yes, run `story.sh confirm`, push, and open the pull request into main with that description and the story's key in brackets at the start of its title, such as `[PAY-12]`.
9. **After it opens.** The user merges. Watch open pull requests with one background command that prints a line only when something changes and wakes the session on it (Claude Code's Monitor tool runs one), never a prompt re-run on an interval. Check each review comment's claim against the code before answering; a confirmed defect gets a failing test, then the fix. Draft each reply for the user to post. On merge, `story.sh close <branch>` and start the next story in the feature's `Order:`.

## Talking to the user

* **A fact a tool can reach** (what a table holds, what a route returns, what CI runs): look it up and use it.
* **A technical choice a `git revert` undoes,** that no person sees and no later story inherits: decide it and list it in the confirm message.
* **Product intent, or a choice expensive to reverse:** ask, one question per message, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion), recommended option first, each option's consequence in one sentence.
* **The user is away:** take the recommended option, keep going up to the confirm step, and list every choice made that way.

Build one story at a time unless `AGENTS.md` says otherwise. When the user writes part of the code themselves, wait for their commit, then continue at the review.
