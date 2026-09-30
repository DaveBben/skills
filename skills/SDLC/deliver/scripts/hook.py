#!/usr/bin/env python3
"""Claude Code hooks for the deliver skill.

Every handler runs this one script; the event comes from the hook input on
stdin. The rules it points to are the step files story.sh next prints, so an
agent without hooks reaches the same text by running story.sh.

Registered by deliver's SKILL.md frontmatter for the rest of a session that
invoked deliver. Claude Code runs these for the main session's calls only:
  PreToolUse   denies merging a pull request or into main; reading a file in a
               story worktree other than AGENTS.md or CLAUDE.md, a git diff or
               show there without --stat; opening a story's pull request (the
               checkout's branch, or the one --head names) before
               `story.sh confirm` or without its issue key; editing a file, in a
               checkout that is not a story worktree, that had uncommitted
               changes when this hook first saw that checkout, unless this
               session wrote it since
  PostToolUse  points to the next step when the setup, refute or description
               agent returns in the foreground, with a reminder after every
               agent; points to the resume step once when `story.sh status`
               prints a story; records each file the session writes and each
               agent launched in the background
  Stop         blocks one stop per change in story state while a story is
               between steps, no question waits for the user and no background
               agent runs

Registered with the argument `plugin` by plugins/SDLC/hooks/hooks.json, so it
runs in every session and subagent:
  PreToolUse   (a Bash command holding "merge") denies merging to SDLC agents
  SubagentStop clears the record of a background agent that finished; Claude
               Code does not run a skill's SubagentStop hooks
  SessionStart (on resume) asks a session with an open story to invoke deliver
               again, since skill hooks do not survive a resume

Run with --self-test to check it.
"""
import hashlib, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
STORY = os.path.join(HERE, "story.sh")
MAINS = {os.environ.get("MAIN", "main"), "main", "master"}
EDITS = ("Edit", "Write", "MultiEdit")
KEEP_GOING = ("no red commit", "red commit and no review", "refactored and not reviewed",
              "reviewed, not refuted", "reviewed, security needed", "reviewed and confirmed")
AFTER_AGENT = ("Sort every question the agent returned by the list under \"Talking to the user\" "
               "in the deliver skill; when nothing needs the user, send nothing.")
RETURNS = (("setup", "criteria"), ("refute", "verdicts"), ("description", "confirm"))


def git(d, *args):
    r = subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def checkout(path):
    """(top, branch) of the working tree holding path, or (None, None)."""
    d = path if os.path.isdir(path) else os.path.dirname(path) or "."
    while d and not os.path.isdir(d):
        d = os.path.dirname(d)
    top = git(d, "rev-parse", "--show-toplevel") if d else None
    return (top, git(top, "branch", "--show-current")) if top else (None, None)


def is_story(top, branch):
    return bool(branch) and (branch.startswith("story/") or git(top, "config", "--get", f"branch.{branch}.story") == "true")


def open_stories(cwd):
    """story.sh status --local as (branch, worktree, where it stands) triples."""
    r = subprocess.run([STORY, "status", "--local"], capture_output=True, text=True, cwd=cwd)
    return [ln.split("\t") for ln in r.stdout.splitlines() if ln.count("\t") == 2] if r.returncode == 0 else []


def real(cwd, p):
    return os.path.realpath(os.path.join(cwd, p))


def dirty(top):
    """Real paths of every file git status reports in the checkout at top."""
    out = subprocess.run(["git", "-C", top, "status", "--porcelain", "-z", "-uall"],
                         capture_output=True, text=True).stdout
    paths, skip = [], False
    for e in out.split("\0"):
        if skip:  # the old path of a rename or copy
            skip = False
        elif len(e) > 3:
            paths.append(os.path.realpath(os.path.join(top, e[3:])))
            skip = e[0] in "RC"
    return paths


def snapshot(s, top):
    """The checkout's dirty paths when this hook first saw it in the session."""
    # ponytail: a checkout first seen after a script or subagent changed it counts
    # those files as the user's; snapshot each checkout a Bash command names if that bites.
    snap = s.setdefault("dirty", {})
    if top not in snap:
        snap[top] = dirty(top)
    return snap[top]


