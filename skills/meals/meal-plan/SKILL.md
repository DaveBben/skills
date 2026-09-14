---
name: meal-plan
description: Use this skill whenever the user wants a number of days of meals planned from their existing meal templates and written into the recipe manager. Use it on 'plan my meals for the week', 'plan 5 days of dinners', 'make a meal plan', 'fill the mealie meal plan', 'what should we eat this week', 'plan meals using up the leftover spinach'. Fixed breakfast and lunch, dinners chosen from templates, batch meals stretched across days, daily averages checked against calorie, protein, and fiber targets. Delivers the plan in the Mealie meal planner plus a shopping list scaled to the servings made, after the user approves it. Do not use it to build or change a template; that is `meal-template`.
---

# Meal plan

Plan meals for two people, the user and their partner, over the number of days the user names (the **plan period**). Plan them from finished meal templates. Deliver two things in the recipe manager: meal plan entries, and a shopping list covering every serving made in the plan period.

The endpoints in `references/mealie-mealplan.md` are for Mealie. If the user's library is a different recipe manager, adapt the endpoints and keep the rules.

A **template** is a recipe tagged with a tag containing "Template" (for example "Dinner Template", "Breakfast Template"). Its stored nutrition is per serving and already verified; use it as is. Do not recompute template macros.

## Ask before planning

Ask in one message, and accept defaults for anything the user skips:

* **Number of days and start date.** Default start: tomorrow.
* **Leftover ingredients to use up, with rough amounts.** Always ask. These guide dinner selection and reduce the shopping list.
* **Changes to the fixed meals** in the plan period, such as travel, eating out, or a different breakfast.
* **Dinners to avoid or to repeat.**
* **How many granola bowls are left in the current batch.**
* **Whether pantry staples are stocked:** oil, salt, pepper, dried spices, soy sauce.

## Fixed meals

Unless the user says otherwise, every day gets:

| Slot (Mealie `entryType`) | Recipe | Servings made per day | Counts toward the user's totals |
|---|---|---|---|
| `breakfast` | Breakfast - Protein Egg Bomb (cottage cheese eggs) | 2: user + partner | 1 serving |
| `drink` | Beverage - Morning Honey Espresso Latte | 2: user + partner | 1 serving |
| `lunch` | Lunch - Honey Walnut Granola Protein Yogurt Bowl | 1: user only | 1 serving |

Look the recipes up by name. If one no longer exists, or has no stored calories, protein, or fiber, stop and ask.

Read their nutrition and `recipeServings` at run time. Subtract one serving of each from the daily targets. The remainder is the **dinner budget**. For example, on 2026-09-14 the fixed meals came to ~1,330 kcal / 112 g protein / 24 g fiber. That left dinner ~670-720 kcal, with protein and fiber already near their floors.

The egg bomb includes berries. Ask whether the partner's serving includes them, and scale the berry rows to the servings that do.

## Targets

Averaged per day across the plan period, for the user only. The partner's servings do not count.

| Metric | Target | Tolerance | Acceptable average |
|---|---|---|---|
| Calories | 2,000 kcal | +50 | ≤ 2,050 |
| Protein | 120 g | −10 | ≥ 110 g |
| Fiber | 30 g | −5 | ≥ 25 g |

* **Plan-wide averages are hard constraints.** Individual days may miss.
* **Days without nutrition are excluded.** A day with no nutrition for a meal ("eating out", no recipe) drops out of the average; say which days were left out.
* **Infeasible targets stop the plan.** If no set of dinners can bring the averages inside tolerance, report the numbers and ask. Do not plan anyway.

## Dinners

Choose from recipes tagged "Dinner Template". Do not use "Carb Load Template", "Dessert Template", or other tags unless the user asks. Carb-load templates break the fiber and protein targets on purpose.

**Batch stretching.** Every dinner day eats 2 servings. A template with `recipeServings` = S is cooked once and then eaten as leftovers on the following consecutive days, up to `floor(S / 2)` dinner days in total.

* **S = 4 (the common case):** day 1 cook, day 2 leftovers.
* **S of 6 or more:** show the third and later days in the review, and let the user cut them. Three days of one dinner is often unwanted.
* **S below 4:** one day.
* **Plan-period boundary:** a batch whose later days would fall after the plan period ends is cut at the last day.
* **Spare servings:** servings not eaten inside the plan period are not planned and not bought.

