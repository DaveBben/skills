---
name: ynab-api
description: "Use this skill before reading from or writing to a YNAB (You Need A Budget) budget through api.ynab.com or a YNAB MCP server: fetching categories, transactions, accounts, months or scheduled transactions; analysing spending; or changing a category's target, note, name or group, a month's assigned amount, or a transaction. Use it on: 'how much did I spend on X', 'pull my YNAB data', 'what is in my budget', 'set this target', 'fix this category note', 'move money between categories', 'create a category', 'delete this duplicate transaction', 'why is my income wrong', or any script that calls the YNAB API."
license: MIT
metadata:
  version: "0.1.0"
---
# YNAB API

Read a YNAB budget correctly and change it safely.

## Settings

The user's settings live outside this skill, in the directory named by the `FINANCE_CONFIG_DIR` environment variable, or `~/.config/finance/` when it is unset:

* **`config.toml`:** read with Python's `tomllib`. `[ynab] budget_id` is the budget to use; `[ynab] keychain_service` is the macOS keychain service that holds the YNAB personal access token. [references/config.example.toml](references/config.example.toml) shows every key.
* **`profile.md`:** free-text household context. Read it before interpreting spending or changing a category.
* **`history/`:** dated change logs and the before/after snapshots of every write.

When `config.toml` is missing, tell the user the path you checked and offer to create it from the example. Never put a budget id, a name or an amount from these files into a repository.

## Authenticate

Read the token from the keychain inside the command that uses it, so it never reaches output, a log or shell history:

```bash
curl -s -H "Authorization: Bearer $(security find-generic-password -s "$SERVICE" -w)" \
  https://api.ynab.com/v1/budgets
```

```python
tok = subprocess.run(["security", "find-generic-password", "-s", service, "-w"],
                     capture_output=True, text=True).stdout.strip()
```

* **Never print the token.** Do not echo it, log it, put it in a URL or paste it into a message.
* **A call that hangs** is usually the keychain waiting for the user to approve access in a dialog.

Base URL is `https://api.ynab.com/v1`. `/budgets/{id}` and `/plans/{id}` are the same resource; YNAB renamed budgets to plans and kept both paths. Pass the budget id from config; `default_budget` is often null.

## Reading: the traps

* **`GET /transactions` without `since_date` returns about the last 12 months**, with nothing marking the cut. Pass `since_date=2000-01-01` for full history, then compare the earliest date with when the user started YNAB.
* **The rate limit is 200 requests per hour per token, with no remaining-count header.** Count your own calls. `GET /months` returns every month summary in one call, and `GET /categories` already carries the current month's `budgeted`, `activity` and `balance`, so do not loop.
* **Amounts are milliunits.** Divide by 1000: `-263110` is −263.11.
* **A month path segment needs a full date.** `/months/2026-02-01/...` works; `/months/2026-02/...` returns 400. `current` also works.
* **Income is `month.income`,** not the sum of inflows to Ready to Assign. The sum also picks up transfers, reconciliation adjustments and refunds. `month.income` counts paychecks received that month, so a month with three biweekly paychecks shows half again the usual figure.
* **Transfers have `transfer_account_id` set.** Exclude them from spending. A transfer to a tracking account is saving, not spending.
* **Splits hide their categories.** A transaction with a non-empty `subtransactions` array has a null top-level category; read the children.
* **Reimbursements are inflows to a spending category.** Sum signed amounts per category per month to get net spend. A reimbursement that lands a month later makes that month net negative; aggregate over the window rather than reading one month.
* **Tracking accounts (`on_budget: false`) are not the budget.** Their reconciliation adjustments are market movement; drop transactions whose account is off budget.
* **Overspending does not carry forward in the category.** A negative cash balance at month end resets the category to zero next month and is taken from next month's Ready to Assign; overspending on a credit card becomes card debt instead. A category's balance never shows last month's overspend, so read each month's `activity` and `balance` to find it.
* **A funded category can look dead.** Money that leaves by transfer, such as a retirement contribution, shows `budgeted` every month and no spending. Check `budgeted` before calling a category unused.
* **Goals need three fields to read.** `goal_target` is per `goal_cadence` period (`1` monthly, `2` weekly, `13` yearly); cross-check with `goal_under_funded`.
* **Delta requests save calls.** Pass the last `server_knowledge` as `last_knowledge_of_server` to get only changes; deleted entities come back with `deleted: true`.

