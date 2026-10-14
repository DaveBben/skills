# Implement a story

* **Check command:** the `Full check:` line of `AGENTS.md`, else its `Check:` line, else what CI runs, else the README's test command.
* **The guard:** a hook ([../scripts/guard.py](../scripts/guard.py)) denies a merge, a commit that changes a locked test other than by removing its expected-fail marker, and a pull request while a red test still carries that marker. It asks the user before a `git config` command removes or replaces the tests' lock. Where it does not run, these rules still hold.
* **Tests:** write the tests of steps 3, 4 and 7 yourself by the `failing-tests` skill (`SDLC:failing-tests`).
* **The `test-challenger` agent:** `SDLC:test-challenger` where the harness loads named agents, otherwise a general subagent told to follow `../agents/test-challenger.md` beside this skill's folder. Launch it fresh each time.
* **A fix with no story:** its reproduction is the one acceptance criterion.
* **No behaviour change:** skip steps 2 and 3. Where no test covers the code touched, commit characterization tests first. Run step 7 with the one criterion "every existing test passes unchanged".

1. **Branch:** work in a git worktree on a new branch from main. Name the branch `story/<feature-slug>/<key>-<title-words>`, or `story/<key>-<title-words>` with no feature; use the title words alone when there is no key.
   * **Glossary:** add each `Glossary:` line under the story's `Decided` to `docs/glossary.md`, one `<term>: <meaning>` line each, and commit it alone. When `AGENTS.md` has no pointer to the glossary, add one: read `docs/glossary.md` before naming a function, a type or a test. Name the interface, the tests and the code with the glossary's terms.
2. **Interface:** from the acceptance criteria, write the signatures the change adds or alters (functions, commands, routes, types) as stubs whose bodies only raise.
   * Commit the stubs alone.
   * Skip this step when every acceptance criterion goes through an interface that already exists.
   * Prefer a deep module. Add no signature that only passes a value through to another; the locked tests would hold it in place. An adapter around a service outside the repository is the exception.
3. **Failing tests:** write them by the `failing-tests` skill, one per example through that interface, before any implementation.
   * After the lock, a commit may not change a locked test, or a test that existed where the branch left main, except to remove a marker. Put a new test in a new test file.
   * **Challenge:** launch `test-challenger` with these inputs and nothing from this chat or your plan:
     * The story with its context, and the owning story's `Outcome:` line when the feature has one.
     * The worktree path and branch.
     * The interface commit's hash, or "none".
     * Your red commit's hash.
     * The absolute path of the `failing-tests` skill's `SKILL.md`.
   * Show the user both test lists and any `Changes existing:` line, and continue. Answer each `Questions:` line yourself where a tool can, else put it to the user and wait.
   * **A `Disagrees:` line:** put both readings of the criterion to the user and wait. When the user takes the challenger's reading, correct your test by the `failing-tests` skill's path for a locked test the user agrees is wrong.
   * **A framework with no marker:** when a turn-end check reports the red tests failing, say that failure is expected.
4. **Implement** until every new test passes and every test on its `At risk:` line still does.
   * Make one red test pass at a time, and run it after each edit. Never outrun your headlights.
   * A pass you cannot explain is programming by coincidence: find the reason before you go on.
   * Remove a test's expected-fail marker once the code makes it pass.
   * Change only what the acceptance criteria need. Add no config with one value, no interface with one implementation, and no retry, cache or flag no criterion names. The exception is an adapter around a service outside the repository, which tests double in place of that service.
   * A test you cannot satisfy for a reason that holds against the code is a stop: report the test and the reason to the user, and change nothing in it.
   * A test the user agrees is wrong: correct it by the `failing-tests` skill's path for a locked test the user agrees is wrong.
5. **Green:** run the check command. The whole suite must pass, and no red test may still carry a marker.
   * Run the new test files again when a test touches time, randomness, concurrency or the network. A test whose result changes is flaky: report it as a test to correct.
6. **Refactor** inside the diff with every test green, by the `refactoring` skill (`SDLC:refactoring`), then run the check command again.
   * Remove code no acceptance criterion asked for.
7. **Review:** run the `review-code` skill on the branch, given the story's acceptance criteria, the merge target, the red commit's hash and the check command, and nothing from this chat. Run no second review. For each row it keeps:
   * **Finding,** blocking or not: add a failing test for it by the `failing-tests` skill, in a new test file, locked like the others; then fix it.
   * **Weak test:** add, by the `failing-tests` skill and in a new test file, a test the row's named wrong implementation fails; it may pass at once.
   * **Question,** a finding the fix does not settle, or behaviour no criterion states: put it to the user with its evidence.
8. **Pull request:** commit and push, then open it into main once every acceptance criterion passes. An example marked `(checked by the user)` passes when the user confirms it on the branch: show it running, such as a local run or a screenshot, and wait.
   * Title: the story's key in brackets first when it has one, such as `[PAY-12] Refund a partial order`.
   * Body: the story, what changed and why, and how to verify it by hand.
   * When the repository runs its full check before a pull request opens, a refused open is a failing check. Fix the cause and open it again.
9. **Report** to the user the pull request, the check's result, each finding and how it was settled, and each choice made without them. On a linked issue, comment the pull request's link by the `using-trackers` skill. Then continue by [ship.md](ship.md) without waiting.

When the feature has an acceptance test, run it after each story; it is a check, not the specification.
