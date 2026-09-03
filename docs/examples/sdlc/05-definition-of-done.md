# How you know the feature is finished

> Learning example. The chain in this folder shows how a PRD becomes tests. It
> did not, until this file, say how you know you are done — which is the
> question every other artifact quietly assumes has an answer.

> **On the file split:** in real use these checks belong in the PRD's last
> section, not a separate document — every one of them is derived from content
> already in the PRD, and derived content that lives elsewhere drifts. They are
> split out here only so the reasoning has room to be explained.

## Three gates, not one

The most common mistake is asking one artifact to answer all three.

| Gate | Question | Answered by | Size | When |
|---|---|---|---|---|
| **Slice done** | Does this increment work? | Its acceptance test, plus a green suite | 1 test | Per slice |
| **Feature complete** | Did we build what was asked? | The checklist below | 5 checks | Once, before GA |
| **Feature successful** | Did it work? | The PRD's success metrics | 3 metrics | 60 days after GA |

Gate 3 can fail while gates 1 and 2 pass. You built exactly what was asked and
it did not move the number. That is a real and common outcome, and the PRD
should be amended when it happens rather than quietly forgotten.

## Gate 1: slice done

Beck's rule, and it needs no ceremony: **the story is done when its acceptance
test passes.** Executable, binary, evaluated on every commit.

| Slice | Done when |
|---|---|
| 1 | A CSV downloads from a real deploy behind the flag |
| 2 | `a signed-in user downloads a CSV containing their own transactions` passes |
| 3 | The round-trip property holds for merchant names containing delimiters |
| 4 | A date range constrains the export |
| 5 | An over-limit range returns `413` and no body |
| 6 | The flag is gone and the button works |

No checkbox list. The test runner already reports this continuously and for
free.

## Gate 2: feature complete

Five checks. They derive from the PRD's functional requirements, dependencies
and non-goals — none of which move while you build, which is what makes the
list stable enough to write down in advance.

| # | Check | Source | Also a requirement? |
|---|---|---|---|
| 1 | Every functional requirement has a passing acceptance test — FR1 download, FR2 date range, FR3 over-limit `413` | PRD requirements | **Yes.** One line, not three. A PRD with twelve FRs still has five checks |
| 2 | All four open questions are resolved, and each resolution is asserted by a test | PRD open questions — each blocks a Must requirement | No |
| 3 | The non-goals still hold: no scheduled export, no second format, no export-on-behalf-of, no API | PRD non-goals | No |
| 4 | Support's `manual-export` tag is deployed, and the `transaction_export` flag is removed | PRD dependency, plus slice 6 | No |
| 5 | `export.started`, `export.completed` and `export.failed` are emitting in production | The PRD's metrics have no source without them | No |

**Four of the five check things that are not requirements.** That is what the
gate is for. Nobody forgets to check whether the feature works; everybody
forgets to check whether a non-goal quietly became true. The requirements are
already a list of falsifiable statements — this gate is the protocol for when
they get evaluated, and what gets evaluated beside them.

**Check 3 is the one people skip.** Non-goals are usually treated as a planning
device and then never revisited. Read as a completion check, they catch the
scope that arrived during implementation — the small convenience endpoint, the
"while we were in there" JSON variant. If a non-goal is now false, either it
shipped without a decision, or the PRD should have been amended and was not.

**Check 2 is the one that bites.** Four product questions surfaced while
writing slice 2's tests. Each blocks a Must requirement. A feature that ships
with them unanswered has shipped someone's guess about timezones and refunds.

## Gate 3: feature successful

| Metric | Target | Measured |
|---|---|---|
| Manual export tickets per quarter | < 238 | Support tag, 60 days post-GA |
| Self-serve exports completed | > 500 / month | `export.completed` |
| Export failure rate | < 1% | `export.failed / export.started` |

Note what is absent from gate 2: **the ticket reduction.** It cannot gate
shipping, because it is measured two months after shipping. Conflating
completion with success means either shipping late or declaring victory early.

## Why not enumerate every test upfront

A tempting alternative: list all the feature's test headers in the spec, each
with a checkbox, and call the feature done when every box is ticked. Slice 2
alone has 23 tests, so the finished suite is somewhere near double that.

It fails for three reasons, all visible in this example.

| Problem | In this feature |
|---|---|
| **The list cannot be written correctly** | `occurred_at renders in the user's timezone` is unwritable until the timezone question is answered — and that question only surfaced while writing slice 2's tests. Boxes would be ticked against tests asserting the wrong thing |
| **It duplicates the test runner** | Once a test exists, the runner reports pass/fail on every commit. A hand-maintained parallel list is a copy of a machine-generated fact, and it drifts within a week |
| **It measures the wrong thing** | A ticked list says "we wrote the tests we thought of in September." It cannot say "we did not miss anything" — and the September version knew less than the November one |

The impulse behind it is correct: completion should be mechanical, not a
judgment call. The fix is to enumerate at the level that is knowable in advance
— requirements — rather than the level that is not.

**Requirements are stable while you build. Test lists are not.**

## Where the enumerated list is right

Contract and regulated work: an FDA submission, a defence contract, an audited
financial system. There the signed, checkbox-tracked verification matrix *is*
the deliverable, because the customer is buying evidence of verification, not
only working software. That is ISO/IEC/IEEE 29148's Verification section, and
it is a legitimate context — it is simply a different one, and adopting its
paperwork without its obligations buys the cost and none of the benefit.
