#!/usr/bin/env python3
"""Usage: accepted_tests.py <test glob>... | --self-test

Pre-commit hook. While deliver has recorded red commits for the current branch
(git config branch.<branch>.redCommit, or the older agile.redCommit), fail when
the staged tree changes or deletes a test file a red commit touched, compared
with the newest red commit that touched it. The edit-time accepted-test guard
sees only the agent's edit tool; this also catches the shell (sed, mv, rm)."""
import fnmatch, os, subprocess, sys


def git(*args, cwd=None):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.split() if r.returncode == 0 else []


def violations(globs, cwd=None):
    branch = git("branch", "--show-current", cwd=cwd)
    keys = [f"branch.{branch[0]}.redCommit"] if branch else []
    reds = {c for k in keys + ["agile.redCommit"] for h in git("config", "--get-all", k, cwd=cwd)
            for c in git("rev-parse", "--verify", "-q", h + "^{commit}", cwd=cwd)}
    newest = {}
    for c in git("rev-list", "HEAD", cwd=cwd):  # newest first
        if c in reds:
            for f in git("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", c, cwd=cwd):
                if any(fnmatch.fnmatch(f, g) for g in globs):
                    newest.setdefault(f, c)
    return sorted((f, c) for f, c in newest.items() if git("diff", "--cached", "--name-only", c, "--", f, cwd=cwd))


def main(globs):
    bad = violations(globs)
    for path, red in bad:
        print(f"{path} is an accepted test from red commit {red[:12]}, and this commit changes "
              f"or deletes it. The build makes accepted tests pass and never changes them. "
              f"Restore it with `git checkout {red[:12]} -- {path}`. Put a case the table missed "
              f"in a new test file. If the test itself is wrong, stop and say so.", file=sys.stderr)
    return 1 if bad else 0


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        run = lambda *a: subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *a],
                                        cwd=d, check=True, capture_output=True)
        write = lambda name, body: (os.makedirs(os.path.join(d, os.path.dirname(name)), exist_ok=True),
                                    open(os.path.join(d, name), "w").write(body))
        run("init", "-q", "-b", "story/x/K-1-y")
        write("src.py", "def f(): raise NotImplementedError\n")
        write("tests/test_f.py", "assert f()\n")
        run("add", "-A"); run("commit", "-qm", "red")
        red = git("rev-parse", "HEAD", cwd=d)[0]
        write("tests/test_f.py", "assert True\n")
        run("add", "-A")
        assert violations(["tests/*"], d) == [], "no red commit recorded, nothing guarded"
        run("config", "--add", "branch.story/x/K-1-y.redCommit", red)
        assert violations(["tests/*"], d) == [("tests/test_f.py", red)], "a weakened test must fail"
        run("checkout", red, "--", "tests/test_f.py")
        write("src.py", "def f(): return 1\n")
        run("add", "-A")
        assert violations(["tests/*"], d) == [], "implementing the stub must pass"
        run("rm", "-q", "tests/test_f.py")
        assert violations(["tests/*"], d) == [("tests/test_f.py", red)], "a deleted test must fail"
    print("accepted_tests self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if sys.argv[1:] == ["--self-test"] else main(sys.argv[1:]))
