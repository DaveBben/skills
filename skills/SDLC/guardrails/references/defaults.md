# Set up the default checks

## The check command

Write an executable `check` at the repository root. It runs these in order and stops at the first failure.

* **`./check`:** the format check, the linter, the rule checks and the unit tests.
* **`./check --full`:** all of `./check`, then the integration tests, mutation tests over the files changed since the main branch, and the end-to-end tests.
* **Rule checks:** `semgrep --config .semgrep/ --error` once `.semgrep/` exists, and each rule script.

Choosing tools:

* **Empty slot:** name the tool to add, and add it on the user's yes.
* **Slot with nothing to run yet,** such as end-to-end tests: leave it out and say so.
* **Task runner:** `check` calls its targets rather than repeating their commands.
* **Mutation tools:** `mutmut` (Python), StrykerJS (JavaScript, TypeScript), `cargo-mutants` (Rust), `go-mutesting` (Go), PIT (Java), each with its failure threshold set so surviving mutants fail the run (StrykerJS `thresholds.break`, PIT `mutationThreshold`).

Run `./check` and `./check --full` once.

* **Failure on existing code:** the user picks one of these.
  * Fix it first, as its own change.
  * Leave the failing part out of `check` until it is fixed.
* **Never** commit `check` failing.

## When it runs

* **Claude Code:** copy [../scripts/gate.py](../scripts/gate.py) to `.claude/hooks/gate.py` and merge [../scripts/settings.json](../scripts/settings.json) into `.claude/settings.json`. It runs `./check` at turn end and `./check --full` before a pull request opens.
  * **Timeout:** `./check --full` must finish within the hook's 3600-second timeout; a timeout lets the pull request open unchecked.
* **Another harness:** wire the same two commands to its turn-end and pre-tool events where it has them.

Then run:

```sh
python3 .claude/hooks/gate.py --self-test
```

## Record it

* **`AGENTS.md`:** under Commands, write `Check: ./check` (runs at turn end) and `Full check: ./check --full` (runs before a pull request).
* **No `AGENTS.md`:** create it by the `orient` skill.
* **Commit** everything on a branch of its own.
