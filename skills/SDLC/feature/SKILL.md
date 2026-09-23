---
name: feature
description: "Use this skill whenever work has to be defined before any test or code exists: writing a user story, agreeing what done means, drafting or repairing acceptance criteria, or turning a PRD, a feature request, a complaint or a bug report into stories. Use it on: 'write the user story', 'what are the acceptance criteria', 'define this work', 'is this story ready', 'what does done mean here', 'what could go wrong with this feature', 'turn this prd into stories', 'make this testable', 'refine this'. Use it to review a feature someone else defined: 'review these acceptance criteria', 'is this story ready to build', 'what is missing from this spec'. Use it on any statement of work containing better, faster, robust, seamless, properly or handled, each of which hides the measurement. Produce one outcome sentence, one problem statement, and one Given/When/Then criterion per story, each observable through the interface the user actually uses, with the failure paths and the abuse paths enumerated, and every engineering standard nobody would choose against kept out of the criteria. Do not use it to enumerate the tests behind one criterion (`test-table`), to record a decision (`adr`), or to build the code (`agile`)."
license: MIT
compatibility: any-agent
metadata:
  version: "1.0.0"
---
# Feature

Agree what a person will be able to do, and how anyone can check it, before a test or a line of code exists.

Four words, used this way throughout:

* **Outcome:** one sentence saying what a person does differently once all of this ships.
* **Acceptance criterion:** one Given/When/Then that a person can pass or fail by using the system, without opening the code.
* **Story:** one acceptance criterion and the work that makes it true. A story ships on its own.
* **Feature:** one outcome, and the ordered stories that reach it. The whole set of criteria describes the outcome, and each single criterion is one story.

Everything here is agreed with the user. Propose, then wait.

```text
Outcome:   <what a person does differently once this ships, and where they see it>
Problem:   <who hits it, how often, what they do today instead>
Not doing: <one checkable non-goal per line>

1. <Title: what the person will be able to do, five to eight words>
   Given <a concrete starting state>, when <a concrete action>, then <what the person sees, with real values>
2. ...
```

## 1. Outcome

Write one sentence saying what a person does differently once this ships, and where they see it. Reject an outcome naming a component, table, endpoint or file, and reject one that contradicts a stated non-goal unless the user overrides it. "Verdicts land in the table" is true while the work is half done. "I open one list each morning and read from it" is not.

## 2. Why

Write who hits the problem, how often, and what they do today instead. The reason changes what done means. An email captured for a newsletter needs the owner's consent and a way to stop the mail; the same email captured for an internal list needs neither. When the user cannot say what the person does today, the work is not understood yet. Ask before writing criteria.

## 3. Who observes

The criteria are written in whatever the user of this feature can see. Decide which user that is.

* **A person** sees a screen, a message, a document, a file. Write the criteria in what appears there. A criterion that reads a database table asserts an implementation someone can change without the person noticing, and it passes while the screen shows an error.
* **A service** sees status codes, an error code in the body, and the response shape. Write those exact values into the criteria, because the calling code branches on them and cannot read a sentence. Add two criteria a person never needs: what a repeated identical request returns, since a caller retries automatically when a response is slow or lost, and what the response is when the caller sends a field of the wrong type. Where another team owns the caller, have them state what they depend on and run their expectations against the interface in the build.

## 4. Write the happy path first

Write the criterion for the case where everything works, as one Given/When/Then sentence in the domain's nouns with real values.

* **Use concrete values.** "When the visitor submits `a@b.com`" beats "when the visitor submits a valid email".
* **Ban the words that hide the measurement:** improve, better, faster, seamless, robust, correct, properly, handled, intuitive, flexible, scalable, modern. Replace each with the number or the observable event. "Faster" becomes "the list appears within 2 seconds of the click".
* **One Given/When/Then per criterion.** A criterion joining two outcomes with "and" is two criteria, and later two stories.
* **Name the interface.** The criterion says where the person acts and where they see the result, because that fixes what any acceptance test has to drive.
* **Use the domain's nouns.** When the work opens a domain this system has no words for, ask the user for its three to five core nouns and use those exact terms in every criterion, and later in types, tables and variables. Never invent a synonym for a noun the user already uses.

## 5. Generate the failure paths

Walk this list against the outcome. Each item that can happen earns its own criterion saying what the person sees. Each item is a decision only the user can make, and leaving it out means whoever builds it decides silently.

* **Empty or malformed input** at each field the person fills.
* **Input outside the limits:** too long, too many, too old, out of range. The limit is a number the user chooses here.
* **The same action repeated:** the person submits twice, or clicks twice, or the caller retries. Say what the second one returns.
* **Two of the same action at the same moment**, where the result depends on what already exists.
* **The action half completes:** something is stored and the confirming step never happens. Say how long that state lives and what clears it.
* **A thing the work depends on is unavailable:** the database, a third-party API, the network. Say what the person sees and whether anything was stored.
* **A step that takes unbounded time.** Say the limit and what the person sees when it passes.
* **The person abandons the flow** partway.

