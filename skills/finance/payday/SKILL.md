---
name: payday
description: "Use this skill when money arrives and must be assigned in YNAB: 'I got paid', 'paycheck landed', 'payday', 'bonus arrived', 'third paycheck this month', 'assign my paycheck', 'what do I do with this paycheck'. Assigns only money already in Ready to Assign, by a fixed priority: fixed and steady gaps, then bill funds, then emergency-fund repayment, then savings goals and the practice payment, then retirement, then wants. Third paychecks and bonuses go to savings goals by rule on arrival. Writes to YNAB only after the user confirms."
license: MIT
compatibility: Needs Python 3.11+, network access to api.ynab.com and a YNAB personal access token.
metadata:
  version: "0.1.0"
---

# Payday

Assign a paycheck that has landed, so each dollar has a job the day it arrives. For YNAB API mechanics, follow the `ynab-api` skill if it is installed.

## Settings

Personal settings live in the directory named by `FINANCE_CONFIG_DIR`, default `~/.config/finance/`. Read `config.toml` and `profile.md` before advising. When either is missing, tell the user the path you checked and stop.

* **`[income]`:** `pay_frequency` (`biweekly`, `semimonthly` or `monthly`), `base_monthly` (the income each month is budgeted on, e.g. two biweekly paychecks), `bonus_months` (month numbers).
* **`[roles]`:** category names by role: `fixed`, `steady`, `bill_funds`, `wants`, `savings_goals`, `retirement` (lists); `emergency_fund`, `trial_category` (strings). `trial_category` is the practice-payment category, if any. An optional `paused` list names categories that receive nothing on payday.
* **`[scripts] ef_repay_months`:** months to repay an emergency-fund draw, default 6.
* **`profile.md`:** household context, including a known pay date. It overrides a default here when the two conflict; say so.

## Rules

The R-numbers are the rule labels the other finance skills also use.

* **Budget on base income (R6).** Each month's plan fits inside `base_monthly`: two paychecks for biweekly or semimonthly pay, one for monthly pay.
* **Classify income by its source, not by its size (R7).** A paycheck is regular unless it is the third paycheck of a calendar month (biweekly pay produces two such months a year; step 14 days from a known pay date to find them) or a bonus (`bonus_months`, or the user says so). A month is lean only if a paycheck was missed or the pay rate fell.
* **Never assign money not yet received (R8).** Assign only what is in Ready to Assign now. Do not pre-assign next paycheck's money to this month's targets.
* **Repay an emergency-fund draw on a schedule (R16).** The regular plan repays the emergency fund before savings goals and wants, but its line is the fund's whole gap. Cut that line to the draw ÷ `ef_repay_months` per month, and keep that amount each month until the fund is back at target.
* **Third paychecks and bonuses go to goals on arrival (R8).** First repay any remaining emergency-fund draw, then the rest to the first savings goal, the trial category first. The user may name another goal; ask before routing any of it to wants.
* **Leave a bonus out of a planned mortgage payment (R9).** Fannie Mae counts bonus income only after about two years of history (no less than 12 months), averaged, and not if declining (Selling Guide B3-3.3-02).
* **Automate (R1).** Suggest scheduling savings transfers, the trial transfer and bills on or one day after the payday that funds them, when they are not already scheduled.
* **The trial needs base income.** The practice payment counts only when assigned from regular paychecks (R20 criterion a), so fund it in the regular-paycheck plan, not from a bonus.

## Assign

1. **Plan.** Run `python3 scripts/payday.py plan --amount <net amount> --kind regular|third|bonus`. It reads this month's categories and Ready to Assign and returns lines by tier:
   * **regular:** fixed and steady gaps → bill funds → emergency-fund repayment → savings goals (trial first) → retirement → wants.
   * **third or bonus:** emergency-fund gap → everything left to the first savings goal.

   A gap is the category's `goal_under_funded` for the month: what its target still needs. Categories in `paused` and categories without a gap get nothing. If Ready to Assign is below the paycheck, the plan covers only what is there and warns; check that the deposit has imported.
2. **Review.** Show the lines as a table, the amount left unassigned, and which tier ran short. When money is left after every gap is filled, ask where it goes; the default is the first savings goal. When a tier cannot be filled, say which categories wait for the next paycheck.
3. **Write.** After the user approves, save the plan (edited as agreed) and run `python3 scripts/payday.py assign plan.json`, which prints a dry run, then again with `--confirm`. It refuses a plan larger than Ready to Assign or one that touches a paused category. Some YNAB MCP servers can set a month's assigned amount directly; that path works too, but keep the same checks.
4. **Record a bonus or third paycheck.** Append one line to `history/YYYY-MM-payday.md` in the settings directory: date, kind, amount, and where it went. The monthly close reads it to judge whether the trial was funded from base income.
