# Record one decision

Loaded by the `architecture` skill for every decision it records: an answer from its Decide step, an expensive or irreversible choice, an accepted hazard, a rejected alternative, a choice a spike made alone that the user chose to record, knowledge that cost time to acquire, or a test the story's test table dropped as "no test required" whose absence a later reader would question. An ADR (architecture decision record) is one Markdown file under `docs/adr/` that says what was decided, why, and what it gave up.

Write it immediately when the decision is made, not at the end of the feature, and only after the user gives the reasons in their own words.

## Ask before writing

The reasons in the ADR are the user's. Never fill them in from what the agent can infer.

* **From the Decide step, the answer is the reasons.** When the decision came from putting alternatives and a tradeoff to the user, their answer to that message is the reasons. Ask nothing more unless it gives no reason at all.
* **Otherwise ask three things in one message,** then wait. Name the obvious route in the third question:

```text
Before recording <decision>:
1. Why this?
2. What are the tradeoffs?
3. Why not <the obvious route>?
```

* **When the decision was the agent's own choice,** state the agent's reason, the obvious alternative and the tradeoff in the same message, and ask the user to confirm, change or replace the reason.
* **Give feedback on the answer before writing, only when there is something to give.** One message: a tradeoff the answer did not name, an alternative nobody considered, a hazard the answer accepts without a test, or a reason that does not hold against the code, each with its mechanism. When the answer holds up, write the file without a feedback message. The user amends the decision or the reason, or says write it.
* **Quote the user's reasons** in the Decision paragraph and in "Why the obvious fixes don't work here", in their words. The agent's feedback goes in "What it doesn't buy" or "Alternatives rejected", marked as the agent's.

## File Naming and Location

Write every ADR by the "For a reader who was not here" writing rules, reconstruction test included.


* **Feature-scoped:** `docs/adr/{slug}/<decision-name>.md` for a decision belonging to one change. The `{slug}` is the feature's slug, the one in its `story/{slug}/` branches and its log path.
* **Global:** `docs/adr/architecture/<decision-name>.md` for a decision applying to the whole repository, or when no feature is open.
* **Format:** `<decision-name>` is short and kebab-case, e.g. `use-redis-for-rate-limiting.md`.
* **Already recorded:** when the change's own PRD records the decision with its rejected alternative, write no ADR; put the PRD path on the feature header's `Decided:` line.
* **Commit each ADR on its own when it is written:** on the plan branch before the first story, on the story's branch when a story forced it, and on main when no feature is open.

## Error handling

* **The user gives no reasons:** write no file. With a feature open, put the item on the feature header's `Deferred:` line as "no reasons given"; with none, say in chat that the decision is unrecorded. Carry on with the work.
* **An existing ADR contradicts the new one:** leave the old file in place, name its path on the new one's `Supersedes:` line, and add the `Superseded by:` line to the old one.
* **The detector test does not exist yet:** name the test ID the change will add, and say what it will assert.

## The Template

Title: an imperative sentence stating the decision, e.g. `# Keep the LLM safe with a concurrency cap, not a timeout`. Readers read the title, the Decision and the Detector, and open the rest only when the Decision names what they touch, so those three carry the decision on their own.

Short form, the default, under 20 lines:

```text
**Decision:** One paragraph. What we do, and the one-clause reason the obvious alternative
cannot work.

**Detector:** the test ID, what it asserts, and what it deliberately does not assert.

## Alternatives rejected
One bullet per alternative: what it is, the exact metric or reason it lost.

**Supersedes:** none, or the exact file it replaces.
```

Long form, only when the decision accepts a hazard or follows an incident: add these sections after `Alternatives rejected`, each only when it has something to say.

* `## The problem`: what the feature does, the platform mechanism it strains with its config key and default, and the incident.
* `## Why the obvious fixes don't work here`: one bullet per fix a reader reaches for first and why it misses, then the actual cause in one sentence.
* `## What it buys`: load or risk before versus after in the reader's terms, the kill switch, and any dependency added or avoided.
* `## What it doesn't buy`: what stays soft or accepted, the assumptions it rests on, and the measurements to take before the next expansion.

When a new ADR supersedes an old one, add `**Superseded by:** <new file>` under the old one's title.

Read `references/adr-example.md` before drafting the first long-form ADR in a repository: it is a complete one, and the draft must match its density and tone.
