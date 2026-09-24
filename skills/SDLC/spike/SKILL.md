---
name: spike
description: "Use this skill whenever the user wants to find something out by building, rather than to ship what they build: proving an approach, prototyping an idea, mocking something up (not a test double), standing up a demo, or exploring what an integration or change would involve. Use it on: 'let's prove this works first', 'let's try an approach before building', 'let's prototype this idea', 'let's mock this up', 'create a throwaway project', 'build a quick throwaway', 'build a demo', 'let's do a spike on it', 'let's see if X is feasible', 'let's see how this integration would work', 'let's see the changes which would be needed', 'explore how this would fit into the system'. Use it on the words prototype, mock, demo, throwaway, spike, feasible and explore even when the ask sounds small: deciding what is disposable is the whole point. Build the smallest thing that answers the open question, record findings as they surface, and treat all code as disposable. Do not use it for code meant to ship; that is `agile`."
license: MIT
compatibility: any-agent
metadata:
  version: "0.6.0"
---
# Spike

Prove or disprove a specific assumption with the smallest amount of throwaway code.

## Frame the Spike Before Writing Code

Establish two facts with the user before touching the filesystem:

* **The question:** The single assumption or feasibility unknown the spike must resolve. State it as a falsifiable outcome: "the library can stream partial results under 200ms", not "look into the library." When the user has no crisp question, ask one question to extract it. Refuse to start a spike that has no failing condition.
* **The finish line:** The observable signal that answers the question.

## Declare the Code Disposable

State to the user, before writing any code, that everything produced in this spike is throwaway: this code will be deleted, not merged.

Hardcode values. Skip abstraction. Inline everything. Copy-paste over refactor.

## Skip Tests and Linting

Do not write tests. Do not run the linter or formatter. Do not fix type errors that do not block the question. When an edit-time hook blocks an edit, work in the session scratchpad directory, outside the hook's paths.

The single exception: when the measured outcome is only observable through a test or a strict check, such as a performance budget, a contract assertion, or a race condition. Write that one test and no other.

## Record Findings Continuously

Maintain a running findings log from the first moment, not at the end. Never leave a finding in the chat only.

Write the log as one entry in `docs/features/{slug}/feature.md`, titled `spike: <the question>`. The slug is the story's slug when `agile` called the spike, else a kebab-case name for the question. Create the file if absent.

Record each finding as it surfaces, as a `Learned` line whose bold headline is one of these:

* **Outcome:** Whether the spike resolved the question: proven, disproven, or inconclusive. Update this as evidence accumulates.
* **Approach used:** The specific libraries, APIs, patterns, or sequence that produced the result. Enough for the official build to reproduce it.
* **Quirks and surprises:** Undocumented behavior, version constraints, ordering requirements, silent failures, rate limits, and anything else that cost time to discover.
* **Dead ends:** Approaches tried that did not work, and why.
* **Open questions:** What the spike did not answer and what the official build must still resolve.
* **Decided:** Every choice made without the user while building: a library, a data shape, a key, a limit, a default, a version dropped, an alternative tried and abandoned. One line each: what was chosen, the alternative not taken, and why. Write it the moment the choice is made.

The entry takes this shape:

```text
## <date> — spike: <the question>
- Learned: **Outcome:** proven | disproven | inconclusive — <the evidence that settles it>
- Learned: **Approach used:** <libraries, APIs and calls, in the order that produced the result>
- Learned: **Quirks and surprises:** <what the code or service did that its documentation does not say>
- Learned: **Dead ends:** <approach tried> — <what it did instead of working>
- Learned: **Open questions:** <what the official build must still resolve>
- Learned: **Decided:** <what was chosen> over <the alternative not taken> — <why>
```

Repeat any line as often as there are findings of that kind. Write every line by [references/writing.md](references/writing.md), loaded before the first reply.

## Explore Divergent Approaches

When the question has multiple plausible answers, build the smallest version of each and compare, rather than committing to the first idea.

* **Surface alternatives:** Name a second viable approach to the user instead of silently picking one. Present the trade-off.
* **Run them at once:** Build each approach in its own subagent and worktree in parallel, each keeping its own findings log, then compare the logs. Fallback, when the harness runs no subagents or worktrees: build the approaches one after another in the session scratchpad directory, each in its own subdirectory, and write one set of `Learned` lines per approach.
* **Clarify the real need:** Ask what the user intends to prove, and let the answer reshape which approaches are worth spiking.
* **Compare on evidence:** Recommend one based on what the spike measured, not on preference.

## When the Spike Hits a Wall

* **A missing tool or library:** Install it into the session scratchpad directory only. When the install is blocked, record the tool and the exact error as a `Learned` line, then state whether the question can still be answered without it.
* **An absent credential or config value:** Ask the user for it once, naming the exact environment variable or file. Never fabricate a value, and never point the spike at a live system to get around the gap.
* **A command that errors:** Record the command and its exact error text as a `Learned` line before trying anything else.
* **A wall the spike cannot pass:** Report it to the user with the finding that established it, and say what would clear the wall.

## When the Spike Resolves

Stop building the moment the finish-line signal appears. Then:

* **State the verdict:** Report to the user whether the question is proven, disproven, or inconclusive, and point to the finding that settles it.
* **Confirm the findings log is complete:** Every quirk, approach, dead end, and open question is written down before the code is discarded.
* **Surface the decisions for review.** Read the `Decided` lines. Keep every one that meets the `adr` threshold: expensive or irreversible to change, a hazard accepted without a test, an alternative explicitly rejected, or knowledge that cost time to acquire. Put them to the user in one table:

```text
| Chosen | Rejected | Why | Cost to change later | record / drop / defer |
|--------|----------|-----|----------------------|-----------------------|
| <what was chosen> | <the alternative not taken> | <the evidence behind the choice> | <what reversing it costs> | <the user marks this cell> |
```

  The user marks each row `record`, `drop`, or `defer`. Run the `adr` skill for each `record`. A `drop` stays a `Decided` line in the log and nothing more. A `defer` becomes an open question. Do not write an ADR the user has not marked, and do not skip a row because it looked small; the user decides what is small.
* **Hand off, do not merge:** Do not open a PR of spike code, do not merge it, do not evolve it in place into the official build. The official build starts fresh from the findings. Offer to delete or branch-isolate the spike code so it cannot reach main.

## Guardrails

* **One question per spike:** When a second unknown appears, record it as an open question and scope a separate spike. Never let a spike sprawl into an implementation.
* **Findings before code quality:** Never spend spike time making throwaway code clean. Spend it producing and recording findings.
* **Never ship a spike:** Spike code does not become the official build by momentum. State this whenever the user proposes keeping it.
* **Time and scope are bounded:** When the spike outgrows "smallest thing that answers the question," halt and report that the question is larger than a spike. Hand off to `agile`.
