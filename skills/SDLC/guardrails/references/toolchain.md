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

## Verify each choice

Before writing the config into the repo:

1. Run the tool once on the untouched codebase.
2. Introduce one violation it should catch.
3. Confirm it exits non-zero and the message says what to do.
4. Remove the violation.

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

### Red-commit scope

One more hook keeps that skip honest. `red-commit-scope` runs on every commit and never goes in a skip list. When `SKIP` names `tests` or `e2e`, it fails unless every staged file is a test file, matching the test paths the test runner's config uses, or a file whose staged diff removes no lines: a stub adds lines only. Commit the script as `scripts/red_commit_scope.py`, pass it the test runner's test paths, and run `python3 scripts/red_commit_scope.py --self-test` once, which fails when the rule stops holding.

```python
#!/usr/bin/env python3
"""Allow SKIP=tests,e2e only for a red commit: test files, plus stubs that add lines only.

Usage: red_commit_scope.py <test glob>...   (the test paths the test runner config uses)
       red_commit_scope.py --self-test
"""
import fnmatch, os, subprocess, sys


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def violations(globs, cwd=None):
    bad = []
    for line in git("diff", "--cached", "--numstat", "--no-renames", cwd=cwd).splitlines():
        added, removed, path = line.split("\t", 2)
        if any(fnmatch.fnmatch(path, g) for g in globs):
            continue
        if removed != "0":  # "-" is a binary file
            bad.append(path)
    return bad


def main(globs):
    skipped = {h.strip() for h in os.environ.get("SKIP", "").split(",")}
    if not skipped & {"tests", "e2e"}:
        return 0
    bad = violations(globs)
    for path in bad:
        print(f"SKIP=tests,e2e is only for the red commit, which holds failing tests and "
              f"stubs that add lines. This commit removes lines from {path}, which is not "
              f"a test file. Commit it without the skip.", file=sys.stderr)
    return 1 if bad else 0


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        git("init", "-q", cwd=d)
        for name, body in [("src.py", "a\nb\n"), ("tests/test_x.py", "x\n")]:
            os.makedirs(os.path.dirname(os.path.join(d, name)) or d, exist_ok=True)
            open(os.path.join(d, name), "w").write(body)
        git("add", "-A", cwd=d)
        git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "base", cwd=d)
        open(os.path.join(d, "tests/test_x.py"), "w").write("y\n")
        open(os.path.join(d, "src.py"), "a").write("def stub(): raise NotImplementedError\n")
        git("add", "-A", cwd=d)
        assert violations(["tests/*"], d) == [], "a test edit plus an added stub must pass"
        open(os.path.join(d, "src.py"), "w").write("a\n")
        git("add", "-A", cwd=d)
        assert violations(["tests/*"], d) == ["src.py"], "removed source lines must fail"
    print("red_commit_scope self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if sys.argv[1:] == ["--self-test"] else main(sys.argv[1:]))
```

```yaml
- repo: local
  hooks:
    - id: red-commit-scope
      name: SKIP=tests,e2e only for the red commit
      entry: python3 scripts/red_commit_scope.py "tests/*" "**/test_*.py"
      language: system
      pass_filenames: false
      always_run: true
```

## CI

- Install from the lockfile, not the manifest.
- Run each check as its own step rather than chaining them.
- Where the ecosystem has more than one supported runtime version, run the whole span and do not stop the matrix at the first failure.
- Set the thorough property-test profile here.
- Run mutation testing over the changed source files as its own step. A surviving mutant fails it.
- Run the e2e slot as its own step against a built artifact, with role-and-label locators and no clock waits; retry a failure once and label it flaky rather than green.
