# Record one decision

Loaded by the `architecture` skill for every decision it records: an answer from its Decide step, an accepted hazard, a rejected alternative, a choice a spike made alone that the user chose to record, or knowledge that cost time to acquire. An ADR (architecture decision record) is one Markdown file under `docs/adr/` that says what was decided, why, and what it gave up.

Write an ADR to document an expensive or irreversible decision, an accepted hazard, or a test the story's test table dropped as "no test required" whose absence a later reader would question.

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

* **Feature-scoped:** `docs/adr/{slug}/<decision-name>.md` for a decision belonging to one change. The `{slug}` is the feature's slug, the one in its `story/{slug}/` branches and its log path.
* **Global:** `docs/adr/architecture/<decision-name>.md` for a decision applying to the whole repository.
* **Format:** `<decision-name>` is short and kebab-case, e.g. `use-redis-for-rate-limiting.md`.
* **Already recorded:** when the change's own PRD records the decision with its rejected alternative, write no ADR; put the PRD path on the feature header's `Decided:` line.
* **Commit each ADR on its own when it is written:** on the plan branch before the first story, on the story's branch when a story forced it, and on main when no feature is open.

## Writing for a reader who was not here

Write the file by the "For a reader who was not here" rules in the writing reference this skill loads first. Run its reconstruction test before writing the file.

## Error handling

* **The user gives no reasons:** write no file. With a feature open, put the item on the feature header's `Deferred:` line as "no reasons given"; with none, say in chat that the decision is unrecorded. Carry on with the work.
* **No feature is open:** write to `docs/adr/architecture/`.
* **An existing ADR contradicts the new one:** leave the old file in place and name its path on the `Supersedes:` line.
* **The detector test does not exist yet:** name the test ID the change will add, and say what it will assert.

## The Template

Title: an imperative sentence stating the decision, e.g. `# Keep the LLM safe with a concurrency cap, not a timeout`.

```text
**Decision:** One paragraph. What we do, and the one-clause reason the obvious alternative
cannot work.

## The problem
What the feature does. The platform mechanism it strains, with the config key and default.
The incident, if one happened.

## Why the obvious fixes don't work here
One bullet per fix a reader would reach for first. State what already exists (a timeout,
a cache, a background worker), and why it does not address the actual cause. End with
the actual cause in one sentence.

## What we decided
Numbered. Each item is one bolded lead and one sentence of mechanism.

## What it buys
Load or risk before versus after, in the reader's terms ("clinicians currently recording",
not "N"). Name the kill switch and any dependency added or avoided.

## What it doesn't buy
What stays soft, unmeasured, or accepted. What must stay true. The measurements to take
before the next expansion, each named, and what to do if they fail.

## Alternatives rejected
One bullet per alternative: what it is, the exact metric or reason it lost.

**Detector:** the test ID, what it asserts, and what it deliberately does not assert.

**Supersedes:** none, or the exact file it replaces.
```

Omit a section only when it has nothing to say. `Detector` and `Supersedes` are always present.

Read `references/adr-example.md` before drafting the first ADR in a repository, and again whenever a draft runs short of mechanism: it is a complete ADR in this form, and the draft must match its density and tone.
