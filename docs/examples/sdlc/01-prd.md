# PRD: Transaction history export

> Learning example. A deliberately small PRD — three functional requirements — used to show how a product decision becomes a design, then slices, then tests.

| | |
|---|---|
| **Owner** | PM, Payments |
| **Participants** | Eng lead (Payments), Designer, Support lead |
| **Status** | Approved — 4 open questions |
| **Target release** | 2026-Q4 |
| **Links** | [Spec](02-spec.md) · JIRA PAY-1420 · [Support ticket analysis](#) |

## Problem

Customers cannot get their transaction history out of the product. Support
manually runs queries and emails CSV files: 340 such tickets in the last
quarter, averaging 18 minutes of agent time each — 102 agent-hours per quarter. Customers ask for the data
at tax time and at month-end close, so volume spikes are predictable and
currently unstaffable.

## Objective

Remove manual export work from Support, and remove the reason customers open
the ticket at all.

## Success metrics

| Metric | Baseline | Target | Measured by |
|---|---|---|---|
| Manual export tickets per quarter | 340 | < 238 (-30%) | Support tag `manual-export`, 60 days post-GA |
| Self-serve exports completed | 0 | > 500 / month<br>(~113 tickets/month today; Support estimates 4-5x latent demand suppressed by the ticket friction) | `export.completed` event |
| Export failure rate | n/a | < 1% | `export.failed` / `export.started` |

## Users

**Sam, small-business owner.** Exports the prior month at close and hands the
file to a bookkeeper. Works in a spreadsheet, not an API. Does not know what a
webhook is.

## Scope

**In scope**
- Self-serve CSV download of the signed-in account's own transactions.

**Out of scope (non-goals)**
- Scheduled or recurring exports.
- Formats other than CSV (no XLSX, no JSON, no PDF).
- Exporting on behalf of another account, including by Support staff.
- An export API. This release is UI-only.

## Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR1** | A signed-in user downloads their own transaction history as a CSV file. | Must |
| **FR2** | A user constrains the export to a date range before downloading. | Must |
| **FR3** | When a requested range exceeds 50,000 transactions, the user is told to narrow the range rather than receiving a truncated file. | Must |

## UX

Export button on the Transactions page opens a date-range dialog.
[Figma: Transaction export](#) — flows and empty states are there, not here.

## Assumptions, constraints, dependencies

- **Assumption:** a spreadsheet-compatible CSV is sufficient. Unvalidated; the
  first 20 self-serve exports get a follow-up email asking if the file worked.
- **Constraint:** 50,000 rows is the largest export Engineering will commit to
  delivering inside the 60-second gateway timeout, with headroom. Not the
  theoretical maximum. Derivation is in the spec.
- **Dependency:** Support must add the `manual-export` tag before launch, or
  the primary metric has no baseline.

## Open questions

| Question | Owner | Status |
|---|---|---|
| Which timezone are dates rendered in — user's, UTC, or account's? | PM | Open |
| Are refunded transactions included? | PM + Support | Open |
| Are pending transactions included? | PM | Open |
| Multi-currency accounts: one amount column or one per currency? | PM + Eng | Open |

> These four surfaced while writing the slice tests, not while writing this
> PRD. That is normal and is why this section exists.
