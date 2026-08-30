# Spec

`docs/spec/{slug}/spec.md`. Written at the spec stage, delete once the code is complete.

It records the problem, not the solution. No mechanism, no module names, no data models. Those belong in the design document. Finished when the constraints have origins, the unpriced adjectives are named, and the open questions are marked unsettled.

Written for somebody who has not been in the conversation. One voice throughout, present tense, describing the system rather than the plan: "callers over the cap get 429", never "we will add a cap". Every table takes the example row as the depth expected of it.

```
# <feature_name> spec

*(Instruction to Agent: Delete all italicized instructions and example rows when filling out this template.)*

**Disposable.** Delete once the code is complete. Architectural decisions live in `docs/adr/{slug}/`.

---

## 1. Need & Success
*(State the single-sentence core need from the Idea phase.)*

* **Target Outcome:** *(The measurable change in user behavior or business health that proves this solved the problem, e.g., "Reduce manual export tickets by 80%".)*

## 2. Glossary
*(Use a table. Every term that carries a specific meaning here, in the words the user uses. Include anything the request used loosely, and anything two people have turned out to be using differently.)*

| Term | What it means here | Example |
|---|---|---|
| Delivered | The mail server accepted the message, not that anyone read it | accepted 14:02, message-id 8f21c |

## 3. Functional Requirements
*(The observable behaviors the system must exhibit. Target 3-8. Every requirement must tie directly back to the user need and delegate its testable proof strictly to the AC Ref.)*

| Requirement | Why it is needed | AC Ref |
|---|---|---|
| Lock account after consecutive failed logins | Mitigate automated credential stuffing attacks | AC-1, AC-2 |
| Reject payload if `user_id` is missing | Prevent orphaned records in the ledger database | AC-3 |

## 4. Acceptance Criteria
*(Observable from outside. Target 10-25. Use the Given/When/Then structure. Each must name exactly how it is observed so the Design Document's Test Checklist can disposition it.)*

| ID | Given (Context/State) | When (Action/Trigger) | Then (Outcome) | How it is observed |
|---|---|---|---|---|
| AC-1 | a user has 4 failed login attempts | they submit a 5th failed attempt | the account state changes to `locked` | `users` table reflects locked state, UI displays lock banner |
| AC-2 | a user has 4 failed login attempts | they successfully log in | the failure counter resets to `0` | counter in the session store drops to `0` |
| AC-3 | an incoming API payload | `user_id` is null | the system rejects the payload | API returns an HTTP 400 response |

## 5. Constraints
*(Numbers with origins. An adjective is not a constraint. Record each number at the value somebody committed to, not a round number near it.)*

| # | Constraint | Who or what enforces it | Origin | What breaks if it is wrong |
|---|---|---|---|---|
| C-1 | p95 under 200ms at the API boundary | the caller times out at 250ms | measured 2026-08-15 | caller drops the request and retries, doubling load |

*(Origin must be: raised by user; proposed by you and confirmed; lifted from [document/date]; or measured [date/what was measured]. The last column is the bar for being here at all. A row that cannot name what breaks is a preference; leave it out.)*

## 6. Unquantified Adjectives
*(Use a bulleted list. Every word from the request that sounds like a limit but carries no number, e.g., "fast", "scalable", "seamless". For each: state which constraint replaces it, or explicitly mark it as `[UNQUANTIFIED]`.)*
* TBD

## 7. Hazards
*(Use a bulleted list. Each hazard must be resolved to a criterion, designed out with a written reason, or explicitly accepted without a detector. "Accepted without a detector" requires an ADR via the `adr` skill.)*
* TBD

## 8. Open Questions
*(Use a bulleted list. Everything here is unsettled. Each names the fallback that applies absent an answer.)*
* TBD

## 9. Out of Scope
*(Use a bulleted list. Raised and excluded, with what excluded it. Say whether the list is complete.)*
* TBD
```