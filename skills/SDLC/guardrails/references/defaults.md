# Set up the default checks

## The check command

Write an executable `check` at the repository root. It runs these in order and stops at the first failure.

* **`./check`:** the format check, the linter, the rule checks and the tests that need no network, database or other process.
* **`./check --full`:** all of `./check`, then the tests that need a database, the network or another process, the end-to-end tests, and the mutation tool over the lines changed since the main branch. It prints surviving mutants and does not fail on them.
* **`./check --scheduled`:** for CI's schedule, outside both gates. It runs the mutation tool over the whole repository, contract tests of each third-party adapter against the real service, and tests that call a real language model. A failure is reported to the user and blocks no pull request.
* **Rule checks:** `semgrep --config .semgrep/ --error` once `.semgrep/` exists, and each rule script.

Choosing tools:

* **Empty slot:** name the tool to add, and add it on the user's yes.
* **Slot with nothing to run yet,** such as end-to-end tests: leave it out and say so.
* **Task runner:** `check` calls its targets rather than repeating their commands.
* **Mutation tools,** restricted to changed, covered lines, using the stack's own incremental or diff option.
  * **No gate on survivors:** about 4 to 39% of mutants are equivalent, meaning no input tells them from the original, so no test can kill them.
  * **A score gate the user asks for:** set it just under the score measured today (StrykerJS `thresholds.break`, PIT `mutationThreshold`) and raise it as the score rises.
* **Flaky tests:** a test that fails and then passes on an unchanged tree is flaky. The gate shows the user both runs. Never run a check again to get past a failure. Quarantine a flaky test only on the user's yes, with an expiry date in the skip reason.

Run `./check` and `./check --full` once.

* **Failure on existing code:** the user picks one of these.
  * Fix it first, as its own change.
  * Leave the failing part out of `check` until it is fixed.

## When it runs

* **Claude Code:** copy [../scripts/gate.py](../scripts/gate.py) to `.claude/hooks/gate.py` and merge [../scripts/settings.json](../scripts/settings.json) into `.claude/settings.json`. It runs `./check` at turn end and `./check --full` before a pull request opens.
  * **Timeout:** `./check --full` must finish within the hook's 3600-second timeout; a timeout lets the pull request open unchecked.
* **Another harness:** wire the same two commands to its turn-end and pre-tool events where it has them.
* **`./check --scheduled`:** on the user's yes, add it to CI as a scheduled job, such as a nightly GitHub Actions `schedule:` trigger, that opens an issue on failure.

Then run:

```sh
python3 .claude/hooks/gate.py --self-test
```

## Record it

* **`AGENTS.md`:** under Commands, write `Check: ./check` (runs at turn end), `Full check: ./check --full` (runs before a pull request) and, when it exists, `Scheduled check: ./check --scheduled` (runs on CI's schedule).
* **No `AGENTS.md`:** create it by the `orient` skill.
* **Commit** everything on a branch of its own.
