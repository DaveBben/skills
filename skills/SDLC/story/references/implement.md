# Implement a story

* **Check command:** the `Full check:` line of `AGENTS.md`, else its `Check:` line, else what CI runs, else the README's test command.
* **The guard:** [../scripts/guard.py](../scripts/guard.py), a hook on shell commands that refuses a merge, and a commit that changes a locked test.
* **No behaviour change:** write no new acceptance criteria; where no test covers the code touched, commit tests that pin its current behaviour first.

1. **Branch:** create a worktree on a new branch from main, and work there. Put the story's key in the branch name when it has one.
2. **Interface:** from the acceptance criteria, write the signatures the change adds or alters (functions, commands, routes, types) as stubs whose bodies only raise.
   * Commit the stubs alone.
   * Skip this step when every acceptance criterion goes through an interface that already exists.
3. **Failing tests:** launch the `test-author` agent, fresh, with these inputs and nothing from this chat or your plan:
   * The story with its context, and the feature's `Outcome:` line when it has one.
   * The worktree path and branch.
   * The interface commit's hash, or "none".

   It writes one test per example through that interface, confirms each fails for the reason its acceptance criterion states, commits them alone and locks them in git config.
   * After the lock, the guard refuses a commit that changes a locked test, or a test that existed where the branch left main. Put a new test in a new test file.
   * Show the user the test list and any `Changes existing:` line. Answer its `Questions:` or put them to the user.
4. **Implement** until every new test passes and every test on its `At risk:` line still does.
   * Change only what the acceptance criteria need. Add no config with one value, no interface with one implementation, and no retry, cache or flag no criterion names.
   * A test you cannot satisfy for a reason that holds against the code is a stop: report the test and the reason to the user, and change nothing in it.
   * A test the user agrees is wrong: save `git config --get-all branch.<branch>.redCommit`, unset it, and give `test-author` the test, the correction and the saved hashes. It commits the corrected test and locks it and each earlier red commit again.
5. **Green:** run the check command. The whole suite must pass, not only the new tests.
6. **Refactor** inside the diff with every test green, then run the check command again.
   * Remove code no acceptance criterion asked for and comments that restate the code.
   * Reuse an existing helper instead of a second copy.
   * Improve names, function size and nesting.
7. **Review:** run the `review-code` skill on the branch, given the story's acceptance criteria, the merge target, the red commit's hash and the check command, and nothing from this chat. Run no second review.
   * For each kept finding, `test-author` adds a failing test in a new test file, locked like the others; then fix it.
   * A finding the fix does not settle, and each behaviour no acceptance criterion states, goes to the user as a question with its evidence.
8. **Pull request:** commit and push, then open it into main once every acceptance criterion passes.
   * Title: the story's key in brackets first when it has one, such as `[PAY-12] Refund a partial order`.
   * Body: what changed and why, the acceptance criteria, and how to verify it by hand.
   * When the repository runs its full check before a pull request opens (the `guardrails` skill sets that up), a refused open is a failing check. Fix the cause and open it again.
9. **Report** to the user the pull request, the check's result, each finding and how it was settled, and each choice made without them. On a linked issue, comment the pull request's link.
10. **The user merges;** the guard refuses a merge.
    * Check each review comment's claim against the code before acting on it. A confirmed defect gets a failing test, then the fix.

```sh
git worktree add -b <branch> <path> main
git config --get-all branch.<branch>.redCommit
git config --unset-all branch.<branch>.redCommit
```

When the feature has an acceptance test, run it after each story; it is a check, not the specification.
