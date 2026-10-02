# Create a story

Sections: Clear up ambiguity, Write the story, When to stop, Agree it, Where stories live.

* **Read first:** the request, the code it touches and that code's tests. Read a story linked on a tracker with its comments.
* **Several stories:** make the request a feature by [split.md](split.md) first; then create one story at a time.

## Clear up ambiguity

* **Draft the examples first:** an example whose `then` you cannot fill with a real value from the request, the code or a tool is a question for the user, not a guess.
* **Another outcome possible** from the givens listed: a given is missing. Look it up or ask.

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

A bug story in code with no end user:

```text
Title: Refund caller gets the partial amount back

As the billing service calling refund(),
I want a partial refund to return the amount refunded
so that the invoice shows what the customer was paid.

Context: refund() returns the order total even for a partial refund, so invoices overstate refunds. Reported in PAY-88.

Acceptance criteria
1. A partial refund returns the amount refunded.
   changes: it returned the order total.
   Given order 1042 totals $80.00 and nothing is refunded yet,
   when billing calls refund(1042, amount=$30.00),
   then it returns $30.00 and order 1042 shows $50.00 refundable.

Out of scope
* Refunds in a currency other than the order's.
```

* **Role:** whoever uses the changed interface. Use a kind of person the system has (a registered customer, a clinic admin), or, in code with no end user, the program or developer that calls it (a billing service calling `refund()`).
* **Role, never:** "user", or the person building the change.
* **`I want`:** what they can do, never a control or a design (a dropdown, a modal, a new table). The design comes after the need.
* **Reason:** what they gain, not the feature restated. When neither the request nor the code gives one, ask; the reason decides which acceptance criteria matter.
* **Context:** write it from the request, the tracker or the PRD, never from your plan. Whoever writes the tests reads it and nothing from this chat.
* **Acceptance criterion 1:** the outcome. For a bug, the reproduction: the starting state, the action, and what the person should see instead of what they see now.
* **Real values:** name the input, the number, the message text, the status code.
* **Error messages:** every error the person sees says what went wrong and what they can do next.
* **Banned words:** improve, better, faster, robust, correct, properly, handled, seamless. Write the number or the event.
* **Each Given:** state every fact the outcome depends on, and nothing else. An unneeded value is clutter the test copies into its fixture.
* **Boundaries:** when a rule covers a range, give an example at the limit itself, and one past it when that is a different rule.
* **One action per example.** Its `then` and `and` lines name what a caller or a person sees, in the names the code and its tests already use.
* **Not a result:** a mechanism (an exception class, a lock, a log line, a call to a function).
* **Past about 8 criteria:** check whether they are separate variations of one action (each kind of code, each file type), and split by variation when they are.
* **A rule with many examples** may be several rules.
* **Existing behaviour:** leave out acceptance criteria it already covers, unless this story changes them.
* **A changed behaviour:** mark the criterion `changes: <the old behaviour>`.

Walk the three lists below to find what this change can break, not to fill the story:

* **Write a criterion** only where the right outcome is wrong or unknown in the code today, or where the user might choose differently.
* **Write an `Out of scope` line** only for what a reader would expect this story to do.
* **For a bug,** walk only the paths the fix touches.

**Failure paths:**

* **Input:** empty or malformed; the maximum, one past it, very long text and unicode.
* **Repetition:** the same action twice; two at the same moment.
* **Interruption:** an action stopped halfway, including a session that expires or a network that drops. Does the person's work get lost?
* **Dependencies:** down, slow or partly succeeded.
* **Equivalent inputs:** inputs that differ in case, whitespace or format but must give the same result.
* **Existing data:** each state it can be in (disabled, deleted, unverified, empty), and data created before this change, with any migration it needs.
* **Time:** when the story has a date, an expiry or a schedule, midnight, a daylight-saving change and month end.

**Abuse paths,** when the story takes input from outside the system:

* **Ownership:** another person's data.
* **Volume:** bulk repetition.
* **Disclosure:** a response that reveals a third party, and a difference in timing or error that reveals what the system holds.
* **Hidden input:** input that arrives outside the visible field (a header, a query parameter, a file name).

**What the result reaches:**

* **Accessibility:** someone using a screen reader or only a keyboard, where the story shows them anything.
* **Roles:** a role that may not do this, and what it sees instead.
* **Other viewers:** another person who must see the result (a support agent, an operator, an auditor) gets their own story.
* **Messages:** each email, notification or webhook fires exactly once.
* **Readers of a changed API, file or message:** each program that reads it.
* **Caches:** a cached result, and how soon it shows the change.
* **Data changes:** an action that changes or deletes data, and whether it can be undone.

## When to stop

The story is ready when all of these hold, and no sooner:

* **Each example can become a test without asking anybody:** a starting state, one action, and a result with real values.
* **No question is open:** every reading that would change an acceptance criterion is answered by the user or recorded under `Decided`.
* **It is one story:** a named role and reason, and every example's `when` is the same action by that role. An `I want` joined by "and" or "or" is two stories.

Then stop writing. Add no criterion for a walk item that cannot happen here, for behaviour existing tests already cover, or to reach a count.

## Agree it

* **Show the story** in one message.
* **The agreement:** the user edits it or says go; the build starts from that.

## Where stories live

* **With a tracker:** a story is an issue, its description the story text; a feature is an epic whose child issues are its stories.
* **Without one, a single story:** the red commit's message and the pull request's description hold it.
* **Without one, a feature:** it lives in `docs/stories/<slug>.md`, committed on its own branch: the feature header, then each story under its title.

The feature header goes at the top of the feature file or the epic's description:

```text
Outcome:      <what a person does differently once the whole feature ships, and how you will see that they do>
Out of scope: <one checkable non-goal per line>
Order:        <the story titles or keys, in the order they will be built>
Decided:      <one ADR path per line, written by the adr skill>
Deferred:     <one open decision per line, with what will force it>
Repositories: <one line per repository the feature touches, when more than one>
```
