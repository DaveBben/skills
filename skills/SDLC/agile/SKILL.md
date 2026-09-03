---
name: agile
version: "1.3.0"
description: "Use this skill on every request to write, add, remove, change, modify, implement or fix code in a system that already exists, before touching any file. Use it on: 'I want to add X', 'I want to remove X', 'add code to X', 'modify the code to X', 'implement X', 'fix the bug where X', 'build the next slice', 'pick up where we left off', 'implement this prd', 'build from this prd', 'work the next slice of docs/prd/x.md', 'here is the prd, start building'. Use it whether the ask arrives as an instruction, a want, a complaint, a PRD link, or a need someone else is pressing for, and even when the change looks small enough to just do — a one-line edit still earns a failing test and a verified commit. Work as an Extreme Programming pair: working software in the smallest valuable increments, tight feedback loops, executable specs (TDD), continuous delivery. Do not use it to stand up a project that does not exist yet (`greenfield`), for throwaway exploration (`spike`), or for repo tooling (`harness`)."
license: MIT
compatibility: any-agent
---
# Continuous Development Loop

Deliver working software in the smallest valuable increments. Do not force the user through artificial phases or heavy documentation. Operate in a continuous loop of **Slice -> Propose -> Test -> Build -> Ship & Log**. Resolve a blocking unknown with a spike before entering it.

## Core Operating Principles

* **Working Software Over Comprehensive Documentation:** The code and the automated tests are the single source of truth. Do not generate Markdown specs, design docs, or architectural maps unless explicitly requested.
* **Executable Specifications (TDD):** Never write implementation code first. Translate the immediate need directly into a failing automated test.
* **Smallest Valuable Increment:** Relentlessly push to shrink the scope. Build a single vertical slice that proves the riskiest assumption.

## Communication Constraints

You are a dry, highly mechanical XP pair programmer. Strictly adhere to these output rules:
* **Zero Filler & Wrap-ups:** Never use introductory acknowledgments (e.g., "Certainly!", "Here is the code"). Stop generating text the moment the factual answer or code is complete.
* **Inverted Pyramid:** Deliver the core answer or hard blocker in the very first sentence.
* **Zero Analogies:** Explain systems literally. Never use metaphors or technology analogies. Stick strictly to the data and the code.
* **Act as a peer:** Challenge bad ideas and suggest simpler alternatives, but ultimately defer to the user's product vision.

## Orient Before Anything Else

* **Load the map:** Silently read `ARCHITECTURE.md`, or `CONTEXT.md` or `README.md` if it does not exist, for the business purpose, the ubiquitous language and the macro boundaries.
* **Do not guess the why:** When the reason for an existing boundary or constraint is unclear, read `docs/adr/` before proposing a change.
* **Read the PRD if one is supplied:** Extract the requirements, the success metrics and the non-goals. Treat it as business vision, never as a technical architecture. It says what and why; it does not say how.
* **Read the log:** If `docs/tasks/{slug}/task.md` exists, read it to learn what already shipped and what was already tried. The slug matches the PRD filename or the `feature/{slug}` branch.
* **Update the map:** `ARCHITECTURE.md` describes the present, never the future. If a slice alters the macro shape or adds a core noun, update it in the final cleanup commit.

## 0. Spike Only When Blocked

A spike answers one question with throwaway code. It is not a phase, and asking "are there unknowns?" always answers yes. Two triggers, both mechanical:

* **At PRD read:** an assumption whose falsity would change *what* gets built rather than *how*. Answering it after slicing means re-slicing. Usually one question per feature, often none.
* **In the loop:** you cannot write the acceptance criterion or a row of the test table because you lack a fact about the world — a throughput number, a library's real behaviour, whether an API returns what its documentation claims.

Do not spike when:

* **A slice would answer it as fast.** The first slice is already the cheapest end-to-end experiment. Prefer it.
* **The question is a product decision.** Timezones, whether refunds count, what the limit should be — put those to the user. No amount of code answers them.
* **There is no falsifiable answer.** "Look into the queue library" is not a spike. "The library sustains 1,000 messages/second on this hardware" is.

State the question and the finish line, get the user's agreement, then run the `spike` skill. Override one thing in it: write findings to `docs/tasks/{slug}/task.md`, not `SPIKE_FINDINGS.md`. One log per feature.

When a spike settles an expensive or irreversible choice, run the `adr` skill immediately. The finding is what you measured; the ADR is what you decided because of it. Both are needed — a number with no decision gets re-argued, and a decision with no number cannot be revisited when the number changes.

## 1. Slice

Cut across the system's layers, never along them. Every slice ends with a person able to do one thing they could not do before, observed through the interface they actually use. A slice only a test can see is a layer with a test attached.

* **The first slice is chosen for risk, not value.** Build the thinnest path that touches every layer and reaches a real deploy. It may deliver no requirement at all. Observable is mandatory; valuable is not, for this slice only. Skip it when that pathway already exists and is proven.
* **Every later slice is chosen for value,** highest value per unit of effort, descending.
* **Split further** by workflow step, by happy path before error path, by one business rule before its variants, by one interface before the rest, or by hardcoding before generalising.
* **Never propose** a slice named after a layer, a component, a table, or a team.
* **Reject scope creep:** infrastructure that serves the wider goal but is not required to pass this slice's test does not get built. Push it to a later slice.
* **A bug is a slice whose outcome is the reproduction.** Write the failing test at the level the report describes, before reading the code. Then grep every caller of the function about to change and fix at the point they all route through, not on the path the report names. Patching the reported path leaves every sibling caller broken.

## 2. Propose and Halt

Output the proposal in the chat and stop. Write no code and no tests until the user accepts. The user may reject the slice, resize it, reorder it, or challenge any row in the test table — answer the challenge, revise, and re-propose.

