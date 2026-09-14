# Mealie meal plan and shopping list API

Mealie is a self-hosted recipe manager with a REST API. Adapt the endpoints if the library is something else.

## Access

Authenticate with a long-lived bearer token. Take the base URL and token from the environment (`$MEALIE_BASE_URL`, `$MEALIE_API_KEY`), or wherever the user keeps them. Ask if neither is set.

```
curl -s -H "Authorization: Bearer $MEALIE_API_KEY" "$MEALIE_BASE_URL/api/households/mealplans?start_date=2026-09-15&end_date=2026-09-21"
```

## Recipes

| Operation | Call |
|---|---|
| List templates by tag | `GET /api/recipes?page=1&perPage=2000&tags=<tag-slug>` (for example `dinner-template`). Summary only: no nutrition, no ingredients. |
| One recipe, full | `GET /api/recipes/<slug>`: `id`, `recipeServings`, `nutrition`, `recipeIngredient`, `tags` |

`nutrition` is per serving, stored as strings: `calories`, `proteinContent`, `fiberContent`, `fatContent`, `carbohydrateContent`, `sodiumContent`. Parse the leading number; a value may be `null` or carry a unit suffix such as `"11g"`.

`recipeIngredient` rows carry `quantity`, `unit.name`, `food.name`, `note`, and `title`. A non-empty `title` starts a section, such as "Granola batch" or "Bowls". Only the first row of a section carries the title; it applies to that row and the rows after it, up to the next titled row.

## Meal plan

| Operation | Call |
|---|---|
| Read a date range | `GET /api/households/mealplans?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&perPage=500` → `{items, total}` |
| Create an entry | `POST /api/households/mealplans` |
| Update an entry | `PUT /api/households/mealplans/<id>` |
| Delete an entry | `DELETE /api/households/mealplans/<id>` |

Create payload:

```json
{"date": "2026-09-15", "entryType": "dinner", "recipeId": "<recipe uuid>", "title": "", "text": "Cook: 2 servings tonight, 2 leftover for Wed 9/16"}
```

* **`entryType`:** one of `breakfast`, `lunch`, `dinner`, `side`, `snack`, `drink`, `dessert`.
* **`recipeId`:** link the recipe with it. Leave `title` empty when a recipe is linked. Use `title` only for an entry with no recipe, such as "Eating out".
* **No servings field.** Put servings and leftover notes in `text`.
* **Several entries can share a date and `entryType`.** Mealie does not deduplicate, so check the range before writing.

## Shopping list

| Operation | Call |
|---|---|
| Create a list | `POST /api/households/shopping/lists` with `{"name": "..."}` → `{id, ...}` |
| Add scaled recipes (bulk) | `POST /api/households/shopping/lists/<list id>/recipe` with a JSON array |
| Read a list with items | `GET /api/households/shopping/lists/<list id>` → `listItems`, `recipeReferences` |
| Update one item | `PUT /api/households/shopping/items/<item id>` with the full item object from the read, changed fields edited |
| Delete a list | `DELETE /api/households/shopping/lists/<list id>` |

Bulk add payload:

```json
[
  {"recipeId": "<egg bomb uuid>", "recipeIncrementQuantity": 10},
  {"recipeId": "<granola bowl uuid>", "recipeIncrementQuantity": 0.4167, "recipeIngredients": [<per-bowl rows copied from the recipe>]}
]
```

These behaviors were tested on 2026-09-14:

* **Scaling:** `recipeIncrementQuantity` multiplies every row. Scale 4 on a 1-serving recipe turned 2 eggs into 8. Fractions work: 2/12 turned 8 cups of yogurt into 1.33 cups.
* **Row subsets:** `recipeIngredients` limits the add to the rows passed. Pass the row objects exactly as read from `GET /api/recipes/<slug>`.
* **Merging:** items that share a food and unit merge into one line, so one line can carry several recipes' needs. Checking it off hides all of them.
* **Same recipe twice:** send two array items with the same `recipeId` to add different row subsets at different scales.
* **Rows without a unit:** such rows (for example "8 egg") come through with `unit: null`.
* **Order:** `listItems` order is not recipe order. Group items yourself for the report.

## Server behavior

* **Request pacing:** The server is slow and stalls under concurrent requests. Send one request at a time, with timeouts of 180 s or more.
* **Timed-out writes:** A POST that times out may still be saved. Re-read the date range or the list before retrying.
* **Catalog fetch:** Fetching every candidate recipe in full takes minutes. Fetch once per session and cache the results locally.
