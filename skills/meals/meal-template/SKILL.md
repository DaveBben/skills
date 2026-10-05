---
name: meal-template
description: "Use this skill whenever a meal must be built or rebuilt to hit numeric nutrition targets drawn from a personal recipe library: a calorie ceiling, a protein floor, a fiber floor. Use it on: 'build a dinner template', 'create breakfast templates', 'make reusable meal templates', 'make this recipe hit 40g protein', 'fit my recipes into my macros', 'I want 10 dinners I can repeat'. Use it when the user names a recipe they already like and wants it adjusted rather than replaced. Builds each template from a base recipe the user chooses plus a fixed add-on, verifies it, and writes it back to the recipe manager. Do not use it to invent recipes from nothing, and do not use it to schedule a week of meals from templates that already exist."
license: MIT
compatibility: Needs HTTP access to a recipe manager API (Mealie by default) and Python 3.
metadata:
  version: "0.2.0"
---
# Meal template

Build a reusable meal from a recipe the user already makes, plus a fixed add-on that closes the gap to numeric nutrition targets.

A **template** is one base recipe, one add-on, and a verified per-serving macro figure. The user cooks it repeatedly without recalculating anything.

## Establish before building

* **Get the three numbers.** A calorie ceiling, a protein floor, a fiber floor, all per meal. Ask if not stated. Do not assume targets from a daily total.
* **Get read and write access to the recipe library.** For Mealie, `MEALIE_BASE_URL` and `MEALIE_API_KEY`; see `references/mealie-api.md`.
* **Pull the whole catalog once and cache it.** Fetch every recipe's nutrition and ingredient list to a local file. Re-fetching per query wastes minutes on a library of a few hundred.
* **Report the feasibility count first.** State how many recipes meet each target alone and all targets together. Expect zero to meet all three. That number justifies the base-plus-add-on structure, and skipping it makes the structure look arbitrary.

## The loop

Build one template at a time. Each template ends with the user confirming before the next starts.

1. **Let the user name the base recipe.** They know which meals they actually cook. Offer candidates only when asked.
2. **Record their deviations from the written recipe.** Users routinely omit ingredients. An omission changes the macros and must be computed against the version they cook, not the version on file.
3. **Compute the base macros.**
4. **State the gap and the headroom.** Report the shortfall on each target and the calories remaining under the ceiling. The headroom sets the add-on budget.
5. **Choose the add-on.**
6. **Recompute with the add-on.** Confirm every target clears.
7. **Write it to the library.** Create the template as a new recipe. Leave the base recipe unchanged; the verifier compares against it, and pass its identifier to the verification subagent. See `references/mealie-api.md`.
8. **Verify it.** Dispatch the verification subagent and the realism subagent. See below.
9. Apply the fixes, rewrite `nutrition` and the macros in `description` from the recomputed figures, then ask for the next base recipe.

## Computing macros

* **Ignore stored nutrition and compute from the ingredient list.** Library nutrition is sparse, often absent, and never reflects the user's omissions.
* **Use USDA FoodData Central per-100 g values.** Convert every ingredient to grams first. Volume measures for solids are the largest error source.
* **Write the calculation as a script with a food table, not as arithmetic in prose.** A worked example is in `references/macro-calc.py`.
* **Divide by the recipe's own serving count.** Do not renormalize to the number of people eating; the library scales that separately.
* **State the tolerance.** USDA entries and brand labels disagree by 10-20%. Report figures as approximate and never to more than three significant digits.
* **Test the assumption that moves the result most.** Protein portion size and added fat dominate. Recompute at the low end of the recipe's stated range and confirm the targets still clear.
* **Estimate sodium when the add-on is canned or jarred.** Canned legumes, jarred vegetables, and cured olives stack past 1500 mg per serving quickly. Report it and name the rinse.

## Choosing the add-on

The add-on must close the macro gap and belong on the plate. A macro-correct meal the user will not cook twice is a failed template.

