# Review code the agent built

Loaded by the `reviewing` skill when the subject is code this session or a build subagent made. `deliver` runs it in a review subagent.

Run three passes, separately and in order. Never merge them.

Inputs: the change, its acceptance tests and the accepted test table (an index table with a `Killed by` column naming the one-line mutation that must turn the row red). When `deliver` ran, both are in the red commit message; read them from git. When no table exists, use the tests the change added. The check command is the one `AGENTS.md` names; when none is named, run the linter, the type checker and the tests. The permitted directory is the one the build instruction named; when none was named, it is the repository root. When no change is named, review the working tree against the last commit; when that diff is empty, ask which commit range to review rather than reviewing the whole repository.

## 1. Correctness

* **Run the mutation step over the changed files** where the harness has one; a surviving mutant on an accepted row is the finding. Where no runner exists, apply every `Killed by` mutation from the accepted test table by hand, and every builder-added test by its listed `Killed by`, one at a time, and confirm the named row goes red. A row that stays green asserts nothing: fix the test, not the mutation. When no table exists either, mutate one line per test. Where a `Killed by` names an observable change instead of a line, find the line in the built code that produces the behaviour and mutate that. A surviving mutant you judge cannot change behaviour (`>=` for `>` on a value never equal) is listed with its reason; when it sits on a line an accepted row's `Killed by` names, or in a path under a `# owner reads:` heading of `CODEOWNERS`, it goes on the `Exceptions:` line too, since that judgement is the review grading the build's own test.
* **Diff every accepted test file against the red commit**, the commit `deliver` makes before the build. Any change to an accepted test is a finding. When no red commit exists, say so in the Done block.
* **Check every accepted test is present** and asserts observable behaviour.
* **Delete tests asserting incidental detail** of how the code was built: a private function, internal call order, a log line. The user's feature acceptance test, in the test tree's `feature-acceptance` directory, is outside every pass: never edit, delete or re-mark it.

## 2. Subtraction

Delete anything no requirement asked for:

* Config with one value.
* An interface with one implementation.
* A parameter only ever passed its default.
* Unrequested retry, backoff, caching or feature flags.
* Error handling for cases no test names.
* Logging no one asked to read.
* A class where a function does.

**Delete, do not research.** When it is unclear whether something is load-bearing, delete it and see what fails; a green suite then means a missing test.

**Invert this in old code.** Characterise it with a test first, then delete, then look.

## 3. Scars

* Pinned addresses, ports and hostnames unchanged.
* Concurrency and rate limits unchanged.
* Byte-frozen files unchanged; pin with a hash test where load-bearing.
* Query shapes known to be slow absent.
* No name the change claims already claimed at the merge target: a storage key, a route, a column, an environment variable, a flag, an event name. Grep the target for each new name.
* Nothing touched outside the permitted directory.

## Refactor While Green

Order: passes the tests, reveals intent, no duplication, fewest elements.

* **Intent.** Rename to the domain's own terms. Split any function whose name needs "and".
* **Duplication.** Hunt duplicated *knowledge*: the same rule in the job, the metric and the query will drift.
* **Mechanical change goes through the tool, not the model.** A rename, a signature change or a move across a package uses the language's refactoring tool or a codemod. The same edit in more than three places is a script, committed.

Refactor only toward duplication or confusion pointable-at now. Refactor a file outside the story's diff only to remove duplication this story's code created, and only while the full suite stays green. Any other refactor outside the diff goes on the `Proposed refactor:` line of the Done block, not into the code.

Commit before the refactor and again after it. After the refactor commit, re-run the accepted-test diff against the red commit; a rename the guard let through is still a finding.

## Done

Write this block when all three passes have run. Every line is a fact from this session, never a summary. Run by `deliver`, write it to `done-block.md` in the worktree's git directory (`git rev-parse --git-dir`) and return only whether the review is done, the `Rules:` line and the `Proposed refactor:` lines. Run alone, print it.

```text
DONE
Correctness: <runner or by hand>; one line per accepted and builder-added row: its Test cell, the mutation applied, red or survived; accepted tests unchanged since <red commit>, or the diff
Subtraction: <what was deleted, one line each, or "nothing">
Scars:       <each pinned value checked, or "none pinned">
Refactor:    <renames and merges, or "none">
Proposed refactor: <one line per refactor outside the diff that was not made: the files and the duplication or confusion it removes; or "none">
Decided alone: <the choices the build listed, then the review's own; one line each: what was chosen, why, the tradeoff>
Gate:        <the check command and its result>
Criteria:    <one row per acceptance criterion: the criterion in a few words, the exact test name, and passed as seen in this run>
Changed:     <one line per new function, module or branch: what it is for and its file>
Rules:       <each confirmed finding a pattern could match, for the `guardrails` skill; or "none">
Exceptions:  <one line per code the user must read: <file>:<line>, the equivalent mutant or the finding no failing test confirmed and no reading refuted, and the one test that would settle it; or "none">
```

A survived mutation that is neither fixed nor listed as unable to change behaviour, or a scar that is not checked, means the block cannot be printed and the change is not done. The same holds when the check command errors instead of reporting pass or fail: report the command, its exit status and its output, and stop. `Decided alone:` lists every choice between alternatives the user did not see and did not have to: an internal name, a helper split, a fixture shape, a default a test pins. A choice a later change inherits (a dependency, a port, an address, a schedule, a format, a schema, a domain noun) is asked before it is made, never listed here after. An empty line means no such choice was made, not that none was noticed.
