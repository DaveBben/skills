# No spec: two ADRs and slice 1

> Learning example. The third point on the spectrum, after
> [the full spec](02-spec.md) and [the XP spec](02b-spec-xp.md). Here the design
> document does not exist. What was load-bearing in it becomes two ADRs, one
> spike finding, and a set of tests.
>
> This file is short on purpose. A long document arguing for fewer documents
> would refute itself.

In a real repository these are two files under `docs/adr/`, not one document.
They are inlined here so the example reads in sequence.

---

## ADR 0007: Stream transaction exports synchronously

**Status:** Accepted — 2026-09-14. Accepted by: Eng lead (Payments), Platform.

### Context

FR1 requires customers to download their transaction history. Nothing in the
product currently returns a file to a browser, and the gateway terminates any
response over 60 seconds. The open question was whether a large export fits
inside that window or needs asynchronous delivery.

A two-day spike answered it. `TransactionQuery` sustains **~1,200 rows/second**
against production-shaped data; a pre-flight `COUNT` on a wide range costs up
to 2 seconds. So 50,000 rows costs 2.0 s + 41.7 s = 43.7 s of a 60 s budget,
leaving ~16 s headroom. The ceiling is nearer 69,000 rows.

The spike code was deleted. This paragraph is the part worth keeping — in a
year, "why is the limit 50,000?" has an answer that outlives whoever ran it.

### Decision

Stream the CSV synchronously from the request. Cap exports at 50,000 rows.
Add no queue, no object storage, and no email path.

### Considered options

| Option | Rejected because |
|---|---|
| Async job → object storage → email link | Three new production dependencies for a dataset that streams in under a minute. The spike removed the reason to consider it |
| Buffer the whole CSV, then send | Memory scales with account size; a large account takes the process down |
| Paginate, client stitches the files | Pushes correctness into the browser and produces several files for a user working in a spreadsheet |
| Raise the gateway timeout | A global change to serve one endpoint. Rejected by Platform |

### Consequences

- No new infrastructure and no new on-call surface.
- Accounts whose common date ranges exceed 50,000 rows cannot export in one
  file. Accepted; revisit as async if it is reported more than twice.
- The 50,000 figure is bound to the measured throughput. If `TransactionQuery`
  gets slower, this limit is wrong and nothing will notice automatically.
  **Accepted hazard, no test.** That is precisely why it is written down.

---

## ADR 0008: Count before streaming; reject over-limit exports

**Status:** Accepted — 2026-09-14. Accepted by: Eng lead (Payments).

### Context

FR3 requires a user whose range exceeds the limit to be told to narrow it,
rather than to receive a truncated file. HTTP sends the status code with the
first byte, so once streaming begins the response is already committed to
`200`. A limit discovered mid-stream can only be honoured by cutting the file
off — which produces a well-formed CSV that looks complete.

### Decision

Run `COUNT` before writing any bytes. Over 50,000 rows, return `413` naming
the actual count, with no body.

### Considered options

| Option | Rejected because |
|---|---|
| Stream and truncate at the limit | Silent truncation of financial data. Customers discover it in an audit, months later |
| Stream and append a warning row | Still a `200`, still parses, and a spreadsheet user never reads row 50,001 |
| No limit at all | The gateway truncates anyway, at an unpredictable point |

### Consequences

- Every export pays the `COUNT`, including small ones. Measured at up to 2 s
  and inside budget.
- `COUNT` and the subsequent stream are separate reads. A row inserted between
  them changes the count. **Open, deliberately:** off-by-one in a count that
  only gates a limit is not worth a transaction. Revisit if it ever matters.

---

## Then: slice 1

No further design. The next action is code.

**Slice 1 — walking skeleton.** An engineer hits `/export/transactions` behind
the `transaction_export` flag and a CSV file downloads containing two hardcoded
rows, from a real deploy.

**What it discovers**, which is everything the two specs wrote down in advance:

| Discovered by building | Was pre-specified in |
|---|---|
| Content-type, content-disposition, chunked transfer | Full spec's *Response shape* |
| Where the permission middleware attaches | Full spec's seam 1 |
| Whether a streaming response survives the deploy path at all | Nothing. Neither spec would have caught this on paper |
| Whether the UTF-8 BOM question matters | Both specs listed it as an open question, deferred |

**What gets written down afterwards:** nothing, unless a decision was made. The
component names, the column list, and the seams are now visible in the code,
which is a more reliable description of them than a document that can drift.

Slices 2 onward proceed as in [03-vertical-slices.md](03-vertical-slices.md).
The slice sequence does not change — only the paperwork preceding it does.

## Where the obligations went

The spec sections that were neither ADR nor spike did not vanish. They changed
medium.

| Spec section | Now lives as |
|---|---|
| Security: account isolation | Two tests in slice 2, one per direction. Prose does not fail the build; a test does |
| Privacy: no PII in filename or logs | Two tests in slice 2 |
| Observability: three events | Two tests in slice 2, one in the mid-stream failure test |
| Invariant: header stability | A property test in slice 2 |
| Seams | The integration test list, written after slice 1 makes the seams physical |
| Rollout plan | Flag configuration, plus the slice that removes the flag |
| Risks | The two that mattered are ADR *Consequences*. The rest was hedging |

**This is the substantive difference, and it is not about documents.** XP does
not move the content to a smaller file. It moves it to an executable medium
wherever one exists, and writes down only what cannot be executed: a decision,
a rejected alternative, an accepted hazard.

## What you give up

One thing, and it is real: **there is no single surface to review.**

A reviewer who must approve "the export feature" reads two ADRs, finds no
description of the components, and must infer from the code the parts that were
obvious to the team and therefore never written. That cost is invisible to the
team and paid entirely by the reviewer.

For a team reviewing its own work, the cost is zero and the spec was waste. For
a security reviewer, a platform team, or an engineer joining in six months, it
is the whole reason the document format exists.

## Choosing between the three

| | [Full spec](02-spec.md) | [XP spec](02b-spec-xp.md) | ADRs + slice 1 |
|---|---|---|---|
| Teams involved | Several | One, with outside approvers | One |
| Reviewer builds it? | No | Partly | Yes |
| Decisions made before code | Many | Few | Two |
| Coordination surface | One document | One document | Two ADRs and the code |
| Fails when | Nobody reads it; it drifts | Reviewers need more than it holds | An outsider must review or join |

The example feature belongs in the right-hand column. It is presented in all
three because most teams are somewhere in the middle, and the useful skill is
knowing which column you are actually in — not defaulting to the leftmost
because it looks the most thorough.
