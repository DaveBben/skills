#!/usr/bin/env python3
"""status.py <run-dir> <base-sha> <last-turn.jsonl>: print 'done' or 'resume: <why>'.
Done means some ref or worktree holds a committed change to a non-test file,
no worktree is dirty, and the last message does not end on a question."""
import json, re, subprocess, sys, pathlib
run, base, log = sys.argv[1:4]
repo = pathlib.Path(run) / "repo"
g = lambda *a, cwd=repo: subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True).stdout
TEST = re.compile(r"(^|/)(tests?|__tests__)/|_test\.go$|\.test\.ts$|(^|/)test_[^/]*\.py$")
changed = False
for ref in g("for-each-ref", "--format=%(refname)", "refs/heads").split():
    files = g("diff", "--name-only", f"{base}...{ref}").split()
    if any(not TEST.search(f) and not f.endswith((".md", ".mdx", ".rst")) for f in files):
        changed = True
dirty = [l.split()[1] for l in g("worktree", "list", "--porcelain").splitlines() if l.startswith("worktree ")
         if [x for x in g("status", "--porcelain", "--untracked-files=no", cwd=l.split()[1]).splitlines() if not x.endswith("uv.lock")]]
last = ""
for line in open(log):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("type") == "result":
        last = d.get("result") or ""
asks = "?" in last.strip()[-400:] and "DONE" not in last[-50:]
why = [w for w, bad in (("no committed source change", not changed), (f"dirty worktree {dirty}", dirty), ("ends on a question", asks)) if bad]
print("done" if not why else "resume: " + "; ".join(why))
