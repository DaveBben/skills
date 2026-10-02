#!/usr/bin/env python3
"""Score each SDLC skill's description against 30 phrases the user types for it.

Reuses gauge.py's fixtures and methodology notes (read them before believing a
number). Adds a UI, an LED controller, an AGENTS.md and a story file to the
fresh fixture so phrases about them have something to land on, and stops each
session as soon as a skill fires instead of running out the turn budget.

Usage:
    python3 tools/trigger-gauge.py                   # every skill, sonnet
    python3 tools/trigger-gauge.py --only spike      # one skill's phrases
    python3 tools/trigger-gauge.py --repeat 2 --jobs 10
"""
import argparse
import json
import os
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gauge

TARGET = 0.85
TIMEOUT = 300

EXTRA = {
    "public/login.html": """<!doctype html>
<title>Sign in</title>
<form action="/login" method="post">
  <input type="email" name="email" placeholder="Email">
  <input type="password" name="password" placeholder="Password">
  <button>Sign in</button>
</form>
""",
    "public/dashboard.html": """<!doctype html>
<title>Orders dashboard</title>
<style>.toast { transition: opacity 300ms; }</style>
<div id="orders"></div><div class="toast" id="toast"></div>
<script>
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.style.opacity = 1;
  setTimeout(() => { t.style.opacity = 0; }, 2000);
}
fetch('/orders').then(r => r.json()).then(rows => {
  document.getElementById('orders').textContent = rows.length + ' orders';
});
</script>
""",
    "firmware/status_led.py": """# Drives the RGB status LED on the packing-station controller.
from machine import Pin

RED, GREEN, BLUE = Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT)

def set_color(r, g, b):
    RED.value(r); GREEN.value(g); BLUE.value(b)

def on_order_status(status):
    if status == "paid":
        set_color(0, 1, 0)
""",
    "AGENTS.md": """# orders-api

Express + Postgres service. Run `npm test` before committing.

## Layout
- src/ holds the service code; src/db.js is the only module that talks to Postgres.
- public/ holds the operator pages.
- firmware/ holds the packing-station LED controller (MicroPython).

## Conventions
- Use async/await everywhere.
- Money is stored in cents.
- Write good code and follow best practices.
- Be careful with the database.
""",
    "docs/stories/cancel-order.md": """# Story: cancel an order

As a customer, I want to cancel an order within 30 minutes of placing it,
so that I am not charged for a mistake.

## Acceptance criteria
1. Given an order placed 10 minutes ago with status pending, when the customer
   cancels it, then its status becomes cancelled and no payment is captured.
2. Given an order placed 31 minutes ago, when the customer cancels it, then the
   request is refused with "Cancellation window has closed".
""",
}

