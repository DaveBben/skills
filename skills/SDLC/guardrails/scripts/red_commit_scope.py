#!/usr/bin/env python3
"""Usage: red_commit_scope.py <test glob>... | --self-test"""
import fnmatch, os, subprocess, sys


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def violations(globs, cwd=None):
    bad = []
    for line in git("diff", "--cached", "--numstat", "--no-renames", cwd=cwd).splitlines():
        added, removed, path = line.split("\t", 2)
        if any(fnmatch.fnmatch(path, g) for g in globs):
            continue
        if removed != "0":  # "-" is a binary file
            bad.append(path)
    return bad


def main(globs):
    skipped = {h.strip() for h in os.environ.get("SKIP", "").split(",")}
    if not skipped & {"tests", "e2e"}:
        return 0
    bad = violations(globs)
    for path in bad:
        print(f"SKIP=tests,e2e is only for the red commit, which holds failing tests and "
              f"stubs that add lines. This commit removes lines from {path}, which is not "
              f"a test file. Commit it without the skip.", file=sys.stderr)
    return 1 if bad else 0


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        git("init", "-q", cwd=d)
        for name, body in [("src.py", "a\nb\n"), ("tests/test_x.py", "x\n")]:
            os.makedirs(os.path.dirname(os.path.join(d, name)) or d, exist_ok=True)
            open(os.path.join(d, name), "w").write(body)
        git("add", "-A", cwd=d)
        git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "base", cwd=d)
        open(os.path.join(d, "tests/test_x.py"), "w").write("y\n")
        open(os.path.join(d, "src.py"), "a").write("def stub(): raise NotImplementedError\n")
        git("add", "-A", cwd=d)
        assert violations(["tests/*"], d) == [], "a test edit plus an added stub must pass"
        open(os.path.join(d, "src.py"), "w").write("a\n")
        git("add", "-A", cwd=d)
        assert violations(["tests/*"], d) == ["src.py"], "removed source lines must fail"
    print("red_commit_scope self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if sys.argv[1:] == ["--self-test"] else main(sys.argv[1:]))
