#!/usr/bin/env python3
"""Usage: agents_md_size.py [AGENTS.md ...] | --self-test"""
import os, sys

MAX_LINES, MAX_BYTES = 100, 8192


def too_big(path):
    data = open(path, "rb").read()
    return data.count(b"\n") > MAX_LINES or len(data) > MAX_BYTES


def main(paths):
    bad = [p for p in paths or ["AGENTS.md"] if os.path.exists(p) and too_big(p)]
    for p in bad:
        print(f"{p} is over {MAX_LINES} lines or {MAX_BYTES // 1024} KB. Move one module's "
              f"conventions into a nested AGENTS.md in that module, a rule for one file type "
              f"into a path-scoped rule file, and delete lines a check already enforces.",
              file=sys.stderr)
    return 1 if bad else 0


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "AGENTS.md")
        open(path, "w").write("line\n" * MAX_LINES)
        assert main([path]) == 0, "100 short lines must pass"
        open(path, "a").write("one more\n")
        assert main([path]) == 1, "101 lines must fail"
        open(path, "w").write("x" * (MAX_BYTES + 1))
        assert main([path]) == 1, "over 8 KB must fail"
    print("agents_md_size self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if sys.argv[1:] == ["--self-test"] else main(sys.argv[1:]))
