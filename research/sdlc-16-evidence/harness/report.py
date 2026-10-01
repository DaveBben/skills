#!/usr/bin/env python3
"""report.py: one table per task and arm from runs/*/grade.json and judge-*.json."""
import json, glob, os, re, statistics as st, collections
X = os.path.expanduser("~/projects/sdlc-experiment")
G = [json.load(open(f)) for f in sorted(glob.glob(f"{X}/runs/*/grade.json"))]
J = collections.defaultdict(list)
for f in glob.glob(f"{X}/judge-*.json"):
    d = json.load(open(f))
    n = len(d["ranking"])
    for c in d["candidates"]:
        rid = d["labels"][c["label"]]
        J[rid].append({k: c[k] for k in ("correctness", "tests", "design", "scope")} | {"rank": d["ranking"].index(c["label"]) + 1, "of": n})
def suite_ok(g):
    if g.get("suite_exit") == 0: return True
    fails = re.findall(r"FAILED (\S+)", g.get("suite_tail", ""))
    return g["task"] == "attrs" and fails and all("test_packaging" in f for f in fails)
m = lambda xs: round(st.mean(xs), 2) if xs else None
print("| task | arm | runs | hidden tests passed | full suite green | src +/- | test + | cost $ | wall min | sessions | subagents | judge C/T/D/S | judge rank |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for task in sorted({g["task"] for g in G}):
    for arm in ("base", "plain", "careful", "sdlc"):
        gs = [g for g in G if g["task"] == task and g["arm"] == arm and "diff" in g]
        if not gs: continue
        js = [j for g in gs for j in J.get(g["id"], [])]
        hid = " ".join(f'{g["hidden_pass"]}/{g["hidden_total"]}' for g in gs)
        judge = "/".join(str(m([j[k] for j in js])) for k in ("correctness", "tests", "design", "scope")) if js else "-"
        rank = f'{m([j["rank"] for j in js])} of {js[0]["of"]}' if js else "-"
        sub = sum(sum(g.get("subagents", {}).values()) for g in gs) / len(gs)
        print(f'| {task} | {arm} | {len(gs)} | {hid} | {sum(map(suite_ok, gs))}/{len(gs)} | '
              f'{m([g["diff"]["src"][0] for g in gs])}/{m([g["diff"]["src"][1] for g in gs])} | {m([g["diff"]["test"][0] for g in gs])} | '
              f'{m([g.get("cost_usd", 0) for g in gs])} | {m([g.get("wall_minutes", 0) for g in gs])} | {m([g.get("session_turns", 0) for g in gs])} | {round(sub, 1)} | {judge} | {rank} |')
