---
name: reviewing
description: "Use this skill when something must be reviewed or critiqued: a pull request, a diff, an epic or story list, or code, a design, a plan or a fix idea the user made. Use it on: 'review PR 412', 'is this PR ready to merge', 'review what you built', 'security review', 'review this epic', 'are these the right stories', 'give me feedback', 'poke holes in this'. Reads what the subject lands on, has a second agent try to refute each finding before reporting it, and never rewrites the user's work."
license: MIT
compatibility: any-agent
metadata:
  version: "2.0.0"
---
# Reviewing

## Pick the review

The subject is the thing under review. When it is ambiguous, ask once.

| Subject | Load | Output |
|---|---|---|
| Any pull request or merge request, or a diff an agent built | [references/pull-request.md](references/pull-request.md) | Conventional Comments, blocking first, then Merge or Changes requested, printed; posted only when the user says to |
| Uncommitted code, a test, a design, a plan, an ADR or a fix idea the user made | [references/feedback.md](references/feedback.md) | Points sorted into Wrong, Unverified, Shape and Preference |
| An epic, a PRD's breakdown or a story list someone wrote | "Review an epic" below | The epic report |

Run the review, then the refute step, then report only what survives, in the subject's output.

## Rules every review keeps

* **Read the ground first:** the code the subject lands on and the code it calls. Read the merge target for every name the change claims (a key, a route, a column, a variable, a flag). Check a fix idea against every caller of what it changes. Never judge from the subject's description of itself. When the ground cannot be read, say what is missing and give only the points that stand without it.
* **Read what the tools reported first.** Never raise by hand what a tool that ran owns. Where one did not run, do its job and name it.
* **A finding needs a failure behind it:** the input, the sequence, the caller. Without one it is a preference.
* **List every candidate, doubted ones included,** one line each in `findings.md` in the git directory (`git rev-parse --git-dir`): `<n>. <anchor> — <what breaks> — case: <...> — blocking | non-blocking[ — rule]`. The anchor is `<file>:<line>`, `<document>:<section>` or `<card>:<field>`. Mark `rule` where a pattern could match it; after the report, offer the `guardrails` skill once for all surviving ones.
* **Never rewrite the user's work.** Describe the change; write code only when asked.

## Refute

Start one fresh subagent that found none of the candidates, on another model where the harness offers one, with `findings.md`, the subject's path and the merge target, and nothing else. It treats each candidate as false until the subject shows the failure, reads what the case passes through, runs it where it can, and marks each: `confirmed` (the line or command that shows it), `refuted` (the line that stops it), `unsettled` (the one test that would settle it) or `lowered` (the new severity and the line that bounds it). A comment, a docstring or the finder's wording never settles one.

| Output | `confirmed` or `lowered` | `unsettled` | `refuted` |
|---|---|---|---|
| Pull request | `issue` comment | `question` comment with the settling test | `Refuted:` line |
| Feedback | `Wrong:` point | `Unverified:` point with the settling test | dropped |
| Epic | a finding line | `Unanswered:` line | `Refuted:` line |

## Review an epic

An epic is one tracker issue whose child issues are its stories (changes a person can observe) and spikes, linked by blocking links; read them through the tracker the `Backlog:` line of `AGENTS.md` names, or from what the user pasted. Change nothing without the owner's agreement. Read every comment on every card first. Report, quoting the text each is about:

* **No shared understanding:** no outcome a person would notice, no success signal someone can check, no non-goals.
* **Not a story:** a card for something a person cannot perceive alone (a requirement on how well another story behaves, an enabler like a column or a service, a property, a task, a decision). Say which story it folds into as criteria.
* **Too many cards:** siblings that are one story. Search for one distinctive sentence; the cards containing it are the ones to merge.
* **Ships nothing:** a story that leaves no person able to do something new, or covers more than one workflow step and one variation.
* **Wrong blocker:** a link in the wrong direction, a story shown ready whose blocker was dropped with a closed ticket, a hardening story blocked by the story it hardens.

```text
Unanswered:      <card> "<quoted comment>" -> <what in the card it changes>
No shared understanding: <the missing line> -> <the question for the owner>
Not a story:     "<title>" -> <kind> -> criteria on <story>
Too many cards:  <cards> -> <shared sentence> -> one story
Ships nothing:   "<title>" -> <what a person still cannot do>
Wrong blocker:   <story> -> <what blocks it in fact>
Refuted:         <card>:<field> -> <what was raised> -> <what stops it>

Ready to build.   (or: <n> blocking items)
```

Before deleting cards the owner agreed to delete, archive each in full, confirm each named person's comment survives on a remaining card, and rewrite every remaining mention of a deleted key.
