---
name: failing-tests
description: "Use this skill whenever tests must be written before the code they test exists or is fixed: for a story's acceptance criteria, a bug or a review finding, or a locked test the user corrects. Use it on: 'write the failing tests', 'tests first', 'TDD this', 'red tests', 'write them red', 'an acceptance test that fails until the feature is implemented', 'add a regression test', 'reproduce this bug, don't fix it yet', 'this test is wrong'. Use it even when the request names a story or bug, if it asks for the tests. Writes one test per example, confirms each fails for its criterion's reason, and commits and locks them."
license: MIT
metadata:
  version: "1.4.0"
---
# Failing tests

Write a change's tests before its implementation exists, from what the change must do and through its interface, then lock them so the implementation must meet them unchanged.

## Words used here

* **Acceptance criterion:** one numbered rule of the change, with one to three examples under it. A fix with no criteria has its reproduction as the one criterion.
* **Example:** Given/When/Then in real values.
* **Interface:** the signatures the change adds or alters (functions, commands, routes, types), committed as stubs whose bodies only raise; or the existing ones the criteria go through.
* **Red commit:** a commit that holds failing tests and nothing else.
* **Lock:** the red commit's hash recorded in git config under `branch.<branch>.redCommit`. Where the story skill's guard hook runs, it refuses a commit that changes a locked test other than by removing its marker, and asks the user before a `git config` command removes or replaces the lock.

## 1. Read the ground

* **Read** the interface and the nearby tests for the framework, fixtures and naming.
* **Run** the existing tests of that area once and note which pass.
* **Read `docs/glossary.md`,** the user's confirmed domain terms, where it exists, and name each test with its terms.

## 2. The test list

Write one numbered line per test:

```text
<n>. <acceptance criterion number> — <test name> — <fixture: the concrete input values> — rejects: <the one wrong implementation a builder could plausibly ship that this fixture fails>
```

* **One test per example under each rule:** a rule with no example gets one test with values you choose from its words. Add a further test only where it rejects a wrong implementation the others pass.
* **A rule over a range or an invariant:** test it with at least two different values. Where the repository already has a property-testing library, such as Hypothesis or fast-check, add one property test of the rule beside its example tests.
* **Interface:** test only through the interface. Never invent a public name, argument or type.
* **Level:** test each example at the lowest level whose interface shows its result. An end-to-end test covers a whole journey a person takes, and it sets up its data through the API or the database, never the UI.
* **Real implementations:** run the real code wherever the test can, even when nearby tests mock it.
  * Use the real collaborators, the database engine production uses (started locally or in a container), the real filesystem in a temporary directory, and a real server on localhost.
  * Never use an in-memory substitute for the database, such as SQLite for Postgres.
  * Double only what a test cannot run or control: a service outside the repository (a payment provider, email, a third-party API), the clock, and randomness.
  * For those, prefer the repository's own fake, then a stub returning fixed values. Mock a call only to check a side effect on an outside service, through the repository's own adapter for it: don't mock what you don't own.
* **Expected values:** take each from the criterion's words, never from what the current code does, which makes a tautological test, or from how you plan to build it.
* **Fixtures:** choose ones a plausible wrong implementation fails. Avoid:
  * a batch of one, or the failing item first or last;
  * the same value in two fields;
  * an identity or default value (quantity 1, discount 0);
  * input already in order, or fewer rows than a page;
  * two calls in sequence for a race;
  * a fake that never fails for a retry;
  * an error test that asserts only the raise and not the state left behind;
  * a sleep: wait by polling for the condition with a deadline;
  * a key, row or file another test also uses: create the test's own with a unique value.
* **Assertions:** assert exact values a person or caller sees. Never assert a private function, internal call order or a log line, and never only that something is non-empty or did not raise.
  * For text a language model generates, assert its schema and required fields, never its exact wording.
* **An example marked `(checked by the user)`:** gets no test and no `Questions:` line.
* **Questions:** a criterion you cannot write as a test (no observable result, an undecided value), or one that needs a public name the interface lacks, gets no test. Put it on `Questions:`.

## 3. Existing tests

An existing test the acceptance criteria contradict is a decision.

* **Contradicted:** change its expected value only when a criterion states the new behaviour. List each change on `Changes existing:` with the criterion that requires it.
* **Not mentioned:** leave it as it is. List it on `At risk:` when the change could break it.

## 4. Red and lock

Write the tests and run them. Each must fail because the behaviour is missing, not because of a typo, an import or a fixture error. List a test that already passes as `characterizing`, or delete it when it adds nothing.

1. **Mark** each failing test with the framework's strict expected-fail marker: pytest `@pytest.mark.xfail(strict=True, reason="red")`, Jest or Vitest `test.failing`, Playwright `test.fail()`, RSpec `pending`, XCTest `XCTExpectFailure("red")` as the test's first line, Swift Testing `withKnownIssue("red") {` on its own line with the closing brace written `} // red`. Mark nothing else, and leave a `characterizing` test unmarked. **No strict marker in the framework:** leave the tests unmarked; the test run fails on them until they pass, and that failure is expected.
2. **Commit** the tests alone, on a branch other than main; on main, create a branch first. The commit message holds the story, or the acceptance criteria when there is no story, the test list and the `Changes existing:` line.
3. **Hook refuses the commit** because a test fails: skip that hook alone by its id and report it. Never skip every hook.
4. **Lock** the commit:

   ```sh
   git config --add branch.<branch>.redCommit $(git rev-parse HEAD)
   ```

After the lock, change no locked test, and no test that existed where the branch left main, except to remove its marker once the code makes it pass. Put every later test in a new test file.

## Later tests

* **A confirmed review finding:** write one test that fails on it, through the interface its criterion names, marked as above. Commit it alone in a new test file and lock it the same way.
* **A weak test from a review,** a row naming a wrong implementation the suite lets pass: write, in a new test file, a test that implementation fails. It may pass at once; leave it unmarked then. Commit and lock it the same way.
* **A locked test the user agrees is wrong:**
  1. Save `git config --get-all branch.<branch>.redCommit`.
  2. Run `git config --unset-all branch.<branch>.redCommit`, which the user approves where the guard asks.
  3. Change only that test and commit it alone.
  4. Lock that commit and each saved hash again with `--add`.

## Report

Show the user:

```text
Red: <hash>; tests: <paths>; <n> failing, <n> characterizing; marker: <the expected-fail marker used, or "none in this framework">
Tests:
  <the numbered test list>
Changes existing: <test name — the acceptance criterion that requires it>; or "none"
At risk: <existing test names the change could break that the acceptance criteria do not mention>; or "none"
Doubles: <each double used, and why the real implementation cannot run in the test>; or "none"
Questions: <one line each: the acceptance criterion, and what must be decided>; or "none"
```