def state_file(session):
    return os.path.join(tempfile.gettempdir(), f"deliver-hook-{re.sub(r'[^A-Za-z0-9_-]', '', session or 'none')}.json")


def load(session):
    try:
        with open(state_file(session)) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save(session, data):
    with open(state_file(session), "w") as f:
        json.dump(data, f)


def deny(reason):
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                   "permissionDecisionReason": reason}}


def context(event, text):
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def command_dir(cmd, cwd):
    """The directory a git or gh command runs in: git -C <dir>, a leading cd <dir>, else cwd."""
    m = re.search(r"\bgit\s+-C\s+(\S+)", cmd) or re.match(r"\s*cd\s+(\S+)\s*&&", cmd)
    d = m.group(1).strip("'\"") if m else cwd
    return d if os.path.isabs(d) else os.path.join(cwd, d)


def merge(cmd, cwd):
    if re.search(r"\b(gh\s+pr|glab\s+mr)\s+merge(?![-\w])", cmd):
        return deny("deliver never merges a pull request: the user merges. Tell the user it is ready to merge.")
    # merge-base reads, and a fast-forward to the remote's own branch only updates the checkout
    if re.search(r"\bgit\b(\s+-C\s+\S+)?\s+merge(?![-\w])(?!\s+--ff-only\s+(origin/|@\{u\}))", cmd):
        branch = checkout(command_dir(cmd, cwd))[1]
        if branch in MAINS:
            return deny(f"deliver never merges into {branch}: the user merges the pull request.")
    return None


def pre(inp, s):
    tool, ti, cwd = inp.get("tool_name"), inp.get("tool_input") or {}, inp.get("cwd") or "."
    if tool == "Bash":
        cmd = ti.get("command", "")
        m = merge(cmd, cwd)
        if m or not re.search(r"\b(git|gh|glab)\b", cmd):
            return m
        top, branch = checkout(command_dir(cmd, cwd))
        if not top:
            return None
        if is_story(top, branch) and re.search(r"\bgit\b(\s+-C\s+\S+)?\s+(diff|show)\b", cmd) \
                and not re.search(r"--(stat|shortstat|numstat|name-only|name-status|quiet)\b", cmd):
            return deny("This session never reads a diff, a test or source: hand the task to the build or worker agent.")
        if re.search(r"\b(gh\s+pr|glab\s+mr)\s+create\b", cmd):
            head = re.search(r"\s(?:--head|-H|--source-branch|-s)(?:\s+|=)['\"]?([^\s'\"]+)", cmd)
            b = head.group(1).split(":")[-1] if head else branch
            if not is_story(top, b):
                return None
            if git(top, "config", "--get", f"branch.{b}.criteriaConfirmed") != "true":
                return deny(f"The user has not confirmed this story. Run `{STORY} next confirm` and follow it; "
                            "run `story.sh confirm` only after the user's one-line confirmation.")
            key = git(top, "config", "--get", f"branch.{b}.issueKey")
            title = re.search(r"(?:--title|-t)(?:\s+|=)(\"[^\"]*\"|'[^']*'|\S+)", cmd)
            if key and title and key not in title.group(1):
                return deny(f"Put the issue key in the pull request title, e.g. `[{key}] <title>`.")
    elif tool == "Read":
        p = ti.get("file_path", "")
        top, branch = checkout(p)
        if top and is_story(top, branch) and os.path.basename(p) not in ("AGENTS.md", "CLAUDE.md"):
            return deny("This session never reads a diff, a test or source: hand the task to the build or worker agent.")
    elif tool in EDITS:
        p = real(cwd, ti.get("file_path", ""))
        top, branch = checkout(p)
        if top and not is_story(top, branch) and p in snapshot(s, top) and p not in s.get("touched", []):
            return deny(f"{p} held uncommitted changes this session did not make, in a checkout deliver did not "
                        "create. Never touch them: ask the user, or make the change in a story worktree.")
    return None


