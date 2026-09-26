#!/usr/bin/env python3
"""Measure whether the right skill auto-triggers across the SDLC and context plugins.

Self-contained: builds its own throwaway fixture repos in .gauge-fixtures/, then
runs `claude -p` once per query with `--plugin-dir` pointed at the working copy.
`--plugin-dir` loads the plugin for that session only, so this never touches the
user's installed plugin cache and needs no commit, push, or `/plugin update`.

Three methodology notes, all learned by getting them wrong first. Each one, on
its own, manufactures a triggering failure that is not there:

  * Do NOT build the fixture under the system temp dir. On macOS that is
    /var/folders/..., and skills do not auto-invoke there. Measured directly:
    the same query, same wording, 3/3 fired from a fixture under the repo and
    0/3 from one under tempfile.TemporaryDirectory(). This masqueraded as
    two whole skills scoring 0/4 and 0/2. Fixtures now go in
    .gauge-fixtures/ beside the repo.

  * Run inside a realistic repo. In an empty cwd the model orients with `ls`
    before doing anything else, which reads as a miss and is not.
  * Score "did the skill fire at all in a bounded run", not "was it the first
    call" and not "within the first N calls". These skills instruct the agent to
    explore before acting, so any positional window penalises exactly the
    behaviour they ask for. Observed: `scoping` firing at tool call 7 after
    reading six files, and `scoping` at call 9, both scored as misses by a
    4-call window. Position is still reported, since a very late fire is worth
    eyeballing.

Taken together the three traps are worth more than any wording change made here:
the same suite, on identical skill wording, scored 11/21, then 14/22, then
21/22, purely as the harness was corrected. Fix the harness before you touch a
description.

Usage:
    python3 tools/gauge.py                # whole suite
    python3 tools/gauge.py --only engineering    # one expected skill
    python3 tools/gauge.py --jobs 8       # more parallelism
"""
import argparse
import json
import os
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_DIRS = [os.path.join(REPO, "plugins", "SDLC"),
               os.path.join(REPO, "plugins", "context")]
# Bound the run; a skill firing anywhere inside it counts as triggered. Keep
# this generous. These skills instruct the agent to read the ground before it
# acts, and fires have been observed at tool call 8, so a tight bound truncates
# the run before the skill can fire and reads as a wording defect. Measured:
# "Review my diff against the plan" went 2/3 at 6 turns, firing at calls 3 and
# 7, and the third run was still exploring when the budget ran out.
TURNS = 12
MODEL = None  # set from --model; None leaves the harness default
OURS = {"orient", "greenfield", "guardrails", "define-work", "story", "spike",
        "architecture", "deliver", "reviewing", "handing-off"}
TARGET = 0.80  # suite passes at 80% or better

FILES = {
    "package.json": '{ "name": "orders-api", "version": "0.4.1",\n'
                    '  "scripts": { "test": "jest" },\n'
                    '  "dependencies": { "express": "^4.19.0", "pg": "^8.11.0" } }\n',
    "README.md": "# orders-api\n\nExpress + Postgres service handling order "
                 "placement, payment capture and export.\n",
    "src/orders.js": """const db = require('./db');
async function placeOrder(userId, items) {
  const total = items.reduce((s, i) => s + i.price * i.qty, 0);
  return db.insert('orders', { userId, items, total, status: 'pending' });
}
async function exportOrders(page = 0) {
  return db.query('SELECT * FROM orders LIMIT 50 OFFSET $1', [page * 50]);
}
module.exports = { placeOrder, exportOrders };
""",
    "src/db.js": """const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
module.exports = { query: (q, p) => pool.query(q, p), insert: async (t, r) => r };
""",
    "tests/orders.test.js": """const { placeOrder } = require('../src/orders');
test('places an order and totals it', async () => {
  const o = await placeOrder('u1', [{ price: 10, qty: 2 }]);
  expect(o.total).toBe(20);
});
""",
}

DESIGN = """# cursor-pagination build plan

**Disposable.** Delete once the code is complete and the last slice has landed.

## Problem
`exportOrders` moves from OFFSET paging to keyset paging. Spec:
`docs/spec/cursor-pagination/spec.md`.

## Approach
Keyset on `orders.id`. The response gains `nextCursor`; offset clients keep
working through the rollout.

## Constraint to test manifest
| # | Constraint | Origin | Disposition |
| 1 | A page returns at most 50 rows | carried from the spec | test, unit |
| 2 | nextCursor is null on the last page | created by the shape | test, unit |

### Failure paths
| # | Failure | Detected by |
| F1 | Cursor points at a deleted row | test, returns the next live row |

## Slices
1. [x] exportOrders accepts a cursor and returns nextCursor
2. [ ] the admin export UI reads nextCursor

## Before deleting this file
- [ ] Every manifest row is discharged
"""

