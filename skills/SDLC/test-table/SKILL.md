---
name: test-table
description: "Use this skill whenever the tests for a change need to be enumerated before any test is written: proposing a test plan, deciding which tests a slice, feature or bug fix needs, or reviewing whether an existing set of tests is complete. Use it on: 'what tests should this have', 'propose the tests', 'which tests do we need', 'test plan for X', 'enumerate the tests', 'test table', 'is this covered', 'what am I missing in the tests', 'review the test coverage for X'. Use it on a bare 'tests?' after a proposal. Produce one table, one row per test, each row naming the rule that generated it and the user-visible failure it prevents; the user cuts rows and adds rows; a row not cut is accepted. Do not use it to write the tests; that follows acceptance."
license: MIT
compatibility: any-agent
metadata:
  version: "1.6.1"
---
# Test Table

Propose the tests for one change as a table. The user cuts the rows they do not want and adds any they do; a row not cut is accepted. Write no test until the table has been in front of the user.

Inputs: the change's acceptance criterion (one falsifiable statement of what a person can observe afterwards) and the code the change touches. Read seams and fields off the existing code, not off a design document.

## The Table

One row per test. `Generator` names the rule below that produced the row. `Killed by` names the one-line implementation change that must turn the row red. Delete any row with no generator and no requirement behind it. Delete any row whose `Killed by` is a change production never makes.

| Test | Level | Generator | Prevents | Killed by |
|---|---|---|---|---|
| Given <a concrete starting state>, when <a concrete action>, then <what the person sees>, in the domain's nouns with real values | Acceptance, Integration, Unit, Property, Fuzz, Budget | Requirement, Seam, Type, Cardinality, Both sides, Invariant, Metric, Budget | The user-visible failure it stops | The mutation: `WORKERS = 2` to `8`, drop the second `ILIKE` clause, read `a` instead of `u` |

The Test column is written for a reader who will never open the diff. No class, method, symbol or call in it; that precision lives in `Killed by`. A concrete example ("the note already says 'reports fatigue'; the doctor adds 'cough for 3 days'; the screen shows both, fatigue first") beats the rule it illustrates. Before proposing, read the tables in the two most recent red commits and match their register where those rows pass the rule above; otherwise ignore them. Tell the user once per table: read Test and Prevents; Level, Generator and Killed by are for the review.

`Killed by` is the assertion made explicit. Name the mutation at proposal time. The `review` skill's correctness pass applies it; run alone, apply each mutation yourself once the tests exist and confirm the row goes red.

## Generators

Apply in order. A generator that finds nothing to fire on produces no row.

* **Requirement:** the one acceptance test, driven through the front door the user actually uses. Its level is fixed by the interface the outcome names: a screen is a browser test against the real UI, an API is a request against a running service, a CLI is the command. Never propose it at unit level. This row cannot be cut; cutting it means the criterion is wrong, so return to the criterion. One front-door row per criterion, edge cases in the rows below it. Under a screen, edge-case rows render the real component and drive it by role and label; a row that mocks the store or the renderer is cut. Under a command, only the front-door row runs the command; edge-case rows drive the stage the command calls. A browser row locates by role and label, never by CSS or XPath, and never waits on a clock.
* **Seam:** one row per boundary crossed: database, queue, third-party API, process edge. Pin the contract against a recorded exchange when the real dependency is unreachable.
* **Type:** for each field touched, what the type can legally hold: empty, null, zero, negative, the delimiter itself, every enum variant.
* **Cardinality:** zero, one and many, for every collection, page or retry.
* **Both sides:** every authorisation check earns a negative test written from the attacker's seat.
* **Invariant:** a round trip, ordering or conservation law becomes one property test. Fuzz only where untrusted input crosses a boundary.
* **Metric:** when a requirement names a metric, the event feeding it earns a test.
* **Budget:** a strict number on any hot path: latency, memory, row count, cost. Read the root instructions file's constraints, whatever the section is called; every constraint this change touches earns a row, with the constraint's own number as the assertion.

## Cut Rules

* **Assert observable behaviour.** Never assert a private function, internal call order, or a log line.
* **Do not test** the language, framework or standard library.
* **Delete row B** if it only fails when row A fails.
* **Delete a row that is already green** on the current code; it asserts today's behaviour, not the change.
* **Name the user-visible failure** each row prevents. If the answer is "nothing", disposition it as "no test required" in chat and drop the row.
* **State what is deliberately absent** and why: a property deferred to a later change, a fuzz target skipped because nothing parses untrusted input.

## When a Row Exposes a Product Decision

Writing an assertion often exposes a decision nobody has made: timezones, whether refunds count, what the limit is. Stop and put the question to the user. A decision the PRD already records is cited, not asked. Never guess and encode the guess in a test.
