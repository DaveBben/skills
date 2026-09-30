# Set up the checks

Load this when a repository's checks, hooks, deny list, commit gate or CI must be set up or repaired. Decide nothing about what the system should be. Resume at the first missing output when a repository is part-way through.

```text
SURVEY -> SLOTS -> CONTRACTS -> RULES -> LOOP -> GUARDS -> INSTRUCTIONS -> GATE -> CI
```

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
| `deadcode`, `duplication`, `audit`, `secrets` | commit | unreferenced symbols; new clones in changed files; dependencies against a CVE feed; credentials and personal data in staged changes, by "Secrets and personal data" below |

Edit time finishes one file in under a second; turn end covers the whole project in under five seconds; everything else, and anything needing the network, runs at commit. Where no single-file semantic check exists, leave `fast_check` returning 0 and wire `types` at turn end. Where no contract tool exists, write contracts as tests on the import graph. Use Semgrep for `rules` unless the project has a pattern engine.

Write config to disk, not chat, and name the one line the user would argue with. Take the tool's defaults except these decisions: warnings as errors in the test runner; strict expected-failure handling; a committed dead-code allowlist; no coverage threshold until there is real code; suppression comments that name a code; the linter's target version equal to the support floor; small property-test profiles locally and large ones in CI; mutation testing over the changed files in CI. Hand bulk cleanup to subagents on the cheapest model that can do it.

## Contracts and rules

Write dependency contracts, and on brownfield the codebase's own anti-patterns as rules, by `rules.md`. Show each rule with one real violation it catches before adding it.

## Loop

Wire three layers, each a subset of one command list, to the agent harness's events: edit time, turn end, session start. Auto-fix and silence what is mechanical; surface only what needs a decision. Count retries per session and give up after three, saying so. Re-check after each fix. Skip when nothing relevant changed. Fail open when the tool itself breaks. Apply only to this repository and its worktrees, including story worktrees outside the project directory. A harness with no events still gets the checks at commit and in CI, a turn later.

**Claude Code.** Copy each script from `scripts/` into `.claude/hooks/` unchanged, `chmod +x` it, and merge `scripts/settings.json` into `.claude/settings.json`. Edit only lines marked `# EDIT` and the entries named here.