* **Match the flavor base of the dish.** Take the fat, acid, and aromatics already in the recipe as the constraint.
* **Prove the pairing exists.** Search for the base plus the add-on as an established dish. Two independent published recipes or one from a tested source is sufficient. Cite the URLs.
* **Reject the pairing if the search returns nothing.** Choose a different add-on rather than arguing the macros justify it.
* **Draw from the priority foods.** `references/nutrient-priority.md` ranks foods by protein, fiber, and fat quality per 100 kcal. Prefer an add-on that appears on the list the template is short on.
* **Size the add-on to a published portion.** A proven pairing still fails at the wrong amount. Convert the add-on to grams per serving and keep it inside the range published recipes of that dish serve. An amount above that range is a macro graft, whatever the pairing evidence says.
* **Prefer one add-on that closes both gaps.** Cooked legumes carry protein and fiber together. Two separate add-ons double the prep.
* **Fold the add-on into the existing cooking step.** An add-on needing its own pan is a second recipe, not a template.
* **Name the target the template does not cover.** A lean-protein template carries no omega-3; say so and assign that nutrient to a different template rather than breaking the calorie ceiling.

## Verification

Dispatch a subagent with read-only access once the recipe is written. Verifying your own arithmetic in the same pass finds nothing.

Give it three tasks and require a one-line verdict on each:

* **Parsing.** Every ingredient row has a correct quantity, unit, and food, and the list scales sensibly to half and double the servings.
* **Macro math.** An independent recompute from USDA values, per ingredient, against the stored figures. Require it to audit the per-100 g assumptions used and name any that are off.
* **Instructions.** The method is sound and complete: temperatures, sequence, doneness, and what will burn, overcook, or go watery. Then low-effort technique upgrades, using only ingredients already listed, and give the calorie cost per serving of each upgrade.

### Realism pass

Dispatch a second read-only subagent for realism, separate from the three checks above. Run it on the most capable model available. A reviewer asked to confirm arithmetic approves nearly everything; this one is asked to find what a professional recipe tester would change. Defects it exists to catch: 3 cups of wheat bran stirred into 12 yogurt bowls, 2 lb of green beans for 4 plates of curry, 3 cans of beans with no cooking liquid, 170 g of cottage cheese scrambled into 2 eggs.

Require it to:

* **Compare portions per plate.** Convert every component to grams per serving: protein, vegetable, legume, starch, sauce, seasoning. Set each beside at least 3 published recipes of the same dish, cited, with the published range.
* **Challenge every add-on.** Would a cook of this cuisine serve this amount? Does it dilute or ruin the dish? Do the sauce, salt, acid, and spice scale to cover the added volume?
* **Check the equipment.** The volume fits the pan, it sears rather than steams, the times fit the amounts, and leftovers hold up when the batch spans several days.
* **Ask whether anyone would eat the plate.** Judge texture, sogginess, and proportion.
* **Decide, then fix.** Realism outranks the targets. Close a gap with a lever native to the cuisine: more of the main protein, a leaner cut, a starch swap, or a legume or vegetable at a published amount. When no realistic version meets the targets, keep the realistic version with the smallest miss and state the miss. Never keep an unrealistic quantity to pass a number.
* **Return fixed rows, not options.** Give the corrected ingredient amounts, the method changes, and recomputed per-serving nutrition. Do not hand the user a menu of alternatives.

A template is not finished until it passes this review.

## Recurring defects

A template that adds bulk to a hot pan fails in these ways. Apply each when the add-on adds that bulk.

* **Volume added without a plan for its water.** Leafy greens are over 90% water and 8-10 qt loose per pound. They will not fit the pan and will not wilt off-heat. Wilt them in the cooking vessel, in batches, before the protein goes in.
* **Reallocated fat.** Moving oil from the protein to the vegetables leaves lean protein dry and pale. Keep the protein's share.
