---
name: spike
description: "Use this skill when the user wants to find something out by building throwaway code rather than ship it: proving an approach, prototyping, mocking something up (not a test double), a demo, comparing approaches, or exploring what an integration or change would involve. Use it on: 'let's prove this works first', 'let's prototype this idea', 'let's mock this up', 'build a quick throwaway', 'build a demo', 'let's do a spike on it', 'is X feasible', 'let's see how this integration would work', 'what would it take to move to X', 'try a few approaches and see which works best', 'test whether X makes Y faster', 'find the best model for this'. Use it on the words prototype, mock, demo, throwaway, spike, feasible, experiment and explore even when the ask sounds small. Builds the smallest thing that answers one question inside a timebox, records findings as they surface, and deletes the code. Not for code meant to ship; that is `deliver`."
license: MIT
metadata:
  version: "2.0.0"
---
# Spike

A spike answers one question with the smallest throwaway code inside a timebox, records what it learned, and deletes the code.

## Frame it

When the user links a spike issue on a tracker (Jira, GitHub, GitLab or another), it is already scoped: read the question, finish line and timebox from it, skip this section, start building, and write the findings as a comment on that issue.

Otherwise, before any code, agree three things with the user in one message:

* **The question,** as an outcome that can fail: "the library streams partial results under 200 ms", not "look into the library". When the user has no crisp question, ask one question to get it. Refuse a spike with no failing condition.
* **The finish line:** the observable signal that answers it.
* **The timebox:** a wall-clock limit or a number of attempts, proposed for the user to correct.

In the same message, tell the user the code is throwaway: deleted once the findings are written, never merged.

## Build it

* **Outside the main checkout:** a scratch directory (the harness's scratchpad where it has one), or a throwaway git worktree when the question needs the repository's code.
* **Throwaway style:** hardcode, inline, copy-paste. No tests, no linter, no formatter, no fixing type errors that do not block the question, except the one test the question can only be observed through (a performance budget, a contract, a race).
* **Several plausible answers:** name them to the user rather than silently picking one, build the smallest version of each, in parallel subagents and worktrees where the harness allows (else one after another, each in its own directory), and recommend on what they measured.
* **A missing tool** installs into the scratch directory only. **A missing credential** is asked for once, by its exact variable or file name; never fake one, and never point the spike at a live system to get around it. **A command that errors** is recorded with its exact error before anything else is tried. **A wall the spike cannot pass** goes to the user with the finding that shows it and what would clear it.
* **One question per spike.** A second unknown is an open question and a spike of its own. When the timebox runs out, or the work outgrows the smallest thing that answers the question, stop and say the question is larger than a spike.

## Record as you go

Write the findings from the first one, never only in chat, to `docs/spikes/<question-slug>.md` on a branch of its own, or as a comment on the spike's issue when the user names a tracker. Add each line the moment it surfaces, and repeat a line for each finding of its kind:

```text
## <date> — spike: <the question>
- Learned: **Outcome:** proven | disproven | inconclusive — <the evidence that settles it>
- Learned: **Approach used:** <libraries, APIs and calls, in the order that produced the result>
- Learned: **Quirks and surprises:** <undocumented behaviour, version limits, ordering, silent failures, rate limits>
- Learned: **Dead ends:** <approach tried> — <what it did instead of working>
- Learned: **Open questions:** <what the real build must still settle>
- Learned: **Decided alone:** <what was chosen> over <the alternative> — <why>; one line per choice made without the user
```

## When it resolves

Stop at the finish line. When the timebox runs out first, the outcome is inconclusive; say what the next attempt would try.

1. **State the verdict** and the finding that settles it.
2. **Put the `Decided alone` lines to the user** that are expensive to change, accept a hazard, reject an alternative or cost time to learn, in one table. The user marks each row; record each `record` row with the `adr` skill, leave a `drop` as its line, and move a `defer` to the open questions. Do not skip a row because it looks small.

```text
| Chosen | Rejected | Why | Cost to change later | record / drop / defer |
```

3. **Delete the spike code** once the findings are complete, and say so in them. Never open a pull request of spike code or evolve it into the real build; the real build starts fresh from the findings, by the `story` and `deliver` skills.
