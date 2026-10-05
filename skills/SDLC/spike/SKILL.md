---
name: spike
description: "Use this skill when the user wants to find something out that throwaway code would answer, including a question about feasibility, effort or impact asked with no request to build: a spike, a prototype, a demo, a mock-up (not a test double), an experiment, a comparison of approaches, or what adopting a library, service or integration would do to this codebase. Use it on: 'let's do a spike on X', 'let's do a demo of X', 'I want to run an experiment on X', 'prototype this', 'what would X look like in my codebase', 'how would adding X affect my code', 'how hard would it be to set up X', 'is X feasible', 'would X make Y faster', 'could we reach X using Y', 'what would it take to move to X', 'try a few approaches and see'. Load it before reading code or answering from memory about this codebase. Builds the smallest thing that answers one question in a timebox, records findings and deletes the code. Not for what a tool is or how two libraries differ in general. Not for code meant to ship; that is `story`."
license: MIT
metadata:
  version: "3.1.0"
---
# Spike

## Frame it

First, when a doc, the source, a changelog or one command answers the question, answer it from there and stop. A spike is for a question only running code can answer.

Before any code, agree three things with the user in one message:

1. **The question:** an outcome that can fail, like "the library streams partial results under 200 ms at 1,000 rows on the staging database", not "look into the library".
   * Name the data size, load and environment each threshold is measured under.
   * Turn an open ask into a closed one: "what would it take to move to X" becomes "X runs with changes only to Y, and here is the list".
   * With no crisp question, ask one question to get it. Refuse a spike with no failing condition.
2. **The finish line:** the observable signal that answers the question.
   * For a judgement only the user can make (a mock-up, a layout, a demo), the signal is their choice or reaction. Keep the code until they have seen it.
   * Write such a question as the user's choice, such as "the user picks layout A or B, or rejects both"; rejecting both is its failing condition.
3. **The timebox:** a number of attempts by default; an attempt is one approach run to a result or an error.
   * Propose it for the user to correct. With several approaches, it covers all of them together.
   * For a timebox in minutes, write the start time from `date` in the findings header and check it before each attempt.

When the user links a spike issue on a tracker (Jira, GitHub, GitLab or another), read the three from it by the `using-trackers` skill and ask only for what is missing or cannot fail. To file a spike on a tracker, put the three in it and nothing else, by the `using-trackers` skill.

In that message, or before building when the issue left nothing to ask, tell the user the code is throwaway: deleted once you accept the findings, never merged. A demo meant to outlive the spike is code meant to ship; that is `story`.

## Build it

* **Location:** a scratch directory (the harness's scratchpad where it has one), outside the main checkout.
* **When the question needs the repository's code:** a worktree with no branch, so no branch outlives it.

```bash
git worktree add --detach <spike-path>
```

* **Throwaway style:** hardcode, inline, copy-paste. No tests, no linter, no formatter, no fixing type errors that do not block the question.
* **The one test allowed:** the one the question can only be observed through (a performance budget, a contract, a race).
* **Several candidate approaches:** list them to the user, build one measurement first, then run each candidate through it at its smallest: in parallel subagents and worktrees where the harness allows, else one after another in separate directories. Make the choices inside one candidate alone and log them as `Decided alone` lines.
* **Subagent findings:** you alone write the findings file. Base the recommendation on the numbers subagents return, not on their opinions.
* **A missing tool:** install it into the scratch directory only.
* **A missing credential:** ask for it once, by its exact variable or file name. Never fake one, and never point the spike at a live system to get around it.
* **A command that errors:** record it with its exact error before anything else is tried.
* **A wall the spike cannot pass:** go to the user with the finding that shows it and what would clear it.
* **One question per spike:** a second unknown goes to the open questions. It becomes a spike of its own only on the user's go-ahead.
* **Work that outgrows the smallest thing that answers the question:** stop and say the question is larger than a spike.

## Record as you go

Write the findings from the first one. Use the first destination that applies:

* **A linked tracker issue:** a comment on it, by the `using-trackers` skill.
* **A timebox of one attempt:** a findings block in the reply, with the header line.
* **In a git repository:** `docs/spikes/<question-slug>.md` on branch `spike-findings/<question-slug>`, in a worktree of its own, never in the throwaway worktree. Commit the file alone when the spike resolves, then offer the user a pull request of that file alone.
* **Otherwise:** `<question-slug>.md` in the scratch directory, its path shown to the user.

```bash
git worktree add -b spike-findings/<question-slug> <findings-path> <default branch>
```

Add each line the moment it surfaces, and repeat a line for each finding of its kind. Write the approach in prose and API names, never code blocks, so no spike code reaches the real build.

```text
## <date> — spike: <the question> — timebox: <limit>, started <time>
* **Outcome:** proven | disproven | inconclusive — <the evidence that settles it>, measured on <data size, load, environment>; differs from production in <what>
* **Approach used:** <libraries, APIs and calls, in the order that produced the result>
* **Quirks and surprises:** <undocumented behaviour, version limits, ordering, silent failures, rate limits>
* **Dead ends:** <approach tried> — <what it did instead of working>
* **Open questions:** <what the real build must still settle>
* **Decided alone:** <what was chosen> over <the alternative> — <why>; cost to change later: <what>. One line per choice made without the user that the real build would inherit.
* **Recommendation:** build with <approach> | don't build | re-scope to <what> — <why>
* **Changes to the plan:** <stories added, dropped, reordered or re-sized, and how cost or risk moved>; only when a feature file or tracker issue lists the stories
```

The outcome is inconclusive when a difference from production could flip it.

## When it resolves

* **Finish line reached:** do steps 1–5.
* **Timebox runs out first:** stop and mark the outcome inconclusive. Ask the user to extend, drop or defer, recommend one, and say what the next attempt would try. On extend, keep the code and continue; on drop or defer, do steps 1–5.
* **Second inconclusive spike on the same question** (an earlier findings file or issue comment exists): ask whether to build, drop or re-scope.

1. **State the verdict,** the finding that settles it, and the recommendation.
2. **Put the `Decided alone` lines to the user** in one table. The user marks each row.
   * `record`: record it with the `adr` skill.
   * `drop`: leave it as its line.
   * `defer`: move it to the open questions.

```text
| Chosen | Rejected | Why | Cost to change later | record / drop / defer |
```

3. **Update the plan:** on the spike's issue, by the `using-trackers` skill, or under the spike's story in the feature file (`docs/stories/<slug>.md`), mark its question answered and link the findings. Apply the `Changes to the plan` line to the stories and their order. Move `defer` rows to the `Open questions` of the story each blocks.
4. **Return to the split:** when `story` started the spike while splitting a request, return to that split with the findings.
5. **Delete the spike code** once the user accepts the verdict, and say so in the findings.

```bash
git worktree remove --force <spike-path>
```

Or remove the scratch directory. Remove the findings worktree once its branch is pushed. Never open a pull request of spike code or evolve it into the real build. The real build starts fresh from the findings, by the `story` skill.
