# Create a story

Read the request, the code it touches and that code's tests first. A story linked on a tracker is read with its comments. A request that is several stories becomes a feature by [split.md](split.md) first; then create one story at a time.

## Clear up ambiguity

When the request, or any answer the user gives, could be read more than one way, follow up with a clarifying question before writing the acceptance criteria it affects.

## Write the story

```text
Title: <what the person can do, five to eight words>

As a <the kind of person this is for>,
I want <what they can do once this ships>
so that <what they gain>.

Acceptance criteria
1. Given <the starting state, with real values>,
   when <one action>,
   then <what the person sees, with real values>,
   and <another result of the same action>.

2. ...

Out of scope
* <what a reader might expect that this story leaves out; one per line>

Decided
* <each choice made without the user, and why; omit the section when none>
```

* **Name a real role and reason.** The role is a kind of person the system has (a registered customer, a clinic admin), never "user". The `I want` is what they can do, never a control or a design (a dropdown, a modal, a new table): the design comes after the need. The reason is what they gain, not the feature restated. When neither the request nor the code gives a reason, ask; the reason decides which acceptance criteria matter.
* **Acceptance criterion 1 is the outcome,** or for a bug, the reproduction: the starting state, the action, and what the person should see instead of what they see now.
* **Use real values.** Name the input, the number, the message text, the status code. Every error the person sees says what went wrong and what they can do next. Never write improve, better, faster, robust, correct, properly, handled or seamless; write the number or the event.
* **One action per acceptance criterion.** Its `then` and `and` lines name what a caller or a person sees, the way the code and its tests already name things. A mechanism (an exception class, a lock, a log line, a call to a function) is not a result.
* **Past about 8 acceptance criteria,** check whether they are separate variations of one action (each kind of code, each file type); when they are, split by variation.
* **Walk the failure paths** and give each that can happen an acceptance criterion or an `Out of scope` line: empty or malformed input; the maximum, one past it, very long text and unicode; the same action twice; two at the same moment; an action stopped halfway, including a session that expires or a network that drops, and whether the person's work is lost; a dependency down, slow or partly succeeded; inputs that differ in case, whitespace or format but must give the same result; each state the existing data can be in (disabled, deleted, unverified, empty), and data created before this change, with any migration it needs; and when the story has a date, an expiry or a schedule, midnight, a daylight-saving change and month end.
* **Walk the abuse paths** when the story takes input from outside the system: another person's data, bulk repetition, a response that reveals a third party, input that arrives outside the visible field (a header, a query parameter, a file name), and a difference in timing or error that reveals what the system holds. Each that matters gets an acceptance criterion.
* **Walk what the result reaches:** someone using a screen reader or only a keyboard gets an acceptance criterion where the story shows them anything, and a role that may not do this gets one saying what it sees instead. Another person who must see the result (a support agent, an operator, an auditor) gets their own story. Each email, notification or webhook fires exactly once; a program that reads a changed API, file or message keeps working, or the break is an `Out of scope` line; a cached result shows the change within a stated time; and an action that changes or deletes data can be undone, or says it cannot.
* **Keep the acceptance criteria the existing behaviour already covers out,** unless this story changes them. An acceptance criterion that changes what existing code does says so: `changes: <the old behaviour>`.

## When to stop

The story is ready when all of these hold, and no sooner:

* **Each acceptance criterion can become a test without asking anybody:** a starting state, one action, and a result with real values.
* **Every walk item that can happen is answered,** with an acceptance criterion or an `Out of scope` line.
* **No question is open:** every reading that would change an acceptance criterion is answered by the user or recorded under `Decided`.
* **It is one story:** a named role and reason, and every acceptance criterion's `when` is the same action by that role.

Then stop writing. Add no acceptance criterion for a walk item that cannot happen here, for behaviour existing tests already cover, or to reach a count: more criteria do not catch more faults.

## Agree it

Show the story in one message and say which acceptance criteria record a choice the user might make differently. The user edits it or says go; that is the agreement the build starts from.

## Where stories live

* **With a tracker:** a story is an issue, its description the story text; a feature is an epic whose child issues are its stories.
* **Without one:** a single story lives in the chat until the red commit's message and the pull request's description hold it. A feature lives in `docs/stories/<slug>.md`, committed on its own branch: the feature header, then each story under its title.

The feature header, at the top of the feature file or the epic's description:

```text
Outcome:      <what a person does differently once the whole feature ships, and how you will see that they do>
Out of scope: <one checkable non-goal per line>
Order:        <the story titles or keys, in the order they will be built>
Decided:      <one ADR path per line, written by the adr skill>
Deferred:     <one open decision per line, with what will force it>
Repositories: <one line per repository the feature touches, when more than one>
```
