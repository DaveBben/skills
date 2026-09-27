#!/usr/bin/env python3
"""Usage: issue_key.py <commit message file> | --self-test

prepare-commit-msg hook. On a branch whose git config holds
branch.<branch>.issueKey, which deliver's `story.sh start` writes, prepend
"[<key>] " to the message unless it already holds "[<key>]". A message with no
text yet (the editor has not opened) is left alone, so an aborted commit stays empty."""
import os, subprocess, sys


def git(*args, cwd=None):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def tag(msg, key):
    text = [l for l in msg.splitlines() if l.strip() and not l.startswith("#")]
    return msg if not text or f"[{key}]" in msg else f"[{key}] {msg}"


def main(path, cwd=None):
    branch = git("branch", "--show-current", cwd=cwd)
    key = branch and git("config", "--get", f"branch.{branch}.issueKey", cwd=cwd)
    if key:
        with open(path) as f:
            msg = f.read()
        with open(path, "w") as f:
            f.write(tag(msg, key))
    return 0


def self_test():
    import tempfile
    assert tag("add refunds\n", "PAY-1") == "[PAY-1] add refunds\n"
    assert tag("[PAY-1] add refunds\n", "PAY-1") == "[PAY-1] add refunds\n", "no double tag"
    assert tag("\n# Please enter the commit message\n", "PAY-1").startswith("\n"), "empty stays empty"
    with tempfile.TemporaryDirectory() as d:
        git("init", "-q", "-b", "story/pay/PAY-1-refunds", cwd=d)
        msg = os.path.join(d, "MSG")
        open(msg, "w").write("add refunds\n")
        main(msg, d)
        assert open(msg).read() == "add refunds\n", "no key recorded, no tag"
        git("config", "branch.story/pay/PAY-1-refunds.issueKey", "PAY-1", cwd=d)
        main(msg, d)
        assert open(msg).read() == "[PAY-1] add refunds\n", "recorded key must be prepended"
    print("issue_key self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if sys.argv[1:] == ["--self-test"] else main(sys.argv[1]))
