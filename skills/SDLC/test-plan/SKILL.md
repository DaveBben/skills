---
name: test-plan
description: "Use this skill when the tests for a change must be listed before any are written, or an existing set of tests checked for gaps. Use it on: 'what tests should this have', 'propose the tests', 'test plan for X', 'which tests do we need', 'enumerate the tests', 'test table', 'is this covered', 'what am I missing in the tests', 'review the test coverage for X', and a bare 'tests?' after a proposal. Produces an index table plus one Given/When/Then block per test, each naming the rule that generated it and the failure it prevents. The user cuts rows by number. Not for writing the tests or the code (`deliver`), acceptance criteria (`story`), or reviewing a finished diff (`review-build`)."
license: MIT
compatibility: any-agent
metadata:
  version: "2.6.1"
---
# Test Plan

Propose the tests for one change as a table. Run alone, the user cuts the rows they do not want and adds any they do; a row not cut is accepted, and no test is written until the table has been in front of the user. Run from `deliver`'s setup subagent, the agent applies the cut rules itself, writes the tests, and the table goes into the pull request description; a row that exposes a product decision is the one thing that still stops for the user.

Inputs: the change's acceptance criteria and the code the change touches. Read seams and fields off the existing code, not off a design document. When no criterion exists, or one offered names no observable outcome, write the criterion the change implies, put it to the user in one line, and propose no rows until it is confirmed. When the code the change touches cannot be found, name the files searched and ask which ones to read.

## The Table

Two parts, in this order. First an index table with short cells. Then one block per test with bold labels. Keep every index cell under forty characters. In the blocks, Given, When and Then each get their own line, and no line runs past one clause.

```text
| # | Test | Level | Generator | Killed by |
|---|---|---|---|---|
| 1 | <title: what the person can do, five to eight words> | Acceptance | Requirement | <the one-line change, or for new code the observable change, that turns it red> |
| 2 | ... | Unit | Type | ... |

**1. <the same title>**
**Given** <a concrete starting state>
**When** <a concrete action>
**Then** <what the person sees, with real values>
**Prevents** <the user-visible failure it stops>

**2. ...**
```

Delete any row with no generator and no requirement behind it. Delete any row whose `Killed by` is a change production never makes.

The Given, When and Then lines are written for a reader who will never open the diff, in the domain's nouns with real values. No class, method, symbol or call in them; that precision lives in the `Killed by` cell. A concrete example ("**Given** the note already says 'reports fatigue' / **When** the doctor adds 'cough for 3 days' / **Then** the screen shows both, fatigue first") beats the rule it illustrates. Before proposing, read the tables in the two most recent red commits and match their register where those rows pass the rule above; otherwise ignore them. Tell the user once per table: read the blocks; the index is for cutting and for the review.

`Killed by` is the assertion made explicit. For code that exists, name the one-line mutation at proposal time. For code the change will add, name the observable change instead, such as "the confirmation email is not sent", and the review finds the line against the built code. Run alone, apply each mutation once the tests exist and confirm the row goes red.

## Generators

Apply in order. A generator that finds nothing to fire on produces no row.

* **Requirement:** the acceptance test for the criterion, driven through the interface the person actually uses. Its level is fixed by the interface the outcome names: a screen is a browser test against the real UI, an API is a request against a running service, a CLI is the command. Never propose it at unit level. This row cannot be cut; cutting it means the criterion is wrong, so return to the criterion. One acceptance row per criterion, edge cases in the rows below it. When a screen only displays what a service returns, the acceptance rows for criteria other than the outcome drive the service beneath the screen. Under a screen, edge-case rows render the real component and drive it by role and label; a row that mocks the store or the renderer is cut. Under a command, only the acceptance rows run the command; edge-case rows drive the stage the command calls. A browser row locates by role and label, never by CSS or XPath, and never waits on a clock.
* **Seam:** one row per boundary crossed: database, queue, third-party API, process edge. Pin the contract against a recorded exchange when the real dependency is unreachable.
* **Type:** for each field touched, what the type can legally hold: empty, null, zero, negative, the delimiter itself, every enum variant. For a value written by something outside this system, add the wrong type, such as a number arriving as a string.
* **Cardinality:** zero, one and many, for every collection, page or retry.
* **Both sides:** every authorisation check earns a negative test written from the attacker's seat.
* **Invariant:** a round trip, ordering or conservation law becomes one property test. Fuzz only where untrusted input crosses a boundary.
* **Metric:** when a requirement names a metric, the event feeding it earns a test.
* **Budget:** a strict number on any hot path: latency, memory, row count, cost. Read the constraints in `AGENTS.md`, whatever the section is called; every constraint this change touches earns a row, with the constraint's own number as the assertion.

## Cut Rules

* **Assert observable behaviour.** Never assert a private function, internal call order, or a log line.
* **Do not test** the language, framework or standard library.
* **Delete row B** if it only fails when row A fails.
* **Delete a row that is already green** on the current code.
* **Name the user-visible failure** each row prevents. If the answer is "nothing", disposition it as "no test required" in chat and drop the row.
* **State what is deliberately absent** and why: a property deferred to a later change, a fuzz target skipped because nothing parses untrusted input.

## When a Row Exposes a Product Decision

Writing an assertion often exposes a decision nobody has made: timezones, whether refunds count, what the limit is. Stop and put the question to the user. A decision the PRD or an ADR already records is cited, not asked. Never guess and encode the guess in a test.
