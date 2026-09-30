# Set up the checks

`scripts/setup-next.sh` prints one stage of this file at a time, in the order below. Each `##` heading is a stage; its first word, lowercased, is the stage's name.

## Survey

Record the language, package manager, agent harness and which slots already have a tool, in one table before proposing anything:

```text
| Slot | Tool now | Fires | Proposed |
```

Name every conflict before changing it: two tools on one slot, two package managers, a manifest with no lockfile, config in a file the new tool will not read. Propose a migration; never perform it unasked. A repository with code that predates the rules is brownfield, whatever its age. Halt before a cleanup that rewrites files an open `story/*` branch touches; offer the config-only part now.

## Slots

| Slot | Fires | The filled slot must |
|---|---|---|
| `fast_fix` | every edit | rewrite one file in place and exit 0 |
| `fast_check` | every edit | judge one file with no project context, with a different exit code for "found problems" than for "could not run" |
| `types` | turn end | check the whole project |
| `contracts` | turn end | assert allowed dependency directions, naming the broken rule |
| `rules` | turn end | match project patterns with a message written for this project |
| `complexity` | turn end | fail any function over the cyclomatic limit (default 6), naming it |
| `deps_check` | manifest edit, commit | fail when manifest and lockfile disagree, offline |
| `env_check` | session start | report whether the environment is built, naming the fixing command |
| `tests` | turn end when fast enough, else commit | run the suite, failing past the time limit `AGENTS.md` states |
| `e2e` | CI, and commit when under a minute | drive the interface users use: a browser, a running service, the command |
| `deadcode`, `duplication`, `audit`, `secrets` | commit | unreferenced symbols; new clones in changed files; dependencies against a CVE feed; credentials and personal data in staged changes, by the secrets stage |

Edit time finishes one file in under a second; turn end covers the whole project in under five seconds; everything else, and anything needing the network, runs at commit. Where no single-file semantic check exists, leave `fast_check` returning 0 and wire `types` at turn end. Where no contract tool exists, write contracts as tests on the import graph. Use Semgrep for `rules` unless the project has a pattern engine.

Write config to disk, not chat, and name the one line the user would argue with. Take the tool's defaults except these decisions: warnings as errors in the test runner; strict expected-failure handling; a committed dead-code allowlist; no coverage threshold until there is real code; suppression comments that name a code; the linter's target version equal to the support floor; small property-test profiles locally and large ones in CI; mutation testing over the changed files in CI.

On brownfield, a tool that turns existing code red lands by an option the user picks: new code only, a cleanup first as its own change, or a ratchet. Never leave it red, and never clean up unasked. Hand a cleanup the user chose to subagents on the cheapest model that can do it.

## Contracts and rules

Write dependency contracts, and on brownfield the codebase's own anti-patterns as rules, by `references/rules.md`. Show each rule with one real violation it catches before adding it. On brownfield, the user picks one of the options `rules.md` lists for code that already breaks a rule, with a ratchet baseline listed under `# owner reads: checks` in `CODEOWNERS`. Adding rules and leaving them red is not an option.

## Loop

Wire three layers, each a subset of one command list, to the agent harness's events: edit time, turn end, session start. Feedback arrives at the edit, on the developer's machine; CI is the backstop. A blocking check needs an escape, so wire the retry limit before the checks: after three failed re-checks in a session, a blocking check stops blocking and says so. A harness with no events still gets the checks at commit and in CI, a turn later.

**Claude Code.** Run `scripts/install.sh <repository>`. It copies the hook scripts into `.claude/hooks/`, merges `scripts/settings.json` into `.claude/settings.json`, and prints every line to edit. Edit only those lines, by the comment above each, and the entries the guards stage names.

**Another harness.** Write hooks that: auto-fix and silence what is mechanical and surface only what needs a decision; count retries per session and give up after three, saying so; re-check after each fix; skip when nothing relevant changed; fail open when the tool itself breaks; apply only to this repository and its worktrees, including story worktrees (git worktrees on `story/*` branches, often outside the project directory).

## Guards

