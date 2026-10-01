#!/usr/bin/env python3
"""PreToolUse guard on Bash commands, for the story skill.

Denies, with a message saying what to do instead:
  * merging a pull request (gh pr merge, glab mr merge) or merging into main:
    the user merges;
  * a commit, on a branch with red commits recorded in git config
    (branch.<branch>.redCommit), that changes a test file a red commit holds or
    a test that existed where the branch left main: those tests are locked,
    whichever tool edited them.

The guard reads the hook input on stdin and prints a deny decision, or nothing. Registered by
story's SKILL.md frontmatter and by the SDLC plugin's hooks.json, so it runs
for the main session and for subagents. Run with --self-test to check it.
"""
import json, os, re, shlex, subprocess, sys

MAINS = {os.environ.get("MAIN", "main"), "main", "master"}
TEST = re.compile(os.environ.get("TESTS", r"(^|/)(tests?|specs?|__tests__)/|(^|/)test_[^/]*$|_test\.[^/]*$|\.(test|spec)\.[^/]*$"))


def git(d, *args):
    r = subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def words(cmd):
    try:
        return shlex.split(cmd)
    except ValueError:
        return cmd.split()


def where(cmd, cwd):
    """The directory a git command runs in: a leading `cd X` or `git -C X`, else cwd."""
    w = words(cmd)
    for i, t in enumerate(w[:-1]):
        if (t == "cd" and i == 0) or (t == "-C" and i > 0 and w[i - 1] == "git"):
            cwd = os.path.join(cwd, os.path.expanduser(w[i + 1]))
    return cwd


def locked_files(d, branch):
    """The test files of the branch's red commits, and the tests that existed at its base."""
    reds = git(d, "config", "--get-all", f"branch.{branch}.redCommit").split()
    if not reds:
        return set()
    files = set()
    for red in reds:
        files |= {f for f in git(d, "diff-tree", "--no-commit-id", "--name-only", "-r", red).splitlines() if TEST.search(f)}
    base = next((b for b in MAINS if git(d, "rev-parse", "-q", "--verify", b)), "main")
    onto = f"origin/{base}" if git(d, "rev-parse", "-q", "--verify", f"origin/{base}") else base
    mb = git(d, "merge-base", onto, "HEAD")
    if mb:
        files |= {f for f in git(d, "ls-tree", "-r", "--name-only", mb).splitlines() if TEST.search(f)}
    return files


GIT = r"\bgit\b[^;&|\n]*?\b"  # a git command, global options allowed, within one shell segment


def check(cmd, cwd):
    d = where(cmd, cwd)
    if re.search(r"\b(gh\s+pr|glab\s+mr)\s+merge\b", cmd):
        return "The user merges pull requests. Tell the user it is ready to merge."
    branch = git(d, "branch", "--show-current")
    merging = re.search(GIT + r"merge(?![-\w])(?!\s+--ff-only\s+(origin/|@\{u\}))", cmd)
    onto_main = branch in MAINS or re.search(GIT + r"(switch|checkout)\s+(" + "|".join(MAINS) + r")\b", cmd)
    if merging and onto_main:
        return "Never merge into main: the user merges the pull request."
    if not branch or not re.search(GIT + r"commit\b", cmd):
        return None
    locked = locked_files(d, branch)
    if not locked:
        return None
    changed = set(git(d, "diff", "HEAD", "--name-only", "--no-renames").splitlines())
    w = words(cmd)
    if any(t in ("mv", "rm", "cp", "tee", ">", ">>") or t.startswith("-i") for t in w):
        changed |= {f for f in locked if f in w or any(t.endswith("/" + f) for t in w)}
    hit = sorted(changed & locked)
    if hit:
        return ("These accepted tests are locked: " + ", ".join(hit) + ". A test you cannot satisfy for a reason "
                "that holds against the code is a stop: undo your change to it, and report the test and the reason "
                "to the user. To add a test, put it in a new test file.")
    return None


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    if inp.get("tool_name") != "Bash":
        return
    reason = check((inp.get("tool_input") or {}).get("command", ""), inp.get("cwd") or os.getcwd())
    if reason:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                 "permissionDecision": "deny",
                                                 "permissionDecisionReason": reason}}))


def self_test():
    import tempfile
    t = tempfile.mkdtemp()
    run = lambda *a: subprocess.run(a, cwd=t, check=True, capture_output=True)
    run("git", "init", "-q", "-b", "main")
    open(f"{t}/old_test.go", "w").write("old\n")
    run("git", "add", "-A")
    run("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init")
    assert check("gh pr merge 3", t), "pr merge"
    assert check("git merge story/x", t), "git merge on main"
    assert not check("git merge-base HEAD story/x", t), "merge-base"
    assert not check("git merge --ff-only origin/main", t), "fast-forward"
    run("git", "switch", "-q", "-c", "story/f/K-1-x")
    assert not check("git push -u origin story/f/K-1-x", t), "push is the agent's call"
    assert not check("gh pr create --fill", t), "so is opening the pull request"
    os.makedirs(f"{t}/tests")
    open(f"{t}/tests/test_a.py", "w").write("x\n")
    run("git", "add", "-A")
    run("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "red")
    red = git(t, "rev-parse", "HEAD")
    run("git", "config", "--add", "branch.story/f/K-1-x.redCommit", red)
    open(f"{t}/tests/test_a.py", "w").write("y\n")
    assert check("git commit -am 'weaken'", t), "commit -a of a locked test"
    assert check(f"cd {t} && git commit -a -m x", "/"), "cd then commit"
    assert check("git commit -m 'only staged'", t), "a modified locked test blocks any commit"
    run("git", "add", "tests/test_a.py")
    assert check("git commit -m x", t), "staged locked test"
    run("git", "reset", "-q", "--hard")
    open(f"{t}/old_test.go", "w").write("weakened\n")
    assert check("git commit -am x", t), "a test that existed before the story"
    run("git", "checkout", "-q", "--", "old_test.go")
    os.makedirs(f"{t}/tests", exist_ok=True)
    open(f"{t}/tests/test_new.py", "w").write("n\n")
    run("git", "add", "tests/test_new.py")
    assert not check("git commit -m 'red: finding'", t), "a new test file"
    run("git", "reset", "-q")
    open(f"{t}/app.py", "w").write("z\n")
    run("git", "add", "app.py")
    assert not check("git commit -m build", t), "source commit allowed"
    open(f"{t}/tests/test_a.py", "w").write("y\n")
    assert check("git add tests/test_a.py && git commit -m x", t), "add then commit"
    assert check("git -c user.name=t commit -am x", t), "global option before commit"
    assert check("sh -c 'git commit -am x'", t), "commit inside sh -c"
    run("git", "checkout", "-q", "--", "tests/test_a.py")
    assert check("git mv tests/test_a.py tests/test_c.py && git commit -m x", t), "mv then commit"
    assert not check("git commit -m 'fix the bug tests/test_a.py found'", t), "message naming a test path"
    os.makedirs(f"{t}/sp ace/tests")
    assert check("git switch main && git merge story/f/K-1-x", t), "switch to main then merge"
    print("self-test passed")


if __name__ == "__main__":
    self_test() if sys.argv[1:] == ["--self-test"] else main()
