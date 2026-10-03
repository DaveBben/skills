---
name: quarterly-checkup
description: "Use this skill once a quarter, or when the user says 'quarterly review', 'quarterly checkup', 'check my targets', 'are my targets still right', 'am I on pace for my 401k', 'how much HSA room is left', 'can I still contribute to my IRA', 'will I owe taxes in April', 'audit my subscriptions', or 'how many months does my emergency fund cover'. Re-prices YNAB category targets for inflation, checks 401(k), IRA and HSA contribution pace against the current year's IRS limits, estimates the April tax balance for the tax sinking fund, audits subscriptions, measures emergency-fund months, flags deadlines such as a 60-day IRA rollover window, and writes a dated report."
license: MIT
compatibility: Needs Python 3.11+, network access to api.ynab.com, irs.gov and FRED, and a YNAB personal access token.
metadata:
  version: "0.1.0"
---

# Quarterly checkup

Check the budget against the year: targets against prices, contributions against limits, the tax fund against the April bill, and dates that expire. For YNAB API mechanics, follow the `ynab-api` skill if it is installed.

## Settings

Personal settings live in the directory named by `FINANCE_CONFIG_DIR`, default `~/.config/finance/`. Read `config.toml`, `profile.md` and the `history/` reports since the last checkup before advising. When the directory or `config.toml` is missing, tell the user the path you checked and stop.

* **`config.toml`:** `[ynab]` budget and keychain service (never print the token); `[income]` pay frequency, `base_monthly`, `bonus_months`; `[roles]` category names by role (`fixed`, `steady`, `bill_funds`, `wants`, `savings_goals`, `retirement`, `surprise_fund`, `emergency_fund`, `trial_category`, optional `paused`); `[cpi]` category name → FRED series id; `[scripts]` windows and thresholds.
* **`profile.md`:** household context: pay dates, age, HSA coverage tier, employer contributions, filing status, a planned home purchase. Ask for any fact a check needs that neither file holds; do not assume it.

Run `python3 scripts/checkup.py scan` first. It is read-only and returns the numbers used below.

## 1. Re-price targets

Use the `budget-targets` skill if it is installed; it implements these rules. Otherwise apply them directly:

* **Fixed bills (R10):** target = the current bill from the contract. Never average.
* **Everything else (R11):** target = (last 12 months' net spend ÷ 12) × (1 + the category's 12-month CPI change), from the FRED series in `[cpi]`; all-items CPI for an unmapped category. Price a recurring payee that started or stopped inside the window from its current bill.
* **Goal type (R12):** replay 12 months from a zero balance under refill-up-to and under set-aside; pick the one with fewer months where spend exceeded the available balance. Split a category whose parts need different types (R13).
* **Raise (R17):** each category in `covered_often_raise_target` was covered at month end in at least `cover_raise_count` of the last `cover_lookback_months`; raise it now.
* **Lower (R18):** a refill-up-to category under `underspend_ratio` of target for `underspend_months` straight months drops to its spend rate. Never lower a set-aside fund this way.
* **Check before applying (R30):** show each change with its reason, apply only the ones the user confirms, and refuse a refill-up-to target below the largest month in its window.

## 2. Contribution pace

Look up the current year's limits on irs.gov on every run; never use remembered figures, since they change each year. Cite the page and the date read.

* **401(k):** the elective-deferral limit, plus the catch-up for the user's age. Employer match does not count against the elective-deferral limit.
* **IRA:** the contribution limit across all of a person's traditional and Roth IRAs, and the Roth income phase-out for the filing status. Contributions for a year are allowed until that year's filing deadline in April.
* **HSA:** the limit for the coverage tier (self-only or family) plus the 55+ catch-up. **Employer contributions count toward the limit.** An excess owes a 6% excise each year unless it and its earnings are withdrawn by the return's due date, including extensions (IRS Pub 969). If the tier is unknown, say both answers and ask the user to check the plan election.

Projected year total = year-to-date (from the latest paystub; YNAB does not see payroll deductions) + per-paycheck amount × paychecks left in the calendar year. Count paychecks left from a known pay date and `pay_frequency`. Report room left and the per-paycheck change that lands on the limit. For a category in `paused`, report the unused room and its deadline only; do not push to resume it. `retirement_categories_ytd` shows contributions made through the budget.

## 3. April tax balance

Estimate what will be owed beyond withholding, to set the tax sinking fund (R27):

1. Wages: year-to-date taxable wages + per-paycheck taxable wages × paychecks left (pre-tax 401(k), HSA and premiums excluded).
2. Add income with no withholding: interest and money-market dividends, realized gains, side or self-employment income (with self-employment tax, and half of it deducted).
3. Subtract the standard deduction and apply the brackets for the filing status, both looked up on irs.gov for the current year.
4. Subtract projected withholding (year-to-date + per-paycheck × paychecks left). Add state and local tax on income those payrolls do not withhold.
5. Monthly tax-fund target = (estimated balance due − the tax fund's balance in `bill_funds`) ÷ months until April.

State the inputs that are estimates. Check the underpayment safe harbor in IRS Pub 505 (withholding against current-year and prior-year tax); report it, since it decides whether a penalty is possible.

## 4. Subscription audit

From `recurring_payees`, keep the ones that look like subscriptions: a similar amount most months, a service or digital payee. For each, show the yearly cost, last charge and categories, and ask the user whether they used it in the last month. In a field experiment with 2 million newspaper readers, about half of auto-renew subscribers kept paying without using the subscription (Miller, Sahni & Strulov-Shlain). Flag a payee filed in two categories, and any recurring charge in the surprise fund, which belongs in its own category (R15).

## 5. Emergency fund

Report `emergency_months`: emergency balance ÷ mean monthly essential spending over the window (fixed, steady and bill-fund categories that are not also wants). Compare it with the number of months in `profile.md`; the count is a household choice. After a home purchase, measure it in months of PITIA (principal, interest, taxes, insurance, association dues) plus the largest single expense of the last 24 months (R22).

## 6. Time-sensitive items

List every item with a date, nearest first:

* **IRA rollover window (R4):** each IRA or Roth withdrawal in `tracking_account_outflows_last_60_days` can be redeposited tax-free within 60 days of receipt (`day_60` assumes receipt on the transaction date; confirm with the custodian). Only one IRA-to-IRA rollover is allowed per 12 months across all of a person's IRAs (IRS Pub 590-A).
* **HSA excess:** the payroll cutoff for the next paycheck, if the year is on track to exceed the limit.
* **401(k) top-up:** the last payroll of the year, if room remains and the user wants it.
* **IRA contributions:** the April filing deadline for last year's room.
* **Tax balance:** April 15.
* **Large deposits before a mortgage application (R21):** when `profile.md` describes a planned purchase, every deposit above 50% of monthly qualifying income needs a documented source (Fannie Mae B3-4.2-02). Name each such transfer in the last two statement cycles.

## Report

Write `history/YYYY-MM-DD-quarterly.md` in the settings directory with sections: Targets (old, new, reason, applied or not), Contributions, Tax, Subscriptions, Emergency fund, Deadlines. Lead with the deadlines. Writes to YNAB happen only through step 1, after the user confirms each change.
