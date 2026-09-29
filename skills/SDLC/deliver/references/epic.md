# The epic: header, story map, pick and close-out

Load this for a request sized as several stories, a request to break work down, "what should I pick up next", and close-out. The header and the story map are agreed with the user: propose them, then wait.

## 1. Find what exists first

Read the epic's description, its children and any requirements document it links. When they state the problem, the outcome and the non-goals, take those lines, citing where each came from. Draft any missing line from them and put the drafts to the user in one message to correct. When the epic has children, they are the candidate stories: show them in rank order, each with an outcome line, and draft no second list. Search this codebase and the product for the behaviour; when something already does the job, say where and wait.

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

Write each blocker on the story it blocks: a story it builds on, a spike it needs, or an open decision. Read one blocking link back from the tracker before creating the rest, and record the direction on the `Blocks:` line under `Backlog:`. Put the drafted header lines and the map to the user in one message, saying that the first story waits for their feature acceptance test (section 5). Create cards only after the user confirms. Record no order.

Ready when the outcome names what a person does and where, `Success` names a signal someone can check, every story sits under a step with its blockers or "nothing", and one slice is the walking skeleton unless the work extends a deployed application.

## 5. The feature acceptance test

The outcome gets one acceptance test, which the user writes. Name the file, the runner and the Given/When/Then it must assert, through the interface the user uses; the user writes the body, or asks the `setup` agent to. It lives in a `feature-acceptance` directory in the test tree that the harness denies to the agent, is marked strictly expected-to-fail (pytest `xfail(strict=True)`, jest `test.failing`), and is committed alone on the first story's branch before its red commit. No agent edits, moves, skips or re-marks it. When the interface has no runner yet, the first story adds one and the header says "after story 1".

## 6. Pick the next story

A story or spike is ready when every blocker is done (a spike is done when its findings comment is written), no question on it is unanswered, its comments hold no answer its description lacks, and no `story/{slug}/{key}-*` branch exists. Re-read each blocker from the tracker now.

Take the tracker's rank. Move a story ahead only because no story has reached a real deploy yet (the walking skeleton goes first), a spike's answer changes other stories, or it unblocks more stories; say which.

```text
Next:    <story> -> <why: rank, or the reason it moved>
Ready:   <the other ready stories, in order>
Blocked: <story> -> <what blocks it>
Refactors: <open Proposed refactor lines and the ready story whose code they touch; omit when none>
```

When the user asked, print it and wait for their choice. When nothing is ready, say which blocker frees the most stories and who can clear it.

## 7. Close out

When every child is done or cut: the feature acceptance test's marker is gone and the suite is green, else give its failure message and propose the story that would pass it. Turn each unpinned `Learned` line into a test, an ADR or an `AGENTS.md` line on one last branch, or delete it with the user's agreement. Put each open `Proposed refactor` to the user. Delete the `Parked:` comments. Ask whether the `Success` signal moved, and which pause cost time without catching anything, for the `guardrails` skill. Close the epic.
