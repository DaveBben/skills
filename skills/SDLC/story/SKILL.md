---
name: story
description: "Use this skill before touching any file on a request to add, change or remove behaviour in existing code, and whenever work must become user stories or a story must be built or resumed. Use it on: 'add X', 'I want to instead have X', 'change X to Y', 'write a story for X', 'write the acceptance criteria', 'review this story', 'implement this story', 'I have an idea', 'pick up where we left off' or 'from the handoff', 'what should I pick up next'. Use it even when the change looks small. Writes each change as a story with acceptance criteria, then builds it test-first. Not for filing an issue, as in 'create a story on gitea'; that is `using-trackers`. Not for a reported bug; that is `bug`. Not for structure alone; that is `refactoring`."
license: MIT
metadata:
  version: "7.3.0"
---
# Story

A story states what a person can do once a change ships, in acceptance criteria concrete enough to write a test from each without asking anybody.
Write the story, agree it with the user, then implement it.

## Words used here

* **Story:** one vertical slice: a change a person, or a program that calls the changed code, can observe, along one path through the workflow end to end, in one variation.
* **Variation:** one business rule, kind of data or way of entering it that changes the main outcome.
* **Acceptance criterion:** one numbered rule of a story in one line, with one to three examples under it.
* **Example:** Given/When/Then in real values.
* **Feature:** several stories that share one outcome.
* **Owning story:** the one story of a feature that owns its outcome, usually the last; it carries the feature's `Measure` section.
* **Glossary:** `docs/glossary.md`, one `<term>: <meaning>` line per domain term the user confirmed.

## When to stop

Stop for the user only to agree a story or a split, to answer an open question, at a test you cannot satisfy, when watching the pull request ends without a merge, and when the outcome check ends.
Do not stop to report progress after the tests are red, after green, after the review or after the pull request opens.

## Pick the path

* **Create a story** from a request, an idea or a PRD: [references/create.md](references/create.md).
* **Review stories** someone wrote: [references/review.md](references/review.md).
* **Implement a story** the user agreed, or a change that needs no story: [references/implement.md](references/implement.md), then [references/ship.md](references/ship.md) once the pull request is open.
* **A reported bug:** the `bug` skill reproduces and decides it first, then builds its fix through implement.md.
* **Measure the feature:** [references/ship.md](references/ship.md).
* **Resume:** find the `story/` branch. `git config --get-all branch.<branch>.redCommit` shows whether its tests exist. Read the story from its issue, `docs/stories/<slug>.md` or the red commit's message, and continue at the first step of implement.md not done: an open pull request resumes at [references/ship.md](references/ship.md)'s watch step, a merged one at its outcome check.
* **Next story:** the first story with no open blocker and no open pull request: on a tracker (the one the request, the user or the repository names), the first such issue; without one, the first such story in `docs/stories/<slug>.md`. A story with an `Open questions` section is not ready: show the user its questions and stop. Every read or write of a tracker goes through the `using-trackers` skill.

## Size first

* **No story:** a change no person or caller sees (a rename, a dependency bump, a refactor by the `refactoring` skill), or a one-sentence fix whose test is obvious. Say so and build it by implement.md with no new acceptance criteria, or with the reproduction as the only one.
* **Otherwise:** create.md sizes it as one story or several.

A decision that costs more than a day to reverse goes to the `adr` skill before any code.

## Talking to the user

* **A fact a tool can reach:** look it up; never ask the user for it.
* **A small choice:** one that changes nothing a person or caller sees, involves no architecture, and touches no money, authentication or personal data, such as a name, a helper's signature, a file layout or which existing library to call. Decide it and list it under the story's `Decided` or in the report.
* **Ask** about product intent, a reading that changes the acceptance criteria, or a choice expensive to reverse.
* **The user is away:** take the recommended option for a small choice, keep going, and list each choice made that way. Anything else goes under `Open questions` and stops the work until the user answers it.
