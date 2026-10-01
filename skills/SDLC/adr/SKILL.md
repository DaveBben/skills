---
name: adr
description: "Use this skill whenever a decision must survive the conversation: a choice that costs more than a day to reverse, whether the user or the agent made it (a library, a data shape, a trust or consistency boundary, a new repository), a hazard accepted without a test, an alternative rejected, or knowledge that cost time to acquire. Use it on: 'adr', 'write an adr', 'make an adr', 'record this architecture decision', 'note this decision', 'this is an architectural decision', 'record the why', 'put it on record', 'we will accept that risk', 'let's go with X instead of Y', 'should I use X or Y'. Writes one Markdown decision record under docs/adr/ carrying the user's own reasons, the rejected alternatives and the test that detects the hazard."
license: MIT
metadata:
  version: "1.0.0"
---
# ADR

An ADR (architecture decision record) is one Markdown file under `docs/adr/` that says what was decided, why, and what it gave up. Write one when the decision is made, not at the end of the feature: for an expensive or irreversible choice, an accepted hazard, a rejected alternative, knowledge that cost time to acquire, or a test dropped as "no test required" whose absence a later reader would question.

## Get the reasons

The reasons are the user's. Never record one the user has not given or confirmed, and add no alternative, mechanism or measurement nobody named.

* **An open decision:** put the alternatives and the tradeoff they turn on to the user in one message. Their answer is the reasons.
* **A decision already made:** draft the three answers from the conversation and the code, and put them to the user in one message to correct. Name the obvious route in the third. Write "unknown" for any you cannot draft.

```text
Before recording <decision>, correct anything wrong:
1. Why this? <draft>
2. What are the tradeoffs? <draft>
3. Why not <the obvious route>? <draft>
```

* **The agent's own choice:** state the agent's reason, the obvious alternative and the tradeoff, and ask the user to confirm, change or replace the reason. When the user defers, record the agent's reason, marked as the agent's, with the line "The user deferred to the agent's recommendation."
* **Feedback, only when there is some:** a tradeoff the answer did not name, an alternative nobody considered, a hazard accepted without a test, or a reason that does not hold against the code, each with its mechanism, in one message before writing. It goes in "Alternatives rejected" or "What it doesn't buy", marked as the agent's.
* **No reasons given:** write no file. Say the decision is unrecorded, and carry on with the work.

## Where it goes

* **One feature's decision:** `docs/adr/<slug>/<decision-name>.md`, where the slug is the feature's, as in its `story/<slug>/` branches. **Whole repository:** `docs/adr/architecture/<decision-name>.md`. The name is short and kebab-case: `use-redis-for-rate-limiting.md`.
* **Commit it on its own** on the current branch. Never switch the branch of a checkout with uncommitted changes; ask instead.
* **With a feature file open** (`docs/stories/<slug>.md`), add the ADR's path to its `Decided:` line.
* **An existing ADR it contradicts:** leave the old file in place, name it on the new one's `Supersedes:` line, and add `Superseded by: <new path>` to the old one.

## Write it like these

Match the examples' sections, order and density. Write the short form by default. Write the long form only when the decision accepts a hazard or follows an incident, leaving out a section with nothing to say. Every ADR has a Detector, the test that fails when the decision is broken (or the test ID the change will add and what it will assert), and a Supersedes line.

Short form:

```markdown
# Cap previews at one render per editor tab, not a timeout

**Decision:** Each editor tab makes at most one render call at a time, and a soft limit caps calls
across the site. A timeout cannot work: it bounds how long one call takes, and the outage came from
how many ran at once on a worker pool of 5.

**Detector:** T-15 asserts one call per request and that the over-limit call is refused. It does
not assert the cap number, which is not measured yet.

## Alternatives rejected
- A timeout: already 30 s, and it did not prevent the outage.
- A strict global limit: the add-on cache has no atomic counter.

**Supersedes:** none.
```

Long form:

```markdown
# Protect the add-on pool with a concurrency cap, not a timeout

**Decision:** Previews makes at most one render call at a time per editor tab, keeps a best-effort
limit on how many run across the whole site, and keeps each render small. It does not rely on a
timeout, because a timeout cannot solve the problem we have.

**Detector:** design test T-15 (one call per `/render`, the over-limit call is rejected, a leaked
slot recovers after its TTL). No assertion on the cap number, since it isn't measured yet.

## Alternatives rejected

- **A timeout** — already exists, didn't help (bounds one call, not concurrency), can't be tuned.
- **Abandon the thread after a deadline** — the network call keeps running, so it protects the user
  experience, not the pool.
- **Retries (`retry_request`)** — more calls holding workers; banned on `/render`.
- **A strict global limit in the add-on cache** — impossible without an atomic counter.

## The problem

Previews renders four sections of a page *while the editor is typing*, so it calls the external
rendering service repeatedly, live, as the editor works.

All add-on code runs in the **add-on host**: a small pool of worker threads shared by every add-on
and every user on the site. The pool is tiny — `ADDON_HOST_WORKERS`, default **5** (a site may set
it to ~8). A render call is blocking: the worker sits idle waiting for the rendering service to
answer. So a handful of slow calls at once fills the pool, and when the pool is full **nothing else
on the site can run** — every add-on, every user, gets 502/504.

An earlier prototype re-rendered in a **continuous loop** — one blocking render call plus some
database reads every cycle, across four sections, for several editors at once. It held more
workers than the pool has, for minutes, and took the **whole site down in production**.

## Why the obvious fixes don't work in the add-on host

- **A timeout doesn't help.** The shared HTTP client already caps every call at 30 seconds, and
  that didn't prevent the outage: a per-call timeout limits how long *one* call takes, not *how
  many* run at once. We also can't shorten it (no timeout option in the add-on settings) or cancel
  a call once it's blocked.
- **There's no real-time background worker.** The only off-request option is `ScheduledJob`, which
  runs at most once a minute — useless for live previews.
- **We can't build a strict limiter ourselves.** The add-on cache has no atomic counter, so a
  perfectly race-free cap would need outside infrastructure (e.g. Redis), deferred past the beta.

The real cause — too many calls running at once, on a tiny shared pool — has no built-in lever in
the host, so we control it in the add-on.

## What it buys

Previews' load becomes roughly "editors currently typing," not "editors × four sections × loop
speed." The worst case drops from "the whole site is down for minutes" to "a few workers are busy
briefly." It ships with no new dependencies, and `PREVIEWS_ENABLED` turns it off instantly.

## What it doesn't buy

This is a beta-grade guard, not a guarantee. The site-wide limit is soft (it can briefly allow a
few over the cap), a single call still holds a worker up to 30 seconds, and the cap number is a
guess (start at 1–2). **Before opening it to every editor**, measure the real load — how many
editors type at once, how often the browser calls, how long each render takes — against the
site's actual `ADDON_HOST_WORKERS`, and add outside infrastructure for a strict limit if needed.

**Supersedes:** none.
```
