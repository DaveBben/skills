---
name: review
description: "Use this skill whenever generated or freshly written code is to be reviewed before it is committed or merged: a slice, a diff, a pull request, a batch of agent output. Use it on: 'review this', 'review the diff', 'review what you built', 'review the slice', 'review the PR', 'check this before I commit', 'what can be deleted', 'is any of this unnecessary', 'did it touch anything it should not have', 'three-pass review'. Run three separate passes in order: correctness (the test would fail if the behaviour were wrong), subtraction (delete everything no requirement asked for), scars (environment facts the model was told not to change). Then refactor while green. Do not use it to find product gaps; that is a question of whether the right thing was built, not whether it was built right."
license: MIT
compatibility: any-agent
metadata:
  version: "1.4.0"
---
# Review

Run three passes, separately and in order. Merged passes mean the second and third do not happen.

Inputs: the change, its acceptance test (the one test a person's observable outcome hangs on), and the accepted test table (one row per test, with a `Killed by` column naming the one-line mutation that must turn the row red). When no table exists, use the tests the change added. The check command is the one the root instructions file names; when none is named, run the linter, the type checker and the tests. The permitted directory is the one the build instruction named; when none was named, it is the repository root.

## 1. Correctness

* **Apply every `Killed by` mutation** from the accepted test table, one at a time, and confirm the named row goes red. A row that stays green asserts nothing: fix the test, not the mutation. When no table exists, mutate one line per test.
* **Check every accepted test is present** and asserts observable behaviour.
* **Delete tests asserting incidental detail** of how the code was built: a private function, internal call order, a log line.

## 2. Subtraction

Delete anything no requirement asked for:

* Config with one value.
* An interface with one implementation.
* A parameter only ever passed its default.
* Unrequested retry, backoff, caching or feature flags.
* Error handling for cases no test names.
* Logging no one asked to read.
* A class where a function does.

**Delete, do not research.** Research biases toward keeping. Deleting takes seconds and a failing test reports the mistake. If it is unclear whether something is load-bearing, that is a missing test: delete it and see what fails.

**Invert this in old code.** Unexplained code in a system running for years is often an undocumented fix. Characterise it with a test first, then delete, then look.

## 3. Scars

Check the silent failures. A model writing config reaches for what looks right, not what is true here.

* Pinned addresses, ports and hostnames unchanged.
* Concurrency and rate limits unchanged.
* Byte-frozen files unchanged; pin with a hash test where load-bearing.
* Query shapes known to be slow absent.
* Nothing touched outside the permitted directory.

## Refactor While Green

Order: passes the tests, reveals intent, no duplication, fewest elements.

* **Intent.** Rename to the domain's own terms. Generated names come from a tutorial. Split a function you cannot name without "and".
* **Duplication.** Each generation has no memory of the last. Hunt duplicated *knowledge*: the same rule in the job, the metric and the query will drift.

Refactor only toward duplication or confusion pointable-at now. Restructuring toward an anticipated shape is speculation.

Commit before the refactor and again after it.

## Done

Print this block when all three passes have run. It is the only evidence the review happened. Every line is a fact from this session, never a summary.

```text
DONE
Correctness: <n> mutations applied, <n> red, <n> survived and fixed: <test names>
Subtraction: <what was deleted, one line each, or "nothing">
Scars:       <each pinned value checked, or "none pinned">
Refactor:    <renames and merges, or "none">
Decided alone: <one line per choice made without the user: what was chosen, why, the tradeoff>
Gate:        <the check command and its result>
```

A survived mutation that is not fixed, or a scar that is not checked, means the block cannot be printed and the change is not done. `Decided alone:` lists every choice between alternatives the user did not see and did not have to: an internal name, a helper split, a fixture shape, a default a test pins. A choice a later change inherits (a dependency, a port, an address, a schedule, a format, a schema, a domain noun) is asked before it is made, never listed here after. The user reverses what they dislike while it is still one commit. An empty line means no such choice was made, not that none was noticed.
