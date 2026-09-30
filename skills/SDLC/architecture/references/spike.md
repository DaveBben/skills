# Run a spike

Brief for the subagent that runs one spike for the `architecture` skill. A spike answers one question with the smallest code inside a timebox, records what it learned, and deletes the code. The task gives you the question as an outcome that can fail, the finish line (the signal that answers it), the timebox (a wall-clock limit or a number of attempts), the repository, and the epic's key or "no epic". You ask nobody: return any question instead.

## Build it

The code is throwaway. Hardcode, inline, copy. Write no tests and run no linter, except the one test the question can only be observed through (a budget, a contract, a race). When an edit hook blocks, work in a temporary directory outside the repository (the harness's scratchpad where it has one).

When the question has several plausible answers, build the smallest version of each, in parallel subagents and worktrees where the harness allows, and compare on what they measured. A missing tool installs into that directory only. A missing credential is never faked: stop and return its exact name as your question, with the findings so far. A command that errors is recorded with its exact error first. A second unknown is its own spike: return it as a question instead of chasing it.

## Record as you go

The findings are the resolution comment of the spike's issue: a child of the epic with the spike type or a `spike` label, blocking each story that waits on it. With "no epic" or no `Backlog:` line in `AGENTS.md`, write `docs/spikes/<question-slug>.md` on its own branch instead, with no tracker setup. Never leave a finding only in your return.

```text
## <date> — spike: <the question>
- Learned: **Outcome:** proven | disproven | inconclusive — <the evidence>
- Learned: **Approach used:** <libraries and calls, in the order that worked>
- Learned: **Quirks and surprises:** <undocumented behaviour, limits, silent failures>
- Learned: **Dead ends:** <approach> — <what it did instead>
- Learned: **Open questions:** <what the real build must still settle>
- Learned: **Decided alone:** <chosen> over <not taken> — <why>, written when chosen
```

## When it resolves

Stop at the finish line. When the timebox runs out first, the outcome is inconclusive; say what the next attempt would try. Delete the spike code once the findings are written, and say so in them. Never merge or evolve spike code into the real build.

## Return

```text
Verdict:   proven | disproven | inconclusive, and the finding that settles it
Findings:  <the issue comment link or the file path>
Questions: <a missing credential's exact name, a second unknown, or "none">
| Chosen | Rejected | Why | Cost to change later | record / drop / defer |
```

The table holds one row per `Decided alone` line that is expensive to change, accepts a hazard, rejects an alternative or cost time to learn, with the last column left for the user to mark.
