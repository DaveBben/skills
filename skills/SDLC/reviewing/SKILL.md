---
name: reviewing
description: "Use this skill when something must be reviewed or critiqued: code the agent built before it is committed or merged, a pull request someone opened, an existing epic or PRD breakdown, or code, a design, a plan or a fix idea the user made. Use it on: 'review what you built', 'review the diff before I commit', 'what can be deleted', 'review PR 412', 'is this PR ready to merge', 'approve or request changes', 'review this epic', 'refine this epic', 'are these the right stories', 'there are too many tickets', 'give me feedback', 'critique this', 'poke holes in this', 'is my approach good'. Picks the review for the subject, reads what the subject lands on before judging, refutes each finding before reporting it, and never rewrites the user's work. Not for a story or ticket, or test coverage even of tests the user wrote (`story`), a choice not yet made (`architecture`), drafting stories (`define-work`), or writing a pull request description (`deliver`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Reviewing

Load [references/writing.md](references/writing.md) before the first reply. Every finding and every report follows it.

## 1. Pick the review

The subject is the thing under review. Who made it decides the review, whatever the request calls it: a diff the user wrote gets the feedback review even when the request says "review the diff before I commit". Load the one reference file for it. When it is ambiguous which, ask once.

| Subject | Load | Output |
|---|---|---|
| Code an agent built, before it is committed or merged | [references/built-code.md](references/built-code.md) | The Done block |
| A pull request or merge request someone opened | [references/pull-request.md](references/pull-request.md) | One finding per line, then Merge or Changes requested |
| An existing epic, a PRD's breakdown or a story list someone else wrote | [references/epic.md](references/epic.md) | The epic report |
| Code, a test's quality, a design, a plan, an ADR, a check configuration or a fix idea the user or a colleague made | [references/feedback.md](references/feedback.md) | Points sorted into Wrong, Unverified, Shape and Preference |

`deliver` runs this skill in a review subagent on the code its builder returned, which takes the built-code review. When the user wrote the story's code, `deliver` asks for the feedback review instead. A request that also asks for a pull request description gets the review first, then the `deliver` skill's path for describing a branch. An `AGENTS.md` or `CLAUDE.md` goes to the `orient` skill's Review; whether a change's tests cover it goes to the `story` skill.

## 2. Rules every review keeps

* **Read the ground before judging.** The ground is the code the subject lands on and the code it calls. Read the merge target for every name the change claims: a storage key, a route, a column, an environment variable, a flag, an event name. A bug-fix idea is checked against every caller of the function it changes. Never assess from the subject's own description of the code.
* **When the ground cannot be read,** say which file or symbol is missing and give only the points that stand without it.
* **Read what the tools already reported first.** A mutation report, static analysis, the formatter and the linter each own a class of finding. Never raise by hand what a tool that ran owns. Where a tool did not run, do its job on the diff and name the tool the review stood in for.
* **Refute before reporting.** Every finding starts as a false positive and is overturned only by reading the code on the path it names. Say what it rests on: read this run, inferred from something read this run, or asserted by a tool, a comment or a document. A comment raises a concern and never lowers one. A claim that would change a rating and cannot be checked ships as a question plus the one test that would settle it.
* **A finding needs a failure behind it.** Give the concrete case: the input, the sequence, the caller. Without one it is a preference; say so or leave it out.
* **Send every confirmed finding a pattern could match to the `guardrails` skill,** so nothing is found by hand twice. Inside a subagent, return them as a `Rules:` line with the report; the session that called it hands them over.
* **Never rewrite the user's work.** Describe the change. Write code only when the user asks for it.

## What this skill does not do

Writing or reviewing one story's criteria, and checking a change's tests for gaps, is `story`. Weighing a technology or design choice not yet made is `architecture`. Drafting the stories for a piece of work is `define-work`. Writing a pull request description is `deliver`.
