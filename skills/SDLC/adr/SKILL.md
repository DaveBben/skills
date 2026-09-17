---
name: adr
description: "Use this skill whenever a decision is made or proposed that must survive the conversation. Fires when you, the agent, pick a library, a data shape, a key, a sync/async boundary, a limit, a retry policy, or drop a supported version without the user choosing it. A default you'll act on without a reply counts too. Notice it and act before the dependent code lands. Fires on any choice costing more than a day to reverse, a hazard accepted without a test, an alternative explicitly rejected ('X instead of Y'), or knowledge expensive to acquire: a measurement, a scar, a cost. Fires too on: 'adr', 'write an adr', 'make an adr', 'create an adr', 'record this architecture decision', 'note this architecture decision', 'this is an architectural decision', 'we need to record the why', 'let's document that decision', 'we will accept that risk', 'let's go with X instead of Y'. Fires on the bare word 'adr', and on 'record the why' with no artefact named: the why is the artefact. Write it immediately, mid-task if needed."
license: MIT
compatibility: any-agent
metadata:
  version: "0.7.0"
---
# Architecture Decision Records (ADR)

Write an ADR to document an expensive or irreversible decision, an accepted hazard, or a test row dispositioned "no test required" whose absence a later reader would question.

Write it immediately when the decision is made, not at the end of the feature development, and only after the user has given the reasons in their own words.

## Ask before writing

The reasons in the ADR are the user's. Never fill them in from what the agent can infer; an ADR whose "why" the agent wrote records what the agent would have decided.

* **Ask three things in one message,** then wait: why they chose this, what they see as the tradeoffs, and why they are not going with the obvious route, naming the obvious route so they can say "that is not the obvious one". When the decision was the agent's own choice, state the agent's reason, the obvious alternative and the tradeoff in the same message, and ask the user to confirm, change or replace the reason.
* **Give feedback on the answer before writing.** One message: a tradeoff the answer did not name, an alternative nobody considered, a hazard the answer accepts without a test, or a reason that does not hold against the code, each with its mechanism. When the answer holds up, say so in one line. The user amends the decision or the reason, or says write it.
* **Quote the user's reasons** in the Decision paragraph and in "Why the obvious fixes don't work here", in their words. The agent's feedback goes in "What it doesn't buy" or "Alternatives rejected", marked as the agent's.

## File Naming and Location

* **Feature-scoped:** `docs/adr/{slug}/<decision-name>.md` for a decision belonging to one change. The `{slug}` matches the `feature/{slug}` branch name.
* **Global:** `docs/adr/architecture/<decision-name>.md` for a decision applying to the whole repository.
* **Format:** `<decision-name>` is short and kebab-case, e.g. `use-redis-for-rate-limiting.md`.
* **Already recorded:** when the change's own PRD records the decision with its rejected alternative, write no ADR; put the PRD path on the log entry's `Decided` line.

## Writing for a reader who was not here

The reader did not see this conversation. Text that reads as complete to the writer and as a list of pointers to the reader is the failure to avoid. Each rule below removes one cause of it.

* **Resolve every pointer on the page.** No bare test ID, config key, abbreviation, or "the X" without one sentence saying what it is. Write "clinician", not "NP". Write "the browser panel that sends one request per keystroke", not "the panel". A pointer is a name local to this project or this session. Do not define industry-standard terms a working engineer knows: SQLite, fsync, Linux, HTTP.
* **Mechanism before label.** Write what physically happens ("the worker thread sits idle until the HTTP response arrives") before any name for it ("blocking"). A name never stands alone. "Racy at the margin" is a label; "two requests can both read 2, both write 3, and the cap admits one extra call" is the mechanism.
* **Check every connective.** For each "because", "so", "therefore", "which means": confirm the left clause causes the right. When it does not, write two sentences and no connective.
* **One rung at a time.** A claim about the system needs the component sentence, then the platform sentence, then the system sentence. Do not go from a function name to an outage in one sentence.
* **Incident as narrative.** When something broke, write what was built, what it did, and what failed, in that order. Narrative is the shortest explanation of a mechanism.
* **Before and after in the reader's units.** "Clinicians currently recording", not a formula, a variable, or "N".
* **Floor, not ceiling.** No word cap. Every claim carries at least one sentence of mechanism. Length follows from that.
* **Never invent a mechanism.** When the cause is not known, write "cause not established" and what would establish it. A plausible mechanism the evidence does not show is the same defect as a label, with a confident tone added. Every fact comes from the session, the code, or a source you can name. Do not add a rejected alternative nobody considered, a hardware rationale nobody measured, or a language or library the notes never named.
* **Reconstruction test before writing the file.** From the text alone, can the reader say what breaks and why, predict what changes when one input changes, and name what to measure next? When they could only repeat the sentences, rewrite. Then list every "because", "so" and "therefore" in the draft and write the cause beside each. Delete any connective whose cause you could not write.

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

`references/example.md` is a complete ADR in this form. Match its density and tone.
