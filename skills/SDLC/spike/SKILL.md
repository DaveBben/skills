---
name: spike
description: "Use this skill whenever the user wants to find something out by building, rather than to ship what they build: proving an approach, prototyping an idea, mocking something up (not a test double), standing up a demo, or exploring what an integration or change would involve. Use it on: 'let's prove this works first', 'let's try an approach before building', 'let's prototype this idea', 'let's mock this up', 'create a throwaway project', 'build a quick throwaway', 'build a demo', 'let's do a spike on it', 'let's see if X is feasible', 'let's see how this integration would work', 'let's see the changes which would be needed', 'explore how this would fit into the system'. Use it on the words prototype, mock, demo, throwaway, spike, feasible and explore even when the ask sounds small: deciding what is disposable is the whole point. Build the smallest thing that answers the open question, record findings as they surface, and treat all code as disposable. Do not use it for code meant to ship; that is `agile`."
license: MIT
compatibility: any-agent
metadata:
  version: "0.3.0"
---
# Spike

Prove or disprove a specific assumption with the smallest amount of throwaway code. A spike answers one question: does this approach work, or what would this integration actually look like. It is not the implementation. Its only durable output is the recorded findings that a later official build will rely on.

State the disposable nature up front. Skip the ceremony that real code requires. Record what you learn the moment you learn it.

## Frame the Spike Before Writing Code

Establish two facts with the user before touching the filesystem:

* **The question:** The single assumption or feasibility unknown the spike must resolve. State it as a falsifiable outcome — "the library can stream partial results under 200ms" not "look into the library." If the user has no crisp question, ask one question to extract it. Refuse to start a spike that has no failing condition.
* **The finish line:** The observable signal that answers the question. Name what you must see to call the spike resolved. When you see it, stop — do not keep building.

## Declare the Code Disposable

State to the user, before writing any code, that everything produced in this spike is throwaway. Say it plainly: this code will be deleted, not merged. The findings survive; the code does not.

This framing changes what you build. Hardcode values. Skip abstraction. Inline everything. Copy-paste over refactor. The code exists only long enough to produce a finding.

## Skip Tests and Linting

Do not write tests. Do not run the linter or formatter. Do not fix type errors that do not block the question. When an edit-time hook blocks an edit, work in a directory outside the hook's paths, such as the session scratchpad.

The single exception: when the outcome you are measuring is itself only observable through a test or a strict check. A performance budget, a contract assertion, or a race condition may require a test to observe at all. Write that one test, and only that one, because it is the instrument — not because the code needs coverage.

## Record Findings Continuously

Maintain a running findings log from the first moment, not at the end. Write each finding as you hit it, while the detail is fresh. A spike whose findings live only in the final chat message has failed — the code gets deleted and the knowledge goes with it.

Write the log as one entry in `docs/tasks/{slug}/task.md`, titled `spike: <the question>`. The slug is the slice's slug when `agile` called the spike, else a kebab-case name for the question. Create the file if absent. `agile` reads the same file, so a spike inside a slice and a spike on its own leave findings in one place.

Record, as they surface, each as a `Learned` line with a bold headline:

* **Outcome:** Did the spike resolve the question — proven, disproven, or inconclusive. Update this as evidence accumulates.
* **Approach used:** The specific libraries, APIs, patterns, or sequence that produced the result. Enough for the official build to reproduce it.
* **Quirks and surprises:** Undocumented behavior, version constraints, ordering requirements, silent failures, rate limits — anything that cost time to discover.
* **Dead ends:** Approaches tried that did not work, and why. This stops the official build from repeating the failure.
* **Open questions:** What the spike did not answer and what the official build must still resolve.

## Explore Divergent Approaches

A spike is the cheap place to try more than one path. When the question has multiple plausible answers, build the smallest version of each and compare, rather than committing to the first idea.

* **Surface alternatives:** When you see a second viable approach, name it to the user instead of silently picking one. Present the trade-off.
* **Run them at once:** Where the harness allows, build each approach in its own subagent and worktree in parallel, each keeping its own findings log, then compare the logs. Non-determinism is a source of options when the runs are side by side.
* **Clarify the real need:** The stated question is often a proxy for a deeper need. Ask what the user actually intends to prove, and let that reshape which approaches are worth spiking.
* **Compare on evidence:** Record each approach's outcome in the findings log. Recommend one based on what the spike measured, not on preference.

## When the Spike Resolves

Stop building the moment the finish-line signal appears. Then:

* **State the verdict:** Report to the user whether the question is proven, disproven, or inconclusive, and point to the finding that settles it.
* **Confirm the findings log is complete:** Every quirk, approach, dead end, and open question is written down before the code is discarded.
* **Hand off, do not merge:** The spike code is throwaway. Do not open a PR of spike code, do not merge it, do not evolve it in place into the real feature. The official build starts fresh from the findings. Offer to delete or branch-isolate the spike code so it cannot leak into production.

## Guardrails

* **One question per spike:** A spike answers a single assumption. If a second unknown appears, record it as an open question and scope a separate spike — do not let the spike sprawl into an implementation.
* **Findings before code quality:** Never spend spike time making throwaway code clean. Spend it producing and recording findings.
* **Never ship a spike:** Spike code does not become production code by momentum. State this whenever the user proposes keeping it.
* **Time and scope are bounded:** If the spike outgrows "smallest thing that answers the question," halt and report that the question is larger than a spike. Hand off to `agile`.
