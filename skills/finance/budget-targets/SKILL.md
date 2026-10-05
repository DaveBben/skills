---
name: budget-targets
description: "Use this skill when YNAB category targets must be set, checked or re-derived from the user's own spending: 'what should my targets be', 'recompute my targets', 'is this target too high or too low', 'am I underfunding anything', 'should this be set aside or refill up to', 'adjust my targets for inflation', 'quarterly target review', 'at what purchase size should I check the budget'. Derives each target from the current bill or the price-adjusted 12-month spend rate, picks the goal type by replaying the last year, and writes only the targets the user approves, one by one."
license: MIT
metadata:
  version: "0.1.0"
---
# Budget targets

Set every category's monthly target from what it actually costs, choose the goal type by replaying the past year, and write only what the user approves. Run [scripts/derive_targets.py](scripts/derive_targets.py). Read its report with the user and decide the cases it flags.

For API traps (milliunits, splits, transfers, carry-forward of overspending) and what the write endpoints can do, use a YNAB API reference such as the `ynab-api` skill in this plugin if it is installed.

## Settings

The script reads `config.toml` in the directory named by `FINANCE_CONFIG_DIR`, or `~/.config/finance/` when unset. Read `profile.md` in the same directory before advising. When `config.toml` is missing, tell the user the path and offer to create it with these keys:

| Key | Use |
|---|---|
| `[ynab] budget_id`, `keychain_service` | Which budget; the macOS keychain service holding the YNAB personal access token |
| `[roles] fixed` | Contract bills. Target = the current bill |
| `[roles] steady`, `wants` | Purchase decisions; the purchase threshold is computed over these |
| `[roles] bill_funds` | Sinking funds for known lumpy bills; derived like any spending category |
| `[roles] emergency_fund`, `surprise_fund`, `savings_goals`, `trial_category`, `retirement` | Balance or dated goals; reported "by hand", never derived |
| `[cpi]` | Category name to FRED series id, e.g. `"Dining Out" = "CUSR0000SEFV"` |
| `[scripts] months`, `long_months`, `cpi_default` | Window (default 12), long window for rare funds (default 36), series for unmapped categories (default `CPIAUCSL`; `""` for none) |

A category with no role is derived from its spending.

## Run it

```bash
python3 scripts/derive_targets.py            # report to <config dir>/history/<date>-targets.md
python3 scripts/derive_targets.py --fresh    # re-fetch YNAB and FRED first
python3 scripts/derive_targets.py --apply --only "Dining Out" --only "Groceries"
python3 scripts/derive_targets.py --selftest # checks the rules on synthetic data, no network
```

Three YNAB GETs and one FRED CSV per CPI series, cached in `<config dir>/cache/`. `--no-cpi` skips FRED. `--apply` always re-fetches, and writes `goal_target`, `goal_needs_whole_amount` and `goal_frequency: monthly` only for the categories named with `--only` (or confirmed one by one when run in a terminal). It snapshots each category before and after to `history/` and appends one line per change to `history/<date>-budget-targets.md`.

## The rules the script applies

* **Fixed bills (roles.fixed): the current bill.** The target is the latest bill divided by its billing period in months, read from the gaps between bills. Do not average a contract. A monthly bill gets refill-up-to; a bill spread over several months gets set-aside. Confirm each amount against the contract, and sum the bills when one category holds several.
* **Everything else: the price-adjusted spend rate.** Target = (last 12 complete months of net spend ÷ 12) × (1 + the category's 12-month CPI change), rounded to $5. A 12-month mean is centred about six months back and the target applies about six months forward, so the gap is about a year of price change. Net spend subtracts reimbursements. History under an archived name of the form `Old (-> New)` counts toward `New`.
* **Rare funds: a longer window.** When a category spent in fewer than two of the last 12 months, the rate is taken over `long_months`. Fewer than two spending months in that window is reported "by hand": set it from the expected bill and its date.
* **Goal type: replay the year.** Starting from a $0 balance, the script replays the window twice at the target, once as refill-up-to ("Refill up to", tops the balance back to the target) and once as set-aside ("Set aside another", adds the target every month). A month is uncovered when its spend exceeds the available balance. Set-aside is chosen only when it leaves fewer uncovered months. Set-aside never leaves more, so refill-up-to results only when the two tie.
* **No cap on a lumpy fund.** A refill-up-to recommendation below the window's largest month is marked REFUSED and cannot be applied. Decide it with the user: usually set-aside, or split the category (below).
* **Purchase-decision threshold.** Over `steady` and `wants` categories only, the smallest of the largest purchases that together carry half the money. Fixed bills are excluded because they are not purchase decisions.

## Reading the report

1. **Spending in archived or uncategorized categories.** Fix routing first: this money counts toward no target. Rename an archived category `Old (-> New)` to fold its history into `New`, then re-run.
2. **"first spend in month k" notes.** The script cannot see when a category was created. If it is newer than the window, the rate is too low; ask the user and set it by hand.
3. **REFUSED rows and "by hand" rows.** Decide each with the user.
4. **The Change column.** `amount`, `type`, `cadence` or `new target` is what differs from today. A row whose current type is `TB`, `TBD`, `MF` or `DEBT` must be changed to a NEED target in the YNAB app before the script can patch it; the API cannot change goal type.

## Split when the parts need different goal types

A category carries one target. When part of a category spends steadily and part lands in lumps (personal care plus clothing, a monthly fee inside a repair fund), the replay sees one blended series and picks a type that fits neither. Split the parts into two categories, each with a note saying what it includes and what it excludes, and re-derive both. Never merge two categories whose replays give different types. The `category-fit` skill in this plugin runs this test with `--split` if it is installed.

Also split out a recurring payee that started or stopped inside the window: set its part from its current bill and the rest from the spend rate.

## Writing targets

* **Confirm each category with the user** before naming it in `--only`. Show current and recommended amount and type. A yes to one category is not a yes to the next.
* **Never write a REFUSED or by-hand row** from this script. Set those in the YNAB app or with a separate confirmed write.
* **YNAB MCP servers** often set only the month's assigned amount and cannot write `goal_target` or `goal_needs_whole_amount`; use the script or the app.

## When to run it

* **Re-derive targets once a quarter**, and only then. Between re-derivations, record covers but leave targets alone.
* **Raise a target at the next re-derivation** when the category was covered from elsewhere in 3 of the last 6 months.
* **Lower a refill-up-to target** that spent under 70% of it for 3 straight months, to its spend rate at the next re-derivation. Never apply this to set-aside funds: a set-aside fund spending nothing is the fund working.

Read the 3-of-6 and 70%-for-3 thresholds from `[scripts] cover_raise_count`, `cover_lookback_months`, `underspend_ratio` and `underspend_months` when set.
