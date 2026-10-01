#!/usr/bin/env python3
"""grade.py <run-id>: grade one finished run in place; writes runs/<id>/grade.json."""
import json, os, re, subprocess, sys, glob, xml.etree.ElementTree as ET
X = os.path.expanduser("~/projects/sdlc-experiment")
rid = sys.argv[1]; task = rid.split("-")[0]
run = f"{X}/runs/{rid}"; repo = f"{run}/repo"
env = dict(os.environ, PATH=f"{X}/tools/node_modules/.bin:" + os.environ["PATH"])
def sh(cmd, cwd=repo, timeout=1800):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, errors="replace", env=env, timeout=timeout)
    return p.returncode, p.stdout + p.stderr
cfg = dict(re.findall(r'^(\w+)=["\']?(.*?)["\']?$', open(f"{X}/tasks/{task}/task.env").read(), re.M))
BASE, MERGE = cfg["BASE"], cfg["MERGE"]
hidden_files = cfg["HIDDEN_FILES"].split()
K = cfg.get("KIND", task)  # the base task whose cache, hidden tests and runner this variant shares
hidden = cfg["HIDDEN_TESTS"].split("|") if K == "zod" else cfg["HIDDEN_TESTS"].split()
out = {"id": rid, "task": task, "arm": rid.split("-")[1]}

# 1. the result: newest branch that differs from base; note uncommitted work
dirty = []
for l in sh("git worktree list --porcelain")[1].splitlines():
    if l.startswith("worktree "):
        w = l.split(" ", 1)[1]
        if [x for x in sh("git status --porcelain --untracked-files=no", cwd=w)[1].splitlines() if not x.endswith("uv.lock")]:
            dirty.append(w)
out["dirty_worktrees"] = dirty
refs = [r for r in sh("git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/heads")[1].split()
        if sh(f"git diff --quiet {BASE} {r}")[0] != 0]
out["branches"] = refs
if not refs and "-base-" in rid: refs = ["main"]
if not refs:
    out["result"] = "no committed change"; json.dump(out, open(f"{run}/grade.json", "w"), indent=1); print(json.dumps(out)); sys.exit()
ref = refs[0]; out["graded_ref"] = ref
sh("git stash -u -q"); sh(f"git checkout -q --detach {ref}")

# 2. diff size by kind (the hidden test files still count as the agent's own edits here)
def kind(f):
    if re.search(r"(^|/)(tests?|__tests__)/|_test\.go$|\.test\.ts$|(^|/)test_[^/]*\.py$|typing-examples/", f): return "test"
    if re.search(r"\.(md|mdx|rst)$|(^|/)(docs|changelog\.d)/", f): return "docs"
    return "src"
size = {"src": [0, 0], "test": [0, 0], "docs": [0, 0]}; files = {"src": [], "test": [], "docs": []}
for l in sh(f"git diff --numstat {BASE} HEAD")[1].splitlines():
    a, d, f = l.split("\t"); k = kind(f)
    if f.endswith("uv.lock"): continue
    if a != "-": size[k][0] += int(a); size[k][1] += int(d)
    files[k].append(f)
# the red commit: the first commit after base that touches only test files; edits to those files afterwards
red = next((c for c in sh(f"git rev-list --reverse {BASE}..HEAD")[1].split()
            if (fs := sh(f"git diff-tree --no-commit-id --name-only -r {c}")[1].split()) and all(kind(f) == "test" for f in fs)), None)
out["red_commit"] = red
if red:
    rf = sh(f"git diff-tree --no-commit-id --name-only -r {red}")[1].split()
    ch = [l.split("\t") for l in sh(f"git diff --numstat {red} HEAD -- " + " ".join(rf))[1].splitlines()]
    out["red_test_lines_changed_after"] = sum(int(a) + int(d) for a, d, _ in ch if a != "-")
out["diff"] = size; out["files"] = files; out["commits"] = int(sh(f"git rev-list --count {BASE}..HEAD")[1])
sh(f"git diff {BASE} HEAD > {run}/result.diff")

# 3. the full suite with the agent's own tests
rc, txt = sh(cfg["SUITE"].replace(" | tail -30", ""))
out["suite_exit"] = rc
tail = "\n".join(txt.strip().splitlines()[-8:])
out["suite_tail"] = tail

# 4. hidden upstream tests overlaid on the agent's code
for f in hidden_files:
    if os.path.exists(f"{X}/tasks/{K}/hidden_test.go"):
        sh(f"cp {X}/tasks/{K}/hidden_test.go {f}")
    else:
        sh(f"git -C {X}/cache/{K}.git show {MERGE}:{f} > {f}")
res = {}
if K in ("chi", "cli"):
    rc, txt = sh("go test -count=1 -v -run '.' . 2>&1")
    for name in hidden:
        m = re.search(rf"--- (PASS|FAIL): {name} ", txt)
        res[name] = m.group(1) == "PASS" if m else False
    other_fail = [n for n in re.findall(r"--- FAIL: (\S+)", txt) if n.split("/")[0] not in hidden]
    compile_err = "build failed" in txt or "[setup failed]" in txt
