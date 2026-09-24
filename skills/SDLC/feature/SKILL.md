---
name: feature
description: "Use this skill whenever a feature, an epic or a PRD has to be turned into stories before any test or code exists, or an existing epic's breakdown has to be checked. Use it on: 'define this work', 'turn this prd into stories', 'break this epic down', 'split this into stories', 'what stories does this need', 'refine this epic', 'review this epic', 'are these the right stories', 'there are too many tickets'. Produces one outcome sentence, one problem statement, the non-goals, and a list of stories and spikes only, each story written with `story` and each carrying what blocks it. Do not use it to write or review the criteria of one story (`story`), to choose which story to build next (`next-story`), to record a decision (`adr`), or to build the code (`execute`)."
license: MIT
compatibility: any-agent
metadata:
  version: "2.0.0"
---
# Feature

Everything here is agreed with the user. Propose, then wait.

```text
Outcome:   <what a person does differently once this ships, and where they see it>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <one checkable non-goal per line>

1. <story title>          Blocked by: <story or spike numbers; "nothing">
2. spike: <the question>  Blocked by: ...
3. ...
```

Each story in the list is written in full with the `story` skill.

## 1. Outcome

Write one sentence saying what a person does differently once this ships, and where they see it. Reject an outcome naming a component, table, endpoint or file, and reject one that contradicts a stated non-goal unless the user overrides it. "Verdicts land in the table" is true while the work is half done. "I open one list each morning and read from it" is not.

## 2. Why

Write who hits the problem, how often, and what they do today instead. When the user cannot say what the person does today, the work is not understood yet. Ask before writing stories.

## 3. Split into stories

Draft the story titles from the outcome, write each story with `story`, then check the split against the rules below. A story whose criteria break a rule is split again or folded.

Decide what each candidate is before it gets a card. Only stories and spikes get cards.

| Kind | Test | Where it goes |
| --- | --- | --- |
| Story | A person outside the system perceives something new | Its own card |
| Spike | The answer needs something found out first | Its own card, run with `spike` |
| Non-functional requirement | Constrains how well a story behaves: security, a rate limit, pagination, alerting | Criteria on the story it constrains |
| Enabler | Real work nobody perceives alone: a new column, a consumer change, a service the story calls | Criteria on the story whose outcome needs it |
| Property | Something that must stay true of a behaviour | Criteria on the story that introduces the behaviour |
| Task | One step of building a story | A row in the story's test table, never a card or sub-task |
| Decision | A value or choice nobody has made yet | A comment on the story it blocks (section 4) |

* **Keep a property or constraint on its own card only when acting on it changes a design decision on another story, or it is a release gate.** Its criterion is the number.
* **Fold hardening into the story that creates the exposure.** A security story ordered after the story that builds the route ships the exposure first. Ordering the hardening card before the story it hardens is the sign it should have been criteria. Keep it separate only when a different team or release owns it.
* **Cut across the system's layers, never along them.** Every story ends with a person able to do one thing they could not do before, through the interface they actually use. Never name a story after a layer, component, table or team.
* **Make the first story the thinnest path touching every layer and reaching a real deploy.** Observable is mandatory; valuable is not.
* **Hardcode everything the first story does not test.** Count the places its outcome crosses from one running piece into another: a database, a trained model, a queue, a third-party API, a container, a host. When more than one of those crossings is untried, the first story fakes all but one.
* **Split by workflow step, happy path before error path, one rule before its variants, hardcoding before generalising.** Split any story crossing more than one of those boundaries, or more than one workflow step. No estimates.
* **Say which kind of boundary a scope cut draws.** A cut to what the product wants first and a cut to what existing code already covers are both legitimate. Name which one it is. An engineering boundary presented as product phasing is overruled the first time someone asks why.
* **Make a story observable once deployed.** When it changes behaviour no test can see afterwards, such as a rate, a failure mode or which path the code took, the same story emits the event that shows it, and a criterion says that event fires.
* **Treat a bug as a story.** Its criterion is the reproduction: the starting state, the action, and what the person should see instead of what they saw.

## 4. Record what blocks each story

* **Write each blocker on the story it blocks.** A blocker is another story whose outcome this one builds on, a spike whose answer it needs, or an open decision.
* **Put a decision on the story it blocks.** A decision blocking one story is a comment on that story. A decision blocking the whole feature is a comment on the epic. Never give a decision its own ticket.
* **Re-attach dependencies when a decision ticket closes.** A ticket that blocked a story may itself be blocked, such as by a spike. Closing it drops that chain, and the story shows as ready when it is not. Link each dependency that ran through the ticket directly to the story, then check again which stories are ready.
* **Check the direction of every blocking link** by reading one back from the tracker before creating the rest. Some trackers store the blocker on the side a reader expects the blocked story.
* **Record no order.** Which ready story goes next is decided at each story start with `next-story`.

## 5. Ready check

Check the result against these before handing it on. A no returns the work to the section that produces it.

* The outcome names what a person does and where, and no component.
* Every card is a story or a spike.
* Every story passes the `story` ready check.
* Each story leaves a person able to do something they could not do before.
* Every story lists its blockers, or "nothing".
* No two stories share a blocker, a repository, an owner and one merge request.

## 6. Review an epic

Run the section 5 check against an epic, a PRD's breakdown or a story list someone else wrote. Change nothing without the owner agreeing; each gap is their decision. Read every comment on every card first, and list each answer not yet folded into the card it answers. Check each subagent finding against the source before reporting it. Run `story` on each story for findings inside it. Report these first, quoting the text each is about.

* **Not a story:** a card that is a non-functional requirement, an enabler, a property, a task or a decision. Say which story it folds into.
* **Too many cards:** sibling cards sharing a blocker, a repository, an owner and one merge request are one story with several criteria. Search the siblings for one distinctive sentence. The number of cards containing it is the number to merge. Other signs are two decision tickets asking the same question, a spike mostly belonging to another epic, and a plan that needs its own guide to reading the cards.
* **Ships nothing:** a story that leaves no person able to do something new, or that crosses more than one boundary from section 3.
* **Wrong blocker:** a link in the wrong direction, a story shown ready whose blocker was dropped with a closed ticket, or a hardening story blocked by the story it hardens.

```text
Unanswered:      <card> "<quoted comment>" -> <what in the card it changes>
Not a story:     "<quoted title>" -> <kind> -> criteria on <story>
Too many cards:  <cards> -> <shared sentence, hit count> -> one story
Ships nothing:   "<quoted title>" -> <what a person still cannot do, or the boundaries crossed>
Wrong blocker:   <story> -> <what blocks it in fact>

Ready to build.        (or: 3 blocking items.)
```

When the owner agrees to delete cards, archive every one in full first, because deletion cannot be undone. Extract each comment a named person wrote on those cards and search the surviving cards for a distinctive phrase from each. A note saying content moved is not evidence that it did. Then search the surviving cards for every deleted key. The tracker removes links to a deleted card and leaves its key in prose. Rewrite each mention to describe the thing it named.

## What this skill does not do

Writing or reviewing one story's criteria is `story`. Choosing which ready story to build next is `next-story`. Answering an unknown by writing throwaway code is `spike`. Judging code, a design or a plan the user wrote themselves is `give-feedback`.
