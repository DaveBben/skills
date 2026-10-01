#!/usr/bin/env python3
"""judge.py <task> <seed>: blind-judge every graded run of a task; writes judge-<task>-<seed>.json."""
import json, glob, random, subprocess, sys, os, re
X = os.path.expanduser("~/projects/sdlc-experiment")
task, seed = sys.argv[1], int(sys.argv[2])
cfg = dict(re.findall(r'^(\w+)=["\']?(.*?)["\']?$', open(f"{X}/tasks/{task}/task.env").read(), re.M))
runs = sorted(r for r in glob.glob(f"{X}/runs/{task}-*-*") + (glob.glob(f"{X}/runs/llamah-*-*") if task == "llama" else []) if os.path.exists(f"{r}/result.diff") and "harness" not in r)
ARMS = os.environ.get("ARMS")
if ARMS:
    runs = [r for r in runs if os.path.basename(r).split("-")[1] in ARMS.split(",")]
random.Random(seed).shuffle(runs)
labels = {chr(65 + i): os.path.basename(r) for i, r in enumerate(runs)}
ref = subprocess.run(["git", "-C", f"{X}/cache/{task}.git", "diff", cfg["BASE"], cfg["MERGE"]], capture_output=True, text=True).stdout
STRIP = os.environ.get("STRIP_TESTS") == "1"
TESTPATH = r"diff --git a/\S*((^|/)(tests?|__tests__)/|_test\.go|\.test\.ts|/test_[^/ ]*\.py|typing-examples/)\S* .*?(?=^diff --git|\Z)"
def clean(d):  # drop lockfile noise, and every test file when STRIP_TESTS=1
    d = re.sub(r"diff --git a/uv.lock.*?(?=^diff --git|\Z)", "", d, flags=re.S | re.M)
    return re.sub(TESTPATH, "", d, flags=re.S | re.M) if STRIP else d
cands = "\n\n".join(f"=== CANDIDATE {l} ===\n{clean(open(f'{X}/runs/{r}/result.diff').read())}" for l, r in labels.items())
story = open(f"{X}/tasks/{task}/story.md").read()
prompt = f"""You are grading independent implementations of one change request against the repository {cfg['REPO']}. Each candidate is a diff against the same base commit. A read-only checkout of that base commit is at {X}/runs/{labels['A']}/judge-base; read any file there for context.

The change request given to every implementer:
<story>
{story}
</story>

The maintainers' merged change, for reference only. It is one good solution, not the only acceptable one; judge candidates on whether they meet the request and handle the cases a careful maintainer would, not on resemblance.
<reference>
{ref}
</reference>

{cands}

{"The candidates test files have been removed; judge the source changes only, and score tests 1 for all." if STRIP else ""}\nFor each candidate, find concrete defects: behaviour the request asks for that is missing or wrong, edge cases mishandled (exceptions, ordering, nesting, async, regressions to existing behaviour), tests that would pass on broken code, changes nobody asked for, and violations of the repository's conventions. Cite file and line. Then score each 1-5 on: correctness (does it do what the request says, including edge cases), tests (would they catch a wrong implementation), design (fits the codebase, minimal, maintainable), scope (only what was asked). Finally rank all candidates best to worst. Be strict and specific; do not reward length."""
schema = {"type": "object", "required": ["candidates", "ranking"], "properties": {
    "candidates": {"type": "array", "items": {"type": "object", "required": ["label", "defects", "correctness", "tests", "design", "scope", "summary"], "properties": {
        "label": {"type": "string"}, "defects": {"type": "array", "items": {"type": "string"}},
        "correctness": {"type": "integer"}, "tests": {"type": "integer"}, "design": {"type": "integer"}, "scope": {"type": "integer"},
        "summary": {"type": "string"}}}},
    "ranking": {"type": "array", "items": {"type": "string"}}}}
base = f"{X}/runs/{labels['A']}/judge-base"
if not os.path.exists(base):
    subprocess.run(["git", "-C", f"{X}/runs/{labels['A']}/repo", "worktree", "add", "-q", "--detach", base, cfg["BASE"]])
p = subprocess.run(["claude", "-p", prompt, "--model", "claude-opus-5-5", "--effort", "high", "--setting-sources", "", "--strict-mcp-config",
                    "--tools", "Read,Grep,Glob", "--add-dir", base, "--output-format", "json", "--json-schema", json.dumps(schema)],
                   capture_output=True, text=True, cwd=base)
d = json.loads(p.stdout)
res = d.get("structured_output") or json.loads(d["result"])
res["labels"] = labels; res["cost_usd"] = d.get("total_cost_usd")
json.dump(res, open(f"{X}/judge-{task}-{seed}{'-src' if STRIP else ''}{'-' + os.environ.get('TAG', '') if os.environ.get('TAG') else ''}.json", "w"), indent=1)
for c in res["candidates"]:
    print(labels[c["label"]], c["correctness"], c["tests"], c["design"], c["scope"], c["summary"][:120])
print("ranking", [labels[l] for l in res["ranking"]])
