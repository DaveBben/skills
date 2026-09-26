# Review an existing epic

Loaded by the `reviewing` skill when the subject is an epic, a PRD's breakdown or a story list someone else wrote. A card is one ticket on the tracker: a story, a spike, or something filed as one.

The rules an epic is judged against live in the `define-work` skill: its ready check, its table of what each kind of card is (story, spike, non-functional requirement, enabler, property, task, decision), its size rule and splitting patterns, and its blocker rules. Run the `define-work` skill against the epic; its section "When `reviewing` asks for a check" applies them and returns the gaps. Do not restate those rules here or judge from memory of them. When `define-work` is not installed, stop and tell the user it is needed to review an epic.

## Before judging

* **Change nothing without the owner agreeing.** Each gap is their decision.
* **Read every comment on every card first,** and list each answer not yet folded into the card it answers.
* **Check each subagent finding against the source** before reporting it.
* **Run the `story` skill's review on each story that already has criteria,** for findings inside it.

## What to report

Report these first, quoting the text each is about.

* **No shared understanding:** the epic states no outcome a person would notice, no success signal, or no non-goals.
* **Not a story:** a card `define-work` would not give a card of its own: a non-functional requirement, an enabler, a property, a task or a decision. Say which story it folds into.
* **Too many cards:** siblings `define-work`'s ready check reports as one story. Search the siblings for one distinctive sentence. The number of cards containing it is the number to merge. Other signs are two decision tickets asking the same question, a spike mostly belonging to another epic, and a plan that needs its own guide to reading the cards.
* **Ships nothing:** a story that leaves no person able to do something new, or that is larger than `define-work`'s size rule allows.
* **Wrong blocker:** a link in the wrong direction, a story shown ready whose blocker was dropped with a closed ticket, or a hardening story blocked by the story it hardens.

```text
Unanswered:      <card> "<quoted comment>" -> <what in the card it changes>
No shared understanding: <the missing line> -> <the question to ask the owner>
Not a story:     "<quoted title>" -> <kind> -> criteria on <story>
Too many cards:  <cards> -> <shared sentence, hit count> -> one story
Ships nothing:   "<quoted title>" -> <what a person still cannot do, or the boundaries crossed>
Wrong blocker:   <story> -> <what blocks it in fact>

Ready to build.        (or: 3 blocking items.)
```

## Deleting cards

When the owner agrees to delete cards, archive every one in full first. Extract each comment a named person wrote on those cards and search the surviving cards for a distinctive phrase from each. A note saying content moved is not evidence that it did. Then search the surviving cards for every deleted key. The tracker removes links to a deleted card and leaves its key in prose. Rewrite each mention to describe the thing it named.
