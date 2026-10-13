---
name: story
description: "Use this skill before touching any file on a request to add, change or remove behaviour in code that exists, and whenever work must become user stories or a story must be built. Use it on: 'add X', 'build story X', 'build this' with a link to an issue, 'pick up where we left off', 'write a story for X', 'write the acceptance criteria', 'break this down', 'I have an idea', 'turn this PRD into stories', 'review these stories', 'what should I pick up next'. Use it even when the change looks small. Writes each change as a user story with concrete acceptance criteria, agrees it with the user, then builds it test-first and opens a pull request into main. Not for a reported bug; that is `bug`, which builds its fix here. Not for a change to structure alone; that is `refactoring`."
license: MIT
metadata:
  version: "7.0.0"
---
# Story

A story states what a person can do once a change ships, in acceptance criteria concrete enough to write a test from each without asking anybody.

* **Build from a story:** write it, agree it with the user, then implement it.

## Words used here

* **Story:** a change someone outside it can observe (a person, or a program that calls the changed code), along one path through the workflow end to end (a vertical slice), in one variation.
* **Variation:** one business rule, kind of data or way of entering it that changes the main outcome.
* **Acceptance criterion:** one numbered rule of a story in one line, with one to three examples under it.
* **Example:** Given/When/Then in real values.
* **Feature:** several stories that share one outcome.
* **Owning story:** the one story of a feature that owns its outcome, usually the last; it carries the feature's `Measure` section.
* **Glossary:** `docs/glossary.md`, one line per domain term the user confirmed: the term, a colon, and what it means in this product.

## When to stop

Stop for the user only to agree a story or a split, to answer an open question, at a test you cannot satisfy, and when the pull request is open. Do not stop to report progress after the tests are red, after green or after the review.

## Pick the path

* **Create a story** from a request, an idea or a PRD: [references/create.md](references/create.md).
* **Review stories** someone wrote: [references/review.md](references/review.md).
* **Implement a story** the user agreed, or a change that needs no story: [references/implement.md](references/implement.md).
* **A reported bug:** the `bug` skill reproduces and decides it first, then builds its fix through implement.md.
* **Resume:** find the `story/` branch. `git config --get-all branch.<branch>.redCommit` shows whether its tests exist. Read the story from its issue, `docs/stories/<slug>.md` or the red commit's message, and continue at the first step of implement.md not done.
* **Next story:** the first story with no open blocker and no open pull request: on a tracker (the one the request, the user or the repository names), the first such issue; without one, the first such story in `docs/stories/<slug>.md`. A story with an `Open questions` section is not ready: show the user its questions and stop. Every read or write of a tracker goes through the `using-trackers` skill.
* **Check the outcome:** once every story of the feature is merged and the date on the owning story's `Measure:` line has passed, or when the user asks how a feature did. Read the measure with a tool where one reaches it, else ask the user for it. Write the value and the date on its `Result:` line and report whether it met the target. A miss becomes new stories or a decision for the user; no merged story reopens.

## Size first

* **No story:** a change no person or caller sees (a rename, a dependency bump, a refactor by the `refactoring` skill), or a one-sentence fix whose test is obvious.
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
* **Keep asking** until none of those is open: what the change must and must not do, who may do it, each value an example needs, and each choice the answers raise. A `No story` change needs no questions, except a decision for the `adr` skill.
* **Order:** a decision opens the decisions that depend on it. Ask a question only when no open question would change its answer.
* **How to ask:** in rounds. A round asks every question that is ready, up to four, each with the recommended option first, through the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion). After each round, work out which questions are ready now.
* **Facts in parallel:** look up a fact a question needs with a subagent where the harness has one, and ask the questions that do not wait on it meanwhile.
* **Last option, always:** "I need to research this." Name the options and the trade-off they turn on, so the user knows what to look up.
* **The user picks research:** write the question under the story's `Open questions` as `Needs research: <question>; options: <the options>`, and keep asking the rest. The story is not ready to build until the user answers it.
* **The user cannot choose** between options a prototype would show: offer a spike by the `spike` skill.
* **The user is away:** take the recommended option for a small choice, keep going, and list every choice made that way. Anything else goes under `Open questions` and stops the work until the user answers it.

Never stop to report progress; stop only at the cases in When to stop.