def post(inp, s):
    tool, ti, cwd = inp.get("tool_name"), inp.get("tool_input") or {}, inp.get("cwd") or "."
    resp = inp.get("tool_response")
    if tool in ("Agent", "Task"):
        status = resp.get("status") if isinstance(resp, dict) else None
        if status == "async_launched":
            s["flight"] = s.get("flight", []) + [resp.get("agentId")]
        if status != "completed":
            return None
        kind, prompt, out = ti.get("subagent_type", ""), ti.get("prompt", ""), json.dumps(resp)
        nxt = next((n for k, n in RETURNS if kind.endswith(k)), None)
        if nxt == "criteria" and not re.search(r"Criteria:|Not ready:|Split:", out) \
                or nxt in ("verdicts", "confirm") and "done-block.md" not in prompt:
            nxt = None
        text = f"Follow `{STORY} next {nxt}` now; run it when its text is not in view.\n" if nxt else ""
        return context("PostToolUse", text + AFTER_AGENT)
    if tool == "Bash" and "story.sh status" in ti.get("command", ""):
        out = resp.get("stdout", "") if isinstance(resp, dict) else str(resp or "")
        if "\t" in out and not s.get("resumed"):
            s["resumed"] = True
            return context("PostToolUse", f"A story is open: run `{STORY} next resume` and follow it.")
    if tool in EDITS:
        s["touched"] = sorted(set(s.get("touched", [])) | {real(cwd, ti.get("file_path", ""))})
    return None


def stop(inp, s):
    if inp.get("stop_hook_active") or s.get("flight") \
            or (inp.get("last_assistant_message") or "").rstrip().endswith("?"):
        return None
    listed = open_stories(inp.get("cwd") or ".")
    moving = [m for m in listed if m[2].startswith(KEEP_GOING)]
    snap = hashlib.sha1(repr(listed).encode()).hexdigest()
    if not moving or s.get("stop") == snap:
        return None
    s["stop"] = snap
    b, wt, at = moving[0]
    return {"decision": "block", "reason":
            f"Story {b} is at '{at}' and no question waits for the user. Run `{STORY} next` in {wt} and continue. "
            "If an agent you launched is still running, or the user asked to stop, stop. Otherwise stop only "
            "for the waiting question, the user's one-line confirmation, a second round of blocking findings, "
            "or when nothing is ready and nothing is building."}


def plugin(inp):
    """The handlers plugins/SDLC/hooks/hooks.json registers for every session and subagent."""
    ev, cwd = inp.get("hook_event_name"), inp.get("cwd") or "."
    if ev == "PreToolUse" and str(inp.get("agent_type", "")).startswith("SDLC:"):
        return merge((inp.get("tool_input") or {}).get("command", ""), cwd)
    if ev == "SubagentStop" and os.path.exists(state_file(inp.get("session_id"))):
        s = load(inp.get("session_id"))
        if inp.get("agent_id") in s.get("flight", []):
            s["flight"].remove(inp.get("agent_id"))
            save(inp.get("session_id"), s)
    if ev == "SessionStart" and open_stories(cwd):
        return context("SessionStart", "A deliver story is open in this repository: invoke the deliver skill "
                                       "before any other tool call, since its guards do not survive a resume.")
    return None


def handle(inp, level="skill"):
    if level == "plugin":
        return plugin(inp)
    if "agent_id" in inp:
        return None  # subagents do the reading and building; plugin() guards their merges
    sid, ev = inp.get("session_id"), inp.get("hook_event_name")
    s = load(sid)
    before = json.dumps(s, sort_keys=True)
    if "dirty" not in s:  # the checkout the session started in, before this session changed it
        top = checkout(inp.get("cwd") or ".")[0]
        s["dirty"] = {top: dirty(top)} if top else {}
    out = None
    if ev == "PreToolUse":
        out = pre(inp, s)
    elif ev == "PostToolUse":
        out = post(inp, s)
    elif ev == "Stop":
        out = stop(inp, s)
    if json.dumps(s, sort_keys=True) != before:
        save(sid, s)
    return out


