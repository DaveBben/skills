---
name: define
description: "Use this skill when work must be defined before it is built: an idea, a PRD or an epic turned into a shared understanding and a map of stories and spikes, or one story, ticket or bug report given its acceptance criteria or its tests. Use it on: 'I have an idea', 'turn this prd into stories', 'break this epic down', 'split this into stories', 'write the acceptance criteria', 'what does done mean here', 'is this story ready', 'make this ticket testable', 'what tests should this have', 'is this covered'. Produces the problem under the request, the epic's shared understanding, the steps a person takes with candidate stories, spikes and their blockers, and for one story Given/When/Then criteria for its outcome, boundary, failure and abuse paths, then its test table. Not for the system's shape or a new application (`architecture`), reviewing an existing epic's cards (`reviewing`, which calls this skill for its check), or fixing, speeding up or building anything (`deliver`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Define

Everything here is agreed with the user. Propose, then wait.

This skill defines work at two levels. For a feature: discovery of the problem under the request, the epic's shared understanding, and the story map of stories and spikes with their blockers. For one story: its acceptance criteria, its list of tests, and, when the user keeps them, holdout scenarios, which are end-to-end checks no agent that builds the feature ever reads.

**The tracker.** Discovery, the shared understanding and the story map need the tracker the `Backlog:` line of `AGENTS.md` names; with no such line, halt and run the `orient` skill, which helps the user connect one and records the line. One story's criteria, a list of tests and holdout scenarios need no tracker: a card that cannot be written goes to chat as text until it can.

## Pick the path

Load exactly one reference.

| Request | Load |
|---|---|
| An idea, a PRD, an epic, a feature bigger than one story, or the check `reviewing` asks for | [references/work.md](references/work.md) |
| One story's criteria: write, repair or review them | [references/criteria.md](references/criteria.md) |
| The tests of a change, whether existing code is covered, or tests for behaviour that already exists | [references/test-plan.md](references/test-plan.md) |
| Holdout scenarios, asked for by name in a session opened in a holdout directory outside every repository | [references/holdout.md](references/holdout.md); no other session loads it |

* **Tests before criteria.** When a change's criteria are not yet written or not yet confirmed by the user, write them by `references/criteria.md` first and wait for the confirmation, then load `references/test-plan.md`.
* **Coverage of existing code:** go straight to the test plan's section "Check existing tests for gaps", taking the behaviours from the code. Write no story.
* **Tests for behaviour that already exists:** take the behaviours from the code, write no criteria, and keep rows that are already green, since each pins today's behaviour.
* **Trivial mode.** When `deliver` sizes a request as trivial, write criterion a only, the outcome, and skip sections 3 to 5 of `references/criteria.md` and the ready check's failure and abuse items.
* **Called from a subagent** (`deliver`'s criteria subagent included), return every question instead of waiting. From the criteria subagent, also return the card text by section 8 of `references/criteria.md` instead of writing it; `deliver` writes the card once the user has confirmed the criteria.
