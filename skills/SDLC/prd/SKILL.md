---
name: prd
version: "0.1.0"
description: "Use this skill whenever a product decision needs to be written down before code is planned: what to build, for whom, and how anyone will know it worked. Use it on: 'write a prd', 'create a prd', 'make a prd', 'product requirements document', 'write this up as a prd', 'we need requirements for X', 'define the requirements', 'scope this feature', 'write up what we are building', 'turn this idea into requirements', 'what should we build for X'. Use it also to review one that already exists: 'review this prd', 'is this prd any good', 'critique these requirements', 'check this prd'. Use it on the bare word 'prd' alone, and on a feature request that arrives as a solution ('add a CSV export button') when nobody has yet stated the problem it solves. Interview the user until the real need is exposed, then write requirements and completion criteria as statements that can be proven false. Do not use it to design an implementation (`adr` records the decisions) or to build one (`agile`)."
license: MIT
compatibility: any-agent
---
# Product Requirements Document (PRD)

Interview the user until the actual need is exposed, then write it down as requirements that can fail.

A PRD answers what and why. It never answers how. Every statement in it must be one a person outside the room could later prove false.

## Scope One PRD to One Decision

Write one PRD per feature or initiative, never one per project. A project is a container, not a decision.

* **Write one when:** the thing being built is genuinely uncertain or contested, and more than one person must agree before work starts. Both conditions, or skip it.
* **Skip it when:** the outcome is already settled — a bug fix, a refactor, a migration, a config change, a fast-follow already scoped by an earlier PRD, or a throwaway that answers a question. None of these hold a product decision.
* **Split it when:** two parts of the ask have different problems, different users, or different measures of success. That is two PRDs.

## Interview Before Writing

Never draft a PRD from the opening request. A feature request is a proposed solution; the need sits underneath it and is usually different.

Ask in rounds (do not announce rounds numbers; make it natural). Batch the questions in each round into one message. Ask only what you cannot already answer from the conversation or the repository. Stop as soon as you can write falsifiable requirements — an interview that continues past that point is stalling.

**Round 1 — the problem.** Who hits it, how often, and what do they do today instead? What did the last person who complained actually say? What does the current workaround cost, in time or money or lost customers?

**Round 2 — the outcome.** What is different afterwards, observed from outside the system? What number moves, what is that number today, and what instrument reads it? Who decides it worked?

**Round 3 — the boundaries.** What is explicitly not being built? What must stay true — constraints, existing behaviour, other teams? What has to land elsewhere before this can ship? What budgets apply — speed, who may see the data, accessibility — and how is this turned off if it goes wrong?

## Interview Rules

* **Ask about the past, not the future.** "When did this last happen, and what did you do?" beats "would you use this?" A hypothetical answer is not evidence and must not be recorded as one.
* **Ask for the workaround.** What people already do by hand is the strongest evidence a problem is real, and it names the users for you.
* **Separate the requester from the user.** Ask who feels the problem. When the answer is "the user," ask which one and what they said.
* **Chase the solution back to its problem.** When the ask is phrased as a feature, ask what happens if it is not built. Keep asking until the answer is a consequence, not a missing feature.
* **Take no for an answer once.** If the user says a question does not matter, record it as an open question and move on. Do not re-ask.
* **Refuse to invent evidence.** When there is no number for how often the problem occurs, write "unquantified" in the PRD. Never estimate on the user's behalf.
* **Tone:** Dry, highly mechanical. Never use introductory acknowledgments (e.g., "Certainly!", "Here is the code", "Great idea!").

## Write Every Statement So It Can Fail

This is the whole discipline. A requirement that cannot be proven false is decoration.

* **Name an actor and an observable outcome.** "A signed-in user downloads their own transaction history as a CSV file." Not "support CSV export." If you cannot name what a person would see if the statement were false, rewrite it.
* **Ban unfalsifiable words.** Improve, better, seamless, robust, intuitive, user-friendly, optimise, streamline, modernise, world-class. Each hides the measurement. Replace with the thing that would be observed.
* **Give every metric four parts:** the number, its value today, the instrument that reads it, and the date it is read. A metric with no instrument has no source and will never be checked.
* **Write non-goals as statements too.** "No scheduled or recurring exports" can be checked. "Keep it simple" cannot.

## Output the PRD