def self_test():
    import shutil
    raw = tempfile.mkdtemp()
    t = os.path.realpath(raw)
    link = t + "-link"  # a second spelling of every path, like /tmp and /private/tmp
    os.symlink(t, link)
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    sh = lambda c, d: subprocess.run(c, shell=True, cwd=d, env=env, check=True, capture_output=True, text=True).stdout.strip()
    sid = f"selftest{os.getpid()}"
    try:
        app = os.path.join(t, "app")
        os.makedirs(app)
        sh("git init -q -b main && git commit -q --allow-empty -m init && echo x > a.py && git add a.py && git commit -q -m a", app)
        sh("echo user > a.py", app)  # the user's own uncommitted change, there before the session
        wt = sh(f"'{STORY}' start pay PAY-1 refunds 2>/dev/null", app)
        gd = sh("git rev-parse --path-format=absolute --git-dir", wt)
        ev = lambda e, tool=None, ti=None, level="skill", **k: handle(dict(
            hook_event_name=e, tool_name=tool, tool_input=ti or {}, cwd=app, session_id=sid, **k), level)
        denied = lambda o: bool(o) and o["hookSpecificOutput"].get("permissionDecision") == "deny"
        ctx = lambda o: o["hookSpecificOutput"]["additionalContext"] if o else ""
        assert denied(ev("PreToolUse", "Read", {"file_path": f"{wt}/a.py"})), "Read of source in a story worktree"
        assert not ev("PreToolUse", "Read", {"file_path": f"{wt}/a.py"}, agent_id="x"), "Read by a subagent"
        assert not ev("PreToolUse", "Read", {"file_path": f"{wt}/AGENTS.md"}), "Read of AGENTS.md"
        assert not ev("PreToolUse", "Read", {"file_path": f"{app}/a.py"}), "Read outside a story worktree"
        merge_cmd = {"command": "gh pr merge 3"}
        assert denied(ev("PreToolUse", "Bash", merge_cmd)), "merge in the main session"
        assert denied(ev("PreToolUse", "Bash", merge_cmd, "plugin", agent_id="x", agent_type="SDLC:build")), "merge by an SDLC agent"
        assert not ev("PreToolUse", "Bash", merge_cmd, "plugin", agent_id="x", agent_type="general-purpose"), "merge by another agent"
        assert not ev("PreToolUse", "Bash", merge_cmd, "plugin"), "merge in a session that never ran deliver"
        assert denied(ev("PreToolUse", "Bash", {"command": "git merge story/x"})), "git merge on main"
        assert not ev("PreToolUse", "Bash", {"command": "git merge-base HEAD story/x"}), "git merge-base on main"
        assert not ev("PreToolUse", "Bash", {"command": "git merge --ff-only origin/main"}), "fast-forward main to origin"
        assert not ev("PreToolUse", "Bash", {"command": f"git -C {wt} merge main"}), "git merge on a story branch"
        assert denied(ev("PreToolUse", "Bash", {"command": f"git -C {wt} diff main"})), "git diff in a story worktree"
        assert not ev("PreToolUse", "Bash", {"command": f"git -C {wt} diff --stat main"}), "git diff --stat"
        create = {"command": f"cd {wt} && gh pr create --title '[PAY-1] Refunds'"}
        assert denied(ev("PreToolUse", "Bash", create)), "pull request before confirm"
        o = ev("PreToolUse", "Bash", {"command": "gh pr create --head story/pay/PAY-1-refunds --title '[PAY-1] R'"})
        assert denied(o), "pull request from main with --head, before confirm"
        assert STORY in o["hookSpecificOutput"]["permissionDecisionReason"], "deny names story.sh by its path"
        o = ev("Stop")
        assert o["decision"] == "block" and STORY in o["reason"], "stop names story.sh by its path"
        assert "asked to stop" in o["reason"], "stop reason lets the user's stop win"
        assert not ev("Stop"), "second stop on the same state"
        assert not ev("Stop", last_assistant_message="Which option?"), "stop on a question"
        sh("git commit -q --allow-empty -m red", wt)
        sh(f"'{STORY}' red", wt)
        ev("PostToolUse", "Agent", {"subagent_type": "SDLC:build"}, tool_response={"status": "async_launched", "agentId": "bg1"})
        assert not ev("Stop"), "stop while a background agent runs"
        ev("SubagentStop", level="plugin", agent_id="bg1", agent_type="SDLC:build")
        assert (ev("Stop") or {}).get("decision") == "block", "stop after the background agent finished"
        sh(f"echo 'Findings:    none' > '{gd}/done-block.md' && '{STORY}' confirm", wt)
        assert (ev("Stop") or {}).get("decision") == "block", "stop after confirmation, before the pull request opens"
        sh(f"'{STORY}' next open", wt)
        assert not ev("Stop"), "stop with the pull request open"
        assert not ev("PreToolUse", "Bash", create), "pull request after confirm"
        assert denied(ev("PreToolUse", "Bash", {"command": f"cd {wt} && gh pr create --title Refunds"})), "title without the key"
        assert denied(ev("PreToolUse", "Edit", {"file_path": f"{app}/a.py"})), "edit of the user's uncommitted change"
        assert denied(ev("PreToolUse", "Edit", {"file_path": f"{link}/app/a.py"})), "same edit, another spelling"
        assert not ev("PreToolUse", "Write", {"file_path": f"{app}/new.py"}), "write of a new file"
        sh("mkdir -p .claude/hooks && echo slot=x > .claude/hooks/_slots.sh", app)  # a script writes it
        assert not ev("PreToolUse", "Edit", {"file_path": f"{app}/.claude/hooks/_slots.sh"}), "edit of a file a script made"
        ev("PostToolUse", "Write", {"file_path": f"{link}/app/a.py"})
        assert not ev("PreToolUse", "Edit", {"file_path": f"{app}/a.py"}), "edit of a file this session wrote since"
        done = {"status": "completed", "content": [{"type": "text", "text": "Criteria: a. ..."}]}
        o = ctx(ev("PostToolUse", "Agent", {"subagent_type": "SDLC:setup", "prompt": "x"}, tool_response=done))
        assert f"{STORY} next criteria" in o and "# Step" not in o, "setup return points to the step"
        o = ctx(ev("PostToolUse", "Agent", {"subagent_type": "SDLC:refute", "prompt": "/g/done-block.md"}, tool_response=done))
        assert f"{STORY} next verdicts" in o, "refute return"
        assert "story.sh next" not in ctx(ev("PostToolUse", "Agent", {"subagent_type": "SDLC:lookup"}, tool_response=done)), "lookup return"
        status = {"command": f"{STORY} status"}, {"stdout": f"story/pay/PAY-1-refunds\t{wt}\tno red commit: set up"}
        assert "next resume" in ctx(ev("PostToolUse", "Bash", status[0], tool_response=status[1])), "status prints a story"
        assert not ev("PostToolUse", "Bash", status[0], tool_response=status[1]), "resume pointer only once"
        assert "invoke the deliver skill" in ctx(ev("SessionStart", level="plugin", source="resume")), "resume with a story open"
        sh(f"'{STORY}' close story/pay/PAY-1-refunds", app)
        assert not ev("Stop"), "stop with no story"
        assert not ev("SessionStart", level="plugin", source="resume"), "resume with no story"
    finally:
        os.remove(link)
        shutil.rmtree(t, ignore_errors=True)
        try:
            os.remove(state_file(sid))
        except OSError:
            pass
    print("self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        sys.exit(0)
    try:
        out = handle(json.load(sys.stdin), (sys.argv[1:] or ["skill"])[0])
    except Exception as e:  # a broken hook must never block the session
        print(f"deliver hook: {e}", file=sys.stderr)
        sys.exit(0)
    if out:
        print(json.dumps(out))
