---
name: test-table
description: "Use this skill whenever the tests for a change need to be enumerated before any test is written: proposing a test plan, deciding which tests a slice, feature or bug fix needs, or reviewing whether an existing set of tests is complete. Use it on: 'what tests should this have', 'propose the tests', 'which tests do we need', 'test plan for X', 'enumerate the tests', 'test table', 'is this covered', 'what am I missing in the tests', 'review the test coverage for X'. Use it on a bare 'tests?' after a proposal. Produce one table, one row per test, each row naming the rule that generated it and the user-visible failure it prevents; the user accepts or cuts rows. Do not use it to write the tests; that follows acceptance."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Test Table

Propose the tests for one change as a table. The user accepts or cuts rows. Write no test until the table is accepted.

Inputs: the change's acceptance criterion (one falsifiable statement of what a person can observe afterwards) and the code the change touches. Read seams and fields off the existing code, not off a design document.

## The Table

One row per test. `Generator` names the rule below that produced the row. Delete any row with no generator and no requirement behind it.

| Test | Level | Generator | Prevents |
|---|---|---|---|
| The falsifiable assertion | Acceptance, Integration, Unit, Property, Fuzz, E2E, Budget | Requirement, Seam, Type, Cardinality, Both sides, Invariant, Metric, Budget | The user-visible failure it stops |

## Generators

Apply in order. A generator that finds nothing to fire on produces no row.

* **Requirement:** the one acceptance test, driven through the front door the user actually uses.
* **Seam:** one row per boundary crossed: database, queue, third-party API, process edge. Pin the contract against a recorded exchange when the real dependency is unreachable.
* **Type:** for each field touched, what the type can legally hold: empty, null, zero, negative, the delimiter itself, every enum variant.
* **Cardinality:** zero, one and many, for every collection, page or retry.
* **Both sides:** every authorisation check earns a negative test written from the attacker's seat.
* **Invariant:** a round trip, ordering or conservation law becomes one property test. Fuzz only where untrusted input crosses a boundary.
* **Metric:** when a requirement names a metric, the event feeding it earns a test. An uninstrumented metric has no source.
* **Budget:** a strict number on any hot path: latency, memory, row count, cost.

## Cut Rules

* **Assert observable behaviour.** Never assert a private function, internal call order, or a log line.
* **Do not test** the language, framework or standard library.
* **Delete row B** if it only fails when row A fails.
* **Name the user-visible failure** each row prevents. If the answer is "nothing", disposition it as "no test required" in chat and drop the row.
* **State what is deliberately absent** and why: a property deferred to a later change, a fuzz target skipped because nothing parses untrusted input.

## When a Row Exposes a Product Decision

Writing an assertion often exposes a decision nobody has made: timezones, whether refunds count, what the limit is. Stop and put the question to the user. Never guess and encode the guess in a test.