The template sets `promptCacheTtl` to `1h` (Claude Code 2.1.242 and later, per https://code.claude.com/docs/en/prompt-caching). A story loop waits on subagents and reviewers for longer than five minutes, and on the five-minute default each wait makes the next turn write the whole conversation to the cache again.

| Script | Event | Does |
|---|---|---|
| `_slots.sh` | sourced | defines every project command once; its `read_json_field` uses `jq` or `sed`, never `python3` |
| `fast-check.sh` | PostToolUse on edits | `fast_fix` then `fast_check` on the edited file |
| `deps-guard.sh` | PostToolUse on the manifest | `deps_check` |
| `turn-end-check.sh` | Stop, SubagentStop | the turn-end slots on the main checkout and the story worktree, with the retry counter; exits early on a clean tree |
| `session-start.sh` | SessionStart | reports readiness on stdout, never exits non-zero |
| `bash-guard.sh` | PreToolUse on Bash | blocks `--no-verify`, the direct install command (edit its `<direct install>` line), and `rm`/`mv` on accepted tests and the feature acceptance directory |
| `main-guard.sh` | PreToolUse on edits | refuses edits on main except `AGENTS.md`, `CLAUDE.md` and `docs/adr/` (`main_ok` in `_slots.sh`) |
| `tests-guard.sh` | PreToolUse on edits | while a red commit is recorded, refuses edits to the test files it touched and to paths under `# owner reads: checks` in `CODEOWNERS` |
| `push-guard.sh` | PreToolUse on Bash | refuses `git push` and opening a pull request for a story branch (`story/*`, or one `story.sh adopt` marked) with a red commit until `story.sh confirm` has run; a pull request title must carry the issue key |

In `_slots.sh`: pick a lockfile check that resolves without installing and stays offline, since a dry run often skips the frozen-lockfile check; pick the dependency check that compares the manifest with the source, not the one that checksums downloads. Check what exit codes the checker uses before trusting the `-eq 1` test in `fast-check.sh`. On `PreToolUse`, `PostToolUse` and `Stop`, exit 2 blocks and feeds stderr to the agent; on `SessionStart`, stdout reaches the agent.

## Guards

* **Two hard blocks, and justify a third.** A rule earns one only when breaking it is never correct and nothing catches it later. Blocking the flag that skips the commit gate qualifies.
* **Block edits on main,** so work happens on story branches.
* **Block edits to accepted tests and to the checks** while a red commit is recorded, at edit time and in the shell.
* **Hold a story branch on this machine** until the user confirmed its criteria (`push-guard.sh`).
* **Deny the feature acceptance directory for good:** edits, writes and deletes, for the agent and every subagent. Replace `tests/feature-acceptance/` in `settings.json` with the project's own, and set `acceptance_dir` in `_slots.sh`.
* **Deny secrets files, the lockfile, and the git directory's config, hooks, objects, refs, `HEAD` and index.** Leave the rest of the git directory writable for the files the story loop keeps there (`done-block.md`, `findings.md`, `security.md`, `attack/`).
* **Write `# owner reads:` sections in `CODEOWNERS`:** `checks` for every file this skill wrote or configured, `deps` for the manifest and lockfile, and `data` for directories the architecture names. Each is a `# owner reads: <label>` heading, then one line per path with the user's handle, ending at a blank line.
* **Pre-approve every verification command,** and say plainly that the deny list stops accidents and is not a security boundary.
* **Add a `UserPromptSubmit` line** where the harness allows it, reminding the agent that a behaviour change starts in a story worktree.

## Instructions

Put each rule in the narrowest scope that still loads when needed: `AGENTS.md` for every session, a nested instructions file for one module, a path-scoped rule for one file type. Never path-scope an instruction that governs the conversation. Create `AGENTS.md` by `SKILL.md` when there is none. Put the check command under Operational Commands and the silencing sentence under Critical Constraints, and state where a future correction goes: a static check into the rules directory, a dependency direction into the contracts, a file-type instruction into a path-scoped rule, anything conversational into `AGENTS.md`.

## Gate

Commit one command that runs this list in order and stops at the first failure: a `check` script at the root, or the task runner's target. Name it in `AGENTS.md` as the check command.

```text
format --check, fast_check (whole tree), rules, complexity, types, contracts, deadcode, duplication, audit, tests (with coverage), e2e
```

Install the ecosystem's pre-commit runner with pinned hooks, one hook per slot with the slot's name as its id, plus trailing whitespace, final newline, large files, conflict markers, debugger statements, the secret scan and the lockfile check. Scope `audit` to lockfile changes. Ask the user once for a time limit on the whole test run and write it in `AGENTS.md`. Wire automated dependency updates.

The red commit is the one commit that skips the `tests` and `e2e` hooks, since it holds failing tests before any code. Write its command under Operational Commands as the red-commit command (with pre-commit, `SKIP=tests,e2e git commit`). Copy these from `scripts/` into the repository's `scripts/` unchanged, run each with `--self-test`, and wire them as local hooks with the test globs the test runner uses:

* **`red_commit_scope.py`:** when `SKIP` names `tests` or `e2e`, fails unless every staged file is a test or a stub that removes no lines. Never skippable.
* **`accepted_tests.py`:** fails a commit that changes or deletes a test file a recorded red commit touched. Never skippable.
* **`issue_key.py`:** a `prepare-commit-msg` hook that prepends `[<key>] ` from `branch.<branch>.issueKey` (needs `default_install_hook_types: [pre-commit, prepare-commit-msg]`).
* **`agents_md_size.py`:** fails an `AGENTS.md` over 100 lines or 8 KB.
* **`ratchet.py`:** for brownfield, holds existing code to its baseline finding counts per rule per file.

A missing mutation or `e2e` slot does not block the story loop: the review applies mutations by hand, and the first story adds the `e2e` runner.

## Secrets and personal data

Nothing secret or personal reaches history. Wire every layer; each catches what the one before misses.

* **At commit:** one secret scanner as the `secrets` hook over staged changes, offline, for example Gitleaks through pre-commit (hook id `gitleaks`), pinned like every hook.
* **Personal data rules** in the scanner's config committed at the root (for Gitleaks, `.gitleaks.toml` with `[extend] useDefault = true` and one `[[rules]]` entry each): one rule per identifier format the data this product touches holds, taken from the stores `AGENTS.md` lists: a national identity number such as a US Social Security number, the product's record or account number format, a date of birth beside a name field. Show each rule one synthetic match before adding it. A known false alarm goes in the scanner's committed ignore file by fingerprint, never as a broader rule.
* **In CI:** the same scanner and config on every pull request, run from `origin/main`'s copy like every check, so a commit made without the hook is still caught and a pull request cannot weaken its own check.
* **On the code host:** check that push protection is on (GitHub: `security_and_analysis.secret_scanning_push_protection` from `gh api repos/{owner}/{repo}`; GitLab: the project's secret push protection setting). It is a repository setting: tell the user when it is off and how to turn it on, and never change it.
* **Once, over all history:** run the scanner over every commit (for Gitleaks, `gitleaks git`) and report each finding by commit and file, never its value. Rewriting history is the user's call. A live credential in history is told to the user at once, to rotate first.
* **Made-up data only:** write under Critical Constraints in `AGENTS.md` that test fixtures, seeds, examples and docs hold made-up data only, and nothing is copied from a real system's rows, logs or screenshots. No scanner reliably finds a name or a free-text note; this rule and the security review are the defence there.

List the scanner's config and ignore file under `# owner reads: checks` in `CODEOWNERS`.

## CI

Install from the lockfile. Run each check as its own step, from `origin/main`'s copy of the check scripts and config, so a pull request cannot edit what judges it. Run the whole span of supported runtime versions without stopping at the first failure. Run mutation testing over changed files, the thorough property-test profile, each twin's contract suite (`tests/twins/<service>/`) against recorded real responses on a schedule, and `e2e` against a built artifact, retrying once and labelling a pass-on-retry flaky.

## Landing rules on existing code

Brownfield only, and the user picks one: enforce on files authored from now on; clean up in a subagent as its own change; or ratchet with a committed baseline under `# owner reads: checks`. Adding rules and leaving them red is not an option. The same choice applies to a failing suite: quarantine or fix before it enters the gate.
