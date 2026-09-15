# Keep the LLM safe with a concurrency cap, not a timeout

**Decision:** Scribe makes at most one AI call at a time per browser, keeps a best-effort limit on
how many run across the whole instance, and keeps each call short. It does not rely on a timeout,
because a timeout cannot solve the problem we have.

## The problem

Scribe writes suggestions for four note fields *while the visit is happening*, so it calls the
Anthropic LLM repeatedly, live, during a visit.

All plugin code runs in the **plugin-runner**: a small pool of worker threads shared by every
plugin and every user on the instance. The pool is tiny — `PLUGIN_RUNNER_MAX_WORKERS`, default
**5** (an instance may set it to ~8). An LLM call is blocking: the worker sits idle waiting for
Anthropic to answer. So a handful of slow calls at once fills the pool, and when the pool is full
**nothing else on the instance can run** — every plugin, every user, gets 502/504.

An earlier prototype generated suggestions in a **continuous loop** — one blocking LLM call plus
some database reads every cycle, across four fields, for several clinicians at once. It held more
workers than the pool has, for minutes, and took the **whole instance down in production**.

## Why the obvious fixes don't work in Canvas

- **A timeout doesn't help.** The shared HTTP client already caps every call at 30 seconds, and
  that didn't prevent the outage: a per-call timeout limits how long *one* call takes, not *how
  many* run at once. We also can't shorten it (no timeout option in the LLM settings) or cancel a
  call once it's blocked.
- **There's no real-time background worker.** The only off-request option is `CronTask`, which runs
  at most once a minute — useless for live suggestions.
- **We can't build a strict limiter ourselves.** The plugin cache has no atomic counter, so a
  perfectly race-free cap would need outside infrastructure (e.g. Redis), deferred past the pilot.

The real cause — too many calls running at once, on a tiny shared pool — has no built-in Canvas
lever, so we control it in the plugin.

## What we decided

1. **No loop.** Suggestions come from a single browser-triggered `/suggest` that makes exactly one
   LLM call and returns. No loop, no retries, no database reads on the LLM path.
2. **One call at a time per browser**, so each clinician occupies at most one worker.
3. **A soft, instance-wide limit** — a best-effort counter in the shared cache that self-heals if a
   worker dies mid-call.
4. **Short calls** — a small `max_tokens` keeps each one well under the 30-second cap.

## What it buys

Scribe's load becomes roughly "clinicians currently recording," not "clinicians × four fields ×
loop speed." The worst case drops from "the whole instance is down for minutes" to "a few workers
are busy briefly." It ships with no new dependencies, and `SCRIBE_ENABLED` turns it off instantly.

## What it doesn't buy

This is a pilot-grade guard, not a guarantee. The instance-wide limit is soft (it can briefly
allow a few over the cap), a single call still holds a worker up to 30 seconds, and the cap number
is a guess (start at 1–2). **Before expanding beyond the pilot group**, measure the real load —
how many clinicians record at once, how often the browser calls, how long each call takes —
against the instance's actual `PLUGIN_RUNNER_MAX_WORKERS`, and add outside infrastructure for a
strict limit if needed.

## Alternatives rejected

- **A timeout** — already exists, didn't help (bounds one call, not concurrency), can't be tuned.
- **Abandon the thread after a deadline** — the network call keeps running, so it protects the user
  experience, not the pool.
- **Retries (`attempt_requests`)** — more calls holding workers; banned on `/suggest`.
- **A strict global limit in the plugin cache** — impossible without an atomic counter.

**Detector:** design test T-15 (one call per `/suggest`, the over-limit call is rejected, a leaked
slot recovers after its TTL). No assertion on the cap number, since it isn't measured yet.

**Supersedes:** none.
