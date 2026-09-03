# Worked example: PRD → spec → slice → tests

A single small feature carried end to end, to show how each artifact hands a
specific thing to the next. Read in order.

| File | Answers | Hands down |
|---|---|---|
| [01-prd.md](01-prd.md) | What and why | Requirements, non-goals, success metrics |
| [02-spec.md](02-spec.md) | How | Seams, invariants, rejected alternatives |
| [02b-spec-xp.md](02b-spec-xp.md) | How, XP-style | The same feature, decisions and consent only — fewer choices made upfront |
| [02c-adrs-and-slice.md](02c-adrs-and-slice.md) | How, with no spec at all | Two ADRs, one spike finding, and straight to slice 1 |
| [03-vertical-slices.md](03-vertical-slices.md) | In what order | An observable outcome per increment |
| [04-slice-2-tests.md](04-slice-2-tests.md) | How we know it works | 23 test headers and the rule that produced each |
| [05-definition-of-done.md](05-definition-of-done.md) | How we know we are finished | Three gates: slice done, feature complete, feature successful — five checks, four of which are not requirements |

## The mechanism

The artifacts are not prose handoffs. **Each one generates a different class of
test**, which is what makes the chain executable rather than decorative.

| Artifact | Section | Test class it generates |
|---|---|---|
| PRD | Success metrics | Acceptance test, plus the event that feeds the metric |
| PRD | Functional requirements | One acceptance test per FR |
| PRD | Non-goals | No test. A guard used to reject slices |
| Spec | Seams | Integration tests — at least one per boundary, one per obligation |
| Spec | Invariants | Property tests |
| Spec | Cross-cutting concerns | Integration tests for authz and privacy |
| Spec | Rollout | One E2E smoke test on the critical path |
| Implementation | Branches written | Unit tests |
| Spec | Untrusted parsers | Fuzz targets — none in this example, and that is the correct answer |

## Three things this example is built to show

1. **Slice 1 delivers no requirement.** It is observable but not valuable, and
   it is still the right first slice, because it retires structural risk while
   failure is cheap.
2. **Test counts fall out of generators, not checklists.** Seams, type value
   spaces, cardinality, and both-sides authorization produced 17 of slice 2's
   23 tests without anyone recalling a failure mode. The other six trace to
   other sections — FR1, the spec's invariants, its cross-cutting concerns, the
   PRD's metrics — and the example says so rather than pretending one rule
   explains everything.
3. **Writing tests surfaces product gaps.** All four questions in the PRD's
   open questions section were discovered while writing slice 2's assertions,
   not while writing the PRD. A fifth was dissolved by a design change instead
   of escalated.

A fourth thing, visible only if you count: **slice 2 is not a pyramid.** It has
more integration tests than unit tests, because it is the slice that first
connects real components. The pyramid is a property of a finished suite, not of
every slice.

And a fifth, in [05](05-definition-of-done.md): **completion and success are
different gates on different clocks.** A feature can be complete and still fail
its metrics two months later. Enumerate completion at the level of
requirements, which are stable while you build — not at the level of tests,
which are not.

## Three specs on purpose

`02`, `02b` and `02c` describe the same feature at three levels of upfront
design. There is a genuine tension between writing a design document and XP's
position that design should emerge from implementation, and the example would
be dishonest if it taught only one side.

| Version | Upfront design | Right when |
|---|---|---|
| `02-spec.md` | Full | Several teams, outside reviewers, no safety net |
| `02b-spec-xp.md` | Decisions and consent only | One team, but outside approvers |
| `02c-adrs-and-slice.md` | Two ADRs, then code | One team that reviews its own work |

Two rules separate them:

- **Reversibility, not phase.** Design upfront only what is expensive to change
  later. A class boundary is cheap; a job queue you must run forever is not.
- **Medium, not length.** XP's real move is not a shorter document. It is
  putting every obligation that can be executed into a test, and writing down
  only what cannot: a decision, a rejected alternative, an accepted hazard.

Feature and figures are fictional.
