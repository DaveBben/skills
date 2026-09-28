---
name: reviewing
description: "Use this skill when something must be reviewed or critiqued: code the agent built, a pull request someone opened, an existing epic or PRD breakdown, or code, a design, a plan or a fix idea the user made. Use it on: 'review what you built', 'review PR 412', 'is this PR ready to merge', 'review this epic', 'are these the right stories', 'give me feedback', 'poke holes in this', 'security review'. Picks the review for the subject, reads what the subject lands on, has a second subagent try to refute each finding before reporting it, and never rewrites the user's work. Not for a story, a ticket or test coverage (`define`), a choice not yet made (`architecture`), or a pull request description (`deliver`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.11.0"
---
# Reviewing

## 1. Pick the review

The subject is the thing under review. Who made it decides the review, whatever the request calls it: a diff the user wrote gets the feedback review even when the request says "review the diff before I commit". Load the one reference file for it. When it is ambiguous which, ask once.

| Subject | Load | Output |
|---|---|---|
| Code an agent built, before it is committed or merged | [references/built-code.md](references/built-code.md) | The Done block |
| A pull request or merge request someone opened | [references/pull-request.md](references/pull-request.md) | Conventional Comments (label, blocking or non-blocking, subject, discussion), blocking first, then Merge or Changes requested |
| An existing epic, a PRD's breakdown or a story list someone else wrote | [references/epic.md](references/epic.md) | The epic report |
| Code, a test's quality, a design, a plan, an ADR, a check configuration or a fix idea the user or a colleague made | [references/feedback.md](references/feedback.md) | Points sorted into Wrong, Unverified, Shape and Preference |

**A subagent a caller started for one step runs only that step.** A review subagent runs step 1 below and writes `Security: pending` and `Refuted: pending` into its output file. A security or refuter subagent follows only the file it was given.

**The session that runs the whole review runs it in this order:**

1. **The review of the subject,** by the reference above. It writes its candidates to `findings.md` in the worktree's git directory (`git rev-parse --git-dir`), replacing any old one; outside a repository, it keeps them for the refuter's prompt.
2. **For code, the security review,** as two subagents in turn, neither given the chat. Give the first [references/security-map.md](references/security-map.md) and the second [references/security-review.md](references/security-review.md), each with the worktree path, the merge target and the branch. A request for a security review of the whole repository runs only this step and the next two.
3. **One refuter** over every candidate, by [references/refute.md](references/refute.md).
4. **The report,** in the subject's output, by the verdict table in `refute.md`.

A request that also asks for a pull request description gets the review first, then the `deliver` skill's path for describing a branch. An `AGENTS.md` or `CLAUDE.md` goes to the `orient` skill's Review; whether a change's tests cover it goes to the `define` skill.

## 2. Rules every review keeps

* **Read the ground before judging.** The ground is the code the subject lands on and the code it calls. Read the merge target for every name the change claims: a storage key, a route, a column, an environment variable, a flag, an event name. A bug-fix idea is checked against every caller of the function it changes. Never assess from the subject's own description of the code.
* **When the ground cannot be read,** say which file or symbol is missing and give only the points that stand without it.
* **Read what the tools already reported first.** A mutation report, static analysis, the formatter and the linter each own a class of finding. Never raise by hand what a tool that ran owns. Where a tool did not run, do its job on the diff and name the tool the review stood in for.
* **A finding needs a failure behind it.** Give the concrete case: the input, the sequence, the caller. Without one it is a preference; say so or leave it out.
* **List every candidate, doubted ones included, and report only what the refuter leaves standing.** Doubt is the refuter's job. Only a claimed failure is a candidate: a `todo`, an equivalent mutant and a finding a failing test already shows skip the refuter. One line per candidate in `findings.md`; the security review appends, numbering on from the last line:

  ```text
  <n>. <review | security> — <anchor> — <what breaks, in one line> — case: <input, sequence or caller> — <blocking | non-blocking>[ — rule]
  ```

  The anchor is `<file>:<line>` for code, `<document>:<section>` for a design, plan or ADR, and `<card>:<field>` for an epic. Mark `rule` on a candidate a pattern could match.
* **Send every `confirmed` or `lowered` finding marked `rule` to the `guardrails` skill,** so nothing is found by hand twice.
* **Never rewrite the user's work.** Describe the change. Write code only when the user asks for it.
