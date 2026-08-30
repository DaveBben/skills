---
name: adr
version: "0.2.0"
description: "Fire when an expensive, irreversible architectural decision is made, a system hazard is accepted without a test, or a technical alternative is explicitly rejected. Fire on: 'let's document that decision', 'write an adr', 'we will accept that risk', 'let's go with X instead of Y'."
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

