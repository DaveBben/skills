# finance

Skills for running a YNAB budget by rules that rest on evidence, not habit.

Six skills. Three set up and maintain the budget; three run it on a calendar.

| Skill | Fires on |
|---|---|
| `ynab-api` | "pull my YNAB data", "how much did I spend on X", "set this target", "move money between categories", any script that calls the YNAB API |
| `budget-targets` | "what should my targets be", "recompute my targets", "adjust my targets for inflation", "should this be set aside or refill up to" |
| `category-fit` | "does this need its own category", "should I merge these categories", "where does this charge belong" |
| `monthly-close` | start of the month, "close the month", "month-end review", "I overspent", "a category went negative" |
| `payday` | "I got paid", "paycheck landed", "bonus arrived", "third paycheck this month", "assign my paycheck" |
| `quarterly-checkup` | every quarter, "quarterly review", "check my targets", "am I on pace for my 401k/HSA/IRA", "will I owe taxes in April" |

## Personal settings stay outside the repo

Nothing personal ships in this plugin. Every skill reads the directory named by `FINANCE_CONFIG_DIR`, default `~/.config/finance/`:

* `config.toml`, read with Python's `tomllib`:
  * `[ynab]` `budget_id`, `keychain_service` (the keychain entry holding the YNAB personal access token; the token itself is never stored in a file).
  * `[income]` `pay_frequency` (`biweekly`, `semimonthly` or `monthly`), `base_monthly` (the amount each month is budgeted on), `bonus_months`.
  * `[roles]` category names by role: `fixed`, `steady`, `bill_funds`, `wants`, `savings_goals`, `retirement` (lists); `surprise_fund`, `emergency_fund`, `trial_category` (strings; the trial category is an optional practice-payment category). An optional `paused` list names categories payday must not fund.
  * `[cover_order] steps`, the order overspending is covered from, default `["wants", "trial_category", "emergency_fund", "bill_funds"]`.
  * `[cpi]` category name → FRED series id.
  * `[scripts]` windows and thresholds, such as `months`, `cover_raise_count`, `trial_min_months`.
* `profile.md`, free-text household context the skills read before advising: pay dates, a planned home purchase, HSA coverage tier.
* `history/`, the dated change logs and close, payday and quarterly reports the skills write.

`skills/ynab-api/references/config.example.toml` is a starting point.

## Why the rules look like this

The rules (R1–R30, in `skills/monthly-close/references/rules.md`) came out of an audit that held each budgeting rule to one standard: an official source, a study read in full or in abstract, or arithmetic on the budget's own data. Each rule carries its source tag and an evidence grade, and every number no source sets is marked as a household choice and read from the settings file.

What the skills insist on:

* **Overspending is covered in a fixed order.** Wants first, then the practice payment, then the emergency fund, then bill funds. Never the surprise fund, because pooling routine overspending there hides it; never a card payment category, because that money is already owed; never retirement, because a Roth withdrawal costs tax-advantaged room that only a 60-day rollover restores.
* **Income is classified by its source, not its variance.** A fixed biweekly paycheck with a yearly bonus scores as "variable" on a coefficient-of-variation test while being entirely predictable. The month is budgeted on base pay; third paychecks and bonuses go to goals the day they land, and nothing is assigned before it arrives.
* **Targets are re-priced quarterly, never at month end.** Month-end covers are recorded in the category note; a category covered in 3 of 6 months is raised at the next quarterly re-pricing, with each 12-month spend rate scaled by its own CPI series.
* **A practice mortgage payment is judged by written criteria.** A month passes only if the full amount came from base pay, nothing was taken back, every overspend was covered from wants, every card was funded, nothing ended negative and the sinking funds were funded. Two failures in a row lower the planned payment rather than repeating the test.
* **Limits are looked up every run.** 401(k), IRA and HSA limits, brackets and the standard deduction change each year, so the quarterly checkup reads them from irs.gov instead of remembering them.
* **Every write waits for the user.** Scripts print a dry run and write only with `--confirm`, after the user approves. Some YNAB MCP servers can only set a month's assigned amount, so notes, targets and deletes go through the scripts.

## Installing

**Claude Code:**

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install finance@davebben-skills
```

**Any other agent** (Codex, Cursor, Windsurf, and more), via the [`skills` CLI](https://github.com/vercel-labs/skills). The skills refer to `ynab-api` and `budget-targets` by name, so install all six together:

```bash
npx skills add DaveBben/davebben-skills --skill ynab-api
npx skills add DaveBben/davebben-skills --skill budget-targets
npx skills add DaveBben/davebben-skills --skill category-fit
npx skills add DaveBben/davebben-skills --skill monthly-close
npx skills add DaveBben/davebben-skills --skill payday
npx skills add DaveBben/davebben-skills --skill quarterly-checkup
```

The canonical `SKILL.md` files live at `skills/finance/` in the repo root.

MIT.
