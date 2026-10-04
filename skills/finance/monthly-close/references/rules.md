# Budget rules R1–R30

The evidence-backed rule set the finance skills apply. Each rule names its source, a source tag and an evidence grade. A number no source sets is a household choice, marked **(configurable)**: read it from the settings file's `[scripts]` table or `profile.md`, and use the default shown here only when neither sets it.

## Tags and grades

* **[OFF]:** an official source (IRS, BLS, CFPB, Fannie Mae, the Federal Reserve, YNAB's own API specification for YNAB mechanics), read directly. Grade A.
* **[STUDY-V]:** a study whose abstract or text was read directly. Grade A.
* **[STUDY-R]:** a study as quoted in a research summary, not checked against the paper. Grade B.
* **[RULEBOOK]:** a study as described in an earlier rulebook, not checked against the paper. Grade B.
* **[ARITH]:** arithmetic on the budget's own data, reproducible from the stated inputs. Grade C.
* **[NOT FOUND]:** no source was found; the rule is a household choice. Grade D.

When a rule and a grade A source disagree, the source wins. Say so to the user.

## Income and automation

* **R1. Automate on payday:** Schedule every savings transfer, the payment-trial transfer and every bill on or one day after the payday that funds it. Source: Baugh et al. 2021 on spending at cash arrival [STUDY-R]; Chetty et al. 2014 on automatic contributions [RULEBOOK]. Grade B.
* **R2. Run the surplus gate per person:** Each month, sum each person's received income and outflow, excluding transfers. If outflow exceeds income in 3 of the last 6 months (configurable), stop adding categories and cut the largest outflows first, housing and car included. Source: [ARITH]; BLS consumer expenditure housing share [STUDY-R]. Grade C.
* **R3. Never cover overspending from retirement accounts:** Treat 401(k), IRA, Roth IRA and HSA balances as unavailable to the budget. A Roth contribution withdrawn cannot be put back beyond the annual limit except as a 60-day rollover, so a withdrawal permanently costs tax-advantaged room. Source: IRS Pub 590-A, "You can withdraw, tax free, all or part of the assets from one Roth IRA if you contribute them within 60 days to another Roth IRA" [OFF]. Grade A.
* **R4. Decide any IRA withdrawal before day 60:** For any withdrawal from an IRA or Roth IRA, decide before the 60th day after the money was received whether to redeposit it as a rollover. Confirm the receipt date from the custodian. Only one IRA-to-IRA rollover is allowed in any 12-month period across all of a person's IRAs; trustee-to-trustee transfers and conversions do not count. Source: IRS Pub 590-A [OFF]. Grade A.
* **R5. Keep retirement category notes consistent with R3:** No category note may describe retirement money as available for spending or for a purchase. Source: R3. Grade A.

## Classify income by source

* **R6. Budget monthly life on base income:** Fit each person's monthly plan, including any housing-payment share, inside the settings file's `base_monthly`: two paychecks for biweekly pay, two for semimonthly, one for monthly. Source: paystub arithmetic [ARITH]. Grade C.
* **R7. Classify income by its source, not by its variance:** Mark a month as lean only if a paycheck was missed or the pay rate fell. Do not compute a coefficient of variation on monthly income: a fixed biweekly paycheck plus a bonus produces a high coefficient on fully predictable money. Source: [ARITH]. Grade C.
* **R8. Assign third paychecks and bonuses by rule on arrival:** Assign each third paycheck and each net bonus to the savings goals (or, after a home purchase, the emergency fund and home capital reserve) on the day it lands. Never assign one before it lands. Biweekly pay produces two three-paycheck months a year; find them by stepping 14 days from a known pay date. Source: Baugh et al. on spending at cash arrival [STUDY-R]; [ARITH]. Grade B.
* **R9. Leave a bonus out of a planned mortgage payment until a lender has averaged it:** Fannie Mae counts bonus income only with a history ("a minimum two-year history is recommended; … no less than 12 months"), averaged over year-to-date plus the prior year, and not if it is declining. Source: Fannie Mae Selling Guide B3-3.3-02 [OFF]. Grade A.

## Targets

* **R10. Set fixed obligations from the contract:** Set rent, insurance, phone and loan targets to the current bill. Do not average them. Source: [ARITH]: an average of a fixed bill is wrong whenever a payment lands in a different month. Grade C.
* **R11. Re-price every other target each quarter:** Set target = (last 12 months' net spend ÷ 12) × (1 + that category's 12-month CPI change). Use a local metro index where BLS publishes one. If a recurring payee started or stopped inside the window, set that payee's part from its current bill and the rest from the spend rate. Source: [ARITH]: a 12-month mean is centred about 6 months back and the target applies about 6 months forward, so the gap is about 12 months of price change; CPI series from BLS through FRED [OFF]. Grade C.
* **R12. Choose the goal type by simulation:** For each non-fixed category, replay the last 12 months twice from a zero balance at the R11 target, once as refill-up-to and once as set-aside, and count the months whose spend exceeded the available balance. Use set-aside if it gives fewer such months, otherwise refill-up-to. Source: [ARITH]; goal-type mechanics in the YNAB API specification [OFF]. Grade C.
* **R13. Split a category whose parts need different goal types:** If the parts of a category give different R12 answers, split them, and write a note on each saying what it includes and excludes. Do not merge two categories that give different answers. Source: a category carries one target [OFF, YNAB spec]; ambiguous categories absorb more spending, Cheema & Soman [STUDY-R, lab]. Grade B.

## Overspending

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
* **R18. Lower a refill-up-to target that under-spends:** If a refill-up-to category spent under 70% of target for 3 straight months (both configurable), lower it to its spend rate at the next re-pricing. Do not apply this to set-aside funds. Source: [ARITH]; Zhang et al. on asymmetric adjustment [RULEBOOK]. Grade C.

## Savings goal held for a purchase, and the payment trial

* **R19. Hold money for a dated purchase where its value on that date is known:** Keep a down payment or other dated goal in insured deposits, a Treasury money-market fund or T-bills maturing before the date. Do not hold it in stock funds. Source: [ARITH]: a fixed amount due on a fixed date needs a fixed value on that date. Grade C.
* **R20. Run a payment trial and judge it monthly:** Each person transfers, on payday, the difference between their future share of the total monthly housing cost and their current housing cost, into the trial category. Source for the trial as a whole: [NOT FOUND]; no study or official rule prescribes one. The CFPB toolkit says "Only you can decide how much you are comfortable paying" and that the lender "considers only if you are able to repay your mortgage, not whether you are comfortable repaying" [OFF]. Payment size causally drives delinquency: "cutting the required payment in half reduces the delinquency hazard by about 55 percent" (Fuster & Willen, NY Fed Staff Report 582, on ARM resets, not first-time buyers) [STUDY-V]. Grade D for the trial, A for the quotes. A month passes only if all of these hold [ARITH for each]:
  * **a.** The full trial amount was assigned from base income, not from a third paycheck or a bonus.
  * **b.** No trial money was moved back out in that month or a later one.
  * **c.** Every overspend was covered from R14 step 1 only.
  * **d.** Every credit-card payment category was at or above its card balance at month end.
  * **e.** No category ended the month negative, and Ready to Assign was not negative.
  * **f.** The capital-reserve stand-in, if any, and the true-expense sinking funds were funded at target in the same month.
* **R20, the amount:** Set it from the CFPB "total monthly home payment" (principal and interest, mortgage insurance, property tax, homeowner's insurance, HOA) at the current Freddie Mac 30-year rate (FRED `MORTGAGE30US`), plus each person's share of a home capital reserve and the utility increase, minus current rent and utilities. Re-price when the rate moves. Source: CFPB Your Home Loan Toolkit [OFF]; [ARITH]. Grade A.
* **R20, the length:** Run at least 6 months, at least 4 of them base-income months, with both people at once (both configurable). Source: [NOT FOUND]. Fannie Mae typically reviews the two most recent months of bank statements (B3-4.2-02) [OFF], which sets no trial length. Grade D.
* **R20, on failure:** In a failed month, record which criterion failed. After 2 failed months in a row (configurable), lower the planned housing payment, by a lower price ceiling or a larger down payment, rather than continuing at the same amount, and re-run the trial at the new amount. Source: Fuster & Willen [STUDY-V]; CFPB: "If this isn't enough, consider options such as buying a less expensive home or paying down debts" [OFF]. Grade A.
* **R21. Keep trial money as documented assets:** Leave trial deposits in the account the down payment will close from. Source any sweep or sale at least two statement cycles before a mortgage application. Fannie Mae defines a large deposit as one exceeding "50% of the total monthly qualifying income" and requires an acceptable source when the funds are used for the purchase. Source: Fannie Mae B3-4.2-02 [OFF]. Grade A.

## After a home purchase

* **R22. Size the emergency fund in months of housing payment:** At closing, recompute the emergency fund as months of PITIA (principal, interest, taxes, insurance, association dues) plus the largest single expense of the last 24 months. The number of months is a household choice (configurable). Update the emergency fund's category note. Source: Fannie Mae's reserve unit and "no minimum reserve requirement for one-unit principal residence" (B3-4.1-01) [OFF]. Grade A for the unit, D for the count.
* **R23. Fund a home capital reserve from the first month:** Create a set-aside category for home repairs and replacement, funded every month from closing. Re-derive it under R11 once a year of real bills exists. Source: CFPB: "Your home needs maintenance and repairs, so budget and save for these too" [OFF]. Grade A.

## Review

* **R24. Keep target-versus-spent visible all month, and review monthly:** Show each category's spend against its target and its own last-12-month rate, and review together once a month. Source: Levi 2025 RCT, about 15% lower discretionary spending while shown, gone 8 months after removal [STUDY-V]. Category limits reduce spending even when exceeded: Lukas & Howard 2023 [STUDY-V]; Hastings & Shapiro on non-fungible category money [STUDY-V]. Grade A.

## Two people

* **R25. Write a shared cost as one number per person, in both budgets:** When two people keep separate budgets, each carries a "my share" category with the same agreed amount and a note naming the split rule and its date. Source: [ARITH]: two files reconcile only if they carry the same number. Grade C.
* **R26. Assign every shared post-purchase cost an owner:** Before closing, assign utilities, the capital reserve and the first-year tax and escrow gap to a person and a category. Source: [ARITH]. Grade C.
* **R27. Fund a tax sinking fund wherever tax is not withheld:** Fund a tax category for every income without withholding (a local wage tax missing from a paystub, investment income, self-employment income) at the applicable rate times that income, until the liability is confirmed. Source: paystub and tax-form arithmetic [ARITH]. Grade C.
* **R28. Judge affordability per person by residual income, and the household by the lender ratio:** Check the household's total monthly home payment against 28% of gross income, and each person's share against what that person has left after their own fixed costs. Source: CFPB: "your total monthly home payment should be at or below 28% of your total monthly income before taxes" [OFF]; residual per person [ARITH]. Grade A.

## Measurement

* **R29. Record two numbers at each month's close:** (1) trailing-3-month discretionary spend (want categories) per person, and (2) liquid emergency balance ÷ monthly essential outflow (after a home purchase: ÷ PITIA plus utilities). Source: [ARITH]. Grade C.
* **R30. Never apply script-derived targets unchecked:** Apply a derived target only after per-category confirmation, and refuse a refill-up-to target below the largest month in its window. Source: [ARITH]: an unchecked bulk apply once capped lumpy funds below their largest months and ignored merged-category history. Grade C.
