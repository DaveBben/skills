# Implement a story

* **Check command:** the `Full check:` line of `AGENTS.md`, else its `Check:` line, else what CI runs, else the README's test command.
* **The guard:** [../scripts/guard.py](../scripts/guard.py), a hook on shell commands. It refuses a merge, a commit that changes a locked test other than by removing its expected-fail marker, and a pull request while a red test still carries that marker. It asks the user before a command removes or replaces the tests' lock. It runs only where the SDLC plugin's hooks run; elsewhere these rules hold without it.
* **The `test-author` agent:** `SDLC:test-author` where the harness loads named agents, otherwise a general subagent told to follow `../agents/test-author.md` beside this skill's folder. Launch it fresh each time.
* **A fix with no story:** its reproduction is the one acceptance criterion; give `test-author` that line as the story.
* **No behaviour change:** skip steps 2 and 3. Where no test covers the code touched, commit tests that pin its current behaviour first. Run step 7 with the one criterion "every existing test passes unchanged".

1. **Branch:** create a worktree on a new branch from main, and work there: `git worktree add -b <branch> <path> main`. Name the branch `story/<feature-slug>/<key>-<title-words>`, or `story/<key>-<title-words>` with no feature; use the title words alone when there is no key.
2. **Interface:** from the acceptance criteria, write the signatures the change adds or alters (functions, commands, routes, types) as stubs whose bodies only raise.
   * Commit the stubs alone.
   * Skip this step when every acceptance criterion goes through an interface that already exists.
3. **Failing tests:** launch `test-author` with these inputs and nothing from this chat or your plan:
   * The story with its context, and the feature's `Outcome:` line when it has one.
   * The worktree path and branch.
   * The interface commit's hash, or "none".

   It writes one test per example through that interface, confirms each fails for the reason its acceptance criterion states, marks each with the framework's strict expected-fail marker so the check command still passes, commits them alone and locks them in git config.
   * After the lock, a commit may not change a locked test, or a test that existed where the branch left main, except to remove a marker. Put a new test in a new test file.
   * Show the user the test list and any `Changes existing:` line, and continue. Answer its `Questions:` yourself where a tool can, else put them to the user and wait.
   * **Its return says the framework has no marker:** the check command fails on the red tests until they pass. That failure is expected; say so when a turn-end check reports it.
4. **Implement** until every new test passes and every test on its `At risk:` line still does.
   * Remove a test's expected-fail marker once the code makes it pass; the strict marker fails the run until you do.
   * Change only what the acceptance criteria need. Add no config with one value, no interface with one implementation, and no retry, cache or flag no criterion names. The exception is an adapter around a service outside the repository, which tests double in place of that service.
   * A test you cannot satisfy for a reason that holds against the code is a stop: report the test and the reason to the user, and change nothing in it.
   * A test the user agrees is wrong: save `git config --get-all branch.<branch>.redCommit`, run `git config --unset-all branch.<branch>.redCommit`, which the user approves where the guard asks, and give `test-author` the test, the correction and the saved hashes. It commits the corrected test and locks it and each earlier red commit again.
5. **Green:** run the check command. The whole suite must pass, not only the new tests, and no red test may still carry a marker.
   * Run the new test files five more times. A test whose result changes is flaky: report it to the user as a test to correct, by the step 4 path for a test the user agrees is wrong.
6. **Refactor** inside the diff with every test green, then run the check command again.
   * Remove code no acceptance criterion asked for and comments that restate the code.
   * Reuse an existing helper instead of a second copy.
7. **Review:** run the `review-code` skill on the branch, given the story's acceptance criteria, the merge target, the red commit's hash and the check command, and nothing from this chat. Run no second review. For each row it keeps:
   * **Finding,** blocking or not: `test-author` adds a failing test for it in a new test file, locked like the others; then fix it.
   * **Weak test:** `test-author` adds, in a new test file, a test the row's named wrong implementation fails; it may pass at once.
   * **Question,** a finding the fix does not settle, or behaviour no criterion states: put it to the user with its evidence.
8. **Pull request:** commit and push, then open it into main once every acceptance criterion passes.
   * Title: the story's key in brackets first when it has one, such as `[PAY-12] Refund a partial order`.
   * Body: the story, what changed and why, and how to verify it by hand.
   * When the repository runs its full check before a pull request opens (the `guardrails` skill sets that up), a refused open is a failing check. Fix the cause and open it again.
9. **Report** to the user the pull request, the check's result, each finding and how it was settled, and each choice made without them. On a linked issue, comment the pull request's link.
10. **The user merges.** Never run a pull request merge or merge into main.
    * Check each review comment's claim against the code before acting on it. A confirmed defect gets a failing test, then the fix.

When the feature has an acceptance test, run it after each story; it is a check, not the specification.
