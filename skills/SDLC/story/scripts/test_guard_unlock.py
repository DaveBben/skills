#!/usr/bin/env python3
"""Review findings on guard.py's unlock ask. Run: python3 skills/SDLC/story/scripts/test_guard_unlock.py"""
import json, os, subprocess, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guard  # noqa: E402

GUARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard.py")
BRANCH = "story/f/K-1-x"
KEY = f"branch.{BRANCH}.redCommit"


def repo():
    """A repository on the story branch with a real redCommit lock, unique to the calling test."""
    d = tempfile.mkdtemp()
    run = lambda *a: subprocess.run(["git", *a], cwd=d, check=True, capture_output=True, text=True).stdout
    run("init", "-q", "-b", "main")
    with open(f"{d}/a.txt", "w") as f:
        f.write("a\n")
    run("add", "-A")
    run("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init")
    run("switch", "-q", "-c", BRANCH)
    run("config", "--add", KEY, run("rev-parse", "HEAD").strip())
    return d


def hook(cmd, cwd):
    """The guard as Claude Code runs it: hook input on stdin, decision on stdout (None when it prints nothing)."""
    inp = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": cwd})
    out = subprocess.run([sys.executable, GUARD], input=inp, cwd=cwd, capture_output=True, text=True).stdout
    return json.loads(out)["hookSpecificOutput"] if out.strip() else None


def asks(reason):
    """Criterion 1's reason: the command unlocks the story's accepted tests; approve only if the user agreed a test is wrong."""
    return bool(reason) and "unlock" in reason.lower() and "accepted tests" in reason and "approve" in reason.lower() and "wrong" in reason


class Unlocks(unittest.TestCase):
    """Criterion 1: each command removes or replaces the lock, so the hook asks."""

    def assert_asks(self, *cmds):
        d = repo()
        for cmd in cmds:
            with self.subTest(cmd=cmd):
                out = hook(cmd, d)
                self.assertIsNotNone(out, "the hook printed nothing")
                self.assertEqual(out["permissionDecision"], "ask")
                self.assertTrue(asks(out["permissionDecisionReason"]), out["permissionDecisionReason"])

    def test_f1_unset_on_a_second_line(self):
        self.assert_asks(f"git config --get-all {KEY}\ngit config --unset-all {KEY}")

    def test_f2_key_built_by_the_shell(self):
        self.assert_asks('git config --unset-all "branch.$(git branch --show-current).redCommit"',
                         "git config --unset-all branch.$(git branch --show-current).redCommit",
                         f'K={KEY}; git config --unset-all "$K"')

    def test_f3_remove_section_quoted(self):
        self.assert_asks(f'git config --remove-section "branch.{BRANCH}"', f"git config --remove-section 'branch.{BRANCH}'")

    def test_f4_set_to_a_read_word(self):
        self.assert_asks(f"git config {KEY} list", f"git config {KEY} get", f"git config --replace-all {KEY} list")

    def test_f5_read_word_in_a_trailing_comment(self):
        self.assert_asks(f"git config --unset-all {KEY} # list")

    def test_f6_key_split_by_shell_quotes(self):
        self.assert_asks(f"git config --unset-all branch.{BRANCH}.red'C'ommit")

    def test_f7_global_option_with_a_value_before_config(self):
        self.assert_asks(f"git --work-tree . config --unset-all {KEY}")

    def test_f8_config_edit_with_a_scripted_editor(self):
        self.assert_asks("GIT_EDITOR='sed -i.bak /redCommit/d' git config --edit")

    def test_f9_alias_for_config(self):
        self.assert_asks(f"git -c alias.u=config u --unset-all {KEY}")

    def test_f10_key_piped_through_xargs(self):
        self.assert_asks(f"echo {KEY} | xargs git config --unset-all")


class LeavesTheLock(unittest.TestCase):
    """Criterion 2 through the hook output: reading the lock or touching another key prints nothing."""

    def test_w2_reads_and_other_keys_print_nothing(self):
        d = repo()
        for cmd in (f"git config --get-all {KEY}", "git config --unset-all user.email"):
            with self.subTest(cmd=cmd):
                self.assertIsNone(hook(cmd, d))

    def test_commit_message_naming_an_unlock_prints_nothing(self):
        self.assertIsNone(hook('git commit -m "docs: explain git config --unset-all branch.x.redCommit"', repo()))


class KeyCase(unittest.TestCase):
    """W1: git config keys are case-insensitive, so any branch's lock in any casing asks."""

    def test_w1_lowercase_and_uppercase_key_on_another_branch(self):
        for cmd in (f"git config --unset-all branch.{BRANCH}.redcommit",
                    "git config --replace-all branch.story/g/Q-27-y.REDCOMMIT 0123abc"):
            with self.subTest(cmd=cmd):
                self.assertTrue(asks(guard.unlock(cmd)), cmd)


if __name__ == "__main__":
    unittest.main()