**Seafood is cooked fresh, never reheated.** A template is seafood when its main protein food is a fish or shellfish; if unsure, ask. A seafood template still covers the same days as any other template. Each day cooks only that day's 2 servings from the recipe, so day 2 is "cook fresh", not "leftovers".

**Selection.** Choose dinners so the targets hold. Within that constraint, prefer in this order:

1. **Leftover ingredients.** Templates that use the leftover ingredients the user named. Match ingredient food names and notes, allowing plurals and near-synonyms (spinach / baby spinach).
2. **Variety.** Avoid repeating a template within the plan period or within the previous 14 days of the existing meal plan. Avoid the same main protein on consecutive cooks. Break these when they would leave too few candidates, and say so.

Fetch full recipes for candidates. The recipe list endpoint returns no nutrition or ingredients.

## Servings and scale

Total the servings of every recipe across the plan period; the totals drive the shopping list. A recipe's **scale** is servings made ÷ `recipeServings`, with `recipeServings` read from the recipe.

* **Egg bomb and espresso:** 2 × days servings each.
* **Dinners:** 2 × dinner days that template covers. A 4-serving template over 2 days is scale 1. A cook on the last day of the plan period is scale 2/S. A template planned twice sums its scales.
* **Granola bowl:** the recipe is one granola batch followed by per-bowl rows, and yields `recipeServings` bowls.
  * The per-bowl rows scale by days ÷ `recipeServings`.
  * **Batches to buy:** ceil((days − bowls left) ÷ `recipeServings`), or 0 when enough bowls are left. The batch rows are added at that whole-number scale.
  * **Splitting the rows:** use each row's section `title`. A title applies to its own row and the rows after it, up to the next titled row.

## Review before writing

Show the plan as a table: date, dinner, and whether it is a cook, leftover, or cook-fresh day, plus the leftover ingredients each dinner uses. State once that the espresso is written as a `drink` entry. Under the table, show:

* **Per-day totals** for the user: kcal, protein, fiber.
* **Plan averages** against the targets.
* **Servings made per recipe and its scale.**

Writing to the meal plan and shopping list is an outward-facing change. Get the user's approval of the table first.

## Writing the meal plan

* **Check existing entries in the date range first.** If any exist, show them and ask whether to keep, replace, or add alongside. Never delete entries without that answer.
* **One entry per slot per day:** breakfast, drink, lunch, dinner. Link each entry by `recipeId`.
* **Put servings and leftovers in `text`**, since Mealie meal plan entries have no servings field:
  * `2 servings (user + partner)` for breakfast and drink, or `1 serving (user)` for lunch
  * `Cook: 2 servings tonight, 2 leftover for <weekday date>`
  * `Leftovers from <weekday date>`
  * `Cook fresh: 2 servings from the same recipe (seafood, not reheated)`
* **Never retry a write blindly.** On a timeout or error, re-read the date range before retrying; a timed-out create may already be saved.
* **After writing, re-read the range.** Confirm one entry per slot per day, with no duplicates.

## Writing the shopping list

* **Create a new shopping list** named `Meal plan <start date> to <end date>`. If a list with that name exists, ask before creating another.
* **Add every recipe in one bulk call** with its scale as `recipeIncrementQuantity`.
  * Mealie multiplies the quantities, and merges rows that share a food and unit.
  * Pass `recipeIngredients` to limit a recipe to some of its rows.
  * The granola bowl is two array items with the same `recipeId`: the per-bowl rows at their scale, and, only when batches are needed, the batch rows at the batch count.
* **Read the list back, then adjust items.** Never delete them.
  * **Leftover ingredients:** lower the merged quantity by the amount the user has. Check a row off (`checked: true`) only when what they have covers the whole merged quantity.
  * **Water, and rows with no quantity** (salt "to taste"): check them off.
  * **Pantry staples:** check them off if the user said staples are stocked.
* **Fresh produce for later days:** in the chat report, flag berries, greens, fish, and other perishables needed more than 3 days into the plan period, so the user can buy them later or frozen.
* **Report the list in chat.**
  * Show what to buy grouped by store section (produce, meat and seafood, dairy and eggs, pantry, frozen).
  * Give totals in purchase-friendly units, for example "2 lb shrimp", "3 cans chickpeas".
  * Then show what was lowered or checked off, and why.