Check the repository for an existing PRD convention and match it. Otherwise write to `docs/prd/<slug>.md`, where the slug matches the eventual `feature/{slug}` branch.

Keep it to one page unless the feature crosses teams. Link to designs, research and tickets rather than pasting them.

```text
Header:       Owner, participants, status, target release, links.
Problem:      Who hits it, how often, what they do today, what that costs.
Objective:    What is different afterwards. One sentence.
Metrics:      Table of metric, baseline, target, instrument, read date.
Users:        Who this is for, and what they do with the result.
Scope:        In scope. Then non-goals, as checkable statements.
Requirements: Numbered FRs. Actor plus observable outcome. Each marked P0, P1 or P2.
UX:           Links only.
Constraints:  Non-functional budgets — perf, permissions, accessibility — and the rollback path.
Assumptions:  What must stay true, and what is unvalidated.
Dependencies: What must land elsewhere first — teams, APIs, data, sign-offs.
Questions:    Open decisions, each with an owner and a needed-by date.
Done:         Completion checks. See below. Always the last section.
```

Mark every assumption that is unvalidated as unvalidated, and name what would test it.

Priorities mean: **P0** the feature does not ship without it, **P1** ships in the release but not the first cut, **P2** explicitly deferred.

## Define Done as a Checklist That Can Be Failed

Completion criteria are the PRD's last section. Every check is derived from content already in the PRD: the requirements, the dependencies, the non-goals, the open questions.

### Standard Checklist
- Every functional requirement has a passing acceptance test, and no shipped behavior lacks a requirement.
- Every open question is resolved in writing; behavioral resolutions have tests.
- Every non-goal is still true or explicitly revised.
- Every dependency has landed or is stubbed with a dated removal.
- Every metric emits in production and one value is verified against a known case.
- Every budget named under Constraints is measured and met.
- The rollback path named under Constraints has been exercised at least once.

## Review an Existing PRD
Reviewing is the same discipline run backwards: find the statements that cannot fail.

Read the whole document first, then report in this order. Quote the offending line for each finding.

* **Scale and Scope.** Detect if the PRD is larger than the thing it describes (e.g., a 400-line PRD for a 150-line CLI). Advise cutting to just Problem, Metrics, Requirements, and Done. Detect if there is no decision in it; if nothing is contested and one person could have built it unambigiously, it is a ticket, not a PRD. Say so.
* **Problem.** Name the solution hiding in it, if any. A problem statement that names a feature is a finding.
* **Template Padding.** Detect sections filled just to complete the template (e.g., "Users: our users", or an assumption that restates a requirement). Empty is better than furniture. Tell them to delete the section.
* **Falsifiability.** List every requirement, non-goal, and objective that cannot be proven false. Flag every banned word. Rewrite one as an example, not all of them.
* **Solution Leakage (Engineering & UX).** Detect if it is a design document wearing a PRD's name (schemas, endpoints, class names, code blocks, or chosen technologies). Say which parts belong in an ADR or implementation, and review only what is left. Similarly, flag requirements that describe screens (buttons, modals, and field layouts). These are UX and belong behind a link. Rewrite one as an outcome to show the difference.
* **Metrics.** Flag any metric missing a baseline, an instrument, or a read date. Flag an invented baseline. Flag a PRD with no metric at all.
* **Done.** Flag any check that is not derived from content in the PRD, and any PRD content — a dependency, a non-goal, an open question — that no check covers. Both directions.
* **Open Questions.** Flag any without an owner or a needed-by date. Flag decisions made silently in the requirements that belong here.

Report findings, ranked. Do not rewrite the PRD unless asked.

## Guardrails

* **Refuse to write a PRD with no problem.** If three rounds of interview produce only a description of a feature, say so and stop. Offer to record it as a decision instead.
* **Never put a solution in the problem statement.** "Users cannot get their data out" is a problem. "Users need an export button" is a solution wearing a problem's clothes.
* **Refuse to ship a PRD with no metric.** Require at least one metric with a named instrument. If the user will not give one, write that success is unmeasurable and name the person who accepted that. Never fill the gap with a plausible number.
* **Expect the requirements to be wrong in places.** Questions surface later, when someone tries to write a test against a requirement and finds they cannot. Route those back into the open questions section rather than deciding them silently.
* **Do not design.** No architecture, no schemas, no components, no technology choices. If the user supplies one, record it as a constraint and name who imposed it.