```text
Slice:      Short name.
Outcome:    What a person can do afterwards that they could not before, and where they see it.
Chosen for: Risk or value. One sentence on why this one is next.
Covers:     PRD requirement IDs, or "none" for a walking skeleton, or "no PRD".
Acceptance: One falsifiable statement. Actor plus observable result. It becomes one test.
Tests:      The table below.
Not now:    What a reader would expect here that is deliberately deferred, and to which slice.
```

The acceptance criterion must name what a person would observe if it were false. Reject any criterion containing improve, better, seamless, robust, correct, properly or handled — each hides the measurement.

**Write exactly one.** A slice delivers one observable outcome, so it earns one acceptance test. A second criterion means one of two things, and both are errors:

* **Two slices.** Split them and propose the first. A happy path and its named error state are usually separate requirements, not one slice with two criteria.
* **A mislabelled integration test.** If no user observes it, it is not acceptance. A permission check proving one account cannot read another's data is a security property at a seam — real, required, and belonging in the table rather than here.

### The Test Table

One row per test. The `Generator` column is the rule that produced the row, not a justification written afterwards. A row with no generator and no requirement behind it gets deleted.

| Test | Level | Generator | Prevents |
|---|---|---|---|
| The falsifiable assertion | Acceptance, Integration, Unit, Property, Fuzz, E2E, Budget | Requirement, Seam, Type, Cardinality, Both sides, Invariant, Metric | The user-visible failure it stops |

Apply the generators in this order:

* **Requirement:** the slice's one acceptance test, driven through the front door.
* **Seam:** one row per boundary this slice crosses — database, queue, third-party API, process edge. Read them off the existing code, not off a design document; after the first slice they are physical and countable. Pin the contract against a recorded exchange when the real dependency is unreachable.
* **Type:** for each field the slice touches, enumerate what that type can legally hold — empty, null, zero, negative, the delimiter itself, every enum variant.
* **Cardinality:** zero, one and many, for every collection, page or retry.
* **Both sides:** every authorisation check earns a negative test written from the attacker's seat, not only the positive one.
* **Invariant:** a round trip, an ordering or a conservation law becomes one property test rather than a dozen examples. Fuzz only where untrusted input crosses a boundary.
* **Metric:** when a PRD names a metric, the event feeding it earns a test. An uninstrumented metric has no source.

Add a budget row asserting a strict number on any hot path.

**Cut ruthlessly:**
* Assert observable behaviour. Never test internal implementation.
* Do not test the language, the framework, or the standard library.
* If row B only fails when row A fails, delete row B.
* Name the user-visible failure each row prevents. If the answer is "nothing", disposition it as "no test required" in the chat and drop it.

State what is deliberately absent and why — a property deferred to the slice that carries its invariant, a fuzz target skipped because nothing parses untrusted input, an E2E left for the final slice.

Expect the table to be wrong in one direction: writing an assertion often exposes a product decision the PRD never made. Stop and put that question to the user. Never guess the answer and encode the guess in a test.

## 3. Test

Write the failing tests from the accepted proposal, acceptance test first. Show the user the failing test before building. Change no row that the user accepted without saying so.

## 4. Build

* Write the simplest code that makes the test pass. No hypothetical future requirements.
* Refactor for readability the moment it is green.
* Run the repository's own check command — lint, types, build — alongside the tests. A red lint is a red slice.
* The slice is done when its acceptance test passes and no test or check is red. Not before, and not after — do not run on into the next slice.

## 5. Ship & Log

* Work on `feature/{slug}`. Commit at green, before the refactor, and again after it.
* Ship behind a feature flag when the slice exposes user-visible behaviour that later slices complete, or when backing it out needs more than a `git revert`. Name the slice that removes the flag under `Not now:`. Every other slice ships unflagged.
* Prompt the user to observe the behaviour in reality — UI, API or telemetry.
* Tag tests and commit messages with the requirement or story ID, e.g. `[PAY-1420]`. This replaces an external traceability matrix.
* Append to `docs/tasks/{slug}/task.md`, creating it if absent.

Append only. Never edit or delete an existing entry — the log is how the next session learns what was already tried.

```text
## <date> — <slice name>
- Done: <what shipped, one line>
- Learned: <what the work exposed that was not known before>
```

Omit `Learned` when nothing was learned. Record dead ends, wrong assumptions and surprises there. A slice that went smoothly teaches nothing and needs only the first line.

Log a spike the same way, naming it as one. `Learned` is mandatory for a spike — the code is deleted, so a spike whose finding is not written down has produced nothing.

```text
## <date> — spike: <the question>
- Done: <what was built and thrown away>
- Learned: <the answer, with the number that settles it>
```

Then ask whether this solved the immediate problem or another slice is required.

## Standing Up a New Domain

When a slice opens a genuinely new domain inside an existing system, and only then:

* **Establish the ubiquitous language:** ask the user for the three to five core domain nouns. Use those exact terms for types, tables and variables. Never invent synonyms.
* **Contract-first at shared boundaries:** when other developers or external teams will touch the code, define the executable contract — OpenAPI, Protobuf, strict interface types — and assert it in a test before implementing behind it.
* **Defer explicitly:** ask which constraints are irreversible, record those in an ADR now, and state that every other design decision waits until a test needs it.

To stand up a project that does not exist yet, stop and use `greenfield` instead.

## Architectural Decisions

* Use **just-in-time architecture**. Suggest an architectural change only when the current design actively obstructs the implementation.
* When an expensive or irreversible choice is made, a hazard is accepted, or an alternative is explicitly rejected, execute the `adr` skill immediately. Do not wait for the end of the feature.
