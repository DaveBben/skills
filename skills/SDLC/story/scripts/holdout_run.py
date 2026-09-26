#!/usr/bin/env python3
"""The holdout runner. Copy it into the holdout directory as `run`.

Usage, from anywhere:
  run [--done <story numbers>] [--diff <file>]   run the confirmed scenarios, print one line
  run --lock S<n>                                 record S<n>'s executable as confirmed
  run --self-test

The holdout directory holds:
  scenarios.md    line 1 `canary: <random id>`, then one block per scenario:
                    ## S3 Refund shows on the statement
                    Due after: 3, 5
                    Runs: 1
                    Spent: 2026-10-02        (only once handed over as a bug report)
                    Given ... / When ... / Then ... / And ...
  executables/    one file per scenario, its name starting with the ID (S3_refund.py)
  runner.txt      one line: the command that runs the files and writes JUnit XML,
                  with {files} and {junit} placeholders, e.g.
                  pytest -q --tb=short --junitxml={junit} {files}
  scenarios.lock  written by --lock: one `S<n> <sha256>` line per confirmed executable
  results.jsonl   written by each run: one line per run
  report.md       written by each run: the failure messages of failing due scenarios

The printed line names scenarios by ID only and never prints their text, values
or failure messages; those stay in report.md for the user."""
import hashlib, json, os, re, shlex, subprocess, sys, tempfile, time
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
LITERAL = re.compile(r"\"([^\"\n]{8,})\"|'([^'\n]{8,})'|\b(?=[\w-]*\d)(?=[\w-]*[A-Za-z])[\w-]{6,}\b")


def parse(root):
    text = open(os.path.join(root, "scenarios.md")).read()
    canary = re.match(r"canary:\s*(\S+)", text)
    scenarios = {}
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        sid = head.split()[0]
        field = lambda k: (re.search(rf"^{k}:\s*(.*)$", body, re.M) or [None, ""])[1].strip()
        scenarios[sid] = {
            "due": {n.strip() for n in field("Due after").split(",") if n.strip()},
            "runs": int(field("Runs") or 1),
            "spent": bool(field("Spent")),
            "body": body,
        }
    return (canary.group(1) if canary else None), scenarios


def executable(root, sid):
    d = os.path.join(root, "executables")
    for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if re.match(rf"{sid}[_.]", name):
            return os.path.join(d, name)
    return None


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def locks(root):
    try:
        return dict(l.split() for l in open(os.path.join(root, "scenarios.lock")) if l.strip())
    except FileNotFoundError:
        return {}


def run_once(root, files):
    junit = tempfile.mktemp(suffix=".xml")
    cmd = open(os.path.join(root, "runner.txt")).read().strip()
    cmd = cmd.replace("{junit}", shlex.quote(junit)).replace("{files}", " ".join(map(shlex.quote, files)))
    subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True)
    if not os.path.exists(junit):
        raise RuntimeError(f"the runner wrote no JUnit file: {cmd}")
    outcome, messages = {}, {}
    for case in ET.parse(junit).iter("testcase"):
        label = " ".join(filter(None, [case.get("classname"), case.get("name"), case.get("file")]))
        m = re.search(r"(?<![A-Za-z0-9])(S\d+)(?!\d)", label)
        if not m:
            continue
        bad = [c for c in case if c.tag in ("failure", "error", "skipped")]
        outcome[m.group(1)] = outcome.get(m.group(1), True) and not bad
        for c in bad:
            messages.setdefault(m.group(1), []).append((c.get("message") or c.text or c.tag).strip())
    os.remove(junit)
    return outcome, messages


def leaks(canary, scenarios, diff_text):
    added = "\n".join(l[1:] for l in diff_text.splitlines() if l.startswith("+") and not l.startswith("+++"))
    hit = ["S0"] if canary and canary in diff_text else []
    for sid, s in scenarios.items():
        lits = {next(g for g in m.groups() if g) if any(m.groups()) else m.group(0)
                for m in LITERAL.finditer(s["body"])}
        if any(lit in added for lit in lits):
            hit.append(sid)
    return hit


def run(root, done, diff_path=None):
    canary, scenarios = parse(root)
    locked = locks(root)
    confirmed, unconfirmed = {}, []
    for sid in scenarios:
        path = executable(root, sid)
        if path and locked.get(sid) == digest(path):
            confirmed[sid] = path
        else:
            unconfirmed.append(sid)
    passed, messages = {sid: True for sid in confirmed}, {}
    for i in range(max([scenarios[s]["runs"] for s in confirmed] or [0])):
        todo = [s for s in confirmed if scenarios[s]["runs"] > i]
        outcome, msgs = run_once(root, [confirmed[s] for s in todo])
        for s in todo:
            passed[s] = passed[s] and outcome.get(s, False)
            messages.setdefault(s, []).extend(msgs.get(s, []) or ([] if outcome.get(s) else ["no test result"]))
    due = [s for s in confirmed if scenarios[s]["due"] <= done]
    history = [json.loads(l) for l in open(os.path.join(root, "results.jsonl"))] \
        if os.path.exists(os.path.join(root, "results.jsonl")) else []
    last = {}
    for h in history:
        last.update(h["results"])
    newly = [s for s in due if not passed[s] and last.get(s) == "pass"]
    again = [s for s in newly if scenarios[s]["spent"]]
    with open(os.path.join(root, "results.jsonl"), "a") as f:
        f.write(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                            "results": {s: "pass" if passed[s] else "fail" for s in confirmed}}) + "\n")
    with open(os.path.join(root, "report.md"), "w") as f:
        for s in due:
            if not passed[s]:
                f.write(f"## {s}\n" + "\n".join(f"- {m}" for m in messages.get(s, [])) + "\n\n")
    leaked = leaks(canary, scenarios, open(diff_path).read()) if diff_path else []
    not_due = [s for s in confirmed if s not in due]
    unspent = sum(not s["spent"] for s in scenarios.values())
    fmt = lambda xs: ", ".join(xs) or "none"
    return (f"Scenarios: {sum(passed[s] for s in due)} of {len(due)} due pass; "
            f"not due {len(not_due)} ({sum(passed[s] for s in not_due)} pass); "
            f"newly failing: {fmt([s for s in newly if s not in again])}; "
            f"failed again after its fix: {fmt(again)}; unconfirmed: {fmt(unconfirmed)}; "
            f"unspent: {unspent} of {len(scenarios)}; leak: {fmt(leaked)}")


