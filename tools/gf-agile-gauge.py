#!/usr/bin/env python3
"""Measure greenfield vs agile triggering: does each fire on its own territory
and stay off the sibling's, across explicit, implicit and agent-decided
phrasing.

Reuses gauge.py's fixture builder and its three methodology traps (fixtures
under the repo, a realistic cwd, "fired anywhere in the run" not position).
Its own run_one checks EVERY Skill call in a run, not just the first -- copied
from adr-gauge.py's run_one -- because an agent-decided greenfield case may
route through other exploration before Skill:greenfield fires, and a
cross-fire case needs to know if the SIBLING skill fired too, not just
whether the first call matched.

Cases are tagged (owner, gf_group, ag_group, query, fixture):
  owner     which skill SHOULD fire: "greenfield", "agile", or None (neither
            -- a spike/harness/adr/question case used only as an agile
            negative).
  gf_group  None, or the greenfield bucket this case scores into: explicit,
            implicit, agent-decided, negative.
  ag_group  None, or the agile bucket: explicit, implicit, negative.

A case can carry both tags at once -- e.g. "Add pagination to the order
export." is an agile-positive (ag_group=implicit) AND a greenfield-negative
(gf_group=negative) in the same run, one subprocess call scoring both. That
overlap IS the point: the real risk is cross-firing between these two
skills, not either skill missing its own territory.

cross_fire counts a case where the WRONG one of the pair fired:
  owner == "greenfield" and agile also fired  -> greenfield case stolen by agile
  owner == "agile" and greenfield also fired  -> agile case stolen by greenfield

Usage:
    python3 tools/gf-agile-gauge.py                    # whole suite
    python3 tools/gf-agile-gauge.py --model             # sonnet
    python3 tools/gf-agile-gauge.py --repeat 3
    python3 tools/gf-agile-gauge.py --skill greenfield
    python3 tools/gf-agile-gauge.py --group negative
"""
import argparse
import json
import os
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gauge

REPO = gauge.REPO

