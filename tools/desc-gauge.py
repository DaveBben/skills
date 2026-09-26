#!/usr/bin/env python3
"""Score the SDLC descriptions against one named list of user phrases, each
with the one skill that should own it.

Reuses gauge.py wholesale: same fixtures, same runner, same three methodology
traps documented at the top of that file. Read those notes before believing a
number from here.

The suite is the 30 phrases the description is being tuned for, grouped by the
stage they arrive at, plus gauge.py's true negatives carried in unchanged as a
guard: widening the description until everything fires is not a pass.

Usage:
    python3 tools/desc-gauge.py                     # whole suite, sonnet
    python3 tools/desc-gauge.py --repeat 2
    python3 tools/desc-gauge.py --group "Bug Fixes"
"""
import argparse
import os
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gauge

REPO = gauge.REPO

# The skill each group should route to; OWNER overrides it for single phrases.
GROUP_OWNER = {"Vague ideas": "define-work", "Discovery": "spike",
               "Spec & design": "architecture", "Build": "deliver",
               "Bug fixes": "deliver", "Resumption": "deliver"}
OWNER = {
    "How does this system currently handle order totals?": None,
    "Let's map the current landscape.": "architecture",
    "Let's write a spec for the CSV import.": "define-work",
}

# (group, phrase, fixture key). fixture key: "fresh" | "mid" | "bare".
TARGET = [
    ("Vague ideas",   "I'm not sure what I want yet.", "fresh"),
    ("Vague ideas",   "I have a vague idea for a feature.", "fresh"),
    ("Vague ideas",   "Trying to work out how to paginate the order export.", "fresh"),
    ("Vague ideas",   "What would happen if I moved order processing off the request path?", "fresh"),
    ("Vague ideas",   "I want to add payment retries but I don't know where to start.", "fresh"),
    ("Discovery",     "Let's run a spike on replacing the pg driver.", "fresh"),
    ("Discovery",     "Build a quick prototype for the admin export screen.", "fresh"),
    ("Discovery",     "How does this system currently handle order totals?", "fresh"),
    ("Discovery",     "Let's map the current landscape.", "fresh"),
    ("Discovery",     "What breaks if we change the orders table primary key?", "fresh"),
    ("Spec & design", "Let's write a spec for the CSV import.", "fresh"),
    ("Spec & design", "Help me design the architecture for the notification service.", "fresh"),
    ("Spec & design", "Draw the module map for this service.", "fresh"),
    ("Spec & design", "Let's define the data contracts.", "fresh"),
    ("Spec & design", "We need a technical approach for multi-tenancy.", "fresh"),
    ("Build",         "Let's pair program this.", "mid"),
    ("Build",         "I want to start building.", "mid"),
    ("Build",         "Write the failing test for the cursor pagination.", "mid"),
    ("Build",         "Implement the CSV import feature.", "mid"),
    ("Build",         "Take over and build this autonomously.", "mid"),
    ("Bug fixes",     "Fix this bug.", "fresh"),
    ("Bug fixes",     "Why is this crashing?", "fresh"),
    ("Bug fixes",     "I got a null pointer exception.", "fresh"),
    ("Bug fixes",     "This is just a minor CSS tweak.", "fresh"),
    ("Bug fixes",     "Quick copy update.", "fresh"),
    ("Resumption",    "Where did we leave off on the cursor pagination?", "mid"),
    ("Resumption",    "Let's resume working on this.", "mid"),
    ("Resumption",    "Did that fix it?", "mid"),
    ("Resumption",    "Let's verify the production logs.", "mid"),
    ("Resumption",    "Check the telemetry.", "mid"),
]

# Carried from gauge.py unchanged. These must keep passing.
NEGATIVE = [
    ("What's the difference between optimistic and pessimistic locking?", "bare"),
    ("Explain how consistent hashing works.", "bare"),
    ("What does the -u flag do in git push?", "fresh"),
    ("What's the difference between a mutex and a semaphore?", "fresh"),
    ("Run the test suite and show me the output.", "fresh"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--group", help="substring filter on the group name")
    ap.add_argument("--grep", help="substring filter on the phrase")
    ap.add_argument("--no-negatives", action="store_true")
    ap.add_argument("--model", default="sonnet")
    args = ap.parse_args()
    gauge.MODEL = args.model

    root = os.path.join(REPO, ".gauge-fixtures")
    subprocess.run(["rm", "-rf", root], check=True)
    os.makedirs(root)
    fresh, mid, bare = gauge.build_fixtures(root)
    paths = {"fresh": fresh, "mid": mid, "bare": bare}

    selected = [(g, q, paths[f]) for g, q, f in TARGET
                if (not args.group or args.group.lower() in g.lower())
                and (not args.grep or args.grep.lower() in q.lower())]
    cases = [(q, OWNER.get(q, GROUP_OWNER[g]), cwd) for g, q, cwd in selected]
    groups = [g for g, _, _ in selected]
    if not args.no_negatives and not args.group and not args.grep:
        cases += [(q, None, paths[f]) for q, f in NEGATIVE]
        groups += ["Negative"] * len(NEGATIVE)

    cases, groups = cases * args.repeat, groups * args.repeat
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(gauge.run_one, cases))

    buckets, per_query = {}, {}
    for group, (query, expected, tools, fired, pos) in zip(groups, results):
        hit = (fired == expected) if expected else (fired not in gauge.OURS)
        buckets.setdefault(group, []).append(hit)
        per_query.setdefault((group, query), []).append(hit)
        got = f"{fired}@{pos}" if fired else "(none)"
        print(f"{'PASS' if hit else 'FAIL'}  {group:14s} got={got:22s} {query[:56]}")

    print()
    if args.repeat > 1:
        for (group, query), hits in per_query.items():
            flag = "  <-- FLAKY" if 0 < sum(hits) < len(hits) else ""
            print(f"    {sum(hits)}/{len(hits)}  {query[:60]}{flag}")
        print()
    target_hits = target_n = 0
    for group, hits in buckets.items():
        print(f"  {group:14s} {sum(hits)}/{len(hits)}")
        if group != "Negative":
            target_hits += sum(hits)
            target_n += len(hits)
    pct = 100.0 * target_hits / target_n if target_n else 0.0
    print(f"  {'TARGET':14s} {target_hits}/{target_n}  ({pct:.0f}%)")
    return 0 if pct >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())
