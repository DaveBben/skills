---
name: story
description: "Use this skill when one story, ticket or bug report needs its acceptance criteria written, repaired or reviewed, without building it. Use it on: 'write the user story', 'write the acceptance criteria', 'write the AC for this', 'what does done mean here', 'is this story ready', 'make this ticket testable', 'what could go wrong with this story', 'review this story', 'review these acceptance criteria', 'rewrite this ticket'. Use it on a ticket full of better, faster, robust, seamless, properly or handled. Produces one story: outcome, why, scope, and Given/When/Then criteria for the outcome plus its boundary, failure and abuse paths, with open decisions marked open and the crossings where its input is interpreted as instructions. Not for splitting an epic (`story-map`), choosing what to build next (`next-story`), listing tests (`test-plan`), or building it (`deliver`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Story

Everything here is agreed with the user. Propose, then wait.

A story is a change a person outside the system can observe. It gets its own card. Work nobody observes alone, such as a new column or a service the story calls, is written as criteria on the story that needs it and never gets a card of its own.

```text
<Title: what the person will be able to do, five to eight words>
Outcome:  <what a person observes once this story is done>
Why:      <what stays broken for them without it>
Scope:    <what this story covers, and what it leaves to which other story>
Criteria:
  a. Given <a concrete starting state>, when <a concrete action>, then <what the person sees, with real values>
  b. <a boundary, a failure path or an abuse path, same form>
Open:     <each undecided value, who decides it, and which criterion waits on it; "none" when none>
Crossings: <each input this story adds and what interprets it as instructions; omit when none>
```

Criterion a is the outcome. The criteria after it are the boundaries, failure paths and abuse paths from sections 3 to 5 that apply to that outcome. Each criterion is proved by its own acceptance test: an automated test that checks what the person sees. The outcome criterion's test drives the interface the person uses. When a screen only shows what a service returns, the tests for the other criteria may drive that service.

## 1. Who observes

The criteria are written in whatever the person or service using this story can see. Decide which of the two it is.

* **A person** sees a screen, a message, a document, a file. Write the criteria in what appears there.
* **A service** sees status codes, an error code in the body, and the response shape. Write those exact values into the criteria. Add two criteria a person never needs: what a repeated identical request returns, and what the response is when the caller sends a field of the wrong type. Where another team owns the caller, have them state what they depend on and run their expectations against the interface in the build.

## 2. Write the outcome criterion first

* **Use concrete values.**
* **Ban the words that hide the measurement:** improve, better, faster, seamless, robust, correct, properly, handled, intuitive, flexible, scalable, modern. Replace each with the number or the observable event.
* **Put a number in every limit.** When nobody can supply the number yet, write on the story that the criterion has no number and is not testable as written. Never leave a vague criterion that reads as complete.
* **For a bug, criterion a is the reproduction:** the starting state, the action, and what the person should see instead of what they saw.
* **One outcome per criterion.** A criterion joining two outcomes with "and" is two criteria.
* **Write from the observer's side.** "The clerk sees the invoice marked overdue" is a criterion. "Each order has exactly one invoice row" is written from the system's side. A criterion written from the system's side is usually a property of another story's behaviour, and it belongs on that story.
* **Name the interface.** The criterion says where the person acts and where they see the result.
* **Use the domain's nouns.** When the work opens a domain this system has no words for, ask the user for its three to five core nouns and use those exact terms in every criterion, and later in types, tables and variables. Never invent a synonym for a noun the user already uses.

## 3. Generate the failure paths

Take boundaries from the requirements document before inventing any. Walk this list against the outcome. Each item that can happen earns its own criterion saying what the person sees.

* **Empty or malformed input** at each field the person fills.
* **Input outside the limits:** too long, too many, too old, out of range. The limit is a number the user chooses here.
* **The same action repeated:** the person submits twice, or clicks twice, or the caller retries. Say what the second one returns.
* **Two of the same action at the same moment**, where the result depends on what already exists.
* **The action half completes:** something is stored and the confirming step never happens. Say how long that state lives and what clears it.
* **A thing the work depends on is unavailable:** the database, a third-party API, the network. Say what the person sees and whether anything was stored.
* **A step that takes unbounded time.** Say the limit and what the person sees when it passes.
* **The person abandons the flow** partway.

## 4. Generate the abuse paths

Ask one question of every input: who else can send this, and what do they gain by sending something the owner did not intend.

* **Someone acts as another person**, using their address, their order, their identifier.
* **A program repeats the action in bulk**, thousands of times.
* **The response reveals something about a third party.** Answering "already registered" tells anyone whether a given person is on the list. Returning the same response for both cases is a product decision with a cost in clarity.
* **The feature sends something to an address the requester chose**, letting it flood a stranger's inbox or phone.
* **Personal data enters the system.** Consent, how long it is kept, and how the person removes it are each a criterion or an explicit non-goal.

Turn each one that matters into a criterion with a number in it: how many requests from one source in a minute, how many messages to one address in a day, how long a link stays valid. Write the numbers the user chooses, not a default from elsewhere.

When nobody defining this work can say what goes wrong for this kind of work, say so and get the knowledge before writing criteria. Ask the user to try three systems that already do it and report what they do, or to name someone who has built one. Read the public documentation of those systems and the law or policy that governs the work. Or reduce the work to calling a service that already solves it.

## 5. Fold in what constrains or enables the story