## 6. Generate the abuse paths

Ask one question of every input: who else can send this, and what do they gain by sending something the owner did not intend. The interface is reachable by any program, so a check that lives only in the page stops nobody.

* **Someone acts as another person**, using their address, their order, their identifier.
* **A program repeats the action in bulk**, thousands of times.
* **The response reveals something about a third party.** Answering "already registered" tells anyone whether a given person is on the list. Returning the same response for both cases is a product decision with a cost in clarity.
* **The feature sends something to an address the requester chose**, letting it flood a stranger's inbox or phone.
* **Personal data enters the system.** Consent, how long it is kept, and how the person removes it are each a criterion or an explicit non-goal.

Turn each one that matters into a criterion with a number in it: how many requests from one source in a minute, how many messages to one address in a day, how long a link stays valid. Write the numbers the user chooses, not a default from elsewhere.

When nobody defining this work can say what goes wrong for this kind of work, say so and get the knowledge before writing criteria: ask the person who has built one before, sign up for three systems that already do it and watch what they do, read the law or policy that governs it, or use a service that already solves it and reduce the work to calling that service.

## 7. Keep the standards out of the criteria

Apply one test to each candidate: could a reasonable person choose the opposite outcome, and would the user notice the difference? Both yes makes it a criterion. Otherwise it is an engineering standard, it applies to every story, and it belongs in the repository's instructions file and in whatever runs on every change.

Standards are the developer's to find and hold, not the user's to approve. For each technology the work touches, read the vendor's security page, the published checklist for that platform, and the product's past vulnerabilities. Then trace each piece of user input to whatever interprets it as instructions: a database reading SQL, a browser reading HTML, a shell reading a command, a file system reading a path. Each of those crossings has a standard defence. Enforce each by a framework default, a rule in the linter, or a check in the build, because a standard that lives only in a document gets forgotten.

## 8. Split into stories

Take the criteria from sections 4 to 6 and order them into stories, one criterion each.

* **Cut across the system's layers, never along them.** Every story ends with a person able to do one thing they could not do before, through the interface they actually use. Never name a story after a layer, component, table or team.
* **Choose the first story for risk:** the thinnest path touching every layer and reaching a real deploy. Observable is mandatory; valuable is not.
* **Hardcode everything the first story does not test.** Count the places the criterion crosses from one running piece into another: a database, a trained model, a queue, a third-party API, a container, a host. When more than one of those crossings is untried, the first story fakes all but one.
* **Order by the largest unknown answered first.** Split by workflow step, happy path before error path, one rule before its variants, hardcoding before generalising. Split any story crossing more than one of those boundaries, or more than one workflow step. No estimates.
* **Give a constraint its own story** when no other story can carry it: a throughput floor, a memory ceiling, a rule about where data may live. Its criterion is the number.
* **Make a story observable once deployed.** When it changes behaviour no test can see afterwards, such as a rate, a failure mode or which path the code took, the same story emits the event that shows it, and a criterion says that event fires.
* **Treat a bug as a story.** Its criterion is the reproduction: the starting state, the action, and what the person should see instead of what they saw.

## 9. Ready check

Check the result against these before handing it on. A no sends you back to the section that produces it.

* Every criterion names what a person sees, in values a stranger could check.
* No criterion contains a banned word from section 4.
* Each story has exactly one criterion.
* Every failure path from section 5 that can happen has a criterion or a written non-goal.
* Every abuse path from section 6 that matters has a criterion with a number in it.
* Nothing in the criteria is a standard nobody would choose against.
* Each story leaves a person able to do something they could not do before.

## 10. Review a proposed feature

Run the section 9 check against an outcome, a story list or criteria someone else wrote, whether a colleague, a PRD, a ticket or another agent. Change nothing without the owner agreeing; each gap is their decision. Report in this order, quoting the text each finding is about.

* **Cannot be tested:** no observable result, a banned word, or an assertion on a database row or an internal call. Say what it would have to say instead.
* **Missing:** each failure or abuse path that can happen here and has no criterion. Ask for a criterion or a non-goal line, and say what a builder would otherwise decide alone.
* **Two things in one:** say which two stories it becomes.
* **A standard rather than a criterion:** say where it belongs instead.
* **A story that ships nothing** a person can do, or that crosses more than one boundary from section 8.
* **Unclear rather than wrong:** "quickly", "the usual limit". Ask for the number.

End with one line: ready to build, or the count of blocking items.

## What this skill does not do

Enumerating the tests behind one criterion is `test-table`. Recording a choice and its tradeoff is `adr`. Building the code from these stories is `agile`. Answering an unknown by writing throwaway code is `spike`; do that when a criterion cannot be written because a fact about the world is missing, such as a throughput number or what an API actually returns.

The review here judges what was asked for. Judging how a diff was built, before it merges, is `review`. Judging code, a design or a plan the user wrote themselves is `give-feedback`.
