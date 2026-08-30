---
name: adr
version: "0.2.0"
description: "Fire whenever an architectural or technical decision needs recording: an expensive or irreversible choice is made, a hazard is accepted without a test, or an alternative is explicitly rejected. Fire on: 'adr', 'write an adr', 'make an adr', 'create an adr', 'record this architecture decision', 'note this architecture decision', 'this is an architectural decision', 'we need to record the why', 'let's document that decision', 'we will accept that risk', 'let's go with X instead of Y'. Fire on the bare word 'adr' alone, and fire on 'record the why' even when no artefact is named \u2014 the why is the artefact. Write the decision, the alternatives turned down, and the consequences to an ADR file immediately, not at the end of the work."
license: MIT
compatibility: any-agent
---
# Architecture Decision Records (ADR)

Write an ADR to document an expensive or irreversible decision, or to formally justify a "Known Permanent Gap" (an accepted hazard or a "no test" disposition from the Design Document). 

Write it immediately when the decision is made, not at the end of the feature development.

## File Naming and Location

* **Feature-scoped:** `docs/adr/{slug}/<decision-name>.md` — Use this when the decision belongs to a specific change. The `{slug}` must match the `feature/{slug}` branch name.
* **Global:** `docs/adr/architecture/<decision-name>.md` — Use this when the decision applies to the entire repository rather than a single change.
* **Format:** `<decision-name>` must be short and kebab-case (e.g., `use-redis-for-rate-limiting.md`).

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

