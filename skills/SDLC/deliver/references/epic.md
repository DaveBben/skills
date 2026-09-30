# The epic: header, story map, pick and close-out

Sections: 1 find what exists, 2 discover the problem, 3 the feature header, 4 the story map, 5 the feature acceptance test, 6 pick the next story, 7 close out, 8 review an existing epic.

Load this for a request sized as several stories, a request to break work down, "what should I pick up next", close-out, and a review of an epic or a story list someone wrote (section 8). The header and the story map are agreed with the user: propose them, then wait.

## 1. Find what exists first

Have the `lookup` agent return the epic's header lines, each child's key, title, rank, blockers and outcome line, and the problem, outcome and non-goals any linked requirements document states. When they state the problem, the outcome and the non-goals, take those lines, citing where each came from. Draft any missing line from them and put the drafts to the user in one message to correct. When the epic has children, they are the candidate stories: show them in rank order, each with an outcome line, and draft no second list. Have it search this codebase for the behaviour; when something already does the job, say where and wait.

## 2. Discover the problem

Only when nothing states it. Treat the request as a proposed solution. Ask what happens if it is not built until the answer is a consequence a person suffers. Ask when it last happened and what the workaround cost; a hypothetical answer is unvalidated. Draft the questions privately, keep those whose wrong answer is expensive to find later, and ask them one per message. Stop when the problem names who hits it, how often and what they do today.

## 3. The feature header

Write it into the epic's description, rewritten in place, at most 16 lines.

```text
Outcome:     <what a person does differently once this ships, and where; no component names>
Problem:     <who hits it, how often, what they do today instead>
Not doing:   <one checkable non-goal per line>
Success:     <the signal that shows the outcome happened; which direction is good; the noise band>
Target:      <the date the outcome must ship by, from the epic's due date; omit when none>
Release:     <the story keys that must ship by Target, in rank order; the release line sits under the last>
Constraints: <one line per rule every story must keep true>
Context:     <facts every story needs: environments, variables, URLs, test accounts, deploy and rollback commands, where each credential lives but never its value; the grants the user gave>
Repositories: <one line per repository: name and remote URL, local path without a remote, or "new: <name>">
Steps:       <what the person does, in order>
Decided:     <one ADR path per line>
Deferred:    <one open decision per line, with the number, story or spike that forces it>
Feature test: <path of the feature acceptance test, or "after story 1">
```

A fact true of the whole repository belongs in `AGENTS.md`, not here.

## 4. The story map

Under each step, draft the stories that let a person do it, each with a title naming what the person can do and an outcome line. Mark the thinnest slice across all the steps, touching every layer and reaching a real deploy, as `[walking skeleton]`. When the work is uncertain, draft the walking skeleton and the spike for the largest unknown in full, and mark the rest `[candidate]`. Write no criteria here; each story's criteria are written when it starts.

Only stories and spikes get cards. A requirement on how well a story behaves, an enabler nobody perceives alone (a column, a service), a property of a behaviour, and a task are criteria or test rows on the story that needs them. A decision is a comment on the story it blocks.

Split a story that covers more than one step or variation with the first pattern that works: one per workflow step; create, then read, update, delete; the simplest business rule first; one kind of data first; the plainest interface first; the simplest version first, each complication its own story; make it work, then make it fast; a timeboxed spike when something unknown blocks every pattern. Cut across layers, never along them. Fold hardening into the story that creates the exposure. Hardcode data in the walking skeleton, never a crossing into another running piece.

Write each blocker on the story it blocks: a story it builds on, a spike it needs, or an open decision. Put the drafted header lines and the map to the user in one message, saying that the first story waits for their feature acceptance test (section 5). Create cards only after the user confirms. Record no order beyond the `Release:` line.

Adding a story that building revealed is expected. A child added after the map is agreed goes below the release line unless the user moves it above, and where things stand counts how many were added. A task, or a fix the outcome does not need, stays off the epic.

Ready when the outcome names what a person does and where, `Success` names a signal someone can check, every story sits under a step with its blockers or "nothing", and one slice is the walking skeleton unless the work extends a deployed application.

## 5. The feature acceptance test

The outcome gets one acceptance test, which the user writes. Name the file, the runner and the Given/When/Then it must assert, through the interface the user uses; the user writes the body, or asks the `setup` agent to. It lives in a `feature-acceptance` directory in the test tree that the harness denies to the agent, is marked strictly expected-to-fail (pytest `xfail(strict=True)`, jest `test.failing`), and is committed alone on the first story's branch before its red commit. No agent edits, moves, skips or re-marks it. When the interface has no runner yet, the first story adds one and the header says "after story 1".

When a named person who owns the outcome (a product owner, a domain expert) writes Given/When/Then examples, take their list as the acceptance set: map each example to the story whose criteria must hold it, add any example no story holds as a criterion on the story that should, and park any example that contradicts an agreed criterion for that person.

## 6. Pick the next story

A story or spike is ready when every blocker is done (a spike is done when its findings comment is written), no question on it is unanswered, its comments hold no answer its description lacks, and no `story/{slug}/{key}-*` branch exists.

Take stories above the release line first, then the tracker's rank. Move a story ahead only because no story has reached a real deploy yet (the walking skeleton goes first), a spike's answer changes other stories, or it unblocks more stories; say which.

```text
Next:    <story> -> <why: rank, or the reason it moved>
Ready:   <the other ready stories, in order>
Blocked: <story> -> <what blocks it>
Refactors: <open Proposed refactor lines and the ready story whose code they touch; omit when none>
```

When the user asked, print it and wait for their choice. When nothing is ready, say which blocker frees the most stories and who can clear it.

## 7. Close out

When every child above the release line is done or cut, in this order:

1. **The feature test:** its marker is gone and the suite is green, else give its failure message and propose the story that would pass it. Report each example of a named person's acceptance set with the test that holds it.
2. **What is left:** ask whether the stories below the line become a new epic or are cut. Turn each unpinned `Learned` line into a test, an ADR or an `AGENTS.md` line on one last branch, or delete it with the user's agreement. Put each open `Proposed refactor` to the user. Delete the `Parked:` comments.
3. **Whether it worked:** ask whether the `Success` signal moved, and which pause cost time without catching anything, for the `guardrails` skill.
4. **The user's model:** when `docs/architecture/summary.md` exists (the one-page summary the user writes in their own words), quote its ranked qualities and its risks and ask which line this feature made wrong; the user edits it or says none. Name one design lesson in four lines: the structural decision the feature's code made (a module boundary, a data shape, where the input and output happen), the pattern it follows by its name, the alternative not taken, and the condition under which that alternative would win.
5. **The user's pattern,** as counts with no judgement, from the stories' `Yours:` log lines and the ADRs: cores written, sketches written and turns skipped; `Read first:` hunks shown; confirmations as shown and edited; ADR reasons the user wrote against ones the agent drafted and the user left.
6. **Close the epic.**

## 8. Review an existing epic

Load this section for 'review this epic', 'are these the right stories', or a story list someone wrote. An epic is one tracker issue whose child issues are its stories (changes a person can observe) and spikes, linked by blocking links; read through the tracker the `Backlog:` line of `AGENTS.md` names, or taken from what the user pasted. Change nothing without the owner's agreement. The whole epic is too long for this session: the `worker` agent, given this section's path and the epic's key, reads every card and every comment on it, and writes each candidate below, quoting the text it is about, to `epic-findings.md` in the git directory (`git rev-parse --git-dir`). This session reports only what the `refute` agent leaves. Look for:

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
