# Interpreting YNAB data

## Contents

- [Income is `month.income`](#income-is-monthincome)
- [Funding is `budgeted`](#funding-is-budgeted)
- [Splits, transfers and reimbursements](#splits-transfers-and-reimbursements)
- [On-budget and tracking accounts](#on-budget-and-tracking-accounts)
- [budgeted, activity and balance](#budgeted-activity-and-balance)
- [Overspending](#overspending)
- [Goals](#goals)
- [Credit card payment categories](#credit-card-payment-categories)
- [Checklist for a spending figure](#checklist-for-a-spending-figure)

## Income is `month.income`

Take income from `month.income` in `/months`. Summing inflows to `Inflow: Ready to Assign` also counts transfers between on-budget accounts, reconciliation adjustments and refunds routed to Ready to Assign, so it overstates income.

`month.income` counts paychecks received in the month. A biweekly earner gets three paychecks in two or three months a year, and those months show about 1.5 times the usual income. A bonus month shows the bonus. Classify a month by which paychecks arrived, not by how far its income sits from the average.

If income must come from transactions, drop transfers and reconciliation adjustments, then reconcile the result with `month.income`.

## Funding is `budgeted`

A category funded every month can show no spending, because its money leaves by transfer: retirement contributions, brokerage deposits, moves to savings. Filtering transfers out, which is right for spending, makes such a category look unused. Check `budgeted` across `/months` before calling a category dead.

## Splits, transfers and reimbursements

* **Splits:** a transaction with a non-empty `subtransactions` array has `category_id: null`. Sum the children. Children have no id the API can update.
* **Transfers:** `transfer_account_id` non-null means money moved between the user's accounts. Exclude it from spending. A transfer to a tracking account is saving.
* **Reimbursements:** a roommate's share, an insurer's payout or a refund arrives as an inflow categorised to the spending category. Net spend is the signed sum per category. When the reimbursement lands in a later month, that month is net negative; clamp a single month at zero for display, but compute rates over the whole window so the offset counts.

## On-budget and tracking accounts

`account.on_budget` decides whether an account feeds Ready to Assign. Checking, savings and credit cards are on budget. Retirement, brokerage, HSA, loans and property are usually tracking accounts. Tracking accounts post large `Reconciliation Balance Adjustment` transactions as market values move; they sit in a raw transaction pull and must be dropped from any spending or income figure.

## budgeted, activity and balance

`balance = previous balance + budgeted + activity`, where a negative previous cash balance is first reset to zero (see below).

A sinking fund shows small `activity` against a large `balance` until its bill lands. That is the fund working. Compare a sinking fund's target with its yearly spend, never with one month's activity.

`budgeted` equal to `activity` to the cent, month after month, on a variable category means the user assigns after spending to land the balance on zero. The category is then a ledger, not a limit, which changes what "overspent" means for it.

## Overspending

* **Cash overspending** (spent from checking or savings beyond the category's balance) leaves the category negative at month end. Next month the category starts at zero and the shortfall is subtracted from Ready to Assign.
* **Credit overspending** (spent on a card beyond the category's balance) also starts the category at zero next month, but the shortfall stays as card debt not covered by the card's payment category.

In both cases next month's category balance shows nothing. To find past overspends, read each month's category `balance` from `/months/{month}` and look for negatives, or read `/money_movements` for the covers.

## Goals

| `goal_type` | `goal_target` means |
|---|---|
| `NEED` | amount per cadence period; `goal_needs_whole_amount` true is "Set aside another", false is "Refill up to" |
| `TB` | a balance to reach |
| `TBD` | a balance to reach by `goal_target_date` |
| `MF` | monthly funding |
| `DEBT` | a debt payment |

`goal_cadence` `1` is monthly, `2` weekly, `13` yearly. A weekly NEED of 100 asks for about 430 a month. Check your reading against `goal_under_funded`.

Through the API you can write `goal_target`, `goal_target_date`, `goal_needs_whole_amount` and `goal_frequency` (monthly, weekly, yearly). You cannot write `goal_type`: a target balance or monthly funding target is set in the YNAB app. Patching `goal_target` on a category whose type is wrong changes the amount and keeps the wrong type.

## Credit card payment categories

Every on-budget card has a payment category that YNAB funds as you spend on the card. Exclude these from spending analysis; their activity is payments, not purchases. Never move money out of one to cover an overspend: the moved amount becomes unpaid card debt. After large budget edits they re-derive themselves and can leave a small residual.

## Checklist for a spending figure

1. Fetched with `since_date` early enough?
2. Splits flattened?
3. Transfers excluded?
4. Off-budget accounts excluded?
5. Credit card payment and internal categories excluded?
6. Deleted and hidden entities filtered, and merged history folded into the category it now lives in?
7. Amounts divided by 1000?
8. Net of reimbursements?
9. Sinking funds compared with yearly spend, not one month?
10. Income from `month.income`?

Cross-check one derived total against a second source in the data before building on it.
