---
name: story
description: "Use this skill before touching any file on a request to add, change, fix or remove behaviour in code that exists, and whenever work must become user stories or a story must be built. Use it on: 'add X', 'fix the bug where X', 'X is broken', 'refactor X', 'build story X', 'build this' with a link to an issue, 'pick up where we left off', 'write a story for X', 'write the acceptance criteria', 'break this down', 'I have an idea', 'turn this PRD into stories', 'review these stories', 'what should I pick up next'. Use it even when the change looks small. Writes each story as As a / I want / so that, its context, numbered rules each with Given/When/Then examples in concrete values, and an Out of scope list, asking wherever a result is not in the request, the code or a tool; then fixes the interface, has a fresh agent write failing tests from the acceptance criteria alone, writes the code until they pass, refactors, has fresh agents review it, and opens a pull request into main."
license: MIT
metadata:
  version: "2.0.0"
# Claude Code only: registered when the skill runs, for the rest of the session.
# scripts/guard.py says what it refuses. Without python3, it exits 0.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: 'f="${CLAUDE_PLUGIN_ROOT}/skills/story/scripts/guard.py"; [ -f "$f" ] && command -v python3 >/dev/null 2>&1 || exit 0; python3 "$f"'
---
# Story

A story says what a person will be able to do once a change ships, in acceptance criteria concrete enough that a test can be written from each one without asking anybody. Every change to behaviour is built from one: write it, agree it with the user, then implement it. Write as little up front as building needs: one story's acceptance criteria when it starts, not a specification for the whole feature.

## Words used here

* **Story:** a change someone outside the change can observe (a person, or a program that calls the changed code), along one path through the workflow end to end, in one variation.
* **Variation:** one business rule, kind of data or way of entering it that changes the main outcome.
* **Acceptance criterion:** one numbered rule of a story in one line, with one to three examples under it, each a Given / When / Then with real values: Given the starting state, When one action, Then what the person or caller sees. A rule so obvious that an example would only restate it has none.
* **Feature:** several stories that share one outcome. Its **feature file** holds the feature header and the stories.
* **Tracker:** the issue tracker the request or the user names, if any; never recorded in a repository.

## Pick the path

* **Create a story** from a request, an idea or a PRD: [references/create.md](references/create.md).
* **Review stories** someone wrote: [references/review.md](references/review.md).
* **Implement a story** the user agreed, or a change that needs no story: [references/implement.md](references/implement.md).

## Size first

* **No story:** a change no person or caller sees (a rename, a dependency bump, a refactor), or a one-sentence fix whose test is obvious. Say so and build it with no new acceptance criteria, or the reproduction as the only acceptance criterion.
* **One story:** one path end to end and one variation; every acceptance criterion's `when` is the same action by the same role.
* **Several stories:** more than one path or variation, an acceptance criterion whose `when` is a different action or person, or an unknown that changes what gets built. Split it by [references/split.md](references/split.md) into a feature, then build one story at a time.

A decision that costs more than a day to reverse goes to the `adr` skill before any code.

## Talking to the user

* **A fact a tool can reach** (what a table holds, what a route returns, what a function does with empty input, what CI runs): look it up and use it; don't ask it.
* **A small choice that changes nothing a person or caller sees, no architecture, and nothing touching money, authentication or personal data** (a name, a helper's signature, a file layout, which existing library to call): decide it and list it under the story's `Decided` or in the report.
* **Product intent, a reading that changes the acceptance criteria, or a choice expensive to reverse:** ask, one question per message, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion), recommended option first.
* **The user is away:** take the recommended option, keep going, and list every choice made that way.
