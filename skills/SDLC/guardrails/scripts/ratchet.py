#!/usr/bin/env python3
"""Usage: <check> | ratchet.py <baseline file> | --self-test

Reads findings on stdin, one per line: <rule><TAB><file>. Fails when any rule's
count in any file rises above the baseline, naming the rule and the file. When
counts fall, rewrites the baseline with the lower counts; a count never rises."""
import json, os, sys
from collections import Counter


def counts(lines):
    c = Counter()
    for line in lines:
        if "\t" in line:
            rule, path = line.rstrip("\n").split("\t", 1)
            c[f"{rule}\t{path}"] += 1
    return c


def ratchet(baseline_path, lines):
    base = json.load(open(baseline_path)) if os.path.exists(baseline_path) else {}
    now = counts(lines)
    risen = [k for k, n in now.items() if n > base.get(k, 0)]
    for k in risen:
        rule, path = k.split("\t")
        print(f"{path}: {now[k]} {rule} findings, up from {base.get(k, 0)}. "
              f"Fix the new one; the count for existing code may only fall.", file=sys.stderr)
    if risen:
        return 1
    lowered = {k: n for k, n in now.items() if n}  # every count is at or below base here
    if lowered != base:
        with open(baseline_path, "w") as fh:
            json.dump(dict(sorted(lowered.items())), fh, indent=1)
    return 0


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        b = os.path.join(d, "baseline.json")
        json.dump({"C901\ta.py": 3}, open(b, "w"))
        assert ratchet(b, ["C901\ta.py"] * 4) == 1, "a rise must fail"
        assert json.load(open(b)) == {"C901\ta.py": 3}, "a rise must not reach the baseline"
        assert ratchet(b, ["C901\tb.py"] + ["C901\ta.py"] * 3) == 1, "a new file's finding must fail"
        assert ratchet(b, ["C901\ta.py"] * 2) == 0, "a fall must pass"
        assert json.load(open(b)) == {"C901\ta.py": 2}, "a fall must lower the baseline"
        assert ratchet(b, ["C901\ta.py"] * 3) == 1, "a count may not climb back"
    print("ratchet self-test passed")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    sys.exit(ratchet(sys.argv[1], sys.stdin))