elif K == "attrs":
    rc, txt = sh(f".venv/bin/python -m pytest -q -p no:cacheprovider -rA {' '.join(hidden_files)} 2>&1")
    for name in hidden:
        m = re.search(rf"^(PASSED|FAILED|ERROR) \S+::{name}\b", txt, re.M)
        res[name] = bool(m) and m.group(1) == "PASSED"
    other_fail = [n for n in re.findall(r"^(?:FAILED|ERROR) \S+::(\w+)", txt, re.M) if n not in hidden]
    compile_err = False
elif K == "llama":
    def tree(out):
        st, res = [], {}
        for line in out.splitlines():
            m = re.match(r"^( *)(\S.*?)(?: \(\d+ assertion\(s\)\))?(?:\s+\[(PASS|FAIL)\])?\s*$", line)
            if not m or line.startswith(("tests ", "assertions ", "failures ", "exceptions ", "skipped ")): continue
            depth = len(m.group(1)) // 2; st[depth:] = [m.group(2).strip()]
            if m.group(3): res[" > ".join(st)] = m.group(3) == "PASS"
        return res
    rc, txt = sh("cmake --build build -j 8 --target test-peg-parser test-chat-peg-parser > build-hidden.log 2>&1 || grep -E ' error' build-hidden.log | head -20; ./build/bin/test-peg-parser 2>&1; ./build/bin/test-chat-peg-parser 2>&1", timeout=3600)
    r = tree(txt)
    want = [k for k in r if re.search(r"until parser > malformed UTF-8 > case \d|malformed UTF-8 rescanned by backtracking$|invalid utf8 > (replaced in reasoning and content|partial input keeps trailing incomplete sequence out)$", k)]
    hidden = want if len(want) == 10 else [f"case {i}" for i in range(10)]
    res = {k: r.get(k, False) for k in hidden}
    other_fail = [k for k, v in r.items() if not v and k not in res and not any(k2.startswith(k + " > ") for k2 in res)]
    compile_err = not r
else:
    j = f"{run}/vitest-hidden.json"
    rc, txt = sh(f"nub exec --node vitest run {hidden_files[0]} --reporter=json --outputFile={j} 2>&1")
    tests = []
    try:
        for fr in json.load(open(j))["testResults"]:
            tests += fr["assertionResults"]
    except Exception as e:
        txt += f"\n[no json: {e}]"
    for name in hidden:
        st = [t["status"] for t in tests if t["title"] == name or t["fullName"].endswith(name)]
        res[name] = bool(st) and all(s == "passed" for s in st)
    other_fail = sorted({t["title"] for t in tests if t["status"] == "failed" and t["title"] not in hidden})
    compile_err = not tests
out["hidden"] = res; out["hidden_pass"] = sum(res.values()); out["hidden_total"] = len(res)
out["hidden_file_other_failures"] = other_fail; out["hidden_compile_error"] = compile_err
open(f"{run}/hidden.log", "w").write(txt)
sh("git checkout -q -- . && git clean -fdq -e .venv -e node_modules")

# 5. cost and process, summed over every turn
cost = dur = turns = 0; skills = set(); agents = {}; tools = {}; hooks = {}
for lf in sorted(glob.glob(f"{run}/log/turn*.jsonl")):
    fcost = 0
    for line in open(lf):
        try: d = json.loads(line)
        except ValueError: continue
        if d.get("type") == "result":
            fcost = max(fcost, d.get("total_cost_usd") or 0); dur += d.get("duration_ms") or 0; turns += d.get("num_turns") or 0
        if d.get("type") == "system" and d.get("subtype") == "hook_response":
            hk = d.get("hook_name") or "?"; hooks[hk] = hooks.get(hk, 0) + 1
            if d.get("exit_code") not in (0, None): hooks[hk + " NONZERO"] = hooks.get(hk + " NONZERO", 0) + 1
        if d.get("type") == "assistant":
            for c in d["message"].get("content", []):
                if c.get("type") == "tool_use":
                    tools[c["name"]] = tools.get(c["name"], 0) + 1
                    if c["name"] == "Skill": skills.add(c["input"].get("skill"))
                    if c["name"] in ("Agent", "Task"):
                        a = c["input"].get("subagent_type", "general"); agents[a] = agents.get(a, 0) + 1
    cost += fcost
out.update(cost_usd=round(cost, 2), api_minutes=round(dur / 60000, 1), turns=turns, skills=sorted(filter(None, skills)),
           subagents=agents, tool_calls=tools, hooks=hooks, session_turns=len(glob.glob(f"{run}/log/turn*.jsonl")))
try: out["wall_minutes"] = round((int(open(f"{run}/end").read()) - int(open(f"{run}/start").read())) / 60, 1)
except Exception: pass
json.dump(out, open(f"{run}/grade.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("id", "hidden_pass", "hidden_total", "suite_exit", "diff", "cost_usd") if k in out}))
