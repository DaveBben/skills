# Set up the default checks

## The check command

Write an executable `check` at the repository root that runs these in order and stops at the first failure:

* **`./check`:** the format check, the linter, the rule checks (`semgrep --config .semgrep/ --error` once `.semgrep/` exists, and each rule script), and the unit tests.
* **`./check --full`:** all of the above, then the integration tests, mutation tests over the files changed since the main branch, and the end-to-end tests.

Use the tools the repository already has; when a slot has none, name the tool to add and add it on the user's yes. Common mutation tools: `mutmut` (Python), StrykerJS (JavaScript, TypeScript), `cargo-mutants` (Rust), `go-mutesting` (Go), PIT (Java). Leave out a slot the repository has nothing for yet, such as end-to-end tests, and say so. When the project has a task runner, `check` calls its targets rather than repeating their commands.

Run `./check` and `./check --full` once. When either fails on code that already exists, the user picks: fix it first as its own change, or leave the failing part out of `check` until it is fixed. Never commit `check` failing.

## When it runs

* **Claude Code:** copy [../scripts/gate.py](../scripts/gate.py) to `.claude/hooks/gate.py` and merge [../scripts/settings.json](../scripts/settings.json) into `.claude/settings.json`. Then:
  * at the end of each turn, once Claude has finished its work, the hook runs `./check` when files changed since it last passed. A failure sends Claude back to fix it once; a second failure ends the turn and tells the user.
  * before Claude opens a pull or merge request (`gh pr create`, `glab mr create`, `tea pr create`, or a tool that creates one), the hook runs `./check --full` and refuses the request when it fails.
* **Another harness:** wire the same two commands to its turn-end and pre-tool events where it has them.

Run `python3 .claude/hooks/gate.py --self-test`.

## Record it

Under Commands in `AGENTS.md`, write `Check: ./check` (runs at turn end) and `Full check: ./check --full` (runs before a pull request), creating `AGENTS.md` by the `orient` skill when there is none. Commit everything on a branch of its own.
