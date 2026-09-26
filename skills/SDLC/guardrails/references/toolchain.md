# Toolchain

## The slots

| Slot | Fires | The filled slot must |
|---|---|---|
| `fast_fix` | every edit | rewrite one file in place, and exit 0 whether or not it changed anything |
| `fast_check` | every edit | judge one file with no project context, and return a different exit code for "found problems" than for "could not run" |
| `types` | turn end | check the whole project |
| `contracts` | turn end | assert allowed dependency directions, and name the broken rule in the failure |
| `rules` | turn end | match project-specific patterns and print a message written for this project |
| `complexity` | turn end | fail any function over the project's cyclomatic limit and name the function |
| `deps_check` | manifest edit, and commit | fail when the manifest and the lockfile disagree, without hitting the network |
| `env_check` | session start | report whether the environment is built and in sync, naming the command that fixes it |
| `tests` | turn end when the suite fits the turn-end budget, else commit | run the suite, and fail when the whole run exceeds the time limit `AGENTS.md` states |
| `e2e` | CI, and commit when it runs under a minute | drive the interface the product's users use: a real browser, a running service, the command; one test per acceptance criterion |
| `deadcode` | commit | find unreferenced symbols |
| `audit` | commit | check dependencies against a CVE feed |
| `secrets` | commit | scan for credentials |

`types`, `contracts`, `rules` and `complexity` compose the single `turn_end` slot, plus `tests` when the suite fits the budget. `references/claude-guardrails.md` writes the hooks and uses these names.

## Placement

- Edit time: finishes **one file in under a second**.
- Turn end: whole project, **under five seconds**.
- Commit time: everything else, and anything needing the network.

## Filling a slot with no obvious tool

- **No single-file semantic check exists for the language.** Leave `fast_check` returning 0 and wire `types` at turn end.
- **No contract tool exists.** Write the contracts as tests in the project's own test framework, asserting on the import or package graph.
- **`rules`.** Use Semgrep unless the project already has a pattern engine. Rules live in `.semgrep/`, one file per rule, and the `message` field is prose the agent reads, not a rule identifier.

## Settings that are decisions, not defaults

- **Warnings as errors** in the test runner.
- **Strict expected-failure handling.** A test marked expected-fail that starts passing must fail the suite.
- **A dead-code allowlist file, committed, and in the tool's paths from day one.**
- **Coverage thresholds left unset** until there is real code.
- **Suppression comments must name a code.**
- **A cyclomatic complexity limit per function, enforced.** Default 6. Set it once as a project decision and let the agent iterate against it.
- **The lint tool's target language version equals the support floor**, where the tool has that setting. Set above the floor, an auto-fix running in the edit-time hook rewrites code into syntax the floor runtime cannot parse.
- **Property-based test profiles**, where the ecosystem has such a runner: a small example count locally, a large one with no per-example deadline in CI.
- **Mutation testing scoped to the diff, in CI.** Configure the runner to take a path list, and have CI pass it the changed source files. A surviving mutant fails the step. Where the runner finishes over the changed files within the commit-time budget, run it in the commit hook as well.

## The canonical gate

Every layer of the feedback loop is a subset of this list, in this order, cheapest first.

```
format --check
fast_check (whole tree)
rules
complexity
types
contracts
deadcode
audit
tests (with coverage)
e2e
```

Commit one command that runs this list in this order and stops at the first failure: a script named `check` at the repository root, or the equivalent target where the project already has a task runner. CI and the agent call that one command. The commit gate wires each slot of the list as its own hook whose id is the slot's name (`tests`, `e2e`, ...), in the same order, so skipping one hook by id skips exactly that slot. Name the check command in `AGENTS.md`; the change loop and the review call it "the check command".

## Commit time

Install the ecosystem's pre-commit runner. Pin every hook version.

Beyond the canonical gate, the commit gate carries checks that need the diff rather than the code:

- trailing whitespace, final newline, large files added, merge conflict markers, leftover debugger statements
- secret scan
- lockfile in sync with the manifest
- container file lint, where one exists, using a build of the linter that does not need a running container daemon

Scope `audit` to lockfile changes only; it needs the network. Give the user the one command that skips a single hook by id, and state that skipping the whole gate is never the answer.

The red commit is the one commit that skips the `tests` and `e2e` hooks: `deliver` commits failing acceptance tests on their own before any code exists, and those hooks would refuse it. Write the command under Operational Commands in `AGENTS.md` as the red-commit command (with pre-commit it is `SKIP=tests,e2e git commit`). No other commit uses it.

### Red-commit scope and AGENTS.md size

Two more hooks ship as files in this skill's `scripts/` directory. Copy each into the repository's `scripts/` directory unchanged, and run each once with `--self-test`, which fails when its rule stops holding.

* **`red-commit-scope`** (`scripts/red_commit_scope.py`) keeps the red commit's skip honest. It runs on every commit and never goes in a skip list. When `SKIP` names `tests` or `e2e`, it fails unless every staged file is a test file or a file whose staged diff removes no lines: a stub adds lines only. Edit only the test globs in its hook entry, to the test paths the test runner's config uses.
* **`agents-md-size`** (`scripts/agents_md_size.py`) fails an `AGENTS.md` over 100 lines or 8 KB, since every line loads on every turn, and says where the overflow goes.

Both hooks, as pre-commit entries:

```yaml
- repo: local
  hooks:
    - id: red-commit-scope
      name: SKIP=tests,e2e only for the red commit
      entry: python3 scripts/red_commit_scope.py "tests/*" "**/test_*.py"
      language: system
      pass_filenames: false
      always_run: true
    - id: agents-md-size
      name: AGENTS.md under 100 lines and 8 KB
      entry: python3 scripts/agents_md_size.py
      language: system
      files: ^AGENTS\.md$
```

## CI

- Install from the lockfile, not the manifest.
- Run each check as its own step rather than chaining them.
- Where the ecosystem has more than one supported runtime version, run the whole span and do not stop the matrix at the first failure.
- Set the thorough property-test profile here.
- Run mutation testing over the changed source files as its own step. A surviving mutant fails it.
- Run each twin's contract suite (`tests/twins/<service>/`, a fake of a third-party service that an ADR decided) against the real sandbox or its recorded responses on a schedule, as its own job. A failure is drift between the twin and the service, reported with both responses.
- Run the e2e slot as its own step against a built artifact, with role-and-label locators and no clock waits; retry a failure once and label it flaky rather than green.
