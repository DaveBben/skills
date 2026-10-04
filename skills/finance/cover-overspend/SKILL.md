---
name: cover-overspend
description: "Use this skill on any day of the month when a YNAB category is overspent: 'I overspent', '<category> went negative', '<category> is overspent', 'cover my overspending', 'cover the clothing overspend'. Covers each negative category in the current month from the user's configured order (wants, then the practice-payment category, then the emergency fund, then bill funds; never the surprise fund, a card payment category, retirement or a paused category), shows the plan, and after the user confirms moves the money and appends one note line per cover. Covers the current month only, before the month rolls over."
license: MIT
compatibility: Needs Python 3.11+, network access to api.ynab.com and a YNAB personal access token.
metadata:
  version: "0.1.0"
---

# Cover overspending

Make every negative category in the current YNAB month whole, from the right source, the day the user notices it. The rules cited as R3, R11 and R14–R20 are in [references/rules.md](references/rules.md); read R14 before the first cover in a session.

For YNAB API mechanics (milliunits, the 200-requests-per-hour limit), follow the `ynab-api` skill if it is installed.

## Why now, not at the start of next month

Cover in the month the overspend happens. At the rollover to the next month, YNAB resets every negative category to zero:

* **Cash overspending** (paid from checking or savings) is subtracted from next month's Ready to Assign.
* **Credit-card overspending** stays on the card as debt that the card payment category does not cover.

YNAB's own guide advises against editing a past month to undo either. A cover on the 1st is too late, so this skill works only on the current calendar month. When the overspend is already in a past month, say so: a cash overspend is now a smaller Ready to Assign, and a card overspend is card debt to fund in the current month's card payment category.

## Settings

Personal settings live in the directory named by `FINANCE_CONFIG_DIR`, default `~/.config/finance/`. Read `config.toml` and `profile.md` before advising. When the directory or `config.toml` is missing, tell the user the path you checked and stop.

* **`[ynab]`:** `budget_id`, and `keychain_service`, the keychain entry holding the token. Never print the token.
* **`[roles]`:** category names by role. Cover sources come from `wants` (list), `trial_category` (the optional practice-payment category), `emergency_fund` and `bill_funds` (list). `surprise_fund`, `retirement` and the optional `paused` list are never sources.
* **`[cover_order] steps`:** the R14 order, default `["wants", "trial_category", "emergency_fund", "bill_funds"]`.
* **`profile.md`:** household context. It overrides a default here when the two conflict; say so.

## Cover

1. **Scan.** Run `python3 scripts/cover.py scan`. It is read-only and prints JSON for the current month: `negative_categories`, a `proposed_plan` of moves and note lines, anything `uncovered`, and `warnings`. Run `scripts/cover.py --help` for the rest.
2. **Check the plan against R14,** whatever the script proposed. The plan takes each negative from the first source in the order that has money, and moves to the next source only for the remainder. The script refuses a `cover_order` step outside the four allowed roles.
   * **Never cover from the surprise fund** for a routine overspend, meaning a category that ran over its own target on ordinary spending. The surprise fund is for charges nobody could forecast (R15). If the overspend is a true surprise, say so and let the user decide.
   * **Never move money out of a credit-card payment category.** That money is already owed on the card; moving it creates card debt.
   * **Never cover from a retirement category** (R3), and skip any category in `paused`.
   * **A draw from the trial category** fails this month's practice-payment criterion c (R20). Say so before the user confirms.
   * **A draw from the emergency fund** needs a repayment next month, ranked above every want (R16). Say so before the user confirms.
   * **A want category overspent on group bills** (memos such as "paid for everyone", paybacks arriving later): suggest paying only your own share next time (R14).
   * **Anything still `uncovered`** after every step: report the amount and ask. Do not reach for a forbidden source.
3. **Show and confirm.** Show the moves and note lines as one table, with each warning, and get the user's approval.
4. **Write.** Save the approved `proposed_plan` (edited as agreed) to a file and run `python3 scripts/cover.py apply plan.json`, which prints a dry run, then again with `--confirm`. It refuses a plan for any month but the current one, and a move out of the surprise fund, a retirement, card payment or paused category.

## Note lines (R17)

Each cover appends one line to the overspent category's note, in this format: `YYYY-MM: target X, spent Y, covered Z from <source>`. Spent is the month's spending so far. Do not change the category's target when covering; targets change only at the quarterly re-pricing (R11), which counts these lines.

Some YNAB MCP servers can set a month's assigned amount but cannot write a category note. Use one for the moves if you like, and use the script for the note lines.
