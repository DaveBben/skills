---
name: bug
description: "Use this skill whenever code that exists behaves wrongly, or a list of open bugs must be sorted: a bug report, a crash, a wrong value, an error a user hit, a regression, or a bug backlog. Use it on: 'fix the bug where X', 'X is broken', 'X stopped working', 'users are getting this error', 'this returns the wrong value', 'here is a bug report', 'fix issue 42' when the issue reports a bug, 'triage our bugs', 'clean up the bug backlog', 'why do we keep getting these bugs'. Load it before reading the code. Reproduces the bug, decides fix now, story or won't fix, hands the fix to the story skill's build, then finds why the bug escaped and proposes the criterion, check or ADR that closes that gap. Not for behaviour nobody asked for before; that is `story`. Not for a test alone, with no fix asked; that is `failing-tests`."
license: MIT
metadata:
  version: "1.0.0"
---
# Bug

A bug is fixed when it is found, through a test that fails on it first, and then the gap that let it through is closed. A bug never waits open "for later": it is fixed, becomes a story, or is closed as won't fix.

## Words used here

* **Bug:** behaviour that contradicts what the code was built to do: an acceptance criterion, a documented contract, a crash, an error the caller cannot act on, or lost or exposed data.
* **Reproduction:** the starting state, the action, what happens now and what should happen instead, in real values. It is the fix's one acceptance criterion.
* **Escape:** how the bug got past the tests and the review before it merged.
* **Won't fix:** a bug closed on purpose, with its workaround or reason written where the next reporter will find it.

## 1. Contain first when it is live

When the bug loses or exposes data, or blocks every user of a path in production, tell the user before anything else. Name the fastest step that stops the harm (revert the commit that introduced it, turn off its flag, roll back the deploy) and let the user choose it. The fix comes after.

## 2. Reproduce

* **Read the report whole:** a tracker issue by the `using-trackers` skill, its comments included, and every log, stack trace and step the user gave.
* **Run it** at the lowest level that shows the fault: the command, the request, one call. Record the exact output.
* **Find where it entered** when a command does it cheaply: `git log -S '<code>'`, or `git bisect run` with the reproduction. The commit names the story whose criteria missed it.
* **Cannot reproduce:** never fix blind. Ask the reporter for the missing fact by name (version, input, environment), or add the logging that would show it, and stop.
* **Not a bug:** the code does what its acceptance criteria or contract state, and the report wants something else. Show the user the criterion the code follows; the request is a new story, by the `story` skill.

## 3. Decide

* **Fix now,** the default: the reproduction is the only acceptance criterion, and the fix needs no answer from the user.
* **Story:** the fix needs a product decision, changes what callers see beyond the reproduction, or covers more than one path. Write it by the `story` skill, with the reproduction as criterion 1 marked `changes:`.
* **Won't fix:** the harm costs less than the fix, and the user agrees. Close it with the workaround or reason in a comment, by the `using-trackers` skill when it has an issue.
* **Same fault elsewhere:** search for the faulty pattern in other callers and copies. Each hit under the same rule is another example under the one criterion; a hit under a different rule is its own bug.

## 4. Fix

Build the fix by the `story` skill's implement path, `../story/references/implement.md` from this skill's folder, with the reproduction as the one acceptance criterion. Its failing-tests step writes the reproduction as a test that fails for the reported reason before any code changes. Fix the cause where the wrong value is first produced, in the shared code, never in the caller that reported it.

## 5. Why it escaped

Before the report, name the first of these that holds:

* **Requirements:** no example covered the input that failed, such as a coupon larger than the cart. Name the missed kind of input. When `git log --grep` or the tracker shows the same kind escaped before, propose it as a rule by the `guardrails` skill, so later stories include it.
* **Test:** an example covered it, and its test passed the wrong code. The new locked test closes it.
* **Design:** the file holding the fault has earlier fixes in `git log --oneline -- <file>`, or the faulty logic is duplicated. Propose a refactor as its own change.
* **Systemic:** a program could detect this kind of fault (an unchecked null, a missing migration, a banned call). Propose the check by the `guardrails` skill.
* **Accepted risk:** the hazard was known and taken. Propose recording it by the `adr` skill when no ADR holds it.

Propose; build none of these without the user's go-ahead.

## Triage a backlog

1. **Read** the open bugs by the `using-trackers` skill, filtered by the label or query the user names.
2. **Propose** one decision per bug from section 3, plus `duplicate of #N` and `cannot reproduce: ask the reporter for <fact>`. Reproduce only a bug whose decision turns on it.
3. **Group** bugs in one file or of one kind, and propose their escape from section 5 once.
4. **Show** the user one table, and apply only the rows they approve:

```text
| Issue | Decision | Why | Escape |
```

Fix the rows marked fix now one at a time, through sections 2 to 5.

## Report

```text
Bug: <reproduction in one line>; entered: <commit or "not found">
Decision: fix now | story | won't fix — <why>
Fix: <pull request or "none">; same fault elsewhere: <places or "none">
Escape: requirements | test | design | systemic | accepted risk — <evidence>
Proposed: <the rule, check, refactor or ADR>; or "none"
```
