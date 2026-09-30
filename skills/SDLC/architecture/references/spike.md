# Spike

Load this to find something out by building throwaway code: proving an approach, a prototype, a demo, exploring an integration. A spike answers one question with the smallest code inside a timebox, records what it learned, and deletes the code. Run inside another step (Crossings or Decide), that step has already framed the question and timebox with the user. Ask nothing more except a missing credential. Return the verdict, the findings link and the decision table below for that step to put to the user.

## Frame it before any code

* **The question,** as an outcome that can fail: "the library streams partial results under 200 ms", not "look into the library". Refuse a spike with no failing condition.
* **The finish line:** the signal that answers it.
* **The timebox:** a wall-clock limit or a number of attempts, proposed with the question for the user to correct. When it runs out, the outcome is inconclusive; say what the next attempt would try.

Tell the user the code is throwaway. Hardcode, inline, copy. Write no tests and run no linter, except the one test the question can only be observed through (a budget, a contract, a race). When an edit hook blocks, work in a temporary directory outside the repository (the harness's scratchpad where it has one).

## Record as you go

The findings are the resolution comment of the spike's issue: a child of the epic with the spike type or a `spike` label, blocking each story that waits on it. With no epic open or no `Backlog:` line in `AGENTS.md`, write `docs/spikes/<question-slug>.md` on its own branch instead, with no tracker setup. Never leave a finding only in chat.

```text
## <date> — spike: <the question>
- Learned: **Outcome:** proven | disproven | inconclusive — <the evidence>
- Learned: **Approach used:** <libraries and calls, in the order that worked>
- Learned: **Quirks and surprises:** <undocumented behaviour, limits, silent failures>
- Learned: **Dead ends:** <approach> — <what it did instead>
- Learned: **Open questions:** <what the real build must still settle>
- Learned: **Decided alone:** <chosen> over <not taken> — <why>, written when chosen
```

When the question has several plausible answers, build the smallest version of each, in parallel subagents and worktrees where the harness allows, and compare on what they measured. A missing tool installs into that directory only; a missing credential is asked for once by its exact name, never faked; a command that errors is recorded with its exact error first.

## When it resolves

Stop at the finish line. State the verdict and the finding that settles it. Put each `Decided alone` line that is expensive to change, accepts a hazard, rejects an alternative or cost time to learn into one table, and the user marks each row:

```text
| Chosen | Rejected | Why | Cost to change later | record / drop / defer |
```

Record each `record` row by `adr.md`; a `defer` becomes an open question. Delete the spike code once the findings are written, and say so in them. Never merge or evolve spike code into the real build. A second unknown is its own spike.