# skill -> 30 phrases. A phrase prefixed with "mid:" runs in the fixture that
# has an uncommitted diff, for phrases about the user's changes.
PHRASES = {
    "adr": [
        "let's capture this adr",
        "make an adr",
        "this is an architecture decision",
        "this is an archtiecture decision",
        "write an ADR for switching the export to keyset pagination",
        "capture this as an adr",
        "can you adr this",
        "we decided to go with postgres over mongo, make an adr for it",
        "record this decision",
        "let's document this architecture decision",
        "log this decision in our ADRs",
        "add an adr for using express over fastify",
        "we're going with SQS instead of kafka for the export jobs. capture that",
        "write up the decision we just made about storing money in cents",
        "this is a big decision, let's get it written down as an ADR",
        "create an architecture decision record for the payment capture flow",
        "make a decision record for moving auth into its own service",
        "put this decision in docs/adr: we never hard delete orders",
        "adr this choice",
        "let's capture why we chose raw pg over an ORM",
        "new adr: we're dropping offset pagination",
        "we should write an adr for this",
        "can you write the architecture decision for the caching approach we picked",
        "document why we picked jest over vitest",
        "this needs an ADR",
        "let's capture this architecture decision before we forget",
        "I want to record that we accept the risk of double-capturing payments on retry",
        "make an architectural decision record",
        "capture this adr: orders are soft deleted, never hard deleted",
        "we chose to keep the firmware in the same repo as the api. record the reasoning",
    ],
    "guardrails": [
        "make a rule that every route handler validates its input",
        "make a rule for no console.log in src",
        "setup guardrails in this repo",
        "what rules are currently in my repo",
        "do I have guard rails in place",
        "can this be a semgrep rule? never build a SQL query with string concatenation",
        "make a rule for always awaiting db calls",
        "add a rule: no raw SQL outside src/db.js",
        "set up guardrails",
        "what guardrails does this repo have",
        "add linting to this repo",
        "setup a pre-commit hook that runs the tests",
        "claude keeps putting business logic in the route handlers, make it stop",
        "the agent keeps committing without running the tests, fix that",
        "can we enforce that money values are always integer cents?",
        "make it impossible to commit if the tests fail",
        "ban process.env outside a config module",
        "never let anything import pg outside src/db.js",
        "write a semgrep rule that catches unparameterized queries",
        "are there any rules enforced in this codebase?",
        "always use async/await instead of .then, make that a rule",
        "set up rules for this repo",
        "can we turn 'money is stored in cents' into a lint rule?",
        "check what guardrails are in place",
        "add a hook that runs the formatter whenever claude edits a file",
        "we have no linting or formatting, set it up",
        "should this be an eslint rule or a semgrep rule?",
        "make a rule so the agent always runs npm test before it says it's done",
        "which of the rules in my AGENTS.md could be enforced automatically?",
        "make a rule for y: every new endpoint needs a test",
    ],
    "orient": [
        "onboard claude to this repo",
        "orient claude to this repo",
        "setup my claude.md",
        "setup my agents file",
        "review my agents.md",
        "review my claude.md",
        "is my claude.md good",
        "is my agent.md too long?",
        "write an AGENTS.md for this repo",
        "create a CLAUDE.md",
        "get claude up to speed on this codebase",
        "onboard yourself to this repo",
        "orient yourself",
        "familiarize yourself with this codebase and write down what the next agent needs",
        "my claude.md is getting huge, trim it",
        "what should go in my claude.md?",
        "audit my CLAUDE.md",
        "can you improve my agents.md",
        "rewrite our CLAUDE.md",
        "does my agents.md have anything useless in it?",
        "is my CLAUDE.md missing anything important?",
        "set up the agent instructions file for this repo",
        "help claude understand this repo",
        "onboard an ai agent to this project",
        "generate a claude.md",
        "check my agents.md",
        "update AGENTS.md now that we've added the firmware folder",
        "is there too much in my agents file",
        "make CLAUDE.md a symlink to AGENTS.md and clean it up",
        "is my agents.md any good for claude?",
    ],
    "review-code": [
        "mid:review this code",
        "mid:do a code review",
        "look at this merge request: https://gitlab.com/acme/orders-api/-/merge_requests/42",
        "review this pull request: https://github.com/acme/orders-api/pull/88",
        "review src/orders.js",
        "mid:can you review my changes",
        "mid:review the diff",
        "mid:code review please",
        "give me a code review on the export function",
        "mid:look over my changes before I merge them",
        "is PR 17 ready to merge?",
        "review MR !42",
        "review PR #17",
        "check src/orders.js for bugs",
        "mid:can you look at my changes in src/orders.js and tell me what's wrong",
        "review the last commit",
        "do a security review of src/db.js",
        "critique my implementation of placeOrder",
        "take a look at this pull request https://github.com/acme/orders-api/pull/91",
        "mid:review what's on this branch",
        "is the code in src/orders.js any good?",
        "poke holes in my placeOrder function",
        "look at MR 42 and tell me if it's good",
        "mid:review my uncommitted changes",
        "i'd like a second pair of eyes on the orders module",
        "can you give feedback on my code in src/",
        "mid:review the code I just wrote",
        "do a pr review on #88",
        "any problems with merge request 42?",
        "mid:sanity check my diff before I push",
    ],
    "spike": [
        "let's do a demo of websockets for live order updates",
        "I want to make an expirement on caching order totals in redis",
        "let's do a spike on keyset pagination",
        "what would a stripe integration into my codebase look like?",
        "how would incorporating prisma into my code affect it",
        "how hard would it be to setup graphql here",
        "would it be feasible to reach 1000 orders a second using express",
        "let's prototype a csv export",
        "can we try out bullmq for the export jobs",
        "build a quick proof of concept for partner webhooks",
        "I want to experiment with replacing pg with drizzle",
        "let's see if sqlite would work for local dev",
        "is it feasible to run this on cloudflare workers?",
        "how much work would it be to add multi-tenancy",
        "what would it take to migrate this to typescript",
        "mock up an admin page for refunds",
        "let's try a couple of approaches to rate limiting and see which is best",
        "spike out an integration with the shipping API",
        "would bun speed up our test suite?",
        "how hard would it be to move from jest to vitest?",
        "build a throwaway to see if streaming the export works",
        "could we use postgres listen/notify instead of polling? try it",
        "let's experiment with an LLM to categorise orders",
        "what would adding opentelemetry to this codebase look like",
        "quick experiment: does connection pooling fix the slow export",
        "would it be possible to get the export under 200ms with an index",
        "let's build a demo of the checkout flow for friday's meeting",
        "how would switching to fastify affect the codebase",
        "test out whether redis caching makes placeOrder faster",
        "is it realistic to do real-time order tracking with server-sent events",
    ],
    "story": [
        "let's add a forgot email link",
        "let's add a timer to the ui",
        "I want modify how long transitions show",
        "let's add this feature: customers can cancel an order",
        "let's create a feature to export orders as csv",
        "I want to modify this feature so the dashboard refreshes every 10 seconds",
        "review this story: docs/stories/cancel-order.md",
        "implement this story: docs/stories/cancel-order.md",
        "I want the LED to turn red",
        "add a forgot password link to the login page",
        "users should be able to cancel an order within 30 minutes",
        "make the dashboard show total revenue for today",
        "add a dark mode toggle to the dashboard",
        "I want customers to get an email when their order ships",
        "change the toast so it stays up for 5 seconds",
        "let's let users filter orders by status",
        "add a button to retry failed payments",
        "the order total should include tax",
        "I want the export to include the customer's email",
        "let's add pagination to the order list",
        "can we show a spinner while the dashboard loads",
        "write a story for bulk order upload",
        "build the cancel order story",
        "are the acceptance criteria in docs/stories/cancel-order.md any good?",
        "make the LED blink blue while an order is being packed",
        "add a confirmation dialog before deleting an order",
        "I want admins to be able to refund an order",
        "let's make the login page remember the user's email",
        "can we add a countdown on the dashboard until the next export runs",
        "when a payment fails, show the user why",
    ],
}

