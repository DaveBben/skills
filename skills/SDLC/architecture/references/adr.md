# Write one ADR

Brief for the subagent that writes one ADR (architecture decision record) for the `architecture` skill: one Markdown file under `docs/adr/` that says what was decided, why, and what it gave up. The task gives you the decision; the user's reasons in their own words, or that the user deferred to the agent's recommendation and the agent's reason; any feedback from the agent that launched you; the alternatives and why each lost; any hazard it accepts or incident it follows; the path of any ADR it supersedes; the feature slug or "none"; and the checkout and branch to commit in. You ask nobody: return any question instead.

## The reasons

* **Quote the user's reasons** in the Decision paragraph and in "Why the obvious fixes don't work here", in their words. Add no reason the task does not give.
* **The launching agent's feedback** goes in "What it doesn't buy" or "Alternatives rejected", marked as the agent's.
* **When the user deferred,** record the agent's reason, marked as the agent's, with the line "The user deferred to the agent's recommendation."

## File naming and location

* **Feature-scoped:** `docs/adr/{slug}/<decision-name>.md` for a decision belonging to one change. The `{slug}` is the feature's slug, the one in its `story/{slug}/` branches.
* **Global:** `docs/adr/architecture/<decision-name>.md` for a decision applying to the whole repository, or when the slug is "none".
* **Format:** `<decision-name>` is short and kebab-case, e.g. `use-redis-for-rate-limiting.md`.
* **Commit the ADR on its own** in the checkout and on the branch the task names, creating the branch from main when it does not exist. Never switch the branch of a checkout with uncommitted changes; return a question instead. Return the file's path and the commit hash.

## Error handling

* **An existing ADR contradicts the new one:** leave the old file in place, name its path on the new one's `Supersedes:` line, and add the `Superseded by:` line to the old one.
* **The detector test does not exist yet:** name the test ID the change will add, and say what it will assert.

## The template

From the file alone, a reader can say what was decided, why, and what would make it wrong. Title: an imperative sentence stating the decision, e.g. `# Keep the LLM safe with a concurrency cap, not a timeout`. Readers read the title, the Decision and the Detector, and open the rest only when the Decision names what they touch, so those three carry the decision on their own.

Short form, the default, under 20 lines:

```text
**Decision:** One paragraph. What we do, and the one-clause reason the obvious alternative
cannot work.

**Detector:** the test ID, what it asserts, and what it deliberately does not assert.

## Alternatives rejected
One bullet per alternative: what it is, the exact metric or reason it lost.

**Supersedes:** none, or the exact file it replaces.
```

Long form, only when the decision accepts a hazard or follows an incident: add these sections after `Alternatives rejected` and before `Supersedes:`, each only when it has something to say.

* `## The problem`: what the feature does, the platform mechanism it strains with its config key and default, and the incident.
* `## Why the obvious fixes don't work here`: one bullet per fix a reader reaches for first and why it misses, then the actual cause in one sentence.
* `## What it buys`: load or risk before versus after in the reader's terms, the kill switch, and any dependency added or avoided.
* `## What it doesn't buy`: what stays soft or accepted, the assumptions it rests on, and the measurements to take before the next expansion.

A short-form ADR, for density and tone:

```text
# Cap the LLM at one call per browser, not a timeout

**Decision:** Each browser makes at most one AI call at a time, and a soft limit caps calls across
the instance. A timeout cannot work: it bounds how long one call takes, and the outage came from
how many ran at once on a worker pool of 5.

**Detector:** T-15 asserts one call per request and that the over-limit call is refused. It does
not assert the cap number, which is not measured yet.

## Alternatives rejected
- A timeout: already 30 s, and it did not prevent the outage.
- A strict global limit: the plugin cache has no atomic counter.

**Supersedes:** none.
```
