---
name: cover-overspend
description: "Use this skill on any day of the month when a YNAB category is overspent: 'I overspent', '<category> went negative', '<category> is overspent', 'cover my overspending', 'cover the clothing overspend'. Moves money from the user's configured sources into each negative category in the current month, after the user confirms, and records a note line per cover."
license: MIT
compatibility: Needs Python 3.11+, network access to api.ynab.com and a YNAB personal access token.
metadata:
  version: "0.1.0"
---

# Cover overspending

Make every negative category in the current YNAB month whole, from the right source, the day the user notices it.

For direct YNAB API calls outside the script, follow the `ynab-api` skill if it is installed.

## Cover only in the current month

At rollover YNAB resets negatives to zero: a cash overspend then shrinks next month's Ready to Assign, and a card overspend stays as card debt. If the overspend is already in a past month, say so and do not edit the past month. A card overspend is card debt to fund in the current month's card payment category.

## Settings

Personal settings live in the directory named by `FINANCE_CONFIG_DIR`, default `~/.config/finance/`. Read `config.toml` and `profile.md` before advising. When the directory or `config.toml` is missing, tell the user the path you checked and stop.

* **`[ynab]`:** `budget_id`, and `keychain_service`, the keychain entry holding the token. Never print the token.
* **`[roles]`:** category names by role. Cover sources come from `wants` (list), `trial_category` (the optional practice-payment category), `emergency_fund` and `bill_funds` (list). Also `surprise_fund`, `retirement` and the optional `paused` list.
* **`[cover_order] steps`:** the cover order, default `["wants", "trial_category", "emergency_fund", "bill_funds"]`.
* **`profile.md`:** household context. It overrides a default here when the two conflict; say so.

## Cover

1. **Scan.** Run `python3 scripts/cover.py scan`. It is read-only and prints JSON for the current month: `negative_categories`, a `proposed_plan` of moves and note lines, anything `uncovered`, and `warnings`. Run `scripts/cover.py --help` for the rest.
2. **Check the plan against the cover order,** whatever the script proposed. The plan takes each negative from the first source in the order that has money, and moves to the next source only for the remainder.
   * **Never cover from the surprise fund** for a routine overspend, meaning a category that ran over its own target on ordinary spending. The surprise fund is for charges nobody could forecast. If the overspend is a true surprise, say so and let the user decide.
   * **Never move money out of a credit-card payment category.** That money is already owed on the card; moving it creates card debt.
   * **Never cover from a retirement category.** Skip any category in `paused`.
   * **A draw from the trial category** fails this month's practice-payment criterion c, that every overspend that month was covered from the first source in the order. Say so before the user confirms.
   * **A draw from the emergency fund** needs a fixed monthly repayment from next month until the fund is back at target, over 6 months unless `profile.md` says otherwise, ranked above every want. Say so before the user confirms.
   * **A want category overspent on group bills** (memos such as "paid for everyone", paybacks arriving later): suggest paying only your own share next time.
   * **Anything still `uncovered`** after every step: report the amount and ask. Do not reach for a forbidden source.
3. **Show and confirm.** Show the moves and note lines as one table, with each warning, and get the user's approval.
4. **Write.** Save the approved `proposed_plan` (edited as agreed) to a file and run `python3 scripts/cover.py apply plan.json`, which prints a dry run, then again with `--confirm`.

## Note lines

Each cover appends one line to the overspent category's note, in this format: `YYYY-MM: target X, spent Y, covered Z from <source>`. Spent is the month's spending so far. Do not change the category's target when covering. Example: `2026-10: target 150, spent 212, covered 62 from Dining out`.

Some YNAB MCP servers can set a month's assigned amount but cannot write a category note. Use one for the moves if you like, and use the script for the note lines.
