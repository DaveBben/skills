# <feature_name> — build plan

**Disposable.** Delete once the code is complete and the last slice has landed. Architecture decisions live in `docs/adr/{slug}/`.

It answers *how*. The spec answers *what* and *why*, and is not repeated here beyond a link. Short and readable. No code snippets. Prefer a diagram to a paragraph wherever the paragraph is describing a shape. 

Written for somebody who has not been in the conversation. One voice throughout, present tense. Every table takes the example row as the depth expected of it.

```
# <feature_name> — build plan

*(Instruction to Agent: Delete all italicized instructions when filling out this template.)*

**Disposable.** Delete once the code is complete and the feature flag is removed. Architecture decisions live in `docs/adr/{slug}/`.

---
## 1. Problem & Context
Two or three sentences. 
* **Spec Link:** [Link to the Feature Spec]

## 2. Glossary (Extensions)
Only what this document adds: the type names, the states, and any word this document uses in a narrower sense than the spec does. Link the spec's glossary rather than repeating it. One sentence each, one example.

## 3. Current Architecture
What is in the area now: modules, what each owns, and what rules already constrain them. Name the exact file and symbol (function/class) where a rule lives.

## 4. Spec Validation (Spike Results)
Every Spec row (Acceptance Criteria & Constraints), re-verified against the reality of the codebase. No row omitted.

| Spec Ref | Verdict | Notes |
|---|---|---|
| AC-2 | broken | the failure path triggers a database lock; measured at 400ms delay |
| Constraint 1 | holds | |

*(Verdict is one of: `holds`; `broken to <failure path>`, with measured number; `corrected to <row>`; `dropped`, with what removed the premise; `settled`, with what answered it. Anything the survey found that the spec never mentioned gets a row marked as such.)*

## 5. Proposed Architecture (The Shape)
The mechanism, where it sits, what it stores, and how it behaves when its dependencies are unavailable.
* **Rules:** Which mechanisms become guardrails or architectural tests.
* **Assumptions:** What must stay true. Mark anything UNMEASURED.

### 5.1 Diagrams
*(Diagrams must be in Mermaid or PlantUML format. Coarse first, one level at a time.)*
* **The Module Map:** The modules in the path, what each owns, which way dependencies run, and the data contract at each boundary.
* **The Type Map:** The classes and interfaces this change adds or reshapes, the methods and fields that matter. Mark what is new.
* **State Diagram:** Only where this change introduces a lifecycle.

## 6. Dependencies & Libraries
Every capability this change needs and what provides it. The standard library is the default, so a row exists to justify leaving it.

| Capability | Provided by | Version | Why not the standard library? | Cost to remove |
|---|---|---|---|---|
| HTTP client | httpx | 0.27.x | pooling and HTTP/2, both measured as needed | one adapter class, isolated in external/http.py |

*(A row that cannot answer the fourth column is a dependency nobody needs yet. Name the transitive weight where it is large.)*

## 7. Test Checklist (The Build Contract)
Every Acceptance Criterion, Constraint, seam, and failure path must land here as a testable assertion. The build loop iterates until every row is checked `[x]` and passing.

| Status | Test ID | Type | Origin (Ref) | Falsifiable Assertion (What the test must prove) |
|---|---|---|---|---|
| `[ ]` | `T-01` | Example | AC-1 | Assert that a valid payload returns `201 Created` and writes exactly one row. |
| `[ ]` | `T-02` | Property | Constraint-2 | Assert that generating 1,000 IDs yields zero collisions and strictly alphanumeric characters. |
| `[ ]` | `T-03` | Integration | Seam (Stripe API) | Assert that firing a checkout emits exactly one `HTTP POST` to the Stripe mock with the correct total. |
| `[ ]` | `T-04` | Example | Failure Path | Assert that a mocked database timeout (`504`) triggers an immediate `429 Too Many Requests` to the caller. |
| `[ ]` | `T-05` | End-to-End | Entire Feature | Assert that a headless client can load the route, submit the form, and reach the success view. |

*(Type: `Example`, `Property`, `Fuzzing`, `Integration`, `Budget`, or `End-to-End`. Origin: AC, Constraint, Seam, or Failure Path.)*

### Known Permanent Gaps
*(List any hazards accepted without a detector, or constraints/ACs explicitly marked `no test` with the specific ADR that justifies the gap.)*
* TBD

## 8. Rollout Plan
* **Feature Flag:** [Name of the flag mechanism] — How this is hidden during the BUILD phase and widened during the SHIP phase.
* **Deployment Order:** [e.g., Run migrations -> Deploy backend -> Enable flag -> Deploy frontend].

## 9. Open Questions
What is still unsettled, and what each would amend.

## 10. Not Applicable
Whole areas that are structurally zero here: storage, concurrency, rollout, reversibility, security, privacy, and anything else the shape makes unreachable. Say *why*, not just that it is excluded.

---

## 11. Pre-Deletion Checklist
**Do not delete this file until:**
- [ ] Every row in the Test Checklist is marked `[x]` with a passing test in the repository.
- [ ] Every "no test" gap or accepted hazard is documented in an ADR.
- [ ] Every open question is closed or promoted to an ADR.
- [ ] Every measurement in this file is inside the ADR that rests on it.
- [ ] Every module this change added or re-scoped says what it owns in its docstring.
- [ ] Every glossary term still in use is carried by the code that owns it (name/docstring).
- [ ] Every boundary the shape diagrams introduced has a contract in the architectural tests.
- [ ] Every dependency row that survived is pinned in the project manifest.
- [ ] Anything this file defers to later lives somewhere that outlives it.
```