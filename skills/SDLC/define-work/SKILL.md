---
name: define-work
description: "Use this skill when work bigger than one story needs its shared understanding written or retrieved and its possible stories drafted, before any code: a PRD, a large feature request or an epic. Use it on: 'turn this prd into stories', 'break this epic down', 'split this into stories', 'story map this', 'what stories does this need', 'plan this feature', 'define this work'. Produces the shared understanding (outcome, problem, non-goals, success signal, constraints, repositories), the steps a person takes, and candidate stories and spikes under each with their blockers, the walking skeleton marked. No acceptance criteria. Not for one story's criteria (`story`), a new application or the system's shape (`architecture`), refining or reviewing an existing epic's cards (`reviewing`, which calls this skill for its check), or choosing what to build next and building it (`deliver`). A request to add one feature is `deliver`, which calls this skill when it turns out to be several stories."
license: MIT
compatibility: any-agent
metadata:
  version: "4.3.0"
---
# Define Work

A story map holds two things. The shared understanding lasts for the whole piece of work, and every story is written against it. The candidate stories are a draft, and the stories built first will change the rest.

Everything here is agreed with the user. Propose, then wait.

```text
Outcome:     <what a person does differently once this ships, and where they see it>
Problem:     <who hits it, how often, what they do today instead>
Not doing:   <one checkable non-goal per line>
Success:     <the signal that shows the outcome happened: the PRD's metric, or what a person is seen doing; which direction is good; the noise band>
Constraints: <one line per rule every story must keep true, such as "ticket text never leaves our network">
Context:     <one line per fact this feature adds that every story needs (section 2)>
Repositories: <one line per repository this work changes (section 2)>

Steps: <step 1> -> <step 2> -> <step 3>   (what the person does, in order)

<step 1>
  1. <story title>                  Outcome: <what a person observes>   Blocked by: <story or spike numbers, open decisions, or "nothing">   [walking skeleton]
  2. spike: <the question>          Blocked by: ...
<step 2>
  3. <story title>                  Outcome: ...   Blocked by: ...     [candidate]
```

Write no acceptance criteria here. The `story` skill writes each story's criteria when that story starts, using what the earlier stories taught.

## 1. Retrieve before writing

The slug is a short kebab-case name for the work, or the epic's key on a tracker; the feature log is `docs/delivery/{slug}.md`.

Look for the shared understanding before writing any: the feature header at the top of `docs/delivery/{slug}.md`, the epic's description on the tracker the `Backlog:` line of `AGENTS.md` lists, the bottom of the change's spec when `AGENTS.md` names a per-change spec directory, and the PRD. When one exists and is sound, read it back to the user and change nothing. Rewrite only the lines that are missing or that the user says are wrong. Read the live PRD, not a saved copy. When the epic already has children, they are the candidate stories: read them and draft no second list.


## 2. The shared understanding

