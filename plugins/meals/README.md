# meals

Skills for eating to numbers without cooking from a spreadsheet.

One skill today. More will follow as the other parts of the problem get their own handling: shopping lists, weekly assembly from finished templates, and nutrient gaps tracked across a week rather than a meal.

| Skill | Fires on |
|---|---|
| `meal-template` | "build a dinner template", "create breakfast templates", "make this recipe hit 40g protein", "I want 10 dinners I can repeat", "fit my recipes into my macros" |

## `meal-template`

Takes a calorie ceiling, a protein floor and a fiber floor, and turns a recipe the user already cooks into a reusable meal that hits all three.

The structure exists because of one measured fact: on a 436-recipe library, **zero recipes met a 600 kcal / 40 g protein / 10 g fiber target at once**. High-protein recipes are fish and chicken mains with 0-2 g fiber; high-fiber recipes are bean dishes with 17-28 g protein. Nothing bridges both. So a template is never one recipe. It is a base the user names, plus a fixed add-on sized to the gap.

What the skill insists on:

- **The user names the base recipe, and their deviations from it.** People omit ingredients. The macros must be computed against the version actually cooked.
- **The add-on must be an established dish with the base, not a macro graft.** It has to survive a search for the pairing before it is allowed to survive the arithmetic. A macro-correct meal nobody cooks twice is a failed template.
- **Macros are computed from the ingredient list, never read from stored nutrition.** Library nutrition is sparse and does not know about omissions.
- **A subagent verifies the result.** Parsing, an independent USDA recompute, and instruction soundness. Checking your own arithmetic in the same pass finds nothing.

`references/nutrient-priority.md` carries the per-100-kcal rankings for protein, fiber, fat quality and micronutrient density, including the portions that win the ratio and lose the meal. `references/mealie-api.md` carries the recipe-manager conventions, most of which exist because a scaled recipe lies in three places the serving slider never touches.

## Installing

**Claude Code:**

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install meals@davebben-skills
```

**Any other agent** (Codex, Cursor, Windsurf, and more), via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add DaveBben/davebben-skills --skill meal-template
```

The canonical `SKILL.md` lives at `skills/meals/` in the repo root.

MIT.