[references/data-model.md](references/data-model.md) explains each field and gives the analysis checklist. [references/endpoints.md](references/endpoints.md) lists every read and write endpoint with its fields.

## Duplicate imports with the sign flipped

A bank feed can import one credit twice: once as an inflow and once as an outflow, on the same account and date, for the same absolute amount. Their `import_id`s have the form `YNAB:<milliunits>:<date>:<occurrence>`, so the pair reads `YNAB:-25000:2026-09-14:1` and `YNAB:25000:2026-09-14:1`. Detect it by grouping non-deleted transactions by `(account_id, date, abs(amount))` and keeping groups that hold one positive and one negative imported transaction. A real purchase and its same-day refund look identical, so check each pair against the bank statement before deleting the wrong-signed one with `DELETE /transactions/{id}`.

## Writing

The API can change less than the YNAB app can. Check that the change is possible before promising it.

| Change | Endpoint | Limits |
|---|---|---|
| Category name, note, group | `PATCH /budgets/{id}/categories/{cid}` | Name at most 50 characters; cannot move into an internal group |
| Category target | same PATCH | `goal_target` (milliunits; `null` removes the target), `goal_target_date`, `goal_needs_whole_amount`, `goal_frequency` |
| New category | `POST /budgets/{id}/categories` | Needs `name` and `category_group_id` |
| Month's assigned amount | `PATCH /budgets/{id}/months/{YYYY-MM-01}/categories/{cid}` | `budgeted` only; one call per category per month; no bulk endpoint |
| New or renamed group | `POST /category_groups`, `PATCH /category_groups/{gid}` | Name only |
| Transactions | `POST`, `PATCH` (bulk), `PUT`, `DELETE /transactions/{tid}` | Split children cannot be changed on an existing split |

* **Target type:** `goal_needs_whole_amount: true` is "Set aside another", `false` is "Refill up to". Both apply only to a NEED target, and to neither a credit card payment category nor a loan category. Setting `goal_target` on a category with no target creates a monthly NEED target.
* **`goal_frequency`** is `monthly`, `weekly` or `yearly`. It requires `goal_target`, cannot be sent with `goal_target_date`, and replaces the existing target.
* **Not writable at all:** goal type as a field (a target-balance or monthly-funding target is set in the app), hiding or deleting a category or group, and the order of categories and groups.
* **A failed PATCH applies none of its fields.** A 51-character name in the same call as a group move loses the move too. Send renames and moves separately.
* **Moving money between categories** is two month-assignment PATCHes: lower one `budgeted`, raise the other by the same amount. `GET /money_movements` reads past moves, with `from_category_id` and `to_category_id`.
* **Recategorising history breaks Ready to Assign.** Overspending already carried forward stays where it landed, so moving old transactions without moving the matching month assignments leaves the budget wrong.

**YNAB MCP servers often expose less than the API.** Some offer only the current month's assigned amount for a category, with no way to set `goal_target`, `goal_needs_whole_amount` or `note`. Check the tool's parameters; when the field is missing, use a script against the API or tell the user to change it in the app.

### How to write

1. **Show the change and get a yes.** List each category, field, current value and new value, and ask the user to confirm each change before writing. A yes to one change is not a yes to the next.
2. **Write from a script, never an import.** Put every write call under `if __name__ == "__main__":` (directly or in a function only that block calls), so a tool that imports the file to inspect it cannot write.
3. **Snapshot before and after.** Save the GET of each object you change to `history/<date>-<task>-before.json` and the response to `-after.json`, and append one line per change to `history/<date>-<task>.md`.
4. **Read the response.** Compare the returned object with what you sent; a 200 with an unchanged field means the field was ignored.

[references/endpoints.md](references/endpoints.md) has the request bodies.