NEGATIVE = [
    "What's the difference between optimistic and pessimistic locking?",
    "explain how keyset pagination works",
    "what does the -u flag do in git push?",
    "Run the test suite and show me the output.",
    "what does placeOrder do?",
    "summarise the README",
    "whats the difference between arq and celery?",
    "what is semgrep?",
]


def add_extras(fresh):
    for rel, body in EXTRA.items():
        path = os.path.join(fresh, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(body)
    os.symlink("AGENTS.md", os.path.join(fresh, "CLAUDE.md"))
    gauge._git(fresh, "add", "-A")
    gauge._git(fresh, "commit", "-qm", "ui, firmware, agents file, story")


def run_one(case):
    """Run one query; stop the session at the first Skill call."""
    query, expected, cwd = case
    cmd = ["claude", "-p", query,
           *[a for d in gauge.PLUGIN_DIRS for a in ("--plugin-dir", d)],
           "--output-format", "stream-json", "--verbose",
           "--max-turns", str(gauge.TURNS), "--setting-sources", "project",
           "--model", gauge.MODEL]
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                            text=True)
    tools, fired = [], None
    try:
        for line in proc.stdout:
            if not line.startswith("{"):
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") != "assistant":
                continue
            for b in d.get("message", {}).get("content", []):
                if b.get("type") == "tool_use":
                    tools.append(b["name"])
                    if b["name"] == "Skill":
                        fired = b.get("input", {}).get("skill", "").split(":")[-1]
            if fired:
                break
    finally:
        proc.kill()
        proc.wait()
    return query, expected, tools, fired


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated skills; 'none' for negatives")
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--model", default="sonnet")
    args = ap.parse_args()
    gauge.MODEL = args.model
    only = set(args.only.split(",")) if args.only else None

    root = os.path.join(gauge.REPO, ".gauge-fixtures")
    subprocess.run(["rm", "-rf", root], check=True)
    os.makedirs(root)
    fresh, mid, _ = gauge.build_fixtures(root)
    add_extras(fresh)
    add_extras(mid)

    cases = []
    for skill, phrases in PHRASES.items():
        if only and skill not in only:
            continue
        for p in phrases:
            cwd, q = (mid, p[4:]) if p.startswith("mid:") else (fresh, p)
            cases.append((q, skill, cwd))
    if not only or "none" in only:
        cases += [(q, None, fresh) for q in NEGATIVE]
    cases *= args.repeat

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run_one, cases))

    buckets = {}
    for query, expected, tools, fired in results:
        hit = (fired == expected) if expected else (fired not in gauge.OURS)
        buckets.setdefault(expected or "none", []).append(hit)
        if not hit:
            print(f"FAIL  want={expected or 'none':12s} got={fired or '(none)':12s} "
                  f"{query[:70]}  tools={tools[:6]}")
    print()
    ok = True
    for skill, hits in buckets.items():
        rate = sum(hits) / len(hits)
        ok &= rate >= TARGET or skill == "none"
        print(f"  {skill:12s} {sum(hits)}/{len(hits)}  ({rate:.0%})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
