# Create a story

Read the request, the code it touches and that code's tests first. A story linked on a tracker is read with its comments. A request that is several stories becomes a feature by [split.md](split.md) first; then create one story at a time.

## Clear up ambiguity

When the request, or any answer the user gives, could be read more than one way, follow up with a clarifying question before writing the acceptance criteria it affects. Draft the examples first: an example whose `then` you cannot fill with a real value from the request, the code or a tool is a question for the user, not a guess. When another outcome is possible from the givens listed, a given is missing: look it up or ask.

## Write the story

```text
Title: <what the person can do, five to eight words>

As a <the kind of person this is for>,
I want <what they can do once this ships>
so that <what they gain>.

Context: <two to five sentences: who hits this and when, what they do today, why now, and a link to the request or PRD>

Acceptance criteria
1. <the rule: the general behaviour, in one line>
   Given <every fact the outcome depends on, with real values>,
   when <one action>,
   then <what the person sees, with real values>,
   and <another result of the same action>.
   Given <the boundary case> ...

2. ...

Out of scope
* <what a reader might expect that this story leaves out; one per line>

Decided
* <each choice made without the user, and why; omit the section when none>
```

A finished story:

```text
Title: Account holder withdraws cash

As an account holder,
I want to withdraw cash from an ATM
so that I can pay in cash when the branch is closed.

Context: Account holders at the three sites that lost their branch this year queue at the post office for cash. Requested in BANK-41.

Acceptance criteria
1. A withdrawal up to the balance dispenses the cash and reduces the balance by the same amount.
   Given the balance is $100, the card is valid and the machine holds $500,
   when the account holder requests $20,
   then the ATM dispenses $20, the balance is $80 and the card is returned.
   Given the balance is $20, when they request $20, then the ATM dispenses $20 and the balance is $0.

2. A withdrawal over the balance dispenses nothing.
   Given the balance is $10 and the card is valid,
   when the account holder requests $20,
   then the ATM dispenses nothing, shows "Not enough money in your account: your balance is $10" and returns the card.

3. A disabled card is kept.
   Given the card is disabled,
   when the account holder requests $20,
   then the ATM keeps the card and shows "Your card has been kept. Call 0800 123 456."

Out of scope
* Overdraft limits.
* Withdrawals in another currency.
```

Criterion 3 states no balance: the outcome does not depend on it.

* **Name a real role and reason.** The role is whoever uses the changed interface: a kind of person the system has (a registered customer, a clinic admin), or, in code with no end user, the program or developer that calls it (a billing service calling `refund()`). Never "user", and never the person building the change. The `I want` is what they can do, never a control or a design (a dropdown, a modal, a new table): the design comes after the need. The reason is what they gain, not the feature restated. When neither the request nor the code gives a reason, ask; the reason decides which acceptance criteria matter.
* **Write the context from the request, the tracker or the PRD,** never from your plan: whoever writes the tests reads it and nothing from this chat.
* **Acceptance criterion 1 is the outcome,** or for a bug, the reproduction: the starting state, the action, and what the person should see instead of what they see now.
* **Use real values.** Name the input, the number, the message text, the status code. Every error the person sees says what went wrong and what they can do next. Never write improve, better, faster, robust, correct, properly, handled or seamless; write the number or the event.
* **State in each Given every fact the outcome depends on, and nothing else.** A value no outcome depends on is clutter the test copies into its fixture.
* **Give each rule an example at its boundary** when it covers a range: the limit itself, and one past it when that is a different rule.
* **One action per example.** Its `then` and `and` lines name what a caller or a person sees, the way the code and its tests already name things. A mechanism (an exception class, a lock, a log line, a call to a function) is not a result.
* **Past about 8 acceptance criteria,** check whether they are separate variations of one action (each kind of code, each file type); when they are, split by variation. A rule with many examples may be several rules.
* **Walk the three lists below to find what this change can break, not to fill the story.** Write an acceptance criterion only where the right outcome is wrong or unknown in the code today, or where the user might choose differently; write an `Out of scope` line only for what a reader would expect this story to do. For a bug, walk only the paths the fix touches.
* **Walk the failure paths:** empty or malformed input; the maximum, one past it, very long text and unicode; the same action twice; two at the same moment; an action stopped halfway, including a session that expires or a network that drops, and whether the person's work is lost; a dependency down, slow or partly succeeded; inputs that differ in case, whitespace or format but must give the same result; each state the existing data can be in (disabled, deleted, unverified, empty), and data created before this change, with any migration it needs; and when the story has a date, an expiry or a schedule, midnight, a daylight-saving change and month end.
* **Walk the abuse paths** when the story takes input from outside the system: another person's data, bulk repetition, a response that reveals a third party, input that arrives outside the visible field (a header, a query parameter, a file name), and a difference in timing or error that reveals what the system holds.
* **Walk what the result reaches:** someone using a screen reader or only a keyboard, where the story shows them anything; a role that may not do this, and what it sees instead; another person who must see the result (a support agent, an operator, an auditor), who gets their own story; each email, notification or webhook, which fires exactly once; a program that reads a changed API, file or message; a cached result, and how soon it shows the change; and an action that changes or deletes data, and whether it can be undone.
* **Keep the acceptance criteria the existing behaviour already covers out,** unless this story changes them. An acceptance criterion that changes what existing code does says so: `changes: <the old behaviour>`.

## When to stop

The story is ready when all of these hold, and no sooner:

* **Each example can become a test without asking anybody:** a starting state, one action, and a result with real values.
* **No question is open:** every reading that would change an acceptance criterion is answered by the user or recorded under `Decided`.
* **It is one story:** a named role and reason, and every example's `when` is the same action by that role. An `I want` joined by "and" or "or" is two stories.

Then stop writing. Add no acceptance criterion for a walk item that cannot happen here, for behaviour existing tests already cover, or to reach a count: more criteria do not catch more faults.

## Agree it

Show the story in one message. The user edits it or says go; that is the agreement the build starts from.

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
