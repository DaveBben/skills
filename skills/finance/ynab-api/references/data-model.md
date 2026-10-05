# Interpreting YNAB data

## Contents

- [budgeted, activity and balance](#budgeted-activity-and-balance)
- [Goals](#goals)
- [Credit card payment categories](#credit-card-payment-categories)

## budgeted, activity and balance

`balance = previous balance + budgeted + activity`, where a negative previous cash balance is first reset to zero.

A sinking fund shows small `activity` against a large `balance` until its bill lands. That is the fund working. Compare a sinking fund's target with its yearly spend, never with one month's activity.

`budgeted` equal to `activity` to the cent, month after month, on a variable category means the user assigns after spending to land the balance on zero. The category is then a ledger, not a limit, which changes what "overspent" means for it.

## Goals

| `goal_type` | `goal_target` means |
|---|---|
| `NEED` | amount per cadence period; `goal_needs_whole_amount` true is "Set aside another", false is "Refill up to" |
| `TB` | a balance to reach |
| `TBD` | a balance to reach by `goal_target_date` |
| `MF` | monthly funding |
| `DEBT` | a debt payment |

Patching `goal_target` on a category whose type is wrong changes the amount and keeps the wrong type.

## Credit card payment categories

Every on-budget card has a payment category that YNAB funds as you spend on the card. Exclude these from spending analysis; their activity is payments, not purchases. Never move money out of one to cover an overspend: the moved amount becomes unpaid card debt. After large budget edits they re-derive themselves and can leave a small residual.
