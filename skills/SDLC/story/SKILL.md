---
name: story
description: "Use this skill when one story, ticket or bug report needs its acceptance criteria or its list of tests written, repaired or reviewed, without building it. Use it on: 'write the user story', 'write the acceptance criteria', 'what does done mean here', 'is this story ready', 'make this ticket testable', 'review this story', 'poke holes in this story', 'rewrite this ticket', 'what tests should this have', 'test plan for X', 'is this covered', 'what am I missing in the tests', and a bare 'tests?' after a proposal. Use it on a ticket full of better, robust, seamless, properly or handled. Produces one story: outcome, why, scope, Given/When/Then criteria for the outcome plus its boundary, failure and abuse paths, open decisions and inputs read as instructions. Once the criteria are confirmed, produces the test table: one Given/When/Then block per test, naming the rule that generated it and the failure it prevents. Not for splitting an epic (`define-work`), or fixing, speeding up or building anything (`deliver`)."
license: MIT
compatibility: any-agent
metadata:
  version: "2.3.0"
---
# Story

Everything here is agreed with the user. Propose, then wait.

## Criteria or tests

* **The request is for criteria,** or for reviewing a story: load [references/criteria.md](references/criteria.md) and follow its sections 1 to 10.
* **The request is for the tests of a change:** load [references/test-plan.md](references/test-plan.md). When the change's criteria are not yet written or not yet confirmed by the user, write them by [references/criteria.md](references/criteria.md) first and wait for the confirmation.
* **The request is whether existing code is covered:** load [references/test-plan.md](references/test-plan.md) and go straight to its section "Check existing tests for gaps", taking the behaviours from the code. Write no story.
* **Tests for behaviour that already exists:** load [references/test-plan.md](references/test-plan.md) and take the behaviours from the code. Write no criteria, and keep rows that are already green, since each pins today's behaviour.
* **Holdout scenarios,** asked for by name in a session opened in a holdout directory outside every repository: load [references/holdout.md](references/holdout.md). No other session loads it.
* **Trivial mode.** When `deliver` sizes a request as trivial, write criterion a only, the outcome, and skip sections 3 to 5 of [references/criteria.md](references/criteria.md) and the ready check's failure and abuse items.
* **Called from `deliver`'s criteria subagent,** return every question instead of waiting, and return the card text by section 8 of [references/criteria.md](references/criteria.md) instead of writing it. `deliver` writes the card once the user has confirmed the criteria.

A story is a change a person outside the system can observe. It gets its own card. Work nobody observes alone, such as a new column or a service the story calls, is written as criteria on the story that needs it and never gets a card of its own.

```text
<Title: what the person will be able to do, five to eight words>
Outcome:  <what a person observes once this story is done>
Why:      <what stays broken for them without it>
Scope:    <what this story covers, and what it leaves to which other story>
Criteria:
  a. Given <a concrete starting state>, when <a concrete action>, then <what the person sees, with real values>
  b. <a boundary, a failure path or an abuse path, same form>
Open:     <each undecided value, who decides it, and which criterion waits on it; "none" when none>
Interpreted: <each input this story adds and what interprets it as instructions; omit when none>
```

Criterion a is the outcome. The criteria after it are the boundaries, failure paths and abuse paths that apply to that outcome. Each criterion is proved by its own acceptance test: an automated test that checks what the person sees. The outcome criterion's test drives the interface the person uses. When a screen only shows what a service returns, the tests for the other criteria may drive that service.
