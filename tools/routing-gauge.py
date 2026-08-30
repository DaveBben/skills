#!/usr/bin/env python3
"""Measure routing accuracy for the sdlc skills against ten
misroute scenarios: solution-as-requirement, story-as-contract, incident-as-
patch, received-spec-as-contract, trivial-bypass, greenfield-as-feature,
boilerplate-renovation, deadline-as-1:1-port, removal-as-subtraction, and
optimize-before-measure.

Unlike tools/gauge.py, which scores "which skill fired first", this scores
whether the *routing decision inside the run* matched the scenario's correct
route, including hand-backs between stages (for example the design stage offering
a return to discovery when the survey exposes holes). That requires reading
the transcript, not just the first Skill tool call, so each run is graded by
a second, judge-only `claude -p` call fed the transcript and the scenario's
signal/exit-test text.

Usage:
    python3 tools/routing-gauge.py                  # all ten scenarios
    python3 tools/routing-gauge.py --only 3          # one scenario by id
    python3 tools/routing-gauge.py --jobs 4
"""
import argparse
import json
import os
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_DIR = os.path.join(REPO, "plugins", "sdlc")
TURNS = 14
TIMEOUT = 480

FILES = {
    "package.json": '{ "name": "orders-api", "version": "0.4.1",\n'
                    '  "scripts": { "test": "jest" },\n'
                    '  "dependencies": { "express": "^4.19.0", "pg": "^8.11.0" } }\n',
    "README.md": "# orders-api\n\nExpress + Postgres service handling order "
                 "placement, payment capture and export. Has a pipeline that "
                 "runs order-export batches, and an upload endpoint for bulk "
                 "order CSVs. Talks to a partner risk-scoring model over a "
                 "vendor API. Operators watch order volume on a small live "
                 "dashboard at `public/dashboard.html`.\n",
    "public/dashboard.html": """<!doctype html>
<title>orders-api operator dashboard</title>
<!-- Shows live order volume and upload status for on-call operators. -->
<div id=\"stats\"></div>
""",
    "docs/partner-webhook-spec.md": """# Partner webhook spec (received, not authored by us)

**Schema:** POST JSON `{ orderId, status, amount, currency }` to our endpoint.

**Signature:** header `X-Partner-Signature: sha256=<hmac>`, computed over the
raw request body with a shared secret.

**Response codes:** we must return 200 on success. The partner retries on
any non-2xx response, up to 5 times with exponential backoff, for 24 hours.

**Timeout:** the partner's client gives up and logs a failure if our
response takes longer than 5 seconds.

**Ordering:** the partner does not guarantee delivery order across events
for the same order.
""",
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
    "src/riskScore.js": """// Calls the vendor's model to score fraud risk on an order.
async function scoreOrder(order) {
  const res = await fetch(process.env.VENDOR_URL, { method: 'POST', body: JSON.stringify(order) });
  return res.json();
}
module.exports = { scoreOrder };
""",
    "src/upload.js": """// Bulk order CSV upload endpoint.
async function handleUpload(fileBuffer) {
  return { accepted: true, rows: fileBuffer.toString().split('\\n').length };
}
module.exports = { handleUpload };
""",
    "tests/orders.test.js": """const { placeOrder } = require('../src/orders');
test('places an order and totals it', async () => {
  const o = await placeOrder('u1', [{ price: 10, qty: 2 }]);
  expect(o.total).toBe(20);
});
""",
}

BARE = {
    "README.md": "# fleet-telemetry\n\nNothing built yet. Intended to ingest "
                 "vehicle telemetry and serve it back to fleet operators.\n",
    ".gitignore": "node_modules/\n.env\n",
}