# A repo with tooling and intent but no system yet: what greenfield attaches to.
BARE = {
    "README.md": "# fleet-telemetry\n\nNothing built yet. Intended to ingest "
                 "vehicle telemetry and serve it back to fleet operators.\n",
    ".gitignore": "node_modules/\n.env\n",
}


def _git(cwd, *args):
    subprocess.run(["git", "-c", "user.email=g@g", "-c", "user.name=g", *args],
                   cwd=cwd, check=True, capture_output=True)


def build_fixtures(root):
    """Return (fresh, mid, bare): a clean repo, one mid-change with a design doc,
    an unbuilt slice and a live diff, and one with no system in it yet."""
    bare = os.path.join(root, "bare")
    for rel, body in BARE.items():
        path = os.path.join(bare, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(body)
    _git(bare, "init", "-q")
    _git(bare, "add", "-A")
    _git(bare, "commit", "-qm", "initial")

    fresh = os.path.join(root, "fresh")
    for rel, body in FILES.items():
        path = os.path.join(fresh, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(body)
    os.makedirs(os.path.join(fresh, "docs", "adr"), exist_ok=True)
    _git(fresh, "init", "-q")
    _git(fresh, "add", "-A")
    _git(fresh, "commit", "-qm", "initial")

    mid = os.path.join(root, "mid")
    subprocess.run(["cp", "-r", fresh, mid], check=True)
    design_dir = os.path.join(mid, "docs", "design", "cursor-pagination")
    os.makedirs(design_dir, exist_ok=True)
    with open(os.path.join(design_dir, "design.md"), "w") as fh:
        fh.write(DESIGN)
    with open(os.path.join(mid, "tests", "orders.test.js"), "a") as fh:
        fh.write("\ntest.failing('exportOrders returns a nextCursor', async () => {\n"
                 "  const r = await exportOrders();\n"
                 "  expect(r.nextCursor).toBe('order_50');\n});\n")
    _git(mid, "add", "-A")
    _git(mid, "commit", "-qm", "test(cursor-pagination): contract and intent")
    # leave an uncommitted implementation so there is a diff to audit
    with open(os.path.join(mid, "src", "orders.js"), "w") as fh:
        fh.write(FILES["src/orders.js"].replace(
            "return db.query('SELECT * FROM orders LIMIT 50 OFFSET $1', [page * 50]);",
            "const rows = await db.query('SELECT * FROM orders WHERE id > $1 "
            "ORDER BY id LIMIT 50', [page || '']);\n  return { rows, nextCursor: "
            "rows.length ? rows[rows.length - 1].id : null };"))
    return fresh, mid, bare


def tuning_cases(fresh, mid, bare):
    """(query, expected skill or None, fixture). The phrases each description is
    tuned against. A number from here is a train score: the wording of these
    queries went into the descriptions, so it measures fit, not generalisation.
    Read validation_cases() for the honest number."""
    return [
        # no application yet: architecture owns the path; greenfield only for a bare template
        ("Let's setup a new project.", "architecture", bare),
        ("I want to start a new python project.", "architecture", bare),
        ("I want to start a new javascript project.", "architecture", bare),
        ("Let's create scaffolding for an iOS app.", "architecture", bare),
        ("Let's put together the blueprint for this project.", "architecture", bare),
        ("I need scaffolding for this.", "architecture", bare),
        ("Let's put together the walking skeleton.", "architecture", bare),
        ("I need a walking skeleton.", "architecture", bare),
        ("Python project template.", "greenfield", bare),
        ("Template project.", "greenfield", bare),
        # adr: a decision exists and the why is the artefact
        ("Record this architecture decision.", "architecture", fresh),
        ("Make an adr.", "architecture", fresh),
        ("Write an adr.", "architecture", fresh),
        ("This is an architectural decision.", "architecture", fresh),
        ("We need to record the why.", "architecture", fresh),
        ("Adr", "architecture", fresh),
        ("Create an adr.", "architecture", fresh),
        ("Note this architecture decision.", "architecture", fresh),
        # harness: the repo gives the agent no feedback of its own
        ("Setup my repo for my agent.", "orient", fresh),
        ("Setup my repo for Claude.", "orient", fresh),
        ("Configure my environment for Claude.", "orient", fresh),
        ("Setup my environment for my AI agent.", "orient", fresh),
        ("Make this repo ready for an AI agent.", "orient", fresh),
        ("Setup harness in this repo.", "guardrails", fresh),
        ("Make repo AI ready.", "orient", fresh),
        # spike: prove or explore before committing, code is disposable
        ("Let's prove this works first.", "spike", fresh),
        ("Let's try an approach before building.", "spike", fresh),
        ("Let's prototype this idea.", "spike", fresh),
        ("Let's create a mock.", "spike", fresh),
        ("Create a throwaway project.", "spike", fresh),
        ("Let's see if Redis Streams is feasible here.", "spike", fresh),
        ("Let's see how this integration would work.", "spike", fresh),
        ("Let's see the changes which would be needed.", "spike", fresh),
        ("Explore how this would fit into the system.", "spike", fresh),
        ("Build a quick throwaway.", "spike", fresh),
        ("Build a demo.", "spike", fresh),
        ("Let's do a spike on it.", "spike", fresh),
        # agile: any request to write, change or remove code in a system
        ("I want to add rate limiting to the export endpoint.", "deliver", fresh),
        ("I want to remove the order export module.", "deliver", fresh),
        ("Add code to validate the order payload.", "deliver", fresh),
        ("Modify the code so the export paginates with cursors.", "deliver", fresh),
        ("Implement the CSV import feature.", "deliver", fresh),
        ("Build the next slice.", "deliver", mid),
        ("Fix the bug where placeOrder ignores quantity.", "deliver", fresh),
        # handing-off: the session itself is the subject
        ("Create a handoff.", "handing-off", mid),
        ("Make a handoff.", "handing-off", mid),
        ("Write a handoff document.", "handing-off", mid),
        ("Your context is getting full.", "handing-off", mid),
        ("You are running out of context.", "handing-off", mid),
        ("You are running low on context.", "handing-off", mid),
        ("There's context rot.", "handing-off", mid),
        # true negatives: shared vocabulary, no skill needed
        ("What's the difference between optimistic and pessimistic locking?", None, bare),
        ("Explain how consistent hashing works.", None, bare),
        ("What does the -u flag do in git push?", None, fresh),
        ("What's the difference between a mutex and a semaphore?", None, fresh),
        ("Run the test suite and show me the output.", None, fresh),
        ("Fix this typo: 'recieve' should be 'receive' in README.md", None, fresh),
    ]


def validation_cases(fresh, mid, bare):
    """Held out. None of this wording was used to write a description, so this
    is the set that says whether a gain generalises or was memorised. Phrased
    the way a user actually types: file paths, backstory, lowercase, typos."""
    return [
        # greenfield
        ("brand new repo for a go service that serves feature flags, nothing in "
         "it yet. get me to a green test run", "architecture", bare),
        ("my team lead wants the ops-console repo spun up before standup "
         "tomorrow, its an empty dir right now", "architecture", bare),
        ("kicking off a rust cli this weekend, cargo workspace, one bin one lib. "
         "where do we start", "architecture", bare),
        # adr
        ("we just settled on sqs over kafka cos nobody here can run kafka. "
         "capture that somewhere permanent", "architecture", fresh),
        ("future me is gonna wonder why we didnt just use the vendor sdk. put it "
         "on record", "architecture", fresh),
        ("we're accepting that the nightly recon job can double count across DST. "
         "no test for it, but it needs writing down", "architecture", fresh),
        # harness
        ("every PR here turns into a style argument, theres no formatter or type "
         "check. wire it up so the tooling tells the agent off, not me", "guardrails", fresh),
        ("claude keeps putting business logic in the route handlers, ive told it "
         "three times. make it a rule it cant ignore", "guardrails", fresh),
        ("i want a pre-commit gate that runs fmt, types and tests so nothing "
         "lands broken", "guardrails", fresh),
        # spike
        ("before we commit to duckdb i want to know if it chews through our 40gb "
         "of parquet. throwaway is fine", "spike", fresh),
        ("ive got two customers on friday and want something clickable for the "
         "new onboarding flow", "spike", fresh),
        ("roughly what would it take to move us off celery onto arq? dont build "
         "it properly", "spike", fresh),
        # agile
        ("the retry loop in src/db.js gives up after 3 tries, make it exponential "
         "backoff with jitter capped at 30s", "deliver", fresh),
        ("deleting a user leaves orphaned sessions lying around. sort it out", "deliver", fresh),
        ("we need csv upload in the admin panel, my PM has been asking for weeks", "deliver", fresh),
        # handing-off
        ("im knackered, stopping for the day. capture where we got to including "
         "the two approaches that didnt work", "handing-off", mid),
        ("we're at like 15% context left, write it up before we lose it", "handing-off", mid),
        ("someone else picks this up tomorrow morning, leave them what they need", "handing-off", mid),
        # near-miss negatives: each shares vocabulary with a skill above
        ("whats the difference between arq and celery?", None, fresh),
        ("heres the EXPLAIN output for our slow orders query, what's it telling me?", None, fresh),
        ("our oncall handoff doc lives in docs/oncall.md, add the new pager "
         "rotation to it", None, fresh),
        ("summarise today's architecture review meeting notes into bullets", None, fresh),
        ("which python lib should i use for parsing ical files?", None, fresh),
        ("write the release notes for the 2.1 tag", None, fresh),
    ]


def run_one(case):
    query, expected, cwd = case
    try:
        proc = subprocess.run(
            ["claude", "-p", query,
             *[a for d in PLUGIN_DIRS for a in ("--plugin-dir", d)],
             "--output-format", "stream-json", "--verbose",
             "--max-turns", str(TURNS), "--setting-sources", "project"]
            + (["--model", MODEL] if MODEL else []),
            cwd=cwd, capture_output=True, text=True,
            stdin=subprocess.DEVNULL, timeout=420)
    except subprocess.TimeoutExpired:
        return query, expected, [], None, "TIMEOUT"

    tools, fired, pos = [], None, None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") != "assistant":
            continue
        for b in d.get("message", {}).get("content", []):
            if b.get("type") != "tool_use":
                continue
            tools.append(b["name"])
            if fired is None and b["name"] == "Skill":
                fired = b.get("input", {}).get("skill", "").split(":")[-1]
                pos = len(tools)
    return query, expected, tools, fired, pos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", choices=("tuning", "validation", "all"),
                    default="tuning",
                    help="tuning: the phrases the descriptions were written "
                         "against (a train score). validation: held-out wording "
                         "that never fed a description, which is the number to "
                         "believe. all: both.")
    ap.add_argument("--only", help="substring filter on the expected skill")
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--repeat", type=int, default=1,
                    help="run each case N times; a case that passes some runs "
                         "and fails others is variance, not a wording defect")
    ap.add_argument("--grep", help="substring filter on the query text")
    ap.add_argument("--model", default=None,
                    help="model for the measured runs. Triggering is a property "
                         "of the model reading the descriptions, so a number "
                         "measured on one model does not transfer to another. "
                         "Use a cheap model to iterate, then confirm on the one "
                         "you actually run.")
    args = ap.parse_args()
    global MODEL
    MODEL = args.model

    # Deliberately not tempfile: see the note at the top of this file.
    root = os.path.join(REPO, ".gauge-fixtures")
    subprocess.run(["rm", "-rf", root], check=True)
    os.makedirs(root)
    fresh, mid, bare = build_fixtures(root)
    pool_cases = []
    if args.suite in ("tuning", "all"):
        pool_cases += tuning_cases(fresh, mid, bare)
    if args.suite in ("validation", "all"):
        pool_cases += validation_cases(fresh, mid, bare)
    selected = [c for c in pool_cases
                if (not args.only or args.only in (c[1] or "none"))
                and (not args.grep or args.grep.lower() in c[0].lower())]
    selected = selected * args.repeat
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run_one, selected))

    buckets, per_query, total = {}, {}, 0
    for query, expected, tools, fired, pos in results:
        hit = (fired == expected) if expected else (fired not in OURS)
        buckets.setdefault(expected or "none", []).append(hit)
        per_query.setdefault((query, expected), []).append(hit)
        got = f"{fired}@{pos}" if fired else "(none)"
        print(f"{'PASS' if hit else 'FAIL'}  want={expected or 'none':20s} "
              f"got={got:24s} {query[:56]}")
        if not hit:
            print(f"        tools: {tools}")
    print()
    if args.repeat > 1:
        print("  per query (a mixed row is variance, not a wording defect):")
        for (query, expected), hits in per_query.items():
            flag = "  <-- FLAKY" if 0 < sum(hits) < len(hits) else ""
            print(f"    {sum(hits)}/{len(hits)}  {query[:60]}{flag}")
        print()
    for expected, hits in buckets.items():
        print(f"  {expected:20s} {sum(hits)}/{len(hits)}")
        total += sum(hits)
    rate = total / len(results) if results else 0.0
    print(f"  {'TOTAL':20s} {total}/{len(results)}  ({rate:.0%}, target {TARGET:.0%})")
    return 0 if rate >= TARGET else 1


if __name__ == "__main__":
    sys.exit(main())
