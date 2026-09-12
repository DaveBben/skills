---
name: meal-template
version: "0.1.0"
description: "Use this skill whenever a meal must be built or rebuilt to hit numeric nutrition targets drawn from a personal recipe library: a calorie ceiling, a protein floor, a fiber floor. Use it on: 'build a dinner template', 'create breakfast templates', 'make reusable meal templates', 'make this recipe hit 40g protein', 'fit my recipes into my macros', 'I want 10 dinners I can repeat'. Use it when the user names a recipe they already like and wants it adjusted rather than replaced. Pair a base recipe the user chooses with a fixed add-on that closes the macro gap, prove the pairing is an established dish rather than a macro graft, then write the result back to the recipe manager with ingredients that scale. Do not use it to invent recipes from nothing, and do not use it to schedule a week of meals from templates that already exist."
license: MIT
compatibility: any-agent
---
# Meal template

Build a reusable meal from a recipe the user already makes, plus a fixed add-on that closes the gap to numeric nutrition targets.

A **template** is one base recipe, one add-on, and a verified per-serving macro figure. The user cooks it repeatedly without recalculating anything.

## Establish before building

* **Get the three numbers.** A calorie ceiling, a protein floor, a fiber floor, all per meal. Ask if not stated. Do not assume targets from a daily total.
* **Get read and write access to the recipe library.** Most are self-hosted with a REST API. See `references/mealie-api.md` for Mealie specifics.
* **Pull the whole catalog once and cache it.** Fetch every recipe's nutrition and ingredient list to a local file. Re-fetching per query wastes minutes on a library of a few hundred.
* **Report the feasibility count first.** State how many recipes meet each target alone and all targets together. Expect zero to meet all three. That number justifies the base-plus-add-on structure, and skipping it makes the structure look arbitrary.

## The loop

Build one template at a time. Never batch. Each template ends with the user confirming before the next starts.

1. **Let the user name the base recipe.** They know which meals they actually cook. Offer candidates only when asked.
2. **Record their deviations from the written recipe.** Users routinely omit ingredients. An omission changes the macros and must be computed against the version they cook, not the version on file.
3. **Compute the base macros.** See below.
4. **State the gap and the headroom.** Report the shortfall on each target and the calories remaining under the ceiling. The headroom sets the add-on budget.
5. **Choose the add-on.** See below.
6. **Recompute with the add-on.** Confirm every target clears with margin.
7. **Write it to the library.** See `references/mealie-api.md`.
8. **Verify it.** Dispatch a subagent. See below.
9. **Apply the fixes, then ask for the next base recipe.**

## Computing macros

* **Ignore stored nutrition and compute from the ingredient list.** Library nutrition is sparse, often absent, and never reflects the user's omissions.
* **Use USDA FoodData Central per-100 g values.** Convert every ingredient to grams first. Volume measures for solids are the largest error source.
* **Write the calculation as a script with a food table, not as arithmetic in prose.** Ten templates reuse it. A worked example is in `references/macro-calc.py`.
* **Divide by the recipe's own serving count.** Do not renormalize to the number of people eating; the library scales that separately.
* **State the tolerance.** USDA entries and brand labels disagree by 10-20%. Report figures as approximate and never to more than three significant digits.
* **Test the assumption that moves the result most.** Protein portion size and added fat dominate. Recompute at the low end of the recipe's stated range and confirm the targets still clear.
* **Estimate sodium when the add-on is canned or jarred.** Canned legumes, jarred vegetables, and cured olives stack past 1500 mg per serving quickly. Report it and name the rinse.

## Choosing the add-on

The add-on must close the macro gap and belong on the plate. A macro-correct meal the user will not cook twice is a failed template.

* **Match the flavor base of the dish.** Take the fat, acid, and aromatics already in the recipe as the constraint.
* **Prove the pairing exists.** Search for the base plus the add-on as an established dish. Two independent published recipes or one from a tested source is sufficient. Cite the URLs.
* **Reject the pairing if the search returns nothing.** Choose a different add-on rather than arguing the macros justify it.
* **Draw from the priority foods.** `references/nutrient-priority.md` ranks foods by protein, fiber, fat quality, and micronutrient density per 100 kcal. Prefer an add-on that appears on the list the template is short on.
* **Prefer one add-on that closes both gaps.** Cooked legumes carry protein and fiber together. Two separate add-ons double the prep.
* **Fold the add-on into the existing cooking step.** An add-on needing its own pan is a second recipe, not a template.
* **Name the target the template does not cover.** A lean-protein template carries no omega-3; say so and assign that nutrient to a different template rather than breaking the calorie ceiling.

## Verification

Dispatch a subagent with read-only access once the recipe is written. Verifying your own arithmetic in the same pass finds nothing.

Give it three tasks and require a one-line verdict on each:

* **Parsing.** Every ingredient row has a correct quantity, unit, and food, and the list scales sensibly to half and double the servings.
* **Macro math.** An independent recompute from USDA values, per ingredient, against the stored figures. Require it to audit the per-100 g assumptions used and name any that are off.
* **Instructions.** The method is sound and complete: temperatures, sequence, pan capacity, doneness, and what will burn, overcook, or go watery. Then low-effort technique upgrades, capped at a stated calorie cost, using only ingredients already listed.

**Pass the subagent the base recipe's identifier too.** It must be able to compare the template against what it was derived from.

## Recurring defects

These appear in nearly every template and are worth checking before verification runs.

* **Volume added without a plan for its water.** Leafy greens are over 90% water and 8-10 qt loose per pound. They will not fit the pan and will not wilt off-heat. Wilt them in the cooking vessel, in batches, before the protein goes in.
* **Reallocated fat.** Moving oil from the protein to the vegetables leaves lean protein dry and pale. Keep the protein's share.
* **Unadjusted cooking time.** Adding cold bulk to a hot pan crashes the temperature. Extend the time and make it thermometer-driven.
* **Unadjusted seasoning.** Bulk added without salt tastes flat. When sodium is already high, add acid and finishing aromatics instead of salt.
* **Aromatics left on the surface.** Minced garlic exposed at high heat scorches bitter. Bury it.
