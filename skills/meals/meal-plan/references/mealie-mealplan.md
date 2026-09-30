# Mealie facts behind mealie.py and plan-calc.py

`mealie.py` holds the endpoints and payloads. These are the field facts and tested behaviours the two scripts rely on; carry them over when adapting the scripts to another recipe manager or another Mealie version.

## Fields

* **`nutrition`** is per serving, stored as strings: `calories`, `proteinContent`, `fiberContent`. A value may be `null` or carry a unit suffix such as `"11g"`; parse the leading number.
* **`recipeIngredient`** rows carry `quantity`, `unit.name`, `food.name`, `note`, and `title`. A non-empty `title` starts a section, such as "Granola batch" or "Bowls", and only the first row of a section carries it. Rows without a unit come through with `unit: null`.
* **Meal plan entries** have no servings field, so servings go in `text`. `entryType` is one of `breakfast`, `lunch`, `dinner`, `side`, `snack`, `drink`, `dessert`. Link a recipe with `recipeId` and leave `title` empty; use `title` only for an entry with no recipe, such as "Eating out".
* **Several entries can share a date and `entryType`.** Mealie does not deduplicate.

## Shopping list behaviour, tested on 2026-09-14

* **Scaling:** `recipeIncrementQuantity` multiplies every row. Scale 4 on a 1-serving recipe turned 2 eggs into 8. Fractions work: 2/12 turned 8 cups of yogurt into 1.33 cups.
* **Row subsets:** `recipeIngredients` limits the add to the rows passed, exactly as read from `GET /api/recipes/<slug>`. Two array items with the same `recipeId` add different row subsets at different scales.
* **Merging:** items that share a food and unit merge into one line. Checking it off hides every recipe's need on that line.
* **Updating an item** takes the full item object from the list read, with the changed fields edited.

## Server

The server is slow and stalls under concurrent requests. Fetching every candidate recipe in full takes minutes.
