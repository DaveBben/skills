#!/usr/bin/env python3
"""Checks that an experiment's run is complete and its raw outputs are intact, for the experiment skill.

Expects each run's raw outputs in RUNS/<unit>/<arm>/<run>/, with runs numbered from 1, and a
manifest.json in each run directory.

  * the run directories are exactly the planned units x arms x runs: none missing, none extra;
  * each manifest has harness_commit, seed, started_at, finished_at, and every --require field;
    an attempt above 1 has a rerun_reason; with --harness-tag, harness_commit is that tag's commit;
  * the ledger, in sha256sum format with paths relative to the ledger, lists every file under
    RUNS, and every listed hash matches its file.

Usage: check_run.py --units SELECTION --arms A,B --runs K [--runs-dir runs] [--ledger runs.sha256]
                    [--require model_id,input_tokens] [--harness-tag harness-v1]
SELECTION is the committed selection file, 1 unit ID per line.
Prints each failure and exits 1, or prints "run check passed". Run with --self-test to check it.
"""
import argparse, hashlib, json, os, subprocess, sys, tempfile

REQUIRED = ["harness_commit", "seed", "started_at", "finished_at"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def first(items):
    return f"{len(items)}, first: {'/'.join(items[0]) if isinstance(items[0], tuple) else items[0]}"


def check_ledger(runs_dir, ledger):
    try:
        lines = open(ledger, encoding="utf-8").read().splitlines()
    except OSError:
        return [f"no ledger at {ledger}: record a sha256 for every raw output"]
    base, listed, errs = os.path.dirname(os.path.realpath(ledger)), {}, []
    for line in filter(str.strip, lines):
        digest, _, name = line.partition(" ")
        listed[os.path.normpath(os.path.join(base, name.strip().lstrip("*")))] = digest
    gone = sorted(p for p in listed if not os.path.exists(p))
    changed = sorted(p for p in listed if os.path.exists(p) and sha256(p) != listed[p])
    on_disk = {os.path.join(r, f) for r, _, fs in os.walk(os.path.realpath(runs_dir)) for f in fs}
    unlisted = sorted(on_disk - set(listed))
    if gone:
        errs.append("files in the ledger are missing: " + first(gone))
    if changed:
        errs.append("files no longer match their ledger hash: " + first(changed))
    if unlisted:
        errs.append("files are not in the ledger: " + first(unlisted))
    return errs


def check(runs_dir, units, arms, runs, ledger, require=(), harness_commit=None):
    errs = [f"unit ID '{u}' contains a path separator" for u in units if os.sep in u]
    planned = {(u, a, str(r)) for u in units for a in arms for r in range(1, runs + 1)}
    found = set()
    for root, dirs, _ in os.walk(runs_dir):
        rel = os.path.relpath(root, runs_dir).split(os.sep)
        if len(rel) == 3:
            found.add(tuple(rel))
            dirs.clear()
    missing, extra = sorted(planned - found), sorted(found - planned)
    if missing:
        errs.append("planned runs have no output directory: " + first(missing))
    if extra:
        errs.append("output directories were not planned: " + first(extra))
    for run in sorted(found & planned):
        where = "/".join(run)
        try:
            m = json.load(open(os.path.join(runs_dir, *run, "manifest.json"), encoding="utf-8"))
        except (OSError, ValueError):
            errs.append(f"{where}: no readable manifest.json")
            continue
        gaps = [f for f in [*REQUIRED, *require] if m.get(f) in (None, "")]
        if gaps:
            errs.append(f"{where}: manifest lacks {', '.join(gaps)}")
        if str(m.get("attempt", 1)) != "1" and not m.get("rerun_reason"):
            errs.append(f"{where}: attempt {m['attempt']} has no rerun_reason")
        hc = str(m.get("harness_commit", ""))
        if harness_commit and hc and not (len(hc) >= 7 and harness_commit.startswith(hc)):
            errs.append(f"{where}: harness_commit {hc} is not the tagged harness {harness_commit[:7]}")
    return errs + check_ledger(runs_dir, ledger)


def self_test():
    d = tempfile.mkdtemp()
    runs_dir, ledger = os.path.join(d, "runs"), os.path.join(d, "runs.sha256")
    head = "a" * 40
    manifest = dict(harness_commit=head, seed=1, started_at="t0", finished_at="t1", model_id="m")

    def write(run, **over):
        path = os.path.join(runs_dir, *run)
        os.makedirs(path, exist_ok=True)
        json.dump({**manifest, **over}, open(os.path.join(path, "manifest.json"), "w"))
        open(os.path.join(path, "output.txt"), "w").write("/".join(run))

    def seal():
        files = sorted(os.path.join(r, f) for r, _, fs in os.walk(runs_dir) for f in fs)
        open(ledger, "w").write("".join(f"{sha256(p)}  {os.path.relpath(p, d)}\n" for p in files))

    for run in [(u, a, str(r)) for u in "ab" for a in ("x", "y") for r in (1, 2)]:
        write(run)
    seal()
    ok = dict(runs_dir=runs_dir, units=["a", "b"], arms=["x", "y"], runs=2, ledger=ledger)
    assert check(**ok) == [], check(**ok)
    assert check(**ok, require=["model_id"], harness_commit=head) == [], "required field and harness match"
    assert check(**ok, require=["cost"]), "a missing --require field"
    assert check(**ok, harness_commit="b" * 40), "a manifest from another harness"
    assert check(**{**ok, "runs": 3}), "a missing run"
    assert check(**{**ok, "units": ["a"]}), "an unplanned unit"
    open(os.path.join(runs_dir, "a", "x", "1", "output.txt"), "a").write("edited")
    assert any("hash" in e for e in check(**ok)), "an edited raw output"
    write(("a", "x", "1"), attempt=2)
    seal()
    assert any("rerun_reason" in e for e in check(**ok)), "a rerun with no reason"
    write(("a", "x", "1"), attempt=2, rerun_reason="API timeout")
    seal()
    assert check(**ok) == [], "a rerun with a reason"
    open(os.path.join(runs_dir, "a", "x", "1", "late.txt"), "w").write("x")
    assert any("not in the ledger" in e for e in check(**ok)), "an unlisted file"
    assert check(**{**ok, "ledger": os.path.join(d, "none")}), "no ledger"
    print("self-test passed")


def main():
    p = argparse.ArgumentParser(description="Checks that an experiment's run is complete and intact.")
    p.add_argument("--units", required=True)
    p.add_argument("--arms", required=True)
    p.add_argument("--runs", type=int, required=True)
    p.add_argument("--runs-dir", default="runs")
    p.add_argument("--ledger", default="runs.sha256")
    p.add_argument("--require", default="")
    p.add_argument("--harness-tag")
    a = p.parse_args()
    units = [l.strip() for l in open(a.units, encoding="utf-8") if l.strip() and not l.startswith("#")]
    head = None
    if a.harness_tag:
        r = subprocess.run(["git", "rev-parse", a.harness_tag + "^{commit}"], capture_output=True, text=True)
        if r.returncode:
            print(f"FAIL: no tag {a.harness_tag}")
            return 1
        head = r.stdout.strip()
    errs = check(a.runs_dir, units, a.arms.split(","), a.runs, a.ledger, list(filter(None, a.require.split(","))), head)
    for e in errs:
        print("FAIL:", e)
    print(f"{len(errs)} failures" if errs else "run check passed")
    return 1 if errs else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    else:
        sys.exit(main())
