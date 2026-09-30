---
name: meal-plan
description: Use this skill whenever the user wants a number of days of meals planned from their existing meal templates and written into the recipe manager. Use it on 'plan my meals for the week', 'plan 5 days of dinners', 'make a meal plan', 'fill the mealie meal plan', 'what should we eat this week', 'plan meals using up the leftover spinach'. Writes the approved plan and a scaled shopping list to Mealie. Do not use it to build or change a template; that is `meal-template`.
compatibility: Needs HTTP access to a recipe manager API (Mealie by default) and Python 3.
---

# Meal plan

Plan meals for two people, the user and their partner, over the number of days the user names (the **plan period**). Plan them from finished meal templates. Deliver two things in the recipe manager: meal plan entries, and a shopping list covering every serving made in the plan period.

Two scripts beside this file do the work. Run one `mealie.py` command at a time; the server stalls under concurrent requests. `references/plan-calc.py` does the arithmetic: per-day totals, plan averages against the targets, batch stretching, servings and scale, the entry text, and the shopping-list payload. `references/mealie.py` makes every Mealie request. Run each with `--help` for its input. If the user's library is a different recipe manager, read `references/mealie-mealplan.md` and adapt `mealie.py` to it, keeping its refusals.

A **template** is a recipe tagged with a tag containing "Template" (for example "Dinner Template", "Breakfast Template"). Its stored nutrition is per serving and already verified by `meal-template`; do not recompute it.

## Ask before planning

Ask in one message, and accept defaults for anything the user skips:

* **Number of days and start date.** Default start: tomorrow.
* **Leftover ingredients to use up, with rough amounts.** Always ask. These guide dinner selection and reduce the shopping list.
* **Changes to the fixed meals** in the plan period, such as travel, eating out, or a different breakfast.
* **Dinners to avoid or to repeat.**
* **How many granola bowls are left in the current batch.**
* **Whether pantry staples are stocked:** oil, salt, pepper, dried spices, soy sauce.
* **Whether the partner's egg bomb includes berries.**

## Fixed meals

Unless the user says otherwise, every day gets:

| Slot (Mealie `entryType`) | Recipe |
|---|---|
| `breakfast` | Breakfast - Protein Egg Bomb (cottage cheese eggs) |
| `drink` | Beverage - Morning Honey Espresso Latte |
| `lunch` | Lunch - Honey Walnut Granola Protein Yogurt Bowl |

Fetch them with `mealie.py recipes --out catalog.json --name` (`plan.json`'s `catalog` names this file). Start a new catalog file, or pass `--refresh`, for every plan: the cache never expires. If one no longer exists, or has no stored calories, protein, or fiber, stop and ask; `plan-calc.py` stops on these cases. Run `plan-calc.py` with no dinners to get the dinner budget before choosing dinners.

## Targets

The plan-wide daily averages `plan-calc.py` prints are hard constraints; individual days may miss. If no set of dinners brings every average to pass, report the numbers and ask. Do not plan anyway.

## Dinners

Choose from recipes tagged "Dinner Template". Do not use "Carb Load Template", "Dessert Template", or other tags unless the user asks. Carb-load templates break the fiber and protein targets on purpose.

List each cook day in `plan.json`; the script stretches each batch over the following days. When the review marks a third or later day of one batch, ask whether to cut it, and pass `days` to cut it. Three days of one dinner is often unwanted.

**Seafood is cooked fresh, never reheated.** A template is seafood when its main protein food is a fish or shellfish; if unsure, ask. Mark it `"seafood": true`.

**Selection.** Choose dinners so the targets hold. Within that constraint, prefer in this order:

1. **Leftover ingredients.** Templates that use the leftover ingredients the user named. Match ingredient food names and notes (spinach / baby spinach).
2. **Variety.** Avoid repeating a template within the plan period or within the previous 14 days of the existing meal plan. Avoid the same main protein on consecutive cooks. Break these when they would leave too few candidates, and say so.

Read the meal plan once with `mealie.py read-plan`, from 14 days before the start date through the end date. The same read shows any entries already in the plan period.

## Review before writing

Show `plan-calc.py`'s output: the dinner table, per-day totals, plan averages, and servings made and scale per recipe. Add the leftover ingredients each dinner uses. State once that the espresso is written as a `drink` entry.

Writing to the meal plan and shopping list is an outward-facing change. Get the user's approval of the table first.

## Writing

Run `plan-calc.py plan.json --out writes.json`, then `mealie.py write-plan writes.json`. When it refuses because entries exist, show them and ask whether to keep, replace, or add alongside, then pass `--keep`, `--replace` or `--add`. When `write-plan` prints "still present, remove in Mealie if unwanted", tell the user which entries remain. Create the list with `mealie.py create-list` using the `list_name` in `writes.json`; if that name exists, ask before passing `--again`. Then run `mealie.py add-recipes`.

Read the list back with `mealie.py read-list`, then adjust items with `mealie.py update-item`. Mealie merges rows that share a food and unit into one item.

* **Leftover ingredients:** lower the merged quantity by the amount the user has. Check an item off only when what they have covers the whole merged quantity.
* **Water, and rows with no quantity** (salt "to taste"): check them off.
* **Pantry staples:** check them off if the user said staples are stocked.

In the chat report, show what to buy grouped by store section (produce, meat and seafood, dairy and eggs, pantry, frozen). Flag berries, greens, fish, and other perishables needed more than 3 days into the plan period, so the user can buy them later or frozen.
