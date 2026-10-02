#!/usr/bin/env python3
"""Claude Code hook for the orient skill: keeps AGENTS.md and CLAUDE.md, at any
depth, at or under 100 lines and 8 KB.

  * PreToolUse on Edit, Write or MultiEdit: denies a change that would leave the
    file over the cap, unless it makes an oversized file smaller.
  * PostToolUse on Bash: a command naming one of the files, when the file was
    modified in the last RECENT seconds and is over the cap, is reported back to
    Claude to cut, since the shell write has happened. A command that only reads
    the file passes.

Reads the hook input on stdin and prints a decision, or nothing. Registered by
the SDLC plugin's hooks.json. Run with --self-test to check it.
"""
import json, os, re, shlex, sys, time

MAX_LINES, MAX_BYTES = 100, 8192
# ponytail: "the command wrote the file" is read as "modified in the last RECENT seconds"; a
# PreToolUse hook recording the size before the command would be exact.
RECENT = 10
NAMES = {"AGENTS.md", "CLAUDE.md"}
FIX = ("Rewrite it by the orient skill instead of adding to it: delete lines a check enforces or the "
       "repository already shows, and move one module's conventions into a nested AGENTS.md in that module.")


def too_big(text):
    data = text.encode()
    lines = data.count(b"\n") + (bool(data) and not data.endswith(b"\n"))
    return lines > MAX_LINES or len(data) > MAX_BYTES


def read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def fresh(path):
    try:
        return time.time() - os.path.getmtime(path) < RECENT
    except OSError:
        return False


def after(tool, inp, old):
    """The file's text once the edit tool runs, or None when the edit cannot apply."""
    if tool == "Write":
        return inp.get("content", "")
    edits = inp.get("edits") if tool == "MultiEdit" else [inp]
    text = old
    for e in edits or []:
        a, b = e.get("old_string", ""), e.get("new_string", "")
        if a not in text:
            return None
        text = text.replace(a, b) if e.get("replace_all") else text.replace(a, b, 1)
    return text


def pre(tool, inp, cwd):
    path = os.path.join(cwd, inp.get("file_path", ""))
    if os.path.basename(path) not in NAMES:
        return None
    old = read(path)
    new = after(tool, inp, old)
    if new is None or not too_big(new) or len(new.encode()) <= len(old.encode()):
        return None
    return f"This change leaves {os.path.basename(path)} over {MAX_LINES} lines or {MAX_BYTES // 1024} KB. " + FIX


def post(cmd, cwd):
    try:
        words = shlex.split(cmd)
    except ValueError:
        words = cmd.split()
    if words[:1] == ["cd"] and len(words) > 1:
        cwd = os.path.join(cwd, os.path.expanduser(words[1]))
    hits = {w for w in re.split(r"[\s;&|<>()]+", " ".join(words)) if os.path.basename(w) in NAMES}
    bad = sorted(h for h in hits if fresh(os.path.join(cwd, h)) and too_big(read(os.path.join(cwd, h))))
    if bad:
        return ", ".join(bad) + f" is now over {MAX_LINES} lines or {MAX_BYTES // 1024} KB. " + FIX
    return None


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    tool, ti, cwd = inp.get("tool_name"), inp.get("tool_input") or {}, inp.get("cwd") or os.getcwd()
    if tool in ("Edit", "Write", "MultiEdit"):
        reason = pre(tool, ti, cwd)
        if reason:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                     "permissionDecision": "deny",
                                                     "permissionDecisionReason": reason}}))
    elif tool == "Bash" and inp.get("hook_event_name") == "PostToolUse":
        reason = post(ti.get("command", ""), cwd)
        if reason:
            print(json.dumps({"decision": "block", "reason": reason}))


def self_test():
    import tempfile
    t = tempfile.mkdtemp()
    f = os.path.join(t, "AGENTS.md")
    full = "line\n" * MAX_LINES
    assert not pre("Write", {"file_path": f, "content": full}, t), "100 lines may be written"
    assert pre("Write", {"file_path": f, "content": full + "x\n"}, t), "101 lines may not"
    assert pre("Write", {"file_path": f, "content": full + "x"}, t), "101 lines with no trailing newline may not"
    assert not pre("Write", {"file_path": os.path.join(t, "README.md"), "content": full * 2}, t), "other files pass"
    open(f, "w").write(full)
    assert pre("Edit", {"file_path": "AGENTS.md", "old_string": "line\n", "new_string": "line\nmore\n"}, t), "edit that grows past the cap"
    assert not pre("Edit", {"file_path": f, "old_string": "line\n", "new_string": "LINE\n"}, t), "edit in place"
    assert pre("MultiEdit", {"file_path": f, "edits": [{"old_string": "line", "new_string": "line\nx", "replace_all": True}]}, t), "multi-edit"
    open(f, "w").write(full * 2)
    assert not pre("Edit", {"file_path": f, "old_string": full, "new_string": ""}, t), "shrinking an oversized file passes"
    assert not pre("Edit", {"file_path": f, "old_string": "absent", "new_string": "x"}, t), "an edit that cannot apply passes"
    assert not pre("Edit", {"file_path": f, "old_string": "line", "new_string": "LINE"}, t), "a same-length fix to an oversized file passes"
    assert post(f"cat extra >> {f}", "/"), "shell write left it over the cap"
    assert post("cd " + t + " && echo x >> AGENTS.md", "/"), "cd then a relative path"
    os.utime(f, (time.time() - 60, time.time() - 60))
    assert not post(f"cat {f}", "/"), "reading an oversized file it did not change passes"
    assert not post(f"wc -l {f}", "/"), "so does counting its lines"
    open(f, "w").write(full)
    assert not post(f"echo x >> {f}", "/"), "under the cap"
    assert not post("ls", t), "no file named"
    print("self-test passed")


if __name__ == "__main__":
    self_test() if sys.argv[1:] == ["--self-test"] else main()
