---
name: deliver
description: "Use this skill before touching any file on a request to add, change, fix or remove behaviour in code that exists, or to build a story. Use it on: 'add X', 'fix the bug where X', 'X is broken', 'build story X', 'build this' with a link to an issue, 'refactor X', 'pick up where we left off'. Use it even when the change looks small. Fixes the interface, has a fresh agent write failing tests through it from the cases alone, writes the code until they pass, refactors, has a fresh agent review it, then commits, pushes and opens a pull request into main."
license: MIT
metadata:
  version: "22.0.0"
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

## The input

* **A story:** an outcome, a `Not doing` list and numbered cases with concrete values, from the `story` skill or from an issue the user links on a tracker. Read a linked issue with its comments.
* **A written prompt:** before any code, write the cases you will test as numbered lines with concrete values: the change itself, then its edge cases (empty and malformed input, input past a limit, the same action twice, two at once, a dependency down), then a `Not doing` line for what you will leave out. Show them to the user. Ask only where two readings of the prompt lead to different cases; decide the rest and keep going.

A bug's first case is its reproduction. A change with no behaviour change (a refactor, a rename, a dependency bump) has no new cases: where no test covers the code it touches, commit tests that pin its current behaviour first. A decision that costs more than a day to reverse goes to the `adr` skill first. Work that is several stories goes to the `story` skill to split, then comes back here one story at a time.

The **check command** is the `Full check:` line of `AGENTS.md`, else its `Check:` line, else what CI runs, else the README's test command.

## The loop

1. **Branch.** Create a worktree on a new branch from main (`git worktree add -b <branch> <path> main`), with the story's key in the branch name when it has one, and work there.
2. **Interface.** From the cases, write the signatures the change adds or alters (functions, commands, routes, types) as stubs whose bodies only raise, and commit them alone. Skip this when every case goes through an interface that already exists. The interface is yours to design; the tests come from someone else.
3. **Failing tests.** Launch the `test-author` agent, fresh, given the story or the case list, the worktree path and branch, and the interface commit's hash or "none", and nothing from this chat or your plan. It writes one test per case through that interface, confirms each fails for the reason its case states, commits them alone and locks them in git config. From then on the guard refuses a commit that changes a locked test or a test that existed where the branch left main; a new test goes in a new test file. Show the user its test list and any `Changes existing:` line; answer its `Questions:` or put them to the user.
4. **Implement** until every new test passes and every test on its `At risk:` line still does. Change only what the cases need: no config with one value, no interface with one implementation, no retry, cache or flag no case names. A test you cannot satisfy for a reason that holds against the code is a stop: report the test and the reason to the user, and change nothing in it. When they agree it is wrong, run `git config --unset-all branch.<branch>.redCommit` and have the `test-author` agent commit the corrected test and lock it and each earlier red commit again.
5. **Green.** Run the check command. The whole suite passes, not only the new tests.
6. **Refactor** inside the diff with every test green: remove code no case asked for and comments that restate the code, reuse a helper that already exists instead of a second copy, and improve names, function size and nesting. Run the check command again.
7. **Review.** Run the `review-code` skill on the branch, given the story's cases, the merge target, the red commit's hash and the check command, and nothing from this chat. Fix each kept finding once: the `test-author` agent adds a failing test for it in a new test file, locked like the others, then you fix it. A finding the fix does not settle, and each behaviour no case states, goes to the user as a question with its evidence. Run no second review.
8. **Commit and push** the branch.
9. **Open the pull request** into main once every case passes. Title it with the story's key in brackets first when it has one, such as `[PAY-12] Refund a partial order`. Write in the body what changed and why, the cases, and how to verify it by hand. When the repository runs its full check before a pull request opens (the `guardrails` skill sets that up), a refusal is a failing check: fix the cause and open it again. Then report to the user: the pull request, the check's result, each finding and how it was settled, and each choice made without them. On a linked issue, comment the pull request's link.
10. **The user merges;** the guard refuses a merge. Check each review comment's claim against the code before acting on it; a confirmed defect gets a failing test, then the fix.

## Talking to the user

* **A fact a tool can reach** (what a table holds, what a route returns, what CI runs): look it up and use it.
* **A technical choice a `git revert` undoes,** that no person sees and no later story inherits: decide it and list it in the report.
* **Product intent, or a choice expensive to reverse:** ask, one question per message, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion), recommended option first.
* **The user is away:** take the recommended option, keep going, and list every choice made that way.