* **The shipped guards are the hard blocks.** Add another only when breaking the rule is never correct and nothing catches it later.
* **Deny the feature acceptance directory for good:** the directory holding the user's end-to-end tests, which the agent never edits. Deny edits, writes and deletes, for the agent and every subagent. Replace `tests/feature-acceptance/` in `settings.json` with the project's own, and set `acceptance_dir` in `_slots.sh`.
* **Deny secrets files, the lockfile, and the git directory's config, hooks, objects, refs, `HEAD` and index.** Leave the rest of the git directory writable for the files the story loop keeps there (`done-block.md`, `findings.md`, `security.md`, `attack/`). Replace `./uv.lock` in `settings.json` with the project's lockfile.
* **Deny the harness's scheduling tools** (in Claude Code the `ScheduleWakeup` and `CronCreate` tools and the `loop` skill, already in `settings.json`). Each timed wake-up re-reads the whole session. A session that must wait runs a background command that exits on the change, or asks the user.
* **Write `# owner reads:` sections in `CODEOWNERS`:** `checks` for every file this skill wrote or configured, `deps` for the manifest and lockfile, and `data` for directories the architecture names. Each is a `# owner reads: <label>` heading, then one line per path with the user's handle, ending at a blank line.
* **Pre-approve every verification command,** and say plainly that the deny list stops accidents and is not a security boundary.

## Instructions

Put each rule in the narrowest scope that still loads when needed: `AGENTS.md` for every session, a nested instructions file for one module, a path-scoped rule for one file type. Never path-scope an instruction that governs the conversation. Create `AGENTS.md` by `SKILL.md` when there is none. Put the check command under Operational Commands and the silencing sentence under Critical Constraints, and state where a future correction goes: a static check into the rules directory, a dependency direction into the contracts, a file-type instruction into a path-scoped rule, anything conversational into `AGENTS.md`.

## Gate

Commit one command that runs this list in order and stops at the first failure: a `check` script at the root, or the task runner's target. Name it in `AGENTS.md` as the check command.

```text
format --check, fast_check (whole tree), rules, complexity, types, contracts, deadcode, duplication, audit, tests (with coverage), e2e
```

With pre-commit, copy `scripts/pre-commit-config.yaml` to `.pre-commit-config.yaml`, and copy `red_commit_scope.py`, `accepted_tests.py`, `issue_key.py` and `agents_md_size.py` from `scripts/` into the repository's `scripts/` unchanged; run each with `--self-test` and edit the lines the config's comments mark. With another runner, wire the same hooks, pinned: one per slot named for the slot, the file hygiene hooks, the secret scan, the lockfile check, `audit` only on lockfile changes, and the four scripts as local hooks with the test runner's test globs. For brownfield, add `scripts/ratchet.py`. Ask the user once for a time limit on the whole test run and write it in `AGENTS.md`. Wire automated dependency updates. A failing suite on brownfield is quarantined or fixed before it enters the gate.

The red commit, which holds a story's failing tests before any code, is the one commit that skips the `tests` and `e2e` hooks. Write its command under Operational Commands as the red-commit command (with pre-commit, `SKIP=tests,e2e git commit`).

A missing mutation or `e2e` slot does not block the story loop: the review applies mutations by hand, and the first story adds the `e2e` runner.

## Secrets and personal data

Nothing secret or personal reaches history. Wire every layer; each catches what the one before misses.

* **At commit:** one secret scanner as the `secrets` hook over staged changes, offline, pinned like every hook. The pre-commit template runs Gitleaks.
* **Personal data rules:** copy `scripts/gitleaks.toml` to `.gitleaks.toml`, or write the same in another scanner's config, and add one rule for each identifier format found in the stores `AGENTS.md` lists, by the comments in it.
* **In CI:** the same scanner and config on every pull request, run from `origin/main`'s copy like every check, so a commit made without the hook is still caught and a pull request cannot weaken its own check.
* **On the code host:** on GitHub, run `scripts/push-protection.sh`; on GitLab, read the project's secret push protection setting. Tell the user when it is off and how to turn it on, and never change it.
* **Once, over all history:** run the scanner over every commit (for Gitleaks, `gitleaks git`) and report each finding by commit and file, never its value. Rewriting history is the user's call. A live credential in history is told to the user at once, to rotate first.
* **Made-up data only:** write under Critical Constraints in `AGENTS.md` that test fixtures, seeds, examples and docs hold made-up data only, and nothing is copied from a real system's rows, logs or screenshots. No scanner reliably finds a name or a free-text note; this rule and the security review are the defence there.

List the scanner's config and ignore file under `# owner reads: checks` in `CODEOWNERS`.

## CI

Install from the lockfile. Run each check as its own step, from `origin/main`'s copy of the check scripts and config, so a pull request cannot edit what judges it. Run the whole span of supported runtime versions without stopping at the first failure. Run mutation testing over changed files, the thorough property-test profile, each twin's contract suite against recorded real responses on a schedule, and `e2e` against a built artifact, retrying once and labelling a pass-on-retry flaky. A twin is a fake of an external service under `tests/twins/<service>/`.