* **Keep the feature's constraints.** Read the `Constraints` and `Context` lines of the feature header or the epic. Write each constraint as a criterion on this story when this story could break it. Use the `Context` facts as given, and never copy a credential's value into a criterion.
* **Write a non-functional requirement as criteria here.** Security, a rate limit, pagination and alerting constrain how well this story behaves. A story does not close until they pass, so they cannot be dropped under schedule pressure.
* **Write an enabler as criteria here.** A new column, a change to what a consumer reads, or a service this story calls is real work nobody perceives alone.
* **Write a property as criteria on the story that introduces the behaviour.**
* **Write a flag as criteria** when the story merges before the feature is complete and exposes half of it: with the flag off, the person sees today's behaviour. The story that completes the behaviour gets a criterion that removes the flag.
* **Own the interface this story produces.** The story that defines an interface carries its contract as criteria. The story that consumes it refers to it.

## 6. Keep the standards out of the criteria

Apply one test to each candidate: could a reasonable person choose the opposite outcome, and would the user notice the difference? Both yes makes it a criterion. Otherwise it is an engineering standard, it applies to every story, and it belongs in the repository's instructions file and in whatever runs on every change.

Standards are the developer's to find and hold, not the user's to approve. Trace each piece of input this story adds to whatever interprets it as instructions: a query, a shell, a template, a parser. List each of those crossings on the story's `Crossings` line. The `make-rule` skill finds the standard defence for each and enforces it, and this skill writes no criterion for it.

## 7. Open decisions

* **Ask the named owner before ruling.** When a value has an owner, put the question to them. Never settle it by counting documents. Three documents against one lose to the owner's current answer.
* **Read the live source.** Fetch the requirements document again before ruling from it. Delete a saved copy once it is stale.
* **Mark an undecided value as undecided.** Head the section **PROPOSED, NOT AGREED**, or say that an example value is only an example: "`unsupported_unit` is invented for illustration. Do not treat that string as specified." Never write an open decision into a story as settled.
* **Put the question on this story.** Write it as a comment on the story it blocks and list it under `Open`. It never gets a ticket of its own.
* **Check a qualifier before claiming it.** When the requirements scope the work to "validated" or "approved" items, find who ran the validation. When nobody did, write that on the story.

## 8. Write the card

Write each card for a reader who has seen none of this work and reads only the top of each section.

* **Write the card where the stories live.** On the tracker the `Backlog:` line of `AGENTS.md` lists, criteria go in the field its `Criteria:` line names, else at the top of the description. With no tracker, or when it cannot be written, give the card as text.
* **Open the description with the outcome and why the story is needed.** Follow the template order: Outcome, Why, Scope, Criteria, Open, Crossings.
* **Title the observable outcome.** "Add the status column" is a work order. "An unconvertible reading shows apart from one never checked" is a story.
* **Spell out every acronym on first use.** Put the point of each section in its first sentence.
* **Keep the description to the work.** Put rationale, ordering, review objections and provenance in comments.
* **Leave tracker fields out of the prose.** Assignee, status and estimate have fields, and prose copies go stale. Name a discipline when it matters: "a clinician sets these, not an engineer".
* **Link completed work instead of restating it.** Check that a ticket marked done was delivered. A one-line pointer, an empty description or an unmet criterion is not delivery.
* **Create no sub-tasks.** The steps inside a story are its test table rows, and the builder works from those.
* **Use at most one coloured block per card.** Bold does ordinary emphasis.
* **Say when a card is large.** Folding criteria in can make a card long. State that trade on the card.
* **Be brief.**
* **Never edit another person's comment.** Find a comment by its author and its content before updating it, never by which is newest.

## 9. Ready check

Check the story against these before handing it on. A no returns the work to the section that produces it.

* Every criterion names what a person sees, in values a stranger could check.
* Every criterion is written from the observer's side.
* No criterion contains a banned word from section 2.
* The story has its outcome criterion plus the boundary, failure and abuse criteria that apply to it.
* Every failure path from section 3 that can happen has a criterion or a written non-goal.
* Every abuse path from section 4 that matters has a criterion with a number in it.
* Nothing in the criteria is a standard nobody would choose against.
* The story leaves a person able to do something they could not do before.
* The story covers one workflow step and one variation, and has no more criteria than the number per story `AGENTS.md` states; ask the user for the number once when it is missing. When it covers more, say it is several stories and hand it to `story-map`.
* Every undecided value is marked undecided and names who decides it.

## 10. Review a story

Run the section 9 check against a story or criteria someone else wrote, whether a colleague, a PRD, a ticket or another agent. Change nothing without the owner agreeing; each gap is their decision. Read every comment on the card first, and list each answer not yet folded into the description. Report in this order, quoting the text each finding is about.

* **Cannot be tested:** no observable result, a banned word, a limit with no number, or an assertion on a database row or an internal call. Say what it would have to say instead.
* **Missing:** each failure or abuse path that can happen here and has no criterion. Ask for a criterion or a non-goal line, and say what a builder would otherwise decide alone.
* **Two things in one:** say which two criteria it becomes.
* **A standard rather than a criterion:** say where it belongs instead.
* **Settled without the owner:** an undecided value written as decided, or a comment answer that contradicts the card.
* **Unclear rather than wrong:** "quickly", "the usual limit". Ask for the number.

```text
Unanswered:        "<quoted comment>" -> <what in the card it changes>
Cannot be tested:  "<quoted text>" -> <what it would have to say instead>
Missing:           <failure or abuse path> -> <what a builder would otherwise decide alone>
Two things in one: "<quoted text>" -> <A> / <B>
A standard:        "<quoted text>" -> <where it belongs instead>
Settled early:     "<quoted text>" -> <who decides it>
Unclear:           "<quoted word>" -> <ask for the number>

Ready to build.        (or: 3 blocking items.)
```

## What this skill does not do

Splitting a feature into stories, and judging whether a card should be a story at all, is `story-map`. Choosing which ready story to build next is `next-story`. Answering an unknown by writing throwaway code is `spike`; do that when a criterion cannot be written because a fact about the world is missing, such as a throughput number or what an API actually returns.
