---
name: adr
description: "Use this skill whenever a decision is made or proposed that must survive the conversation. Fires when you, the agent, pick a library, a data shape, a key, a sync/async boundary, a limit, a retry policy, or drop a supported version without the user choosing it. A default you'll act on without a reply counts too. Notice it and act before the dependent code lands. Fires on any choice costing more than a day to reverse, a hazard accepted without a test, an alternative explicitly rejected ('X instead of Y'), or knowledge expensive to acquire: a measurement, a scar, a cost. Fires too on: 'adr', 'write an adr', 'make an adr', 'create an adr', 'record this architecture decision', 'note this architecture decision', 'this is an architectural decision', 'we need to record the why', 'let's document that decision', 'we will accept that risk', 'let's go with X instead of Y'. Fires on the bare word 'adr', and on 'record the why' with no artefact named: the why is the artefact. Write it immediately, mid-task if needed."
license: MIT
compatibility: any-agent
metadata:
  version: "0.5.1"
---
# Architecture Decision Records (ADR)

Write an ADR to document an expensive or irreversible decision, an accepted hazard, or a test row dispositioned "no test required" whose absence a later reader would question.

Write it immediately when the decision is made, not at the end of the feature development.

## File Naming and Location

* **Feature-scoped:** `docs/adr/{slug}/<decision-name>.md` for a decision belonging to one change. The `{slug}` matches the `feature/{slug}` branch name.
* **Global:** `docs/adr/architecture/<decision-name>.md` for a decision applying to the whole repository.
* **Format:** `<decision-name>` is short and kebab-case, e.g. `use-redis-for-rate-limiting.md`.
* **Already recorded:** when the change's own PRD records the decision with its rejected alternative, write no ADR; put the PRD path on the log entry's `Decided` line.

## The Template

Keep it extremely short: strictly under 50 lines and 250 words.

```text
Problem:    The goal, situation, or unmitigated hazard driving this decision.
Why:        The rationale behind the chosen approach.
Rejected:   The alternatives considered, and the exact metric or reason each lost.
Assumes:    What must stay true, and the specific condition that would invalidate this decision.
Tradeoffs:  What this costs (latency, complexity, tech debt), and what elsewhere now has to hold.
Supersedes: Only if it replaces a previous ADR (link the exact file).
```

