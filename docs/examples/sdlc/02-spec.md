# Spec: Transaction history export

> Learning example. The design document that answers HOW for [the PRD](01-prd.md).

| | |
|---|---|
| **Author** | Engineer, Payments |
| **Approvers** | Eng lead (Payments), Security |
| **Status** | Approved |
| **Links** | [PRD](01-prd.md) · JIRA PAY-1420 · [Slices](03-vertical-slices.md) |

One spec, not several: a single team owns every component this touches, and no
part of it ships on a separate cadence.

## Context

Transactions live in `payments.transactions`, indexed on
`(account_id, occurred_at)`. The Transactions page already reads them through
`TransactionQuery`, paging at 50 rows. Nothing in the product currently returns
a file to the browser, so there is no precedent for content-disposition
handling, streaming responses, or large-response timeouts.

The gateway terminates any response that takes longer than 60 seconds.
Measured throughput of the existing query is ~1,200 rows/second, and the
pre-flight `COUNT` described below costs up to 2 seconds on a wide range. That
gives the PRD's 50,000-row limit:

```
  2.0 s   COUNT
+ 41.7 s  stream 50,000 rows at 1,200 rows/s
= 43.7 s  of a 60 s budget, leaving ~16 s headroom
```

50,000 is not the theoretical maximum — that is nearer 69,000 rows. It is the
largest number Engineering will commit to with headroom for a slow database
day.

## Goals

- Stream a CSV of one account's transactions within the gateway timeout.
- Reuse the existing permission middleware. No new authorization path.
- Constant memory regardless of export size.

## Non-goals (design scope)

- No new infrastructure — no job queue, no object storage, no email sender.
- No changes to `TransactionQuery`'s existing paged read path.
- No caching of generated files.

These differ from the PRD's non-goals, which bound the *product*. These bound
the *design*.

## Proposed design

```
Browser
  │  GET /export/transactions?from=&to=
  ▼
[HTTP handler] ──seam 1──> [PermissionMiddleware]   (existing, unchanged)
  │
  ├──seam 2──> [TransactionQuery.stream(account_id, from, to)]  (new method)
  │                        │
  │                        ▼
  │                   payments.transactions   (existing index)
  ▼
[CsvWriter] ──seam 3──> HTTP response stream
```

**Components**

| Component | Status | Responsibility |
|---|---|---|
| `ExportHandler` | New | Parse and validate range, enforce row limit, set headers |
| `TransactionQuery.stream()` | New method | Cursor over rows for one account, no buffering |
| `CsvWriter` | New | Turn a row into a CSV line. Pure, no I/O |
| `PermissionMiddleware` | Existing | Resolve the signed-in account. Unchanged |

**Row limit.** `ExportHandler` runs a `COUNT` before streaming. Over 50,000, it
returns `413` with a message naming the count, and writes no body. Counting
first is what makes FR3 possible: once bytes are on the wire the status code is
already sent and the user gets a truncated file that looks complete.

**Response shape**

```
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename="transactions-2026-01-01-2026-03-31.csv"
Transfer-Encoding: chunked
```

Header row is always emitted, including for an empty result. Rows are ordered
by `occurred_at` ascending.

**Columns**

| # | Column | Type | Rendering |
|---|---|---|---|
| 1 | `occurred_at` | timestamp | ISO 8601 date. Timezone is an open question in the PRD |
| 2 | `description` | string, nullable | Merchant name. Null renders as an empty field |
| 3 | `type` | enum | One of `charge`, `refund`, `payout`, `adjustment` |
| 4 | `amount` | integer, minor units | Exact division by 100, two decimal places. **No rounding policy is needed and none exists** — amounts are stored as integer minor units, so rendering cannot round |
| 5 | `currency` | ISO 4217 | Multi-currency handling is an open question in the PRD |
| 6 | `balance_after` | integer, minor units | As `amount` |

Column count and order are fixed. This table is what the unit tests enumerate
against, field by field.

## Seams

The integration test list comes from this table — **at least** one test per
row. A seam carrying several obligations yields one test per obligation, not
one per seam.

| # | Boundary | What must hold |
|---|---|---|
| 1 | `ExportHandler` ↔ `PermissionMiddleware` | Unauthenticated requests never reach the query |
| 2 | `TransactionQuery` ↔ database | Returns only the requesting account's rows, honours the range |
| 3 | `CsvWriter` ↔ HTTP response stream | Backpressure holds; memory stays flat; a failure anywhere upstream does not yield a file that looks complete. That last obligation spans seams 2→3: the fault originates at the database and must not be swallowed by the writer |

## Invariants

The property test list comes from here.

- **Round trip:** `parse(render(rows)) == rows` for any set of rows, including
  merchant names containing commas, double quotes, and newlines.
- **Isolation:** the row set rendered for account A contains no row whose
  `account_id` is not A.
- **Header stability:** column count and order match the header row for every
  emitted line.

## Alternatives considered

| Option | Rejected because |
|---|---|
| Async job → object storage → email link | Adds a queue, a bucket, and an email path for a dataset that streams in under a minute. Three new failure modes to run in production for no user-visible gain |
| Buffer the whole CSV, then send | Memory scales with account size; a large account can take the process down |
| Paginate the export, client stitches files | Pushes correctness onto the browser and produces multiple files. Sam uses a spreadsheet |
| Raise the gateway timeout | Global change to serve one endpoint. Rejected by Platform |

## Cross-cutting concerns

- **Security.** Account isolation is the one thing that must not break; it is
  tested from both directions, not just the positive case. Security is a named
  approver on this doc.
- **Privacy.** The export contains PII. `filename` must not leak the account
  name. Rows are never logged.
- **Observability.** Emit `export.started`, `export.completed`,
  `export.failed`, with row count and duration. `export.completed` is the
  PRD's second metric — without this emission the metric has no source.
- **Cost.** No new infrastructure, so no new spend.

## Testing, rollout, operations

- Ships behind flag `transaction_export`, internal accounts first.
- Rollout: internal → 5% → 100%, one week apart. Metric watched between steps
  is `export.failed / export.started`.
- Rollback is the flag. No migration, so no reverse migration.
- Runbook: alert on failure rate > 1% over 15 minutes.

## Risks

| Risk | Mitigation |
|---|---|
| An account grows past 50,000 rows in a common range, making export unusable | The `413` names the count so the user can narrow. Revisit as async if it happens often |
| `COUNT` on a wide range is itself slow | Covered by the existing `(account_id, occurred_at)` index; budgeted at 2 s above and verified in slice 5, which introduces the `COUNT` |
| Spreadsheet software mis-parses UTF-8 | Assumption logged in the PRD; the follow-up email tests it |

## Open questions

| Question | Owner | Status |
|---|---|---|
| Does `CsvWriter` emit a UTF-8 BOM for spreadsheet compatibility? | Eng | Open — decide in slice 1. This is encoding, not escaping, and slice 1 already returns a file, so it is cheapest to settle there |
| Is `COUNT` + stream one transaction or two? | Eng | Open — a row added between them changes the count |

The four open questions in the PRD are product decisions and are not
duplicated here. This spec inherits them by link.
