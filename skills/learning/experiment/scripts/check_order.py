#!/usr/bin/env python3
"""Checks, from git history, that an experiment's decisions came before its data, for the experiment skill.

  * the latest design-v* tag is an ancestor of the first commit that adds the data;
  * so is the latest harness-v* tag, and no --harness path changed between it and the last data commit;
  * the --analysis script was first committed before the data;
  * each --draw SEED:SELECTION has its seed file committed before its selection file, and unchanged since.

Warns, without failing, about each commit that changed the design after its tag or the analysis
script after the data: each belongs in the deviation log.

Usage: check_order.py --data PATH [--design EXPERIMENT.md] [--analysis PATH] [--harness PATH ...]
                      [--draw SEED:SELECTION ...]
Run it inside the repository. --data is the committed raw outputs or their hash ledger.
Prints each failure and exits 1, or prints "order check passed". Run with --self-test to check it.
"""
import argparse, os, subprocess, sys, tempfile


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def first(path):
    out = git("log", "--reverse", "--format=%H", "--", path)[1].splitlines()
    return out[0] if out else None


def last(path):
    return git("log", "-1", "--format=%H", "--", path)[1] or None


def before(a, b):
    return a != b and git("merge-base", "--is-ancestor", a, b)[0] == 0


def tag(pattern):
    tags = git("tag", "--list", pattern, "--sort=-v:refname")[1].splitlines()
    return (tags[0], git("rev-parse", tags[0] + "^{commit}")[1]) if tags else (None, None)


def since(commit, path):
    return git("log", "--format=%h %s", f"{commit}..HEAD", "--", path)[1].splitlines()


def check(data, design="EXPERIMENT.md", analysis=None, harness=(), draws=()):
    d0, d1 = first(data), last(data)
    if not d0:
        return [f"no commit adds {data}: commit the raw outputs, or their hash ledger, to date the data"], []
    errs, warns = [], []
    name, dc = tag("design-v*")
    if not name:
        errs.append("no design-v* tag: tag the committed design before building the harness")
    else:
        if not before(dc, d0):
            errs.append(f"{name} is not an ancestor of the first data commit {d0[:7]}")
        warns += [f"{design} changed after {name}: {c}" for c in since(dc, design)]
    name, hc = tag("harness-v*")
    if not name:
        errs.append("no harness-v* tag: tag the harness after the pilot")
    else:
        if not before(hc, d0):
            errs.append(f"{name} is not an ancestor of the first data commit {d0[:7]}")
        changed = [p for p in harness if git("diff", "--quiet", hc, d1, "--", p)[0] != 0]
        if changed:
            errs.append(f"the harness changed between {name} and the last data commit: {', '.join(changed)}")
    if analysis:
        a = first(analysis)
        if not a or not before(a, d0):
            errs.append(f"{analysis} was not committed before the first data commit {d0[:7]}")
        else:
            warns += [f"{analysis} changed after the data: {c}" for c in since(d0, analysis)]
    for draw in draws:
        seed, _, sel = draw.partition(":")
        s, x = first(seed), first(sel)
        if not s or not x:
            errs.append(f"{draw}: the seed or the selection is not committed")
        elif not before(s, x):
            errs.append(f"{seed} was not committed before {sel}")
        elif since(s, seed):
            errs.append(f"{seed} changed after its first commit")
    return errs, warns


def self_test():
    os.environ.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="t",
                      GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    os.chdir(tempfile.mkdtemp())
    git("init", "-q")

    def commit(path, text):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path, "w").write(text)
        git("add", path)
        git("commit", "-qm", path)

    commit("EXPERIMENT.md", "design")
    git("tag", "design-v1")
    commit("draws/units.seed", "42")
    commit("draws/units.txt", "a\nb")
    commit("analysis.py", "print()")
    commit("harness.py", "run()")
    git("tag", "harness-v1")
    commit("runs.sha256", "x")
    ok = dict(data="runs.sha256", analysis="analysis.py", harness=["harness.py"],
              draws=["draws/units.seed:draws/units.txt"])
    assert check(**ok) == ([], []), check(**ok)
    assert check(**{**ok, "draws": ["draws/units.txt:draws/units.seed"]})[0], "seed after its selection"
    assert check(**{**ok, "data": "absent"})[0], "no data commit"
    commit("EXPERIMENT.md", "design, deviation logged")
    commit("analysis.py", "print(1)")
    errs, warns = check(**ok)
    assert not errs and len(warns) == 2, (errs, warns)
    commit("late.py", "")
    assert check(**{**ok, "analysis": "late.py"})[0], "analysis written after the data"
    commit("draws/units.seed", "43")
    assert check(**ok)[0], "seed changed after the draw"
    ok["draws"] = []
    commit("harness.py", "run(2)")
    assert not check(**ok)[0], "a harness change after the last data commit passes"
    commit("runs.sha256", "y")
    assert check(**ok)[0], "the harness changed during the run"
    git("tag", "-d", "design-v1")
    assert any("design-v*" in e for e in check(**ok)[0]), "no design tag"
    print("self-test passed")


def main():
    p = argparse.ArgumentParser(description="Checks that an experiment's decisions came before its data.")
    p.add_argument("--data", required=True)
    p.add_argument("--design", default="EXPERIMENT.md")
    p.add_argument("--analysis")
    p.add_argument("--harness", nargs="*", default=[])
    p.add_argument("--draw", action="append", default=[])
    a = p.parse_args()
    errs, warns = check(a.data, a.design, a.analysis, a.harness, a.draw)
    for w in warns:
        print("warning:", w)
    for e in errs:
        print("FAIL:", e)
    print(f"{len(errs)} failures" if errs else "order check passed")
    return 1 if errs else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    else:
        sys.exit(main())