# A repo with no users, no persisted state, and nothing depending on it --
# for the boilerplate-renovation scenario.
# A running service in the same domain as the "search my summaries" story,
# so the domain itself isn't the ambiguity -- only the tenancy invariant is.
DIGEST = {
    "README.md": "# digest-api\n\nEmails each subscriber a weekly digest of "
                 "their saved articles. Summaries are generated per "
                 "subscriber and stored for lookup.\n",
    "package.json": '{ "name": "digest-api", "version": "0.2.0",\n'
                    '  "dependencies": { "express": "^4.19.0", "pg": "^8.11.0" } }\n',
    "src/summaries.js": """const db = require('./db');
async function getSummariesForSubscriber(subscriberId) {
  return db.query('SELECT * FROM summaries WHERE subscriber_id = $1', [subscriberId]);
}
module.exports = { getSummariesForSubscriber };
""",
    "src/db.js": """const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
module.exports = { query: (q, p) => pool.query(q, p) };
""",
    "tests/summaries.test.js": """const { getSummariesForSubscriber } = require('../src/summaries');
test('returns a subscriber\\'s summaries', async () => {
  const rows = await getSummariesForSubscriber('sub_1');
  expect(Array.isArray(rows)).toBe(true);
});
""",
}

BOILERPLATE = {
    "README.md": "# my-cli-starter\n\nGeneric starter template scaffolded "
                 "from `create-cli-app`. Not customized. No one has started "
                 "using this yet.\n",
    "package.json": '{ "name": "my-cli-starter", "version": "0.0.1",\n'
                    '  "bin": { "my-cli-starter": "./bin/index.js" },\n'
                    '  "dependencies": { "commander": "^11.0.0" } }\n',
    "bin/index.js": """#!/usr/bin/env node
// Boilerplate entry point from the template generator. Replace this.
const { Command } = require('commander');
const program = new Command();
program.name('my-cli-starter').description('TODO: describe this CLI').version('0.0.1');
program.command('hello').action(() => console.log('Hello from the template!'));
program.parse();
""",
    "lib/example.js": """// Example module left by the scaffold generator. Unused.
function exampleFn() { return 42; }
module.exports = { exampleFn };
""",
}


def _git(cwd, *args):
    subprocess.run(["git", "-c", "user.email=g@g", "-c", "user.name=g", *args],
                   cwd=cwd, check=True, capture_output=True)


def _write_fixture(root, name, files):
    path = os.path.join(root, name)
    for rel, body in files.items():
        p = os.path.join(path, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(body)
    _git(path, "init", "-q")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "initial")
    return path


def build_fixtures(root):
    fresh = _write_fixture(root, "fresh", FILES)
    bare = _write_fixture(root, "bare", BARE)
    boilerplate = _write_fixture(root, "boilerplate", BOILERPLATE)
    digest = _write_fixture(root, "digest", DIGEST)
    return fresh, bare, boilerplate, digest


