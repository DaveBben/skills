# Spec (XP version): Transaction history export

> Learning example. The same feature as [02-spec.md](02-spec.md), written the
> way an XP team would write it. Read both — the difference is the lesson.
>
> The spec proper ends at *What we are not deciding*: 115 lines against the full
> spec's 177, and much of what remains is the spike and the alternatives table,
> which grew rather than shrank. Strip the two teaching sections at the end and
> a real XP team's version is shorter still. **The saving is not mostly in
> length — it is in how many decisions are made before anyone writes code.**

| | |
|---|---|
| **Author** | Engineer, Payments |
| **Approvers** | Eng lead (Payments), Security |
| **Status** | Approved |
| **Links** | [PRD](01-prd.md) · JIRA PAY-1420 · [Slices](03-vertical-slices.md) |

The header survives the cut. It is not design — it records who consented, and
consent is the one thing a conversation cannot leave behind.

## What this document is for

Two things only:

1. **Record the decisions that are expensive to reverse**, and why the
   alternatives lost.
2. **Get Security and Platform to say yes** before work starts.

Everything else in this feature is cheap to change and will be discovered by
building it. That content is deliberately absent — see
[What we are not deciding](#what-we-are-not-deciding).

## Context

Transactions live in `payments.transactions`, indexed on
`(account_id, occurred_at)`. The Transactions page reads them through
`TransactionQuery`, paging at 50 rows. Nothing in the product currently returns
a file to a browser. The gateway kills any response over 60 seconds.

## Spike results

One open question was worth answering before deciding anything, so we built a
throwaway to answer it. Two days, deleted afterwards.

**Question:** can a large export stream inside the gateway timeout, or do we
need a job queue?

**Result:** `TransactionQuery` sustains ~1,200 rows/second against production-
shaped data. A pre-flight `COUNT` on a wide range costs up to 2 seconds.

```
  2.0 s   COUNT
+ 41.7 s  50,000 rows at 1,200 rows/s
= 43.7 s  of a 60 s budget, ~16 s headroom
```

The theoretical ceiling is nearer 69,000 rows. We commit to 50,000, which is
where the PRD's FR3 limit comes from.

**This number is measured, not estimated.** That is the difference between a
constraint and a guess, and it is why the spike came first.

## Decisions

Two, both one-way doors.

### 1. Stream synchronously. No job queue.

The spike shows the whole dataset fits inside the timeout with headroom.

Reversible? **No.** Choosing a queue means running a queue, a bucket, and an
email path in production indefinitely. Three new failure modes and an on-call
burden, adopted before knowing whether they are needed.

### 2. Reject over-limit exports before streaming a single byte.

`COUNT` first. Over 50,000 rows, return `413` naming the count. This is what
makes FR3 possible: once bytes are on the wire the status code is already sent,
and the user receives a truncated file that looks complete.

Reversible? **No.** Silent truncation of financial data is the kind of bug
customers discover in an audit, months later.

## Alternatives considered

The load-bearing section. Not design — a record of what has already been argued,
so it is not argued again in three months by someone who was not in the room.

| Option | Rejected because |
|---|---|
| Async job → object storage → email link | Three new production dependencies for a dataset that streams in under a minute. The spike removed the reason to consider it |
| Buffer the whole CSV, then send | Memory scales with account size; a large account takes the process down |
| Paginate, client stitches the files | Pushes correctness into the browser and produces multiple files. Sam uses a spreadsheet |
| Raise the gateway timeout | A global change to serve one endpoint. Rejected by Platform |

## Security and privacy

Not deferred to emergent design, because a leak is not a refactor.

- **Account isolation** is the invariant that must not break. Tested from both
  directions — that A sees A's rows, *and* that A cannot see B's.
- The export contains PII. The download filename must not leak the account
  name. Rows are never logged.
- Security is a named approver above.

## Observability

The PRD's metrics need a source or they are decoration. Emit
`export.started`, `export.completed`, `export.failed`.

Listed here rather than left to emerge because the PRD's success metrics
depend on them, and a metric with no emitter is discovered after launch.

## Rollout

Behind flag `transaction_export`: internal → 5% → 100%, one week apart. Gate is
`export.failed / export.started` under 1%. Rollback is the flag. No migration,
so no reverse migration.

## What we are not deciding

The section that makes this the XP version. Each item below appears in the
[full spec](02-spec.md) and is omitted here on purpose.

| Omitted | Where it actually comes from |
|---|---|
| **Component breakdown** (`ExportHandler`, `CsvWriter`, `TransactionQuery.stream`) | Refactoring during slices 1–3. Naming three classes before writing one is a guess about boundaries we have not felt yet |
| **The CSV column table** | An *output* of slice 2, recorded once it exists. The full spec presents it as an input, which inverts the order in which it is actually knowable |
| **Response headers** (content-type, disposition, chunked) | Slice 1 discovers all three in an afternoon. Writing them down first saves nothing |
| **The seam table** | Slice 1 makes the seams physical. They still generate the integration tests — the list is just written after the code, not before |
| **Rounding policy** | Dissolved rather than decided: storing amounts as integer minor units makes rounding impossible. That fix was found by trying to write the test, not by designing |
| **Risks table** | The two that mattered became the decisions above. The rest was hedging |

**The test that governs this list:** if getting it wrong costs a refactor, leave
it out. If getting it wrong costs a migration, a customer incident, or a
production dependency, decide it here.

## Open questions

| Question | Owner | Status |
|---|---|---|
| Does `CsvWriter` emit a UTF-8 BOM for spreadsheet compatibility? | Eng | Open — settle in slice 1, which already returns a file |
| Is `COUNT` + stream one transaction or two? | Eng | Open — a row added between them changes the count |

The PRD's four product questions are inherited by link, not restated.

---

## When to write which version

| Write the full spec when | Write this version when |
|---|---|
| Multiple teams own parts of the path | One team owns the whole path |
| A platform or security team must review a design they will not build | Reviewers are the people building it |
| The reader is remote, async, or joins in six months | The reader is in the room |
| The system has no test suite to make refactoring safe | Tests, refactoring and CI are all in place |
| The interface is consumed by code you do not control | You control every caller |

The XP critique lands hardest on the left column's absence. **The more your
situation looks like the right column, the more of the full spec is waste.**

The enabling condition is the one Fowler names in *Is Design Dead?*:
evolutionary design only substitutes for planned design when refactoring is
genuinely cheap. Without tests, this document gets longer, not shorter — and
that is a reason to fix the tests, not to write more spec.
