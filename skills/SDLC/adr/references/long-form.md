# Long-form ADR

Use this form only when the decision accepts a hazard or follows an incident. Match its sections, order and density, and leave out a section with nothing to say.

```markdown
# Protect the add-on pool with a concurrency cap, not a timeout

**Decision:** Previews makes at most one render call at a time per editor tab, keeps a best-effort
limit on how many run across the whole site, and keeps each render small. It does not rely on a
timeout, because a timeout cannot solve the problem we have.

**Detector:** `tests/test_render.py::test_one_render_per_tab` asserts one call per `/render`, that
the over-limit call is rejected, and that a leaked slot recovers after its TTL. No test asserts the
cap number, since it is not measured yet.

## Alternatives rejected

- A timeout: one already exists and did not help. It bounds one call, not how many run at once, and
  it cannot be tuned.
- Abandon the thread after a deadline: the network call keeps running, so it protects the user
  experience and leaves the pool full.
- Retries (`retry_request`): more calls holding workers; banned on `/render`.
- A strict global limit in the add-on cache: impossible without an atomic counter.

## The problem

Previews renders four sections of a page while the editor is typing, so it calls the external
rendering service repeatedly, live, as the editor works.

All add-on code runs in the add-on host: a small pool of worker threads shared by every add-on and
every user on the site. The pool has `ADDON_HOST_WORKERS` threads, default 5; a site may set it to
about 8. A render call blocks: the worker waits for the rendering service to answer. A handful of
slow calls at once fills the pool. When the pool is full, nothing else on the site can run, and
every add-on and every user gets 502 or 504.

An earlier prototype re-rendered in a continuous loop: one blocking render call plus some database
reads every cycle, across four sections, for several editors at once. It held more workers than the
pool has, for minutes, and took the whole site down in production.

## Why the obvious fixes don't work in the add-on host

- A timeout does not help. The shared HTTP client already caps every call at 30 seconds, and that
  did not prevent the outage: a per-call timeout limits how long one call takes, not how many run
  at once. The add-on settings have no timeout option, and a blocked call cannot be cancelled.
- The host has no real-time background worker. The only off-request option is `ScheduledJob`, which
  runs at most once a minute, too slow for live previews.
- We cannot build a strict limiter ourselves. The add-on cache has no atomic counter, so a race-free
  cap needs outside infrastructure such as Redis, deferred past the beta.

The cause is too many calls running at once on a small shared pool. The host has no setting that
limits it, so the add-on limits it.

## What it buys

Previews' load becomes about one call per editor currently typing, instead of editors times four
sections times loop speed. The worst case drops from the whole site down for minutes to a few
workers busy briefly. It ships with no new dependencies, and `PREVIEWS_ENABLED` turns it off at once.

## What it gives up

This is a beta-grade guard. The site-wide limit is soft and can briefly allow a few calls over the
cap. A single call still holds a worker for up to 30 seconds. The cap number is a guess; start at 1
or 2. Before opening it to every editor, measure how many editors type at once, how often the
browser calls and how long each render takes, against the site's actual `ADDON_HOST_WORKERS`. Add
outside infrastructure for a strict limit if the measurement shows it is needed.

**Supersedes:** none.
```