def scenarios(fresh, bare, boilerplate, digest):
    return [
        dict(
            id=1, name="solution-as-requirement", cwd=fresh,
            query="I want to receive an email when my pipeline is done.",
            signal="Request names a delivery mechanism (email) as the object "
                   "of the verb, before stating what problem the notification "
                   "solves.",
            correct="Route to discovery: "
                    "recover the need under the mechanism (how do you find out "
                    "something is wrong, what happens today when nothing "
                    "arrives) before writing an email contract into the spec. The 'when "
                    "it's done' framing also can't fire if the pipeline never "
                    "runs, which is the likely worst failure.",
            wrong="Jumping straight to specifying the email (recipients, "
                  "subject, body) without questioning whether email or "
                  "'done' are the right concepts.",
            exit_test="The transcript shows the agent asking what the user will "
                      "do with the notification and/or what happens today when "
                      "it doesn't arrive, BEFORE or INSTEAD OF designing the "
                      "email's fields. It should not silently start speccing "
                      "recipients/subject/body as if email were already agreed.",
        ),
        dict(
            id=2, name="story-as-contract", cwd=digest,
            query="Story's refined and accepted: as a subscriber I want to "
                  "search my summaries by keyword. Let's build it.",
            signal="Input is a formatted user story with acceptance implied "
                   "('refined and accepted'), plus a possessive pronoun over "
                   "user-scoped data ('my summaries').",
            correct="Treat the story as settled on 'is this worth having', not "
                    "as a complete contract. Derive what the acceptance "
                    "criteria are silent on: empty results, pagination/large "
                    "result sets, matching semantics, and critically the "
                    "authorization/tenancy invariant hidden in 'my summaries' "
                    "(a subscriber must only ever get their own results).",
            wrong="Going straight to writing tests/implementation for search-"
                  "by-keyword without ever surfacing the tenancy/authorization "
                  "invariant or the silent acceptance-criteria gaps.",
            exit_test="The transcript surfaces the authorization/tenancy "
                      "invariant ('my summaries' scoping to the requesting "
                      "user) explicitly as something to test, not just "
                      "matching/search behavior. It does not treat the "
                      "acceptance criteria as a complete, ready-to-implement "
                      "contract without any further questions.",
        ),
        dict(
            id=3, name="incident-fix-as-patch", cwd=fresh,
            query="Postmortem action item: increase the token limit and add a "
                  "length check.",
            signal="Input references a postmortem/incident and proposes a "
                   "specific code change (a diagnosis with a fix already "
                   "attached).",
            correct="Diagnose backwards from the incident, at verify to find "
                    "the earliest step that would have caught it, rather than "
                    "applying the proposed fix directly. Likely lands on "
                    "implementation: the contract never specified what 'done'/"
                    "'complete' output means, so truncation had no defined "
                    "failure behavior. The raised limit only reduces the rate; "
                    "it does not specify the behavior.",
            wrong="Directly implementing 'increase the token limit and add a "
                  "length check' as stated, without asking which step of the "
                  "process failed to catch this originally.",
            exit_test="The transcript explicitly asks/reasons about which step "
                      "or boundary was missed (e.g. was truncation ever "
                      "specified, was there a check for it) BEFORE just "
                      "raising the limit. It should not treat the postmortem's "
                      "proposed fix as already-settled work to implement.",
        ),
        dict(
            id=4, name="received-spec-as-contract", cwd=fresh,
            query="Partner published their webhook spec. Schema, signature, "
                  "response codes. Implement it.",
            signal="Input references an externally authored spec (partner's "
                   "webhook contract) and asks to implement it directly.",
            correct="Recognize the spec defines the sender's obligations, not "
                    "yours. Derive your own implied obligations (e.g. 'we "
                    "retry on non-2xx' implies you must be idempotent; a "
                    "stated timeout is an architecture decision). Treat this "
                    "return edge to the contract as closed/costly since it's "
                    "a third party's spec.",
            wrong="Building directly against the spec as if it were a complete "
                  "contract for your side, without deriving the unstated "
                  "obligations it places on you.",
            exit_test="The transcript identifies at least one obligation the "
                      "spec implies but does not state (idempotency from "
                      "retry-on-failure, or a timeout/architecture "
                      "consequence), before or instead of just building "
                      "against the documented schema.",
        ),
        dict(
            id=5, name="trivial-bypass", cwd=fresh,
            query="Just adding one log line, it's nothing.",
            signal="Minimizing language ('just', 'nothing') attached to a "
                   "change to running code (this repo has a real service).",
            correct="Treat 'trivial' as a claim about blast radius that needs "
                    "checking, not a size to accept at face value. At minimum "
                    "consider one concrete failure mode for the log line (I/O "
                    "blocking, null field crashing the logger, hot-loop log "
                    "volume, sensitive data in the log) before or while adding "
                    "it.",
            wrong="Adding the log line immediately with no consideration of "
                  "failure modes, because the user said it was trivial.",
            exit_test="The transcript names at least one specific failure mode "
                      "or risk for the log line (blocking I/O, sensitive data, "
                      "hot-loop volume, crash on null) and dismisses or "
                      "addresses it with a reason, rather than skipping "
                      "straight to the edit with no risk consideration "
                      "at all.",
        ),
        dict(
            id=6, name="greenfield-as-feature", cwd=bare,
            query="Starting a new service. Let's define the API contract.",
            signal="No existing codebase/deployment; creation language "
                   "('starting a new service'); repo has no system yet.",
            correct="Route to discovery rather than straight to implementation "
                    "(Contract): constraints/anti-goals, one-way vs two-way "
                    "door classification, and a walking skeleton before "
                    "feature-level API contract work.",
            wrong="Jumping directly into defining the API contract's shape as "
                  "if a running system and known archetype already existed.",
            exit_test="The transcript raises greenfield-specific concerns "
                      "(one-way vs two-way door decisions, scale/consistency/"
                      "tenancy constraints, or a walking skeleton) rather than "
                      "immediately drafting API contract details as a normal "
                      "feature change.",
        ),
        dict(
            id=7, name="boilerplate-renovation", cwd=boilerplate,
            query="This repo is all boilerplate. Turn it into a small CLI.",
            signal="Existing code described dismissively (boilerplate/"
                   "scaffold/starter) with no users or dependents mentioned "
                   "(and none exist in the repo).",
            correct="Salvage check: does anything depend on this code? No -> "
                    "tag/archive it and start clean in a new directory rather "
                    "than laboriously stripping it down, or rather than "
                    "treating this as a full greenfield/Phase-Zero exercise. "
                    "Name anything worth copying on purpose.",
            wrong="Either treating this as a serious Phase-Zero greenfield "
                  "architecture exercise, OR spending effort carefully "
                  "stripping down/refactoring the existing boilerplate file "
                  "by file.",
            exit_test="The transcript makes an explicit keep-vs-abandon call "
                      "about the existing boilerplate (e.g. tag and start "
                      "fresh, or name the one piece worth keeping) rather than "
                      "silently doing a big Phase-Zero workup OR silently "
                      "renovating the boilerplate in place piece by piece.",
        ),
        dict(
            id=8, name="deadline-as-1to1-port", cwd=fresh,
            query="Vendor's retiring our model version. 90 days. Port it.",
            signal="External date plus no-choice language (deprecat*, EOL, "
                   "sunset, forced, must migrate) plus a duration.",
            correct="Treat the deadline as removing only the existential-check "
                    "step, not as mandating a like-for-like port. Consider at "
                    "least one alternative to a 1:1 port, and schedule a "
                    "behavioral baseline capture from the outgoing vendor "
                    "model before it's shut off.",
            wrong="Directly swapping the endpoint/model version 1:1 with no "
                  "consideration of alternatives and no baseline capture "
                  "scheduled before shutoff.",
            exit_test="The transcript considers at least one alternative to a "
                      "pure like-for-like port, AND/OR raises the need to "
                      "capture a behavioral baseline from the current vendor "
                      "model before the 90-day shutoff, rather than jumping "
                      "straight to implementing the swap.",
        ),
        dict(
            id=9, name="removal-as-subtraction", cwd=fresh,
            query="Remove the upload feature. Replace it with an ambient "
                  "visual.",
            signal="Removal verb (remove) bundled with a conjunction "
                   "introducing an addition ('replace it with') in the same "
                   "sentence.",
            correct="Split into two changes with separate treatment: the "
                    "addition (ambient visual, its own privacy/surface "
                    "review) and the removal (upload feature, sequenced with "
                    "an explicit gate -- instrument usage, export data, "
                    "disable before delete). Note the replacement may not "
                    "serve the same users and may enlarge the input/privacy "
                    "surface despite less code.",
            wrong="Treating this as one bundled deletion/build task and "
                  "shipping both together as a single simple swap.",
            exit_test="The transcript explicitly treats the removal and the "
                      "addition as two separate changes/decisions (not one "
                      "bundled task), and raises that the 'ambient visual' "
                      "addition has its own risk/privacy surface distinct "
                      "from simply deleting the upload feature.",
        ),
        dict(
            id=10, name="optimize-before-measure", cwd=fresh,
            query="It's too slow. Let's add caching.",
            signal="Performance language ('too slow') with a named remedy "
                   "(caching) and no number/threshold anywhere in the "
                   "request.",
            correct="Ask for or establish a measured baseline and a target "
                    "threshold before designing the fix. Caching is a "
                    "consistency/staleness surface, not a free win, and "
                    "should not be assumed to be the right fix without first "
                    "confirming where the latency actually comes from.",
            wrong="Implementing caching immediately with no measured baseline, "
                  "no named threshold, and no check on whether caching "
                  "actually addresses the bottleneck.",
            exit_test="The transcript asks what's slow / how slow / compared "
                      "to what threshold, or otherwise insists on a measured "
                      "baseline before committing to caching as the fix, "
                      "rather than proceeding straight to a caching "
                      "implementation.",
        ),
    ]


