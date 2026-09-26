# Review work the user made

Loaded by the `reviewing` skill when the subject is code, a test, a design, a plan or a fix idea the user made and wants an opinion on.

## Find the Subject and Its Job

* **The subject** is the thing the user just wrote or said: the last chat message, a file they name, a diff, a document. When it is ambiguous which, ask once.
* **Its job** is what it must do: the behaviour the code must produce, the decision the document must support, the bug the fix idea must remove. Take it from the acceptance criterion or the test that states it; when neither exists, take it from the conversation or the document's own opening. When nothing states it, ask one question and wait.
* **The ground,** beyond the code the subject lands on: an implementation idea is checked against what the codebase already has, a document's claims about the system against the system, and a design for a system that does not exist yet against the constraints the user has stated.

## Sort Every Point Into One Tier

* **Wrong.** It does not do its job, or will stop doing it under an input or a load the job includes. Give the concrete failing case: the input, the sequence, the caller. For an idea, the case it does not cover or the cause it does not remove.
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

The writing rules `reviewing` loads apply. The words subject and job stay out of chat; a tier name is one word at the start of its point. Stop when the points stop: no summary, no encouragement, no offer to rewrite.
