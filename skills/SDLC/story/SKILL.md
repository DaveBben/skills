---
name: story
description: "Use this skill when work must become user stories before it is built, or when stories must be split, reviewed or picked: an idea, a feature request, a PRD, an epic, a bug report too vague to test, or a list of stories someone wrote. Use it on: 'write a story for X', 'write the acceptance criteria', 'turn this into stories', 'break this down', 'I have an idea', 'turn this PRD into stories', 'review these stories', 'are these the right stories', 'what should I pick up next'. Writes each story as an outcome, a Not doing list and numbered cases with concrete values, asking only where two readings of the request lead to different cases."
license: MIT
metadata:
  version: "1.0.0"
---
# Story

A story says what a person will be able to do once a change ships, in cases concrete enough that a test can be written from each one without asking anybody. It is the input the `deliver` skill builds from. Write as little up front as building needs: one story's cases when it starts, not a specification for the whole feature.

## Words used here

* **Story:** a change a person outside the system can observe, in one workflow step and one variation.
* **Case:** one numbered line of a story: a starting state, an action, and what the person sees, with real values.
* **Feature:** several stories that share one outcome. Its **feature file** holds the feature header and the stories.
* **Tracker:** the issue tracker the `Backlog:` line of `AGENTS.md` names, if any. The ways to reach one are in [../deliver/references/tracker.md](../deliver/references/tracker.md).

## The story

```text
<Title: what the person can do, five to eight words>
Outcome:   <what a person observes once this ships>
Not doing: <what a reader might expect that this story leaves out; one per line>
Cases:
  1. <starting state> — <action> — <what the person sees, with real values>
  2. ...
Verify:    <the command, request or screen that shows the outcome end to end>
Decided:   <each choice made without the user, and why; omit when none>
```

* **Case 1 is the outcome,** or for a bug, the reproduction: the starting state, the action, and what the person should see instead of what they see now.
* **Use real values.** Name the input, the number, the message text, the status code. Never write improve, better, faster, robust, correct, properly, handled or seamless; write the number or the event.
* **One observable result per case,** named the way the code and its tests already name things. A mechanism (an exception class, a lock, a log line, a call to a function) is not a case; a case says what a caller or a person sees.
* **Walk the failure paths** and give each that can happen a case or a `Not doing` line: empty or malformed input, input past a limit, the same action twice, two at the same moment, an action stopped halfway, a dependency down.
* **Walk the abuse paths** when the story takes input from outside the system: another person's data, bulk repetition, a response that reveals a third party. Each that matters gets a case.
* **Keep the cases the existing behaviour already covers out,** unless this story changes them. A case that changes what existing code does says so: `changes: <the old behaviour>`.

## Size first

* **No story:** a change no person sees (a rename, a dependency bump, a refactor), or a one-sentence fix whose test is obvious. Say so and hand it to `deliver`.
* **One story:** one workflow step and one variation.
* **Several stories:** more than one step or variation, or an unknown that changes what gets built. Split it by [references/split.md](references/split.md) into a feature.

## Ask only where readings diverge

Read the request, the code it touches and that code's tests first. A fact a tool can reach (what a table holds, what a route returns, what a function does with empty input) is looked up, never asked.

Then find each place where two reasonable readings of the request lead to different cases: a value the request leaves open, a boundary it does not mention, two behaviours it could mean. Ask about those only, one question per message, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion): the recommended reading first, and each option's consequence in one sentence. Decide everything else yourself and list it on `Decided:`. When the request already names the interface, the values and the errors, ask nothing and write the cases from it. When the user is away, take the recommended reading and list it on `Decided:`.

Show the story in one message and say which cases record a choice the user might make differently. The user edits it or says go; that is the agreement `deliver` builds from.

## Where stories live

* **With a tracker:** a story is an issue, its description the story text; a feature is an epic whose child issues are its stories.
* **Without one:** a single story lives in the chat until `deliver` writes it into the red commit's message and the pull request's description. A feature lives in `docs/stories/<slug>.md`, committed on its own branch: the feature header, then each story under its title.

The feature header, at the top of the feature file or the epic's description:

```text
Outcome:      <what a person does differently once the whole feature ships>
Not doing:    <one checkable non-goal per line>
Order:        <the story titles or keys, in the order they will be built>
Decided:      <one ADR path per line, written by the architecture skill>
Deferred:     <one open decision per line, with what will force it>
Repositories: <one line per repository the feature touches, when more than one>
```

## Pick the next story

The next story is the first in `Order:` whose blockers are done and whose questions are answered. When something new is being built, the first story is the thinnest slice a real person can use end to end. Print the next story, the others that are ready, and what blocks the rest, and wait for the user's choice.

## Review stories someone wrote

Read [references/review.md](references/review.md) and follow it.
