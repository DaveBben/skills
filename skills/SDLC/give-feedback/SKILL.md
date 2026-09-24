---
name: give-feedback
description: "Use this skill whenever the user wants feedback on something they made or proposed: code they wrote by hand, a test, a diff, a design or architecture document, a data model, a brainstormed approach, their idea for a bug fix, their idea for an implementation, or a plan they just typed into chat. Use it on: 'give me feedback', 'what do you think of this', 'review what I wrote', 'how could I have done this better', 'critique this', 'poke holes in this', 'is this a good approach', 'here is how I would fix it, thoughts?', 'here is my design', 'rate my code', 'what am I missing'. Use it at any stage, from a half-formed idea in chat to a committed diff. Ground every point in the code or the source it concerns, sort it into what is wrong, what is unverified, what could be shaped better, and what is only taste, name the principle behind each, and leave the rewrite to the user. Do not use it to review agent-generated code before a merge; that is `review`. Do not use it to build the thing; that is `execute`."
license: MIT
compatibility: any-agent
metadata:
  version: "1.1.0"
---
# Give Feedback

## Find the Subject and Its Job

* **The subject** is the thing the user just wrote or said: the last chat message, a file they name, a diff, a document. When it is ambiguous which, ask once.
* **Its job** is what it must do: the behaviour the code must produce, the decision the document must support, the bug the fix idea must remove. Take it from the acceptance criterion or the test that states it; when neither exists, take it from the conversation or the document's own opening. When nothing states it, ask one question and wait.
* **Read the ground before judging.** When the subject touches a repository, read the code it names and the code it will call. A bug-fix idea is checked against every caller of the function it changes. An implementation idea is checked against what the codebase already has. An architecture document's claims about the system are checked against the system. A design for a system that does not exist yet is checked against the constraints the user has stated. Never assess from the subject's own description of the code.
* **When the ground cannot be read,** say which file or symbol is missing and give only the points that stand without it. Do not assume what the unread code does.

## Sort Every Point Into One Tier

* **Wrong.** It does not do its job, or will stop doing it under an input or a load the job includes. Give the concrete failing case: the input, the sequence, the caller. For an idea, the case it does not cover or the cause it does not remove. Never assert wrongness without a case.
* **Unverified.** It rests on a fact neither the user nor the agent has checked: what a library does, what a caller passes, what the data holds, how often something happens. Name the fact and how to check it. Do not guess the answer.
* **Shape.** It works, and there is a cleaner form. Name the principle, say what the cleaner form buys, and say what goes wrong later without it.
* **Preference.** The agent would have done it differently and neither form is better. Say "preference" and move on. Never dress taste as a defect.

Order the reply: Wrong, then Unverified, then Shape, then Preference. All of Wrong and Unverified. One or two Shape points, ranked; keep the rest for the next round. Preference only when asked.

## Reply Template

```text
<What is right: one line, only for a real choice they made. Omit it when nothing stands out.>

Wrong — <the finding in one line>
<what the code does now, then the failing case: input, sequence, caller>
<what it must do differently>

Unverified — <the unchecked fact>
<how to check it>

Shape — <the finding in one line>
<the mechanism, before any verdict>
<the principle by name, what the cleaner form buys, what it costs>

Preference — <one line, only when asked>
```

## Make It Teach

* **Lead with what is right,** only for a real choice they made. Never manufacture praise.
* **Explain the mechanism before the verdict.** "This function returns a value and mutates its argument" lands before "split it in two". "Two requests both read the count as 2 and both write 3" lands before "racy".
* **Name the principle** behind every Shape point, from the real catalogue: the SOLID principles, Fowler's refactorings and code smells by their catalogue names, Beck's four rules of simple design, the Law of Demeter, Command-Query Separation, Tell Don't Ask, connascence, parse-don't-validate, make-illegal-states-unrepresentable, YAGNI, DRY and its misuse. Cite only what is certain, by author and work. Never invent a page number, a URL or a quotation. When unsure who formulated it, say so.
* **Give the cost with the rule.** What following it costs as well as what it buys, and when to ignore it.
* **Ask before telling when the answer is reachable.** "What happens here when the list is empty?" beats "this crashes on an empty list." One question per point, and only when the user can answer it from what is in front of them.
* **Match their level.** When they have said they have not seen a pattern before, explain it before naming it. Ask their level once, only when the subject shows a pattern they may not know.

## Leave the Rewrite to Them

* **Describe the change; write it only when asked.** A code block appears when the user asks for one, or when the change is under five lines and the description would be longer than the code.
* **When they ask for the answer,** give it, explain every line, and say what to look for next time.
* **Review only what they made.** The code around it is ground, not subject, unless they ask.
* **Second round.** When they come back with a revision, review the revision against the same job, say which points it closed, and raise the Shape points held back from the first round.

## Communication

* **A fact stands alone.** Do not explain why finding it matters.
* **No contrast frames.** State what the code does; do not frame every point as "X, not Y".
* **Use the user's words for the subject.** The names in this skill (subject, job, tier) stay out of chat.
* **Full sentences.** No headline fragments in chat. The tier name is one word at the start of the point.
* **Stop when the points stop.** No summary, no encouragement, no offer to rewrite.
