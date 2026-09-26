# Setup and red commit

The setup subagent loads this once the user has confirmed the story's criteria. It works in the story's worktree, runs every step below through the red commit, and returns the red commit's hash on each repository (its message holds the accepted table), the paths of the accepted test files, the filled NON-NEGOTIABLE block of the build prompt, and anything it could not decide. A bug found in shipped work comes back as a new story.

## Before the red commit

* **Do the proposed refactors this story touches.** Make each one its own commit on the story branch before the red commit, with the full suite green before and after. Write the commit beside that `Proposed refactor` line in the log.
* **Pin untested legacy before changing it.** When the code the story touches has no test of its current behaviour, write characterization tests asserting what it does today, bugs included, and commit them before the red commit. They are scaffolding: the review deletes any the accepted rows make redundant.
* **Introduce the seam first.** When legacy code offers no point to test through, add the seam (an injected dependency, an extracted function, a wrapper) as its own commit on this story's branch before the red commit. It changes no behaviour, and the full suite stays green before and after. Where the old path resists a seam, build beside it and route to the new path, rather than editing in place.
* **Hand the story's `Interpreted` line to the `guardrails` skill.** It writes each rule on this story's branch, and the pull request lists them for the user.
* **Note each fact the story rests on** that was read from a document or not checked, and check it before the build. These become the pull request's `Assumes` lines.
* **Generate the table.** Run the `story` skill for the test table of the confirmed criteria, against the code. Apply its cut rules here; the accepted table is the one the review holds the build to. A row that exposes a product decision no PRD or ADR records parks the story.
* **A bug's table is two rows,** the failing test at the level the report describes, written before reading the code, then a unit test isolating the fault. Then grep every caller of the function about to change and fix at the point they all route through.

## Red

* **Write every accepted row as a failing test,** acceptance test first, new rows in a new test file.
* **Run the tests.** A row that passes before the build, or fails for a reason other than the missing behaviour, means the code does not do what the story assumes; read it before going on.
* **Delete or rewrite every existing test that asserts behaviour this story removes,** in the same commit and listed in its message.
* **Commit the red tests as their own commit,** with the criteria and the accepted table verbatim in the message. The commit gate runs the tests and would refuse it: skip only the `tests` and `e2e` hooks, by the red-commit command `AGENTS.md` records (with pre-commit it is `SKIP=tests,e2e git commit`), and never the whole gate. The commit holds test files and stubs only; stubs add lines and remove none, and the gate's `red-commit-scope` hook refuses anything else under the skip. Commit before the turn ends, so the turn-end check sees a clean tree. Where `guardrails` installed the accepted-test guard, record the hash on the story's branch with `git config --add branch.<branch>.redCommit <hash>`; the guard refuses edits to the files of every recorded red commit until the merge clears them with `git config --unset-all branch.<branch>.redCommit`. When the installed guard reads only the older single key `agile.redCommit`, offer `guardrails` to update it, and until then run one story at a time and record the hash under `agile.redCommit`. Change no accepted row after this commit, except through a parked wrong row that the user re-accepts.

When a turn-end hook blocks the red run because the tests name symbols that do not exist yet, add the symbols as stubs whose only body raises. The types pass and the tests still fail on behaviour.
