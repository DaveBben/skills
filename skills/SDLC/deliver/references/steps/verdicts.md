# Step: act on the review

Read the `Findings:`, `Questions:`, `Teach:` and `Hand to build:` lines of `done-block.md` in the worktree's git directory. A **red row** is a test in the story's test table that fails until the build makes it pass.

* **`Teach:` rows** are points on the user's own code. Send them to the user in one message, `wrong` rows first, then `unverified`, then `shape`, each as the review wrote it, and never the rewritten code. The user rewrites and says done, then the `build` agent runs the suite and commits it with the message `yours: <row title>`; or the user says skip and the `build` agent makes the change. A `Teach:` row never parks the story and never becomes a red row unless it is also a finding.
* **A question** about behaviour no criterion states parks the story as a product decision.
* **Each confirmed finding,** blocking or not, and each `unsettled` one's settling test, becomes a red row: the `setup` agent adds a test that fails on it as a new red commit (`story.sh red`). A confirmed weak test is rewritten by the `setup` agent and handled as a wrong row (`story.sh next wrong-row`), with no park, since the user never saw that test.

When a red row was added or `Hand to build:` lists a change, the `build` agent makes the red rows pass and the listed changes, then run `story.sh next review` again, short when no red row was added. A second round of confirmed blocking findings on one story is a split, or a question to the user. When nothing is left to act on, run `story.sh next verify`.
