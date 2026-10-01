---
name: spike
description: "Use this skill when the user wants to find something out by building throwaway code rather than ship it: proving an approach, prototyping, mocking something up (not a test double), a demo, comparing approaches, or exploring what an integration or change would involve. Use it on: 'let's prove this works first', 'let's prototype this idea', 'let's mock this up', 'build a quick throwaway', 'build a demo', 'let's do a spike on it', 'is X feasible', 'let's see how this integration would work', 'what would it take to move to X', 'try a few approaches and see which works best', 'test whether X makes Y faster', 'find the best model for this'. Use it on the words prototype, mock, demo, throwaway, spike, feasible, experiment and explore even when the ask sounds small. Builds the smallest thing that answers one question inside a timebox, records findings as they surface, and deletes the code. Not for code meant to ship; that is `story`."
license: MIT
metadata:
  version: "3.0.0"
---
# Spike

A spike answers one question with the smallest throwaway code inside a timebox, records what it learned, and deletes the code.

## Frame it

First, when a doc, the source, a changelog or one command answers the question, answer it from there and stop. A spike is for a question only running code can answer.

Before any code, agree three things with the user in one message:

1. **The question:** an outcome that can fail, like "the library streams partial results under 200 ms at 1,000 rows on the staging database", not "look into the library".
   * Name the data size, load and environment each threshold is measured under.
   * Turn an open ask into a closed one: "what would it take to move to X" becomes "X runs with changes only to Y, and here is the list".
   * With no crisp question, ask one question to get it. Refuse a spike with no failing condition.
2. **The finish line:** the observable signal that answers the question.
   * For a judgement only the user can make (a mock-up, a layout, a demo), the signal is their choice or reaction. Keep the code until they have seen it.
3. **The timebox:** a number of attempts by default; an attempt is one approach run to a result or an error.
   * Propose it for the user to correct. With several approaches, it covers all of them together.
   * For a timebox in minutes, write the start time from `date` in the findings header and check it before each attempt.

When the user links a spike issue on a tracker (Jira, GitHub, GitLab or another), read the three from it, ask only for what is missing or cannot fail, and write the findings as a comment on it.

In that message, or before building when the issue left nothing to ask, tell the user the code is throwaway: deleted once the findings are written, never merged. A demo meant to outlive the spike is code meant to ship; that is `story`.

## Build it

* **Location:** a scratch directory (the harness's scratchpad where it has one), outside the main checkout.
* **When the question needs the repository's code:** a worktree with no branch, so no branch outlives it.

```bash
git worktree add --detach <path>
```

* **Throwaway style:** hardcode, inline, copy-paste. No tests, no linter, no formatter, no fixing type errors that do not block the question.
* **The one test allowed:** the one the question can only be observed through (a performance budget, a contract, a race).
* **Several plausible answers:** name them to the user rather than silently picking one.
* **Measure once:** build one measurement first and run every candidate through it.
* **Build each candidate** at its smallest, in parallel subagents and worktrees where the harness allows, else one after another, each in its own directory.
* **Subagent findings** return to the session that started the spike, which alone writes them. Recommend on what they measured.
* **A missing tool:** install it into the scratch directory only.
* **A missing credential:** ask for it once, by its exact variable or file name. Never fake one, and never point the spike at a live system to get around it.
* **A command that errors:** record it with its exact error before anything else is tried.
* **A wall the spike cannot pass:** go to the user with the finding that shows it and what would clear it.
* **One question per spike:** a second unknown goes to the open questions. It becomes a spike of its own only on the user's go-ahead.
* **Work that outgrows the smallest thing that answers the question:** stop and say the question is larger than a spike.

## Record as you go

Write the findings from the first one, never only in chat. Pick the destination:

* **In a git repository:** `docs/spikes/<question-slug>.md`, committed alone on branch `spike-findings/<question-slug>` in a worktree of its own, never in the throwaway worktree.
* **Then offer the user** a pull request of that file alone.

```bash
git worktree add -b spike-findings/<question-slug> <path> <default branch>
```

* **With no repository:** `<question-slug>.md` in the scratch directory, its path shown to the user.
* **When the user names a tracker:** a comment on the spike's issue.
* **A timebox of one attempt or under an hour:** the reply only.

Add each line the moment it surfaces, and repeat a line for each finding of its kind. Write the approach in prose and API names, never code blocks, so no spike code reaches the real build.

```text
## <date> — spike: <the question> — timebox: <limit>, started <time>
- Learned: **Outcome:** proven | disproven | inconclusive — <the evidence that settles it>, measured on <data size, load, environment>; differs from production in <what>
- Learned: **Approach used:** <libraries, APIs and calls, in the order that produced the result>
- Learned: **Quirks and surprises:** <undocumented behaviour, version limits, ordering, silent failures, rate limits>
- Learned: **Dead ends:** <approach tried> — <what it did instead of working>
- Learned: **Open questions:** <what the real build must still settle>
- Learned: **Decided alone:** <what was chosen> over <the alternative> — <why>; one line per choice made without the user that the real build would inherit
- Learned: **Recommendation:** build with <approach> | don't build | re-scope to <what> — <why>
- Learned: **Changes to the plan:** <stories added, dropped, reordered or re-sized, and how cost or risk moved>
```

The outcome is inconclusive when a difference from production could flip it.

## When it resolves

* **Stop at the finish line.**
* **Timebox out first:** stop. The outcome is inconclusive.
* **Then ask the user** to extend, drop or defer. Recommend one and say what the next attempt would try.
* **After a second inconclusive spike toward the same goal:** ask whether to build, drop or re-scope.

1. **State the verdict,** the finding that settles it, and the recommendation.
2. **Put the `Decided alone` lines to the user** in one table. The user marks each row.
   * `record`: record it with the `adr` skill.
   * `drop`: leave it as its line.
   * `defer`: move it to the open questions.

```text
| Chosen | Rejected | Why | Cost to change later | record / drop / defer |
```

3. **Update the plan:** when a feature file (the file holding a feature's stories and their `Order:`) or a tracker issue lists the stories this spike unblocks, mark its question answered, apply the `Changes to the plan` line, and link the findings.
4. **Return to the split:** when `story` started the spike while splitting a request, return to that split with the findings.
5. **Delete the spike code** once the user accepts the verdict, and say so in the findings.

```bash
git worktree remove --force <path>
```

Or remove the scratch directory. Never open a pull request of spike code or evolve it into the real build. The real build starts fresh from the findings, by the `story` skill.
