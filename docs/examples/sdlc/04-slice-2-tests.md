# Tests: Slice 2 — "real data, own account only"

> Learning example. Test headers only, no implementation. The point is where
> each test *came from*, so the last column names its generator.

Slice 2 delivers FR1: a signed-in user downloads their own real transactions.
Escaping (slice 3), date ranges (slice 4), and the row limit (slice 5) are not
in this slice, so their tests are not here either. Neither is anything slice 1
already proved.

## Generators

Seventeen of the 23 tests below were produced by one of four mechanical
questions, not by recalling failure modes.

| Generator | Question it asks | Source |
|---|---|---|
| **Seam** | What boundaries does the design cross? | The spec's seam table — transcription, not invention |
| **Type** | What values can this field legally hold? | The spec's column table, field by field |
| **Cardinality** | What happens at 0, 1, and many? | Any collection, retry, or page |
| **Both sides** | If A can see A's data, can A see B's? | Any authorization check |

The other six come from named sections rather than from a generator: the
acceptance test from FR1, the property test from the spec's invariants, the two
privacy tests from its cross-cutting concerns, and the two observability tests
from the PRD's success metrics. **Not every test has a generator.** Pretending
otherwise would be the tidier lesson and the false one.

## Acceptance (1)

Derived from FR1. Drives the system through the interface the user uses.

- `a signed-in user downloads a CSV containing their own transactions`

## Integration — seam 1: handler ↔ permission middleware (2)

- `an unauthenticated request returns 401 and the query never executes`
- `an authenticated request resolves to the session's account`

## Integration — seam 2: query ↔ database (5)

- `the export contains only rows belonging to the requesting account`
- `account B's transactions are absent from account A's export` — *both sides*
- `an account with zero transactions returns 200 and a header-only CSV` — *cardinality: 0*
- `an account with exactly one transaction returns a header row and one data row` — *cardinality: 1*
- `rows are ordered by occurred_at ascending`

## Integration — seam 3: writer ↔ response stream (2)

- `memory stays flat while streaming a large export (100,000 rows)` — *cardinality: many*
- `a database failure mid-stream aborts the response and emits export.failed, rather than emitting a well-formed partial file`

The row count here is deliberately **above** the eventual 50,000-row limit.
That limit belongs to slice 5; hard-coding it into a slice-2 test would leak a
later slice's constant backwards.

## Integration — privacy (2)

From the spec's cross-cutting concerns. Authorization protects the rows;
these protect everything around them.

- `the download filename contains no account name or identifier`
- `no transaction row appears in logs at any level`

## Property (1)

The spec names three invariants. This is the one testable in slice 2.

- `every emitted line has the same column count and order as the header row`

## Unit — CsvWriter (8)

One per legal value of each field in the spec's column table.

| Test | Generator |
|---|---|
| `a whole amount renders with two decimal places` | Type: number |
| `an amount with minor units renders exactly, without rounding` | Type: number |
| `a negative amount renders for a refund` | Type: number, sign |
| `occurred_at renders as an ISO 8601 date` | Type: date |
| `a null description renders as an empty field, not the string "null"` | Type: string, null |
| `an empty description renders as an empty field` | Type: string, empty |
| `every transaction type maps to the documented row shape` | Type: enum, all four variants |
| `the header row is emitted even when there are no rows` | Cardinality: 0 |

The last test is deliberately paired with its integration counterpart in seam
2. The unit test proves `CsvWriter` emits a header for an empty row set; the
integration test proves the handler returns 200 rather than 404. Same
behaviour, two different things that could break it.

## Observability (2)

The PRD's second metric reads `export.completed` and its third reads
`export.failed / export.started`. Without these emissions the metrics have no
source and the PRD's numbers are decoration.

- `a completed export emits export.completed with row count and duration`
- `a started export emits export.started` — the denominator of the failure rate
  and of the rollout gate

`export.failed` is asserted by the mid-stream failure test in seam 3.

**Total: 23 tests** — 11 integration, 8 unit, 2 observability, 1 acceptance,
1 property.

## This is not a pyramid, and that is correct

Integration outnumbers unit here. Slice 2 is the slice that first connects real
components to real data, so its work is almost entirely seam work. The
unit-heavy shape arrives in slice 3, which is nearly all pure formatting logic
and will produce a dozen unit tests against one integration test.

**The pyramid is a property of a finished suite, not of every slice.** Forcing
each slice to look like a pyramid means writing unit tests for logic that does
not exist yet.

## Deliberately absent

| Test class | Why not in this slice |
|---|---|
| **Property: `parse(render(rows)) == rows`** | Arrives in slice 3, which exists to carry that invariant. Writing it here would fail on unescaped commas — a slice-3 concern |
| **Property: isolation** | The spec names it as an invariant, but it is exercised as two example-based integration tests in seam 2 instead. Generating adversarial multi-account row sets costs more than it returns when the boundary is a single `WHERE` clause |
| **Content-type and content-disposition headers** | Slice 1 proved these. Re-testing a previous slice's deliverable inflates the count without adding coverage |
| **Fuzz target** | Nothing parses untrusted input. This code only *writes* CSV. Fuzzing here would test the test's own parser |
| **E2E** | Slice 6 gets exactly one browser-driven smoke test for the whole feature |
| **Date range tests** | Slice 4 |
| **413 row-limit tests** | Slice 5 |

## Product questions this surfaced

Writing the assertions above forced decisions the PRD never made. None are
decidable by Engineering alone; all four are now open questions in
[the PRD](01-prd.md).

| Assertion that could not be written | Question it raised |
|---|---|
| `occurred_at renders as an ISO 8601 date` | In whose timezone — the user's, UTC, or the account's? |
| `every transaction type maps to the documented row shape` | Are refunded transactions included? |
| `every transaction type maps to the documented row shape` | Are pending transactions included? |
| `a whole amount renders with two decimal places` | Multi-currency accounts: one amount column or one per currency? |

One question resolved itself rather than escalating. Writing
`an amount ... renders exactly, without rounding` demanded a rounding policy —
and the cheapest answer was to make rounding impossible by storing amounts as
integer minor units. **The best outcome of a test you cannot write is a design
change that removes the question.**

**This is the argument for writing tests at slice time rather than at PRD
time.** These gaps are invisible from the PRD and only appear when someone
tries to write an assertion.

## Traceability

Run the chain backwards to find breaks.

| Check | Result |
|---|---|
| Every acceptance test maps to an FR | 1 test → FR1 |
| Every integration test maps to a spec seam or cross-cutting concern | 9 → seams 1–3, 2 → privacy |
| Every FR has at least one acceptance test | FR2 and FR3 pending, slices 4 and 5 |
| Every slice has an observable outcome | Yes — a real file downloads |
| Every unit test maps to a column in the spec's table | Yes, all 8 |
| `export.completed`, `export.started`, `export.failed` each have a test | Yes — 2 in Observability, 1 in seam 3 |
| The PRD's headline metric has a test | **No, and correctly so.** Support-ticket volume is measured externally through the `manual-export` tag. Its risk is not a missing test but a missing dependency: if Support has not added the tag before GA, the metric has no baseline |
