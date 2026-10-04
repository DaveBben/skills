# Overspending rules R14–R17

An excerpt of the finance rule set. Each rule names its source, a source tag and an evidence grade. A number no source sets is a household choice, marked **(configurable)**: read it from the settings file's `[scripts]` table or `profile.md`.

* **Tags:** [OFF] is an official source read directly (YNAB's own guide and API specification for YNAB mechanics, the IRS). [STUDY-R] is a study as quoted in a research summary. [ARITH] is arithmetic on the budget's own data.
* **R3:** never cover overspending from a retirement category or account; a Roth IRA withdrawal can be put back only as a 60-day rollover (IRS Pub 590-A) [OFF].
* **R11:** targets other than contract bills are re-priced once a quarter from the 12-month spend rate, never when covering.
* **R20 criterion c:** a practice-payment trial month passes only if every overspend that month was covered from R14 step 1.

* **R14. Cover a routine overspend in the month it happens, in the configured order, stopping at the first source that covers it:** Cover before the month rolls over. At the rollover YNAB resets each negative category to zero: uncovered cash overspending is subtracted from next month's Ready to Assign, and uncovered credit-card overspending stays as card debt the card payment category does not cover. YNAB's guide advises against editing a past month, so a cover on the 1st is too late [OFF, YNAB]. The default order is:
  1. unspent money in want categories this month;
  2. this month's assignment to the trial category, which fails that trial month under R20;
  3. the emergency fund, with repayment scheduled under R16;
  4. true-expense sinking funds and bill funds, last.

  Never use the surprise fund for a routine overspend. Never move money out of a credit-card payment category. Never move money out of a retirement category. Source: [ARITH] for each step: step 1 leaves no dated payment unfunded; steps 2 and 3 reduce net worth by the same amount, so their order is a household choice (configurable) set so the trial measures something; step 4 creates a shortfall on a known due date. Money moved out of a card payment category becomes card debt in YNAB's model [OFF, YNAB]. Cheema & Soman on slack categories [STUDY-R]. Grade C.
  Group bills in a want category: diners ordered 36% more when a bill was split evenly than when each paid alone (Gneezy, Haruvy & Yafe 2004, restaurant field experiment with strangers) [STUDY-R]; suggest paying only your own share. Grade B.
* **R15. Keep the surprise fund for surprises only:** Fund one surprise category. Each month, move any charge in it that recurred, or that was forecastable, to its own category. Source: Sussman & Alter 2012 on underestimating exceptional expenses [STUDY-R]; Cheema & Soman [STUDY-R]. Grade B.
* **R16. Repay the emergency fund on a schedule:** After any draw, assign a fixed monthly repayment until the fund is back at target, and rank it above every want. The repayment period is a household choice (configurable, default 6 months). Source: [ARITH]. Grade C.
* **R17. Record every cover; change targets only on the R11 schedule:** With each cover, append a line to the covered category's note: month, target, spent, amount covered and the source category. Do not write a new target when covering or closing a month. If a category was covered in 3 of the last 6 months (configurable), raise it at the next quarterly re-pricing. Source: [ARITH]. Grade C.
