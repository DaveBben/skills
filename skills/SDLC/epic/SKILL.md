---
name: epic
description: "Use this skill when an idea, a PRD or an epic must become stories, or when an epic's stories must be reviewed, picked or closed out. Use it on: 'I have an idea', 'break this epic down', 'turn this PRD into stories', 'review this epic', 'are these the right stories', 'what should I pick up next', 'close out this epic'. Agrees the feature header, the story map and the feature acceptance test with the user, then hands each story to the deliver skill."
license: MIT
metadata:
  version: "1.1.0"
---
# Epic

Shape a feature before its stories are built: the feature header, the story map and the feature acceptance test. The header and the map are agreed with the user: propose them, then wait. The `deliver` skill builds each story once the map is confirmed.

## Words used here

* **Tracker:** the project tracker the `Backlog:` line of `AGENTS.md` names. An epic per feature, its stories and spikes as child issues with blocking links, each issue's comments as its log. The **slug** is the epic's key.
* **Story:** a change a person outside the system can observe, in one workflow step and one variation. A **spike** is a timeboxed story that answers one unknown; its findings are its resolution comment, every line a `Learned` line.
* **Parked:** a question written on an issue as a comment starting `Parked:`.
* **Release line:** the line under the last story key on the header's `Release:` line.

## Agents and the tracker

The `lookup`, `worker`, `setup` and `refute` agents are each defined by one file in the plugin's shared agents folder, `../agents/<name>.md`. Where the harness loads named agents, launch each by its name (Claude Code's SDLC plugin installs them as `SDLC:lookup` and so on); otherwise launch a general subagent told to follow its file. Give each `lookup` or `worker` agent that touches the tracker the path of `../deliver/references/tracker.md` and the `Backlog:` block; with no `Backlog:` line, connect a tracker by that file's section 1 first. The `lookup` agent does every tracker read and returns only what this session asks for; a whole issue or an API response never enters this session. Hand every tracker write to a `worker` agent, all the writes ready at the same moment as one numbered list. When the tracker cannot be reached, run `../deliver/scripts/story.sh next tracker-down` and follow it. Look up a fact a tool can reach with the `lookup` agent before asking the user. Ask one question per message, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion), recommended option first; ask again, naming the options, when an answer fits none, and never restate a question parked on a story.

## Pick the path

* **An idea, a PRD, an epic to break down, or a request sized as several stories:** sections 1 to 5, ending when the user confirms the map and the cards exist. Then the `deliver` skill takes each story, when the user asked for it built.
* **"What should I pick up next":** section 6.
* **Every child above the release line is done or cut:** close out by [references/close-out.md](references/close-out.md).
* **"Review this epic", "are these the right stories", or a story list someone wrote:** [references/review.md](references/review.md). Change nothing without the owner's agreement.

## 1. Find what exists first

Have the `lookup` agent return the epic's header lines, each child's key, title, rank, blockers and outcome line, and the problem, outcome, non-goals, author and the priority of each requirement (must, should, nice to have, a phase or an MVP label) any linked requirements document states. When they state the problem, the outcome and the non-goals, take those lines, citing where each came from. Draft any missing line from them and put the drafts to the user in one message to correct. An epic with no description gets the header written into it by section 3. Have the `lookup` agent search this codebase for the behaviour; when something already does the job, say where and wait.

When the epic has children, they are the proposed stories: show them in rank order, each with an outcome line written from its text, check them against the ready check in section 4, and draft no second list. The user confirms, rewords, cuts or re-ranks in one turn. Criteria are written when each story starts. Several epics are several features, one loop each.

## 2. Discover the problem

Only when nothing states it. Treat the request as a proposed solution. Ask what happens if it is not built until the answer is a consequence a person suffers. Ask when it last happened and what the workaround cost; a hypothetical answer is unvalidated. Draft the questions privately, keep those whose wrong answer is expensive to find later, and ask them one per message. Stop when the problem names who hits it, how often and what they do today.

## 3. The feature header

A `worker` writes it into the epic's description, rewritten in place, at most 16 lines.

```text
Outcome:     <what a person does differently once this ships, and where; no component names>
Problem:     <who hits it, how often, what they do today instead>
Not doing:   <one checkable non-goal per line>
Success:     <the signal that shows the outcome happened; which direction is good; the noise band>
Target:      <the date the outcome must ship by, from the epic's due date; omit when none>
Release:     <the smallest set of story keys that delivers Outcome, in rank order; the release line sits under the last>
Owner:       <the named person who agrees the release line and each story's product-choice criteria (a product owner, often the requirements document's author); omit when the user decides>
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

Under each step, draft the stories that let a person do it, each with a title naming what the person can do and an outcome line. Mark the thinnest slice across all the steps, touching every layer and reaching a real deploy, as `[walking skeleton]`. When the work is uncertain, draft the walking skeleton and the spike for the largest unknown in full, and mark the rest `[candidate]`. A `[candidate]` has a title and an outcome line only, with no split and no blockers until it is picked. Write no criteria here; each story's criteria are written when it starts.

Draw the release line under the smallest set of stories that delivers the outcome. Place each story by the priority the requirements document gives it, citing it; a story the document marks optional, or one the outcome does not need, goes below the line as a `[candidate]`. Ask the user about the stories whose side no document states, as one question that picks the ones above the line. When the header names an `Owner:`, the line stays proposed until the user reports that person agreed it.

Only stories and spikes get cards. A requirement on how well a story behaves, an enabler nobody perceives alone (a column, a service), a property of a behaviour, and a task are criteria or test rows on the story that needs them. A decision is a comment on the story it blocks.

Split a story that covers more than one step or variation with the first pattern that works: one per workflow step; create, then read, update, delete; the simplest business rule first; one kind of data first; the plainest interface first; the simplest version first, each complication its own story; make it work, then make it fast; a timeboxed spike when something unknown blocks every pattern. Cut across layers, never along them. Fold hardening into the story that creates the exposure. Hardcode data in the walking skeleton, never a crossing into another running piece.

Write each blocker on the story it blocks: a story it builds on, a spike it needs, or an open decision. A spike blocks each story that waits on its answer. Put the drafted header lines and the map to the user in one message, each story marked above or below the release line with its reason, saying that the first story waits for their feature acceptance test (section 5). Have a `worker` create the cards only after the user confirms. Record no order beyond the `Release:` line.

Adding a story that building revealed is expected. A child added after the map is agreed goes below the release line as a `[candidate]` unless the user, or the `Owner:` when the header names one, moves it above. A task, or a fix the outcome does not need, stays off the epic.

Ready when the outcome names what a person does and where, `Success` names a signal someone can check, every story sits under a step, every story above the release line has its blockers or "nothing", every story's side of the line cites the requirements document or the user's answer, and one slice is the walking skeleton unless the work extends a deployed application.

## 5. The feature acceptance test

The outcome gets one acceptance test, which the user writes. Name the file, the runner and the Given/When/Then it must assert, through the interface the user uses; the user writes the body, or asks the `setup` agent to draft it. It lives in a `feature-acceptance` directory in the test tree that the harness denies to the agent, is marked strictly expected-to-fail (pytest `xfail(strict=True)`, jest `test.failing`), and is committed alone on the first story's branch before its red commit. No agent edits, moves, skips or re-marks it. When the interface has no runner yet, the first story adds one and the header says "after story 1".

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

Print it and wait for the user's choice. When nothing is ready, say which blocker frees the most stories and who can clear it.
