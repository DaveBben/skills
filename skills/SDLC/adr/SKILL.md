---
name: adr
description: "Use this skill whenever a decision must survive the conversation: a choice that costs more than a day to reverse, whether the user or the agent made it (a library, a data shape, a trust or consistency boundary, a new repository), a hazard accepted without a test, or an alternative rejected. Use it on: 'adr', 'write an adr', 'make an adr', 'record this architecture decision', 'note this decision', 'this is an architectural decision', 'record the why', 'put it on record', 'we will accept that risk', 'let's go with X instead of Y'. Writes one Markdown decision record under docs/adr/ carrying the user's own reasons, the rejected alternatives and the test that detects the hazard."
license: MIT
metadata:
  version: "1.1.0"
---
# ADR

An ADR (architecture decision record) is one Markdown file under `docs/adr/` saying what was decided, why, and what it gave up.

Write it when the decision is made, not at the end of the feature. Write one for:

* An expensive or irreversible choice.
* An accepted hazard.
* A rejected alternative.

## Get the reasons

The reasons are the user's. Never record a reason the user has not given or confirmed. Add no alternative, mechanism or measurement that neither the user nor your feedback message named.

```text
Before recording <decision>, correct anything wrong:
1. Why this? <draft>
2. What are the tradeoffs? <draft>
3. Why not <the obvious route>? <draft>
```

* **A decision already made:** draft the three answers from the conversation and the code, and put them to the user in one message to correct.
* **Draft answer 3:** name the obvious route. Write "unknown" for any answer you cannot draft.
* **An open decision:** send the block with the alternatives and the tradeoff they turn on in place of the drafts. The user's answer is the reasons.
* **The agent's own choice:** state the agent's reason, the obvious alternative and the tradeoff. Ask the user to confirm, change or replace the reason.
* **The user defers:** record the agent's reason, marked as the agent's, with the line "The user deferred to the agent's recommendation."
* **Feedback, only when there is some:** send it in one message before writing, giving each point its mechanism. It covers:
  * a tradeoff the answer did not name;
  * an alternative nobody considered;
  * a hazard accepted without a test;
  * a reason that does not hold against the code.
* **Where feedback goes:** after the user answers it, put it under "Alternatives rejected" or "What it gives up", marked as the agent's.
* **No reasons given:** write no file. Say the decision is unrecorded, and carry on with the work.

## Where it goes

* **One feature's decision:** `docs/adr/<slug>/<decision-name>.md`, where the slug is the feature's slug, as in its feature file (`docs/stories/<slug>.md`) and its `story/<slug>/` branches. A single story with no feature goes under `architecture/`.
* **Whole repository:** `docs/adr/architecture/<decision-name>.md`.
* **The name:** short and kebab-case, like `use-redis-for-rate-limiting.md`.
* **Commit it on its own** on the current branch. On main, create a branch `adr/<decision-name>` first. Never switch the branch of a checkout with uncommitted changes; ask instead.
* **The story it serves:** add the ADR's path under its `Decided`, in its issue by the `using-trackers` skill or in `docs/stories/<slug>.md`.
* **An existing ADR it contradicts:** leave the old file in place and name it on the new one's `Supersedes:` line.
* **The old ADR:** add `Superseded by: <new path>` to it.

## Write it like this

Match the example's sections, order and density.

* **Short form:** the default.
* **Long form:** only when the decision accepts a hazard or follows an incident; read [references/long-form.md](references/long-form.md) and match it. Leave out a section with nothing to say.
* **Detector:** the test that fails when the decision is broken, or the test the change will add and what it asserts. When no test can detect it, write `none` and what a reader would have to watch instead.
* **Every ADR has a Supersedes line.**

```markdown
# Cap previews at one render per editor tab, not a timeout

**Decision:** Each editor tab makes at most one render call at a time, and a soft limit caps calls
across the site. A timeout cannot work: it bounds how long one call takes, and the outage came from
how many ran at once on a worker pool of 5.

**Detector:** `tests/test_render.py::test_one_render_per_tab` asserts one call per request and that
the over-limit call is refused. It does not assert the cap number, which is not measured yet.

## Alternatives rejected
- A timeout: already 30 s, and it did not prevent the outage.
- A strict global limit: the add-on cache has no atomic counter.

## What it gives up
- The site-wide limit is soft; it can briefly allow a few calls over the cap.

**Supersedes:** none.
```
