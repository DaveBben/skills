# Long-form ADR

Use this form only when the decision accepts a hazard or follows an incident.

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
- A strict global limit in the add-on cache: impossible, because the cache has no atomic counter; a race-free cap needs outside infrastructure such as Redis, deferred past the beta.

## The problem

Previews calls the external rendering service live as the editor types. Every add-on shares `ADDON_HOST_WORKERS` threads (default 5), and each render call blocks one. A prototype looped renders for several editors, held more workers than the pool has, and took the site down.

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