def lock(root, sid):
    path = executable(root, sid)
    if not path:
        sys.exit(f"No file in executables/ starts with {sid}_.")
    entries = locks(root)
    entries[sid] = digest(path)
    with open(os.path.join(root, "scenarios.lock"), "w") as f:
        f.writelines(f"{k} {v}\n" for k, v in sorted(entries.items()))
    return f"{sid} confirmed: {os.path.basename(path)}"


def self_test():
    fake = ("import sys\nfrom xml.sax.saxutils import quoteattr\njunit, files = sys.argv[1], sys.argv[2:]\n"
            "cases = []\nfor f in files:\n    n = __import__('os').path.basename(f).split('.')[0]\n"
            "    body = open(f).read()\n    import os\n    c = os.path.join(os.path.dirname(f), '.count_' + n)\n"
            "    k = int(open(c).read()) if os.path.exists(c) else 0\n    open(c, 'w').write(str(k + 1))\n"
            "    ok = 'PASS' in body or ('FLAKY' in body and k % 2 == 0)\n"
            "    cases.append(f'<testcase classname=\"x\" name=\"test_{n}\">' + ('' if ok else "
            "'<failure message=\"expected -20.00, got none\"/>') + '</testcase>')\n"
            "open(junit, 'w').write('<testsuite>' + ''.join(cases) + '</testsuite>')\n")
    with tempfile.TemporaryDirectory() as root:
        w = lambda p, s: (os.makedirs(os.path.dirname(os.path.join(root, p)) or root, exist_ok=True),
                          open(os.path.join(root, p), "w").write(s))
        w("fake.py", fake)
        w("runner.txt", "python3 fake.py {junit} {files}")
        w("scenarios.md", "canary: 7f3a9c2e-canary\n\n"
          "## S1 Paid invoice shows\nDue after: 1\nRuns: 1\nGiven customer C-1001 has invoice INV-77\n\n"
          "## S2 Refund on statement\nDue after: 1, 2\nRuns: 1\nThen the statement shows \"refund INV-77 -20.00\"\n\n"
          "## S3 Concurrent refunds\nDue after: 1\nRuns: 3\nWhen two refunds arrive at once\n\n"
          "## S4 Not yet built\nDue after: 9\nRuns: 1\nThen it works\n\n"
          "## S5 Unconfirmed\nDue after: 1\nRuns: 1\nThen it works\n")
        w("executables/S1_paid.py", "PASS")
        w("executables/S2_refund.py", "PASS")
        w("executables/S3_race.py", "FLAKY")
        w("executables/S4_later.py", "PASS")
        w("executables/S5_new.py", "PASS")
        for s in ("S1", "S2", "S3", "S4"):
            lock(root, s)
        line = run(root, {"1", "2"})
        assert line.startswith("Scenarios: 2 of 3 due pass; not due 1 (1 pass)"), line
        assert "unconfirmed: S5" in line, "an unlocked executable must not run"
        assert "newly failing: none" in line, line
        w("executables/S2_refund.py", "FAIL")
        lock(root, "S2")
        line = run(root, {"1", "2"})
        assert "newly failing: S2" in line, line
        assert "expected -20.00" in open(os.path.join(root, "report.md")).read(), "report.md keeps the message"
        assert "-20.00" not in line and "INV-77" not in line, "the printed line must not carry scenario values"
        w("executables/S1_paid.py", "FAIL")
        line = run(root, {"1", "2"})
        assert "unconfirmed: S1, S5" in line, "an executable edited after confirmation must not run"
        w("d.diff", "+++ b/src/x.py\n+if invoice == 'INV-77': pass\n")
        assert run(root, {"1"}, os.path.join(root, "d.diff")).endswith("leak: S1"), "a scenario value in the diff is a leak"
        w("d.diff", "+++ b/tests/t.py\n+# 7f3a9c2e-canary\n")
        assert run(root, {"1"}, os.path.join(root, "d.diff")).endswith("leak: S0"), "the canary in the diff is a leak"
    print("holdout_run self-test passed")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--self-test"]:
        sys.exit(self_test())
    if a[:1] == ["--lock"]:
        print(lock(HERE, a[1]))
        sys.exit(0)
    opts = dict(zip(a[::2], a[1::2]))
    try:
        print(run(HERE, {n.strip() for n in opts.get("--done", "").split(",") if n.strip()}, opts.get("--diff")))
    except Exception as e:  # never report a runner fault as a pass
        print(f"Scenarios: runner failed: {e}")
        sys.exit(1)