def run_one(scenario):
    query, cwd = scenario["query"], scenario["cwd"]
    try:
        proc = subprocess.run(
            ["claude", "-p", query, "--plugin-dir", PLUGIN_DIR,
             "--output-format", "stream-json", "--verbose",
             "--max-turns", str(TURNS), "--setting-sources", "user"],
            cwd=cwd, capture_output=True, text=True,
            stdin=subprocess.DEVNULL, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return scenario, [], "TIMEOUT"

    transcript = []
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
            if b.get("type") == "text":
                transcript.append(("text", b["text"]))
            elif b.get("type") == "tool_use":
                name = b["name"]
                if name == "Skill":
                    name = f"Skill:{b.get('input', {}).get('skill', '')}"
                transcript.append(("tool", name))
    return scenario, transcript, None


def render_transcript(transcript):
    lines = []
    for kind, val in transcript:
        if kind == "tool":
            lines.append(f"[TOOL CALL] {val}")
        else:
            lines.append(f"[ASSISTANT TEXT] {val}")
    return "\n\n".join(lines)


def judge(scenario, transcript_text):
    prompt = f"""You are grading whether an AI coding agent routed a request correctly,
per a known-correct routing rubric. Do not re-derive the rubric; apply it.

REQUEST GIVEN TO THE AGENT:
{scenario['query']}

MISROUTE SIGNAL (why this request is a trap):
{scenario['signal']}

CORRECT ROUTE:
{scenario['correct']}

WRONG ROUTE (what a naive agent would do):
{scenario['wrong']}

EXIT TEST (what the transcript must show to PASS):
{scenario['exit_test']}

AGENT TRANSCRIPT (tool calls and assistant text, in order):
{transcript_text[:12000]}

Output EXACTLY one line first: "VERDICT: PASS" or "VERDICT: FAIL".
Then a one-sentence reason on the next line."""

    try:
        proc = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text",
             "--max-turns", "1", "--setting-sources", "user"],
            capture_output=True, text=True, stdin=subprocess.DEVNULL,
            timeout=120, cwd=REPO)
    except subprocess.TimeoutExpired:
        return None, "JUDGE TIMEOUT"

    out = proc.stdout.strip()
    first_line = out.splitlines()[0] if out else ""
    verdict = "PASS" in first_line.upper()
    reason = out.splitlines()[1] if len(out.splitlines()) > 1 else out
    return verdict, reason


