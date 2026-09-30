# Review an existing epic

An epic is one tracker issue whose child issues are its stories (changes a person can observe) and spikes, linked by blocking links; read it through the tracker the `Backlog:` line of `AGENTS.md` names, or take it from what the user pasted. Change nothing without the owner's agreement. The whole epic is too long for this session: the `worker` agent, given this file's path and the epic's key, reads every card and every comment on it, and writes each candidate below, quoting the text it is about, to `epic-findings.md` in the git directory (`git rev-parse --git-dir`). This session reports only what the `refute` agent leaves. Look for:

* **No shared understanding:** no outcome a person would notice, no success signal someone can check, no non-goals.
* **Not a story:** a card for something a person cannot perceive alone (a requirement on how well another story behaves, an enabler like a column or a service, a property, a task, a decision). Say which story it folds into as criteria.
* **Too many cards:** siblings that are one story. Search for one distinctive sentence; the cards containing it are the ones to merge.
* **Ships nothing:** a story that leaves no person able to do something new, or covers more than one workflow step and one variation.
* **No access rule:** a story that crosses a trust boundary or touches personal or health data with no criterion saying who may do what, and what is refused.
* **Wrong blocker:** a link in the wrong direction, a story shown ready whose blocker was dropped with a closed ticket, a hardening story blocked by the story it hardens.
* **Stale card:** criteria or a description naming a route, a module or a design the code no longer has.
* **Over the limit:** a story with more criteria that record a product choice (a number, an arguable rule, an open boundary) than the limit `AGENTS.md` states, else 8; it is several stories.

```text
Unanswered:      <card> "<quoted comment>" -> <what in the card it changes>
No shared understanding: <the missing line> -> <the question for the owner>
Not a story:     "<title>" -> <kind> -> criteria on <story>
Too many cards:  <cards> -> <shared sentence> -> one story
Ships nothing:   "<title>" -> <what a person still cannot do>
Wrong blocker:   <story> -> <what blocks it in fact>
Stale card:      <card> -> <what it names> -> <what the code has instead>
Over the limit:  <card> -> <n> product-choice criteria -> <the split>
No access rule:  <card> -> <the boundary or data it touches>
Refuted:         <card>:<field> -> <what was raised> -> <what stops it>
Refuted by:      <model>

Ready to build.   (or: <n> blocking items)
```

List every candidate first, doubted ones included, anchored `<card>:<field>`, then have the `refute` agent judge each against the cards and their comments: a finding survives only when the quoted text shows it. A confirmed row is a finding line, an `unsettled` one an `Unanswered:` line, a refuted one a `Refuted:` line.

Before deleting cards the owner agreed to delete, archive each in full, confirm each named person's comment survives on a remaining card, and rewrite every remaining mention of a deleted key.
