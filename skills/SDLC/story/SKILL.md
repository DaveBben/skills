---
name: story
description: "Use this skill before touching any file on a request to add, change, fix or remove behaviour in code that exists, and whenever work must become user stories or a story must be built. Use it on: 'add X', 'fix the bug where X', 'X is broken', 'refactor X', 'build story X', 'build this' with a link to an issue, 'pick up where we left off', 'write a story for X', 'write the acceptance criteria', 'break this down', 'I have an idea', 'turn this PRD into stories', 'review these stories', 'what should I pick up next'. Use it even when the change looks small. Writes each change as a user story with concrete acceptance criteria, agrees it with the user, then builds it test-first and opens a pull request into main."
license: MIT
metadata:
  version: "2.1.0"
---
# Story

A story states what a person can do once a change ships, in acceptance criteria concrete enough to write a test from each without asking anybody.

* **Build from a story:** write it, agree it with the user, then implement it.

## Words used here

* **Story:** a change someone outside it can observe (a person, or a program that calls the changed code), along one path through the workflow end to end, in one variation.
* **Variation:** one business rule, kind of data or way of entering it that changes the main outcome.
* **Acceptance criterion:** one numbered rule of a story in one line, with one to three examples under it.
* **Example:** Given the starting state, When one action, Then what the person or caller sees, all in real values.
* **Obvious rule:** a rule an example would only restate has no example.
* **Feature:** several stories that share one outcome.
* **Feature file:** holds the feature header and the stories.
* **Tracker:** the issue tracker the request or the user names, if any.

## Pick the path

* **Create a story** from a request, an idea or a PRD: [references/create.md](references/create.md).
* **Review stories** someone wrote: [references/review.md](references/review.md).
* **Implement a story** the user agreed, or a change that needs no story: [references/implement.md](references/implement.md).
* **Resume:** find the `story/` branch. `git config --get-all branch.<branch>.redCommit` shows whether its tests exist. Read the story from its issue, the feature file or the red commit's message, and continue at the first step of implement.md not done.
* **Next story:** the first in the feature's `Order:` with no open pull request.
* **Check the outcome:** once every story in `Order:` is merged and the `Measure:` date has passed, or when the user asks how a feature did. Read the measure with a tool where one reaches it, else ask the user for it. Write the value and the date on the header's `Result:` line and report whether it met the target. A miss becomes new stories or a decision for the user; no merged story reopens.

## Size first

* **No story:** a change no person or caller sees (a rename, a dependency bump, a refactor), or a one-sentence fix whose test is obvious.
* **No story, build:** say so and build it with no new acceptance criteria, or with the reproduction as the only one.
* **One story:** one path end to end and one variation; every acceptance criterion's `when` is the same action by the same role.
* **Several stories:** more than one path or variation, or an acceptance criterion whose `when` is a different action or person.
* **Several stories, also:** an unknown that changes what gets built.
* **Several stories, then:** split into a feature by [references/split.md](references/split.md) and build one story at a time.

A decision that costs more than a day to reverse goes to the `adr` skill before any code.

## Talking to the user

* **A fact a tool can reach:** look it up and use it; don't ask. Examples: what a table holds, what a route returns, what CI runs.
* **A small choice:** decide it and list it under the story's `Decided` or in the report.
* **A small choice is:** one that changes nothing a person or caller sees, involves no architecture, and touches no money, authentication or personal data. Examples: a name, a helper's signature, a file layout, which existing library to call.
* **Product intent, a reading that changes the acceptance criteria, or a choice expensive to reverse:** ask.
* **How to ask:** one question per message, recommended option first, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion).
* **The user is away:** take the recommended option, keep going, and list every choice made that way.

## When to stop

Stop for the user only to agree a story or a split, to answer an open question, at a test you cannot satisfy, and when the pull request is open. Do not stop to report progress after the tests are red, after green or after the review.