def run_and_judge(scenario):
    scenario, transcript, err = run_one(scenario)
    if err:
        return scenario, None, err, ""
    text = render_transcript(transcript)
    verdict, reason = judge(scenario, text)
    return scenario, verdict, reason, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated scenario ids to run")
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--repeat", type=int, default=1,
                     help="run each scenario N times; a scenario that passes "
                          "some runs and fails others is variance, not a "
                          "wording defect -- flagged FLAKY")
    ap.add_argument("--save-transcripts", help="dir to dump raw transcripts")
    args = ap.parse_args()

    root = os.path.join(REPO, ".gauge-fixtures-routing")
    subprocess.run(["rm", "-rf", root], check=True)
    os.makedirs(root)
    fresh, bare, boilerplate, digest = build_fixtures(root)
    all_scenarios = scenarios(fresh, bare, boilerplate, digest)

    if args.only:
        ids = {int(x) for x in args.only.split(",")}
        all_scenarios = [s for s in all_scenarios if s["id"] in ids]

    all_scenarios = all_scenarios * args.repeat

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run_and_judge, all_scenarios))

    passed = 0
    per_scenario = {}
    for i, (scenario, verdict, reason, text) in enumerate(results):
        if args.save_transcripts:
            os.makedirs(args.save_transcripts, exist_ok=True)
            with open(os.path.join(args.save_transcripts,
                                    f"{scenario['id']:02d}-{scenario['name']}-{i}.txt"), "w") as fh:
                fh.write(text)
        tag = "PASS" if verdict else ("ERR " if verdict is None else "FAIL")
        if verdict:
            passed += 1
        per_scenario.setdefault(scenario["id"], []).append(bool(verdict))
        print(f"{tag}  #{scenario['id']:2d} {scenario['name']:28s} {reason}")

    print()
    if args.repeat > 1:
        for sid, hits in sorted(per_scenario.items()):
            flag = "  <-- FLAKY" if 0 < sum(hits) < len(hits) else ""
            print(f"  #{sid:2d}  {sum(hits)}/{len(hits)}{flag}")
        print()
    print(f"TOTAL {passed}/{len(results)}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
