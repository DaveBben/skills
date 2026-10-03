# YNAB endpoints

Base: `https://api.ynab.com/v1`. Auth header: `Authorization: Bearer <token>`. `/budgets/{id}` and `/plans/{id}` are interchangeable. All amounts are milliunits. Source: the YNAB OpenAPI specification at <https://api.ynab.com/papi/open_api_spec.yaml> (v1.87.0); check it when a field here fails.

## Contents

- [Budgets](#budgets)
- [Categories](#categories)
- [Months](#months)
- [Money movements](#money-movements)
- [Transactions](#transactions)
- [Accounts, payees, scheduled transactions](#accounts-payees-scheduled-transactions)
- [Delta requests](#delta-requests)
- [Writes](#writes)
- [Responses and errors](#responses-and-errors)

## Budgets

```
GET /budgets                    all budgets; data.default_budget is often null
GET /budgets/{id}               everything in one payload, transactions truncated like GET /transactions
GET /budgets/{id}/settings      currency and date format
```

`last_modified_on` shows which budget is in use when there are several.

## Categories

```
GET /budgets/{id}/categories                groups with nested categories and current-month state
GET /budgets/{id}/categories/{category_id}
```

| Field | Meaning |
|---|---|
| `budgeted` | assigned this month |
| `activity` | movement this month, negative is spending |
| `balance` | available now, accumulated |
| `goal_type` | `NEED`, `TB` (target balance), `TBD` (target balance by date), `MF` (monthly funding), `DEBT`, or null |
| `goal_target` | for `NEED` the amount per cadence period; for `TB`/`TBD` the balance to reach |
| `goal_cadence`, `goal_cadence_frequency` | `1` monthly, `2` weekly, `13` yearly; the multiplier |
| `goal_needs_whole_amount` | `true` "Set aside another", `false` "Refill up to"; NEED only |
| `goal_under_funded` | YNAB's own figure for what this period still needs |
| `hidden`, `deleted` | filter both out for live categories |
| `note` | free text |

Exclude the `Internal Master Category` and `Credit Card Payments` groups from category analysis. `Inflow: Ready to Assign` carries a cumulative balance that is not a category total.

## Months

```
GET /budgets/{id}/months                         every month, summary only, one call
GET /budgets/{id}/months/{YYYY-MM-01|current}    one month with per-category detail
GET /budgets/{id}/months/{month}/categories/{category_id}
```

Month fields: `income` (paychecks received; use this for income), `budgeted`, `activity`, `to_be_budgeted` (negative means over-assigned), `age_of_money`.

## Money movements

```
GET /budgets/{id}/money_movements
GET /budgets/{id}/months/{month}/money_movements
GET /budgets/{id}/money_movement_groups
```

Each movement has `month`, `moved_at`, `amount`, `from_category_id`, `to_category_id`, `note`. Read-only. Use it to see which category covered an overspend.

## Transactions

```
GET /budgets/{id}/transactions?since_date=2000-01-01
GET /budgets/{id}/accounts/{account_id}/transactions
GET /budgets/{id}/categories/{category_id}/transactions
GET /budgets/{id}/payees/{payee_id}/transactions
GET /budgets/{id}/months/{YYYY-MM-01}/transactions
GET /budgets/{id}/transactions/{transaction_id}
```

Without `since_date` the list starts one year ago. Optional `type`: `uncategorized` or `unapproved`.

| Field | Notes |
|---|---|
| `amount` | negative is an outflow |
| `category_id`, `category_name` | null on a split parent |
| `subtransactions[]` | the categories of a split; children have no id you can update |
| `transfer_account_id` | non-null is a transfer |
| `account_id` | join to accounts for `on_budget` |
| `import_id` | `YNAB:<milliunits>:<date>:<occurrence>` for bank imports; null for entered transactions |
| `matched_transaction_id` | set when an import matched an entered transaction |
| `cleared`, `approved`, `memo`, `flag_color`, `payee_name` | |

Flatten before summing:

```python
def lines(t):
    subs = [s for s in (t.get("subtransactions") or []) if not s.get("deleted")]
    return [(s.get("category_id"), s["amount"]) for s in subs] or [(t.get("category_id"), t["amount"])]
```

## Accounts, payees, scheduled transactions

```
GET /budgets/{id}/accounts                        on_budget, type, balance, closed, deleted
GET /budgets/{id}/payees                          payee names; one merchant often has several
GET /budgets/{id}/scheduled_transactions          date_next, frequency, amount, category
```

A scheduled transaction forecasts an outflow; it sets no money aside.

## Delta requests

List endpoints accept `last_knowledge_of_server` and return `server_knowledge`. Store it with the cached data and pass it back to receive only changes. Deltas include deletions as `deleted: true`.

## Writes

Every write body wraps its object in a key named for the resource.

**Update a category** — `PATCH /budgets/{id}/categories/{category_id}`:

```json
{"category": {"goal_target": 150000, "goal_needs_whole_amount": false, "goal_frequency": "monthly"}}
```

Fields: `name` (max 50), `note`, `category_group_id` (not an internal group), `goal_target` (`null` removes the target), `goal_target_date`, `goal_needs_whole_amount`, `goal_frequency` (`monthly`, `weekly`, `yearly`; needs `goal_target`; not with `goal_target_date`; replaces the existing target). `goal_needs_whole_amount` and `goal_frequency` do not apply to credit card payment or loan categories. There is no `hidden`, no `goal_type` and no sort order.

**Create a category** — `POST /budgets/{id}/categories`: `{"category": {"name": "...", "category_group_id": "..."}}`, with any of the fields above.

**Create or rename a group** — `POST /budgets/{id}/category_groups` or `PATCH /budgets/{id}/category_groups/{group_id}`: `{"category_group": {"name": "..."}}`. Groups cannot be deleted, hidden or reordered.

**Assign money for a month** — `PATCH /budgets/{id}/months/{YYYY-MM-01}/categories/{category_id}`: `{"category": {"budgeted": 250000}}`. This sets the month's total assigned amount, not an increment.

**Transactions** — `POST /transactions` (one or a `transactions` array), `PATCH /transactions` (bulk, each by `id` or `import_id`), `PUT /transactions/{id}`, `DELETE /transactions/{id}`, `POST /transactions/import` (pull from linked accounts). Changing the children of an existing split returns 400.

**Other writes** — `POST /accounts`, `POST`/`PATCH /payees`, and `POST`/`PUT`/`DELETE /scheduled_transactions`.

## Responses and errors

Success bodies sit under `data`. Errors are `{"error": {"id", "name", "detail"}}`.

| Code | Meaning |
|---|---|
| 400 | Malformed request: a short month segment, an unknown field, a name over 50 characters, a split child change |
| 401 | Token missing, wrong or revoked |
| 403 | Subscription lapsed |
| 404 | Wrong budget or resource id |
| 409 | Conflict, such as a duplicate `import_id` |
| 429 | Over 200 requests in the hour |
