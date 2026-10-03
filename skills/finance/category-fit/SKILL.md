---
name: category-fit
description: "Use this skill when the user asks where a purchase or a new kind of expense belongs in YNAB, or whether to add, split, merge, retire or keep a budget category: 'which category does this go in', 'do I need a category for X', 'should I split X', 'should I merge X and Y', 'can I delete X', 'is my budget too granular', 'category audit', 'clean up my categories'. Tests the proposal against the user's own spending history: a recurring bill raises a target, parts that need different goal types split, categories that need the same goal type and move together may merge, and dead ones are retired."
license: MIT
metadata:
  version: "0.1.0"
---
# Category fit

Decide where spending belongs and whether a category earns its place, from the user's own history. A category is a decision the user makes at every purchase, so add one only when it carries a different kind of target from where the money lands now. Run [scripts/check_category.py](scripts/check_category.py); it is report-only and writes nothing to YNAB.

For API traps (splits, transfers, reimbursements) and what the write endpoints can do, use a YNAB API reference such as the `ynab-api` skill in this plugin if it is installed. To set the target a verdict calls for, use the `budget-targets` skill if it is installed.

## Settings

The script reads `config.toml` in the directory named by `FINANCE_CONFIG_DIR`, or `~/.config/finance/` when unset. Read `profile.md` there before advising. When `config.toml` is missing, tell the user the path and offer to create it. Keys this skill reads:

| Key | Use |
|---|---|
| `[ynab] budget_id`, `keychain_service` | Which budget; the macOS keychain service holding the YNAB personal access token |
| `[roles] fixed` | Contract bills; never merge candidates |
| `[roles] surprise_fund` | The one category for unforeseeable costs; never retired |
| `[roles] emergency_fund`, `savings_goals`, `trial_category`, `retirement` | Balance goals; never retired, merged or judged on spending |
| `[scripts] months` | Window in complete calendar months, default 12 |
| `[scripts] underspend_ratio`, `underspend_months` | Removing test 4, defaults 0.70 and 3 |

## Run it

```bash
python3 scripts/check_category.py                                        # sweep
python3 scripts/check_category.py --add "Pet Care" --match "vet|petco"   # new expense type
python3 scripts/check_category.py --split "Personal Care" --match "cloth|shoe"
python3 scripts/check_category.py --remove "Gifts"
python3 scripts/check_category.py --selftest                             # synthetic data, no network
```

`--match` is a case-insensitive regular expression over payee and memo; give one, because a category name rarely matches a payee. The script reads three cached GETs from `<config dir>/cache/`; pass `--fresh` before acting on a verdict.

## Where one purchase goes

For a single purchase, no script is needed. Put it where its kind of spending already goes, by the category notes. When no note fits, run `--add` for the expense type before inventing a category. Medical, car repair and tax are always their own funds, whatever the numbers say, because each one arrives in amounts too large for any other category to absorb.

## The tests, in order

Every test reads net spending: on-budget accounts only, transfers dropped, refunds subtracted, and history under an archived `Old (-> New)` name counted in `New`.

**Goal type** comes from replaying the window from a $0 balance at the spend rate, once as refill-up-to ("Refill up to", tops the balance back to the target) and once as set-aside ("Set aside another", adds the target every month). Set-aside when it leaves fewer months uncovered, refill-up-to when refill leaves none, otherwise **undecided**: judge it with the user, and an expense that arrives in lumps needs set-aside.

**Adding** (`--add`):

| # | Test | Verdict |
|---|---|---|
| 1 | No net spending matches | Reject; re-run once there is history |
| 2 | One payee, amount within 5%, day of month within 3 days, in 3+ months | Raise the target of the category it lands in by the bill; it is a fixed bill, not a new category |
| 3 | All of it lands in one category | Split it out only if it needs a different goal type from the rest of that category; otherwise reject |
| 4 | Spread over several categories, and per year at least $400, at most 6 payments, largest at least 25% of the total | Add as a set-aside fund at the yearly total ÷ 12 |
| 5 | Otherwise | Leave it where it lands; raise that target if it runs short |

The surprise fund takes only charges nobody could foresee. A charge that recurs or could be forecast moves out of it to its own category; the sweep lists recurring charges it finds there.

**Splitting** (`--split`): split when the matched part and the rest need different goal types. One category carries one target, so a steady part and a lumpy part in one category get a target that fits neither. Write a note on each half saying what it includes and what it excludes.

**Removing** (`--remove`), first that fires:

| # | Test | Verdict |
|---|---|---|
| 1 | It is the surprise fund or a balance-goal role | Keep |
| 2 | No outflow in 6 months, nothing assigned this month, balance under $25 | Retire: hide it in the YNAB app, because the API cannot hide or delete a category |
| 3 | Another category needs the same goal type, their months correlate above 0.7, and neither overran its own target in more than 2 months | Merge into it |
| 4 | Refill-up-to target spent under 70% for 3 straight months | Lower the target to the spend rate at the next re-derivation; never for set-aside funds |
| 5 | None of the above | Keep |

Never merge two categories that need different goal types. The sweep runs tests 2 to 4 over every category and reports category counts for information only; no count limit decides a verdict.

The $400, 6 payments, 25%, 0.7, 2 overruns, 70% and 3 months are household choices with no study behind them. The 70% and 3 months come from the settings above; the rest are constants at the top of the script.

## The judgments the script leaves to you

* **Name the purchase.** Before a merge, ask the user to name a purchase they would decline because one category is empty rather than the other. If they can, keep both.
* **Check what a dead category holds.** It may be the only place a future expense is written down. Then zero its target and keep it.
* **A funded category with no spending is not dead.** Money that leaves by transfer, such as a retirement contribution, shows as no spending. Check `budgeted` across months before retiring.

## After a change

* **Write the note first.** Before the first transaction lands, write what the category includes, what it excludes, and its payees.
* **Merging:** rename the absorbed category `Old (-> New)` and hide it, so its history folds into `New` for target derivation.
* **Creating:** `POST /budgets/{id}/categories` needs a name and a group id. Category order and group order cannot be set through the API; the user arranges them in the app.
* **Order groups by funding priority** in the app: contract bills, then true-expense and bill funds, then savings goals, then wants. Practitioner consensus (YNAB, Ramsey), no study; it puts obligations above the categories money is taken from first.
* **Confirm every write with the user first**, and re-derive the targets of every category the change touched.
