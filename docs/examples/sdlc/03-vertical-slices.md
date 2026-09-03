# Vertical slices: Transaction history export

> Learning example. How [the spec](02-spec.md) becomes shippable increments.

## The rule applied here

Slices are cut **across** the spec's seams, never along them. The spec is
organized by component; slicing along that structure would produce "build
`CsvWriter`", "build `TransactionQuery.stream`", "build `ExportHandler`" — three
units of work, none demonstrable, integration risk deferred to the end. That is
horizontal slicing wearing a story's clothes.

Every slice below ends with a person able to observe something through the
interface they actually use.

## Slice sequence

| # | Slice | Observable outcome | Chosen for | Covers |
|---|---|---|---|---|
| 1 | **Walking skeleton** | An engineer hits the URL behind the flag and a CSV file downloads containing two hardcoded rows | **Risk.** Proves routing, auth wiring, content-disposition, chunked transfer, and the deploy path — none of which exist in this codebase today | — |
| 2 | **Real data, own account only** | A user with the flag sees their actual transactions in the file | Value | FR1 |
| 3 | **Correct escaping** | Merchant names containing commas, quotes, and newlines survive the round trip into a spreadsheet | Value. Silent data corruption is worse than a missing feature | FR1 (hardening) |
| 4 | **Date range** | The user picks a range and gets only those transactions | Value | FR2 |
| 5 | **Row limit** | A range over 50,000 rows returns a clear "narrow your range" message and no file | Value | FR3 |
| 6 | **Ship it** | Any user clicks Export on the Transactions page | Value | — (delivers no new FR; removes the flag) |

## Why slice 1 has no FR

Slice 1 delivers no requirement and nearly no user value. It is still the right
first slice: it is **observable** (an engineer downloads a real file from a real
deploy) even though it is not yet **valuable**. Its job is to retire structural
risk while failure is cheap — this codebase has never returned a file to a
browser, and every unknown in that sentence surfaces in slice 1 instead of in
week six.

Observable is non-negotiable. Valuable is negotiable for the first slice only.

## Why escaping is its own slice

Slice 3 could be folded into slice 2. It is separated because it carries the
spec's round-trip invariant, and that invariant is where the property test
lives. Keeping it distinct means the property test is written against a slice
that exists to satisfy it, rather than buried in a slice about database reads.

## What is deliberately not a slice

| Not a slice | Why |
|---|---|
| "Add the `stream()` method to `TransactionQuery`" | A layer. Nobody can observe it |
| "Set up the CSV library" | Enabler. Folds into slice 1 |
| "Write the export UI" | Half a slice. The button and what it does ship together, in slice 6 |
| "Backend team does 1–5, frontend does 6" | Horizontal slicing rebuilt as a team split |
| "Email the finished CSV to the account owner" | Not horizontal — it is a **PRD non-goal**. Scheduled and pushed exports are explicitly out of scope, so the slice is rejected before it is sized. This is what the non-goals section is *for* |

## Detailed slice

[Slice 2's full test suite](04-slice-2-tests.md) is written out as the worked
example of what a single slice actually costs in tests.