# (owner, gf_group, ag_group, query, fixture_key)
CASES = [
    # ---- greenfield: explicit (must keep passing) ----
    ("greenfield", "explicit", None, "Let's setup a new project.", "bare"),
    ("greenfield", "explicit", "negative", "I want to start a new python project.", "bare"),
    ("greenfield", "explicit", None, "Let's create scaffolding for an iOS app.", "bare"),
    ("greenfield", "explicit", "negative", "I need a walking skeleton.", "bare"),
    ("greenfield", "explicit", "negative", "Template project.", "bare"),
    ("greenfield", "explicit", None, "Bootstrap a codebase for a new service.", "bare"),

    # ---- greenfield: implicit user (no template/scaffold words) ----
    ("greenfield", "implicit", "negative",
     "I've got an empty repo and an idea for a feature-flag service.", "bare"),
    ("greenfield", "implicit", "negative",
     "Nothing here yet, I want to build a URL shortener in Go.", "bare"),
    ("greenfield", "implicit", None,
     "Set me up so I can start writing an API tomorrow.", "bare"),
    ("greenfield", "implicit", None,
     "I need the standard folder layout and test setup for a new CLI.", "bare"),
    ("greenfield", "implicit", None,
     "Give me a starting point for a React app.", "bare"),
    ("greenfield", "implicit", None,
     "There's nothing in this repo yet. I want to build a Slack bot.", "bare"),
    ("greenfield", "implicit", None,
     "I have an idea for a task queue service, but nothing is written yet.", "bare"),
    ("greenfield", "implicit", None,
     "Get me from zero to a green test run for a new Python service.", "bare"),
    ("greenfield", "implicit", None,
     "I want a working skeleton before I add any real logic.", "bare"),
    ("greenfield", "implicit", None,
     "This directory is empty. Help me get a Node project going.", "bare"),
    ("greenfield", "implicit", None,
     "We're kicking off a new inventory service, nothing exists yet.", "bare"),
    ("greenfield", "implicit", None,
     "I want the usual project layout before I write a line of code.", "bare"),

    # ---- greenfield: agent-decided (bare repo, task implies no app exists) ----
    ("greenfield", "agent-decided", None, "Add a health-check endpoint.", "bare"),
    ("greenfield", "agent-decided", None, "Write a test for the login flow.", "bare"),
    ("greenfield", "agent-decided", None, "Set up CI for this repo.", "bare"),
    ("greenfield", "agent-decided", None, "Fix the bug in the login handler.", "bare"),
    ("greenfield", "agent-decided", None, "Add input validation to the signup form.", "bare"),
    ("greenfield", "agent-decided", None, "Wire up the database connection.", "bare"),
    ("greenfield", "agent-decided", None,
     "Add a /users endpoint that returns a list of users.", "bare"),
    ("greenfield", "agent-decided", None, "Write the README for this project.", "bare"),

    # ---- greenfield-negative == agile-positive on fresh (dual-scored) ----
    ("agile", "negative", "implicit", "Add pagination to the order export.", "fresh"),
    ("agile", "negative", "explicit",
     "Fix the bug where placeOrder ignores quantity.", "fresh"),
    ("agile", "negative", "explicit",
     "I want to add rate limiting to the export endpoint.", "fresh"),
    ("agile", "negative", "implicit", "The export times out on big accounts.", "fresh"),
    ("agile", "negative", "implicit",
     "Users can double-submit and get charged twice.", "fresh"),
    ("agile", "negative", "implicit", "We need CSV upload in the admin panel.", "fresh"),
    ("agile", "negative", "implicit", "Make placeOrder reject empty carts.", "fresh"),
    ("agile", "negative", "implicit", "The retry loop gives up too early.", "fresh"),

    # ---- agile: explicit-only (must keep passing) ----
    ("agile", None, "explicit", "Implement the CSV import feature.", "fresh"),
    ("agile", None, "explicit", "Build the next slice.", "mid"),
    ("agile", None, "explicit", "I want to remove the order export module.", "fresh"),
    ("agile", None, "explicit",
     "Modify the code so the export paginates with cursors.", "fresh"),

    # ---- agile: implicit-only (feature/bug/chore/refactor/third-party) ----
    ("agile", None, "implicit", "Can you wire the orders table to the new dashboard?", "fresh"),
    ("agile", None, "implicit",
     "Deleting a user leaves orphaned sessions lying around, sort it out.", "fresh"),
    ("agile", None, "implicit", "My PM wants order totals shown in cents, not floats.", "fresh"),
    ("agile", None, "implicit", "The db.js pool never gets closed in tests, clean it up.", "fresh"),
    ("agile", None, "implicit",
     "Finance wants a CSV export of last month's orders by Friday.", "fresh"),
    ("agile", None, "implicit",
     "exportOrders is slow because it scans the whole table, speed it up.", "fresh"),
    ("agile", None, "implicit",
     "Support keeps getting tickets about orders not showing after checkout.", "fresh"),
    ("agile", None, "implicit", "Let's rename `total` to `orderTotal` throughout placeOrder.", "fresh"),
    ("agile", None, "implicit",
     "The pagination in exportOrders breaks once you pass page 50.", "mid"),

    # ---- agile-negative: not greenfield-on-bare (spike/harness/adr/question) ----
    (None, None, "negative", "Let's prototype this idea before building it for real.", "fresh"),
    (None, None, "negative", "Setup my repo for Claude.", "fresh"),
    (None, None, "negative", "Record this architecture decision.", "fresh"),
    (None, None, "negative", "What does exportOrders return?", "fresh"),
    (None, None, "negative", "Let's do a spike on it.", "fresh"),
]


def run_one(case, cwd):
    """Like adr-gauge.run_one: records every Skill call in the run, not just
    the first, and reports whether each of greenfield/agile fired anywhere."""
    owner, gf_group, ag_group, query, _ = case
    try:
        proc = subprocess.run(
            ["claude", "-p", query,
             *[a for d in gauge.PLUGIN_DIRS for a in ("--plugin-dir", d)],
             "--output-format", "stream-json", "--verbose",
             "--max-turns", str(gauge.TURNS), "--setting-sources", "project"]
            + (["--model", gauge.MODEL] if gauge.MODEL else []),
            cwd=cwd, capture_output=True, text=True,
            stdin=subprocess.DEVNULL, timeout=420)
    except subprocess.TimeoutExpired:
        return case, [], False, False

    tools, skills = [], []
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
            if b["name"] == "Skill":
                skills.append(b.get("input", {}).get("skill", "").split(":")[-1])
    return case, tools, "greenfield" in skills, "agile" in skills


