# Writing templates to Mealie

Mealie is a self-hosted recipe manager with a REST API. An MCP server exists but is not required; every operation below is a plain HTTP call. Adapt the endpoints if the library is something else. The conventions in "Scaling" and "Defects" apply to any recipe manager that scales by serving count.

## Access

Authenticate with a long-lived bearer token.

```
curl -s -H "Authorization: Bearer $MEALIE_API_KEY" "$MEALIE_BASE_URL/api/recipes/<slug>"
```

| Operation | Call |
|---|---|
| List recipes (summary, no nutrition) | `GET /api/recipes?page=1&perPage=500` |
| One recipe (full, with nutrition and ingredients) | `GET /api/recipes/<slug>` |
| Create recipe | `POST /api/recipes` with `{"name": "..."}`, returns the slug as a bare string |
| Update recipe | `PUT /api/recipes/<slug>` with the full object from a prior GET |
| Partial update | `PATCH /api/recipes/<slug>` with only the changed keys |
| List or create tags | `GET`/`POST /api/organizers/tags` |
| List or create foods | `GET /api/foods?perPage=1000`, `POST /api/foods` |
| List or create units | `GET /api/units?perPage=200`, `POST /api/units` |
| Parse ingredient text | `POST /api/parser/ingredients` with `{"parser": "nlp", "ingredients": [...]}` |

**Create then update.** `POST /api/recipes` accepts only a name. Everything else requires a follow-up `PUT` with the object fetched back.

**Cache the catalog.** The summary list carries no nutrition, so a full survey needs one `GET` per recipe. Fetch concurrently, write to a local JSON file, and query the file.

## Ingredient parsing

Structured `quantity`, `unit`, and `food` fields are what the serving slider scales. An unparsed ingredient has free text only and will not scale.

* **Use the `nlp` parser.** The built-in CRF parser needs no API key and returns usable confidence scores. The `openai` parser requires a key configured server-side and fails silently with non-JSON when it is missing, which manifests as a client hanging through its retry backoff.
* **Create missing foods before assigning them.** A parser result whose `food` has no `id` needs `POST /api/foods` first.
* **Verify after patching.** Re-fetch and confirm every row kept its text and gained a food. Restore from a snapshot taken before the write if any row is corrupted.

## Scaling

The serving slider scales structured amounts only. Three things it never touches:

* **The ingredient `note`.** Write prep instructions only, and express any gram figure per unit: `about 200 g each`, `about 250 g drained per can`. An absolute total in a note contradicts the scaled amount above it and is the single most confusing defect a user will report.
* **Instruction prose.** Amounts written into steps stay fixed. Where a recipe divides an ingredient across steps, the split is only correct at the native serving count. State that in the description.
* **Stored nutrition.** It is a flat per-serving string and does not recompute when quantities change. Correct by construction, stale after a hand edit.

Further rules:

* **Split combined amounts into separate rows.** `1 teaspoon zest plus 1 tablespoon juice` scales the zest and silently drops the juice. Two rows, two foods.
* **Give foods a singular `name` and a `pluralName`.** A food stored as `skinless cod fillets` renders `1 skinless cod fillets` at one serving. Foods are global, so fixing one improves every recipe that uses it.
* **Give every row a unit.** A bare count on a packaged good reads as nonsense when halved. Create the unit if the instance lacks it.
* **Write pan capacity into the instructions.** A baking dish sized for the native yield will not hold double. Name the dish and the serving count at which a second one is needed.

## What to store on a template

| Field | Content |
|---|---|
| `name` | Prefix with the template number so the set sorts together |
| `tags` | One tag shared by every template, for filtering |
| `description` | Per-serving macros, the base recipe and its source, what the add-on closes, the targets, the sensitivity result, known weak points such as sodium, valid swaps, and the note that instruction amounts do not scale |
| `nutrition` | Per serving: `calories`, `proteinContent`, `fiberContent`, `fatContent`, `carbohydrateContent`, `sodiumContent`. Strings. |
| `recipeServings`, `recipeYieldQuantity` | Both set to the native serving count. `recipeYieldQuantity` defaults to 0 and is easy to miss. |
| `prepTime`, `performTime`, `cookTime`, `totalTime` | Update after an instruction rewrite; added steps change them |