* **Outcome.** One sentence saying what a person does differently once this ships, and where they see it. Reject an outcome naming a component, table, endpoint or file, and reject one that contradicts a stated non-goal unless the user overrides it. "Verdicts land in the table" is true while the work is half done. "I open one list each morning and read from it" is not.
* **Problem.** Who hits it, how often, and what they do today instead. When the user cannot say what the person does today, the work is not understood yet. Ask before drafting stories.
* **Not doing.** Each non-goal is a statement someone could check.
* **Success.** Take the PRD's success metric when it has one. Otherwise ask what the user will see people doing once the outcome happened. Ask once which direction is good and how large a move between two readings is only noise; a drop past that band after a story ships sends the user to read the code that emits the signal. Close-out asks whether it moved.
* **Context.** Facts this feature adds that every story needs and nobody should rediscover, never facts `AGENTS.md` already holds: which environment to deploy to, the environment variables the app reads, service URLs, test accounts, the deploy and rollback commands. Name where each credential lives (an environment variable's name, a secret manager path, a file outside the repository) and never its value, since this block is committed. A fact true of the whole repository, not just this work, belongs in `AGENTS.md`.
* **Repositories.** Every repository this work changes, one line each: its name and the URL of the remote its pull requests go to, read with `git remote get-url origin` or the tracker's links. Write the absolute local path only when the repository has no remote, and `new: <name> <directory>` when it does not exist yet, the directory left blank; the `architecture` skill decides how many repositories a new application has, and each directory. Work that spans a service and its client, or code in another team's repository, lists each one here, so a story never starts in a repository nobody named.
* **Constraints.** A rule every story must keep true, such as where data may live or a response-time ceiling, goes here once. The `story` skill writes it as a criterion on each story that could break it. A constraint no story can break is an engineering standard and belongs in `AGENTS.md`.

## 3. Map the steps

List the steps a person takes to reach the outcome, in the order they take them, in the domain's own words. The steps are not stories.

Under each step, draft the candidate stories that let a person do that step, each with a title and an outcome line. Mark the thinnest slice across all the steps as the walking skeleton: the smallest end-to-end version a real person can use, touching every layer and reaching a real deploy.

When the work is uncertain, do not try to find every story. Draft the walking skeleton and the spike that answers the largest unknown in full. Mark the rest `[candidate]`.

## 4. Split into stories

Decide what each candidate is before it gets a card. Only stories and spikes get cards.

| Kind | Test | Where it goes |
| --- | --- | --- |
| Story | A person outside the system perceives something new | Its own card |
| Spike | The answer needs something found out first | Its own card, run with `spike` |
| Non-functional requirement | Constrains how well a story behaves: security, a rate limit, pagination, alerting | Criteria on the story it constrains, or a line under Constraints when every story must keep it |
| Enabler | Real work nobody perceives alone: a new column, a model server, a service the story calls | Criteria on the story whose outcome needs it |
| Property | Something that must stay true of a behaviour | Criteria on the story that introduces the behaviour |
| Task | One step of building a story | A row in the story's test plan, never a card or sub-task |
| Decision | A value or choice nobody has made yet | A comment on the story it blocks (section 5) |

A story is the right size when a person can see its change on its own, it covers one step and one variation, and its criteria stay within the number per story `AGENTS.md` states, which the user sets once when it is missing. Split a larger one with the first pattern that works:

1. **Workflow step:** one story per step the person takes.
2. **Operation:** create, then read, then update, then delete.
3. **Business rule:** the simplest rule first, each variant its own story.
4. **Data:** one kind of input first, the others later.
5. **Entry method:** the plainest interface first.
6. **Simplest version:** ask what the simplest version is, build it, and give each complication its own story.
7. **Performance:** make it work, then make it fast, as a later story with the number in its criterion.
8. **Spike:** when no pattern works because something is unknown, split off a timeboxed spike and draft the stories after it answers.

* **Keep a property or constraint on its own card only when acting on it changes a design decision on another story, or it is a release gate.** Its criterion is the number.
* **Fold hardening into the story that creates the exposure.** A security story ordered after the story that builds the route ships the exposure first. Keep it separate only when a different team or release owns it.
* **Cut across the system's layers, never along them.** Never name a story after a layer, component, table or team.
* **Hardcode data the walking skeleton does not test, never a crossing.** A crossing is a place its outcome passes from one running piece into another: a database, a trained model, a queue, a third-party API, a container, a host. The walking skeleton crosses every one with real code. Each crossing nobody has made work yet gets a spike that blocks the walking skeleton; the `architecture` skill lists them.
* **Say which kind of boundary a scope cut draws.** A cut to what the product wants first and a cut to what existing code already covers are both legitimate. Name which one it is. An engineering boundary presented as product phasing is overruled the first time someone asks why.
* **Make a story observable once deployed.** When it changes behaviour no test can see afterwards, such as a rate, a failure mode or which path the code took, the same story emits the event that shows it.
* **Treat a bug as a story.** Its criterion is the reproduction: the starting state, the action, and what the person should see instead of what they saw.
* **No estimates.** When a story's criteria, written later, show it breaks a rule here, it comes back to be split.

## 5. Record what blocks each story

* **Write each blocker on the story it blocks.** A blocker is another story whose outcome this one builds on, a spike whose answer it needs, or an open decision.
* **Put a decision on the story it blocks.** A decision blocking one story is a comment on that story. A decision blocking the whole map is a comment on the epic. Never give a decision its own ticket.
* **Re-attach dependencies when a decision ticket closes.** A ticket that blocked a story may itself be blocked, such as by a spike. Closing it drops that chain, and the story shows as ready when it is not. Link each dependency that ran through the ticket directly to the story, then check again which stories are ready.
* **Check the direction of every blocking link** by reading one back from the tracker before creating the rest. Some trackers store the blocker on the side a reader expects the blocked story. Write the direction under `Backlog:` in `AGENTS.md` as its `Blocks:` line, so the check runs once per project.
* **Number stories once.** Numbers never change, so a `Blocked by` line keeps pointing at the right story.
* **Create cards only after the user confirms the map.** When the tracker cannot be written, give the map as text and create nothing.
* **Record no order.** `deliver` decides which ready story goes next at each story start.

## 6. Ready check

Check the result against these before handing it on. A no returns the work to the section that produces it.

* The outcome names what a person does and where, and no component.
* Success names a signal someone can check.
* Every step is something the person does, and every story sits under a step.
* One slice is marked as the walking skeleton, unless the work extends an application already deployed.
* Every card is a story or a spike.
* Every story has a title naming what a person can do, and an outcome line.
* Every story lists its blockers, or "nothing".
* No two stories share a blocker, a repository, an owner and one merge request.

## 7. Write it down

Once the ready check passes and the user confirms the map, write the whole block above, steps and stories included, where the stories live: the epic's description on a tracker, else under a `## Feature` heading at the top of the feature log, where the stories become its `Stories:` line. Commit it on the plan branch `story/{slug}/0-plan` cut from main, or on main in a repository with no remote. With no repository yet, leave the file uncommitted; the `architecture` skill commits it. Other skills add their lines to that block.

## 8. When `reviewing` asks for a check

The `reviewing` skill runs this skill against an existing epic, a PRD's breakdown or a story list someone else wrote. Change nothing. Apply the section 4 kinds table and size rule, the section 5 blocker rules and the section 6 ready check to what exists, and return each gap with the card and the quoted text it is about. `reviewing` writes the report.