def score(case, gf_fired, ag_fired):
    """Return list of (bucket_key, hit) for the buckets this case scores
    into, plus whether it counts as a cross-fire."""
    owner, gf_group, ag_group, _, _ = case
    results = []
    cross = False

    if gf_group is not None:
        if owner == "greenfield":
            results.append((("greenfield", gf_group), gf_fired))
        elif gf_group == "negative":  # owner == "agile": greenfield must stay off
            results.append((("greenfield", "negative"), not gf_fired))

    if ag_group is not None:
        if owner == "agile":
            results.append((("agile", ag_group), ag_fired))
        elif ag_group == "negative":  # owner is "greenfield" or None: agile must stay off
            results.append((("agile", "negative"), not ag_fired))

    if owner == "greenfield" and ag_fired:
        cross = True
    if owner == "agile" and gf_fired:
        cross = True

    return results, cross


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=7)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--skill", choices=("greenfield", "agile"),
                     help="only run cases relevant to this skill's buckets")
    ap.add_argument("--group", help="substring filter on the group name "
                     "(explicit, implicit, agent-decided, negative)")
    ap.add_argument("--grep", help="substring filter on the query text")
    ap.add_argument("--model", action="store_true",
                     help="use sonnet; omit to use gauge.py's harness default")
    args = ap.parse_args()
    if args.model:
        gauge.MODEL = "sonnet"

    root = os.path.join(REPO, ".gauge-fixtures")
    subprocess.run(["rm", "-rf", root], check=True)
    os.makedirs(root)
    fresh, mid, bare = gauge.build_fixtures(root)
    paths = {"fresh": fresh, "mid": mid, "bare": bare}

    def relevant(case):
        owner, gf_group, ag_group, query, _ = case
        if args.skill == "greenfield" and gf_group is None:
            return False
        if args.skill == "agile" and ag_group is None:
            return False
        if args.group and args.group.lower() not in {(gf_group or "").lower(),
                                                       (ag_group or "").lower()}:
            return False
        if args.grep and args.grep.lower() not in query.lower():
            return False
        return True

    selected = [c for c in CASES if relevant(c)] * args.repeat
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda c: run_one(c, paths[c[4]]), selected))

    buckets, cross_fire, n_cross_eligible = {}, 0, 0
    for case, tools, gf_fired, ag_fired in results:
        owner, gf_group, ag_group, query, fixture = case
        row_results, cross = score(case, gf_fired, ag_fired)
        for bucket, hit in row_results:
            buckets.setdefault(bucket, []).append(hit)
        if owner in ("greenfield", "agile"):
            n_cross_eligible += 1
            if cross:
                cross_fire += 1
        got = f"gf={gf_fired} ag={ag_fired}"
        tag = "/".join(filter(None, [f"gf:{gf_group}" if gf_group else None,
                                      f"ag:{ag_group}" if ag_group else None]))
        status = "FAIL" if any(not h for _, h in row_results) else "PASS"
        marker = " XFIRE" if cross else ""
        print(f"{status}  [{tag:24s}] {got:16s}{marker}  {query[:56]}")
        if status == "FAIL":
            print(f"        tools: {tools}")

    print()
    per_skill = {"greenfield": [], "agile": []}
    for (skill, group), hits in sorted(buckets.items()):
        print(f"  {skill:10s} {group:14s} {sum(hits)}/{len(hits)}")
        per_skill[skill].extend(hits)

    print()
    overall = 0
    overall_n = 0
    for skill in ("greenfield", "agile"):
        hits = per_skill[skill]
        rate = sum(hits) / len(hits) if hits else 0.0
        print(f"  {skill:10s} TOTAL {sum(hits)}/{len(hits)}  ({rate:.0%})")
        overall += sum(hits)
        overall_n += len(hits)
    overall_rate = overall / overall_n if overall_n else 0.0
    print(f"  {'overall':10s} TOTAL {overall}/{overall_n}  ({overall_rate:.0%})")
    print(f"  cross-fire: {cross_fire}/{n_cross_eligible}")

    ok = (per_skill["greenfield"] and sum(per_skill["greenfield"]) / len(per_skill["greenfield"]) >= 0.85
          and per_skill["agile"] and sum(per_skill["agile"]) / len(per_skill["agile"]) >= 0.85
          and cross_fire == 0)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
