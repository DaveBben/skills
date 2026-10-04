---
name: monthly-close
description: "Use this skill on the last day or two of each month, or whenever the user says 'close the month', 'month-end review', 'close out September', or 'did the practice payment pass this month'. Closes the current month of a YNAB budget before it rolls over: covers any remaining negative categories in the user's configured order (never from the surprise fund, a card payment category or retirement), checks each card payment category against its card balance, judges the practice-payment trial, records each cover, flags sign-flipped duplicate imports, records two monthly measurements and writes a dated close report. Writes to YNAB only after the user confirms."
license: MIT
compatibility: Needs Python 3.11+, network access to api.ynab.com and a YNAB personal access token.
metadata:
  version: "0.2.0"
---

# Monthly close

Close one month of the user's YNAB budget: make every category whole by rule, check the card payment categories, judge the practice-payment trial, and leave a record. The rules cited as R1–R30 are in [references/rules.md](references/rules.md); read R14–R17, R20 and R29 before the first close in a session.

For YNAB API mechanics (milliunits, the 200-requests-per-hour limit, truncated transaction history), follow the `ynab-api` skill if it is installed.

## Settings

Personal settings live outside this skill, in the directory named by the `FINANCE_CONFIG_DIR` environment variable, default `~/.config/finance/`. Read both files before advising. When the directory or `config.toml` is missing, tell the user the path you checked and stop.

* **`config.toml`:** `[ynab]` `budget_id` and `keychain_service` (the keychain entry holding the token; never print the token). `[income]` `pay_frequency`, `base_monthly` (the income the month is budgeted on), `bonus_months`. `[roles]` maps category names to roles: `fixed`, `steady`, `bill_funds`, `wants`, `savings_goals`, `retirement` (lists); `surprise_fund`, `emergency_fund`, `trial_category` (strings; `trial_category` is optional); an optional `paused` list, never a cover source. `[cover_order] steps` is the R14 order, default `["wants", "trial_category", "emergency_fund", "bill_funds"]`. `[scripts]` holds the window (`months`) and the household-choice thresholds the rules mark as configurable.
* **`profile.md`:** free-text household context. It overrides a default in this skill when the two conflict; say so.
* **`history/`:** dated reports these skills write. Read the earlier `*-close.md` files before judging the trial.

## Close the month

Close the current calendar month on its last day or two, before it rolls over. At the rollover YNAB resets every negative category to zero: uncovered cash overspending is subtracted from next month's Ready to Assign, and uncovered credit-card overspending stays on the card as debt the card payment category does not cover. YNAB's own guide advises against editing a past month to undo this.

If the user asks to close a month that has already rolled over, `close.py` prints a warning. Pass it on: YNAB advises against editing a past month, and that month's card overspending is now card debt to fund in the current month's card payment category. Still judge the trial and write the report for that month, but propose no covers inside it.

1. **Scan.** Run `python3 scripts/close.py scan` (the current month; `--month YYYY-MM` for another). It is read-only and returns JSON: negative categories, a proposed cover plan, card checks, trial facts, possible duplicate imports and the R29 numbers. Run `scripts/close.py --help` for the rest.
2. **Cover any remaining negatives (R14).** The plan draws from the `cover_order` steps in order and stops at the first source that covers each negative. The script refuses a `cover_order` step outside the four allowed roles. Check the plan against these, whatever the script proposed:
   * **Never cover from the surprise fund** for a routine overspend. A routine overspend is a category that ran over its own target on ordinary spending. The surprise fund is for charges nobody could forecast (R15).
   * **A want category overspent on group bills** (memos such as "paid for everyone", paybacks arriving later) is not a target problem. Suggest paying only your own share: in a restaurant field experiment with groups of strangers, diners ordered 36% more when the bill was split evenly than when each paid alone (Gneezy, Haruvy & Yafe 2004). Grade B; friends may differ.
   * **Never move money out of a credit-card payment category.** In YNAB that money is already owed on the card; moving it creates card debt.
   * **Never cover from a retirement category** (R3), and skip any category in the optional `[roles] paused` list.
   * **A draw from the trial category** is step 2 and fails this month's trial (criterion c). A draw from the emergency fund needs a repayment line in next month's plan, ranked above every want (R16).
   * **Anything still uncovered** after every step: report it and ask. Do not reach for a forbidden source.
3. **Check card payment categories.** Each `cards` row with `ok: false` is a card whose payment category holds less than the card balance. Propose assigning the gap from Ready to Assign or a step-1 want category before the statement is due. A negative `owed` is a credit on the card.
4. **Record covers (R17).** The plan carries one note line per cover: month, target, spent, amount covered, source. Do not change any target at month end. When `covered_months_in_lookback` reaches the `cover_raise_count` setting (default 3 of 6 months), list that category for re-pricing at the next quarterly checkup.
5. **Duplicate imports.** `possible_duplicate_imports` lists pairs in one account on one date with opposite amounts, both bank-imported: the signature of a feed that imported a credit as a debit. A purchase and its same-day refund look identical, so confirm each pair against the bank's own balance or statement before proposing a delete. The real transaction's `import_id` sign matches the bank.
6. **Judge the trial (R20)**, when `trial_category` is set. Decide each criterion from the scan and the earlier close reports:
   * **a.** Full trial amount assigned (`under_funded` is zero) from base income. If `month_income` exceeds `base_monthly`, read `history/YYYY-MM-payday.md` or ask whether a third paycheck or bonus paid for it.
   * **b.** No trial money moved back out this month or since the last close. Compare `assigned` with the amount in the previous close report.
   * **c.** `covers_beyond_step_1` is empty.
   * **d.** Every card row is `ok`.
   * **e.** No category ended negative before covering, and Ready to Assign is not negative.
   * **f.** `bill_funds_under_target` is empty.

   A month passes only if all six hold. Count passed months and base-income months from `history/*-close.md` against `trial_min_months` and `trial_min_base_months` (defaults 6 and 4). After `trial_fail_streak` failed months in a row (default 2), recommend lowering the planned housing payment, by a lower price ceiling or a larger down payment, and restarting the trial at the new amount.
7. **Record R29.** Report `discretionary_last_3_months` and `emergency_months` (emergency balance ÷ mean monthly essential spending; essential means fixed, steady and bill-fund categories that are not also wants).

## Writing

Show the full set of proposed writes as one table (moves, note lines, deletes, card top-ups) and get the user's approval first. Then:

* **Moves and note lines:** save the approved `proposed_plan` (edited as agreed) to a file and run `python3 scripts/close.py apply plan.json`, which prints a dry run, then again with `--confirm`. It refuses a move out of the surprise fund, a retirement, card payment or paused category.
* **A confirmed duplicate:** `python3 scripts/close.py delete-txn <id>`, then with `--confirm`.
* **YNAB MCP servers:** some can only set a month's assigned amount and cannot write a category note or delete a transaction. Use them for moves if you like, and use the script for the rest. If neither path can write a note, put the R17 lines in the close report instead.

## Close report

Write `history/YYYY-MM-close.md` in the settings directory (YYYY-MM is the month closed). Keep it short and use these headings so later closes can read it back:

* `## Covers`: each move with its R14 step, and any amount left uncovered.
* `## Cards`: each card whose payment category was short, and the fix.
* `## Trial`: one line `trial: pass` or `trial: fail <criteria letters>`, then `base-income month: yes|no` and the trial amount assigned.
* `## Measurements`: the two R29 numbers.
* `## Duplicates`: pairs found, and what was deleted after checking.
* `## For the quarterly checkup`: categories covered often enough to re-price, and anything moved to its own category under R15.
