# Refute every finding

## Starting the refuter

Start one fresh subagent that found none of the candidates, on another model where the harness offers one. Give it this file, `findings.md`, the worktree path, the merge target and the branch. When the subject is not code in the repository, add the subject's text or path (the design, the plan, the fix idea, the tracker's cards), its job, and every constraint the user stated for it. When the output is a file, such as `done-block.md`, add its path and its row in the verdict table. Give it nothing else: not the finders' reasoning and not the rest of the chat.

Where the harness has no subagents, run it in a fresh session where the harness allows one. Otherwise refute inline, and say once in the report that the same agent found and refuted the findings.

## The refuter's work

Treat every candidate as false until the subject shows the failure. For each one, read what the case passes through, run the case where you can, and append one verdict to its line in `findings.md`:

* **`confirmed`:** name the `<file>:<line>` read or the command run that shows the failure.
* **`refuted`:** name the line that stops the case: a guard, a type, a constraint, or a caller that never passes that input.
* **`unsettled`:** neither reading nor a run settles it. Name the one test that would.
* **`lowered`:** the failure is real and less severe. Give the new severity and the line that bounds the damage.

A comment, a docstring, a test name or a finder's wording never confirms or refutes. Two documents by the same author are one source. Expect most severity claims to come down once the code on the path is read.

When you were given an output file, write the verdicts into it by the table below, then delete `findings.md`. Return the count per verdict and the number of blocking findings left.

## Verdict table

`lowered` takes the row of `confirmed` at its new severity.

| Output | `confirmed` | `unsettled` | `refuted` |
|---|---|---|---|
| Pull request | `issue` comment | `question` comment with the settling test | `Refuted:` line in the review body |
| Done block | a `review` candidate on `Findings:`, a `security` one on `Security:` | `Exceptions:` | `Refuted:` |
| Feedback | `Wrong:` point | `Unverified:` point with the settling test | dropped |
| Epic report | its report line | its report line, ending `(unsettled: <settling test>)` | `Refuted:` line |
| Security review of the whole repository | one line: `<file>:<line>`, the path, the input that breaks it, blocking or not | the same, ending `(unsettled: <settling test>)` | `Refuted:` line |

Every `Refuted:` entry gives the anchor, what was raised and the line that stops it, so the user can check the refuter.

In a Done block, every row starts with its field's label, so a grep for the label returns every row:

* **`Findings:`** `<file>:<line>`, what breaks, the case, blocking or not. Replace the field.
* **`Security:`** `<file>:<line>`, the path, the input that breaks it, blocking or not. Replace `Security: reviewed, <n> candidates`.
* **`Rules:`** `<file>:<line>` and the pattern, for each `confirmed` or `lowered` candidate marked `rule`. Replace the field.
* **`Exceptions:`** `<file>:<line>`, what was raised, the one test that would settle it. Append; keep the rows already there.
* **`Refuted:`** replace `Refuted: pending`, with `none` when nothing was refuted.
