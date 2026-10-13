#!/usr/bin/env python3
"""Claude Code SessionStart hook for the adr skill: prints one line per ADR under
docs/adr/ that has no `Superseded by:` line, its title and path, so a session
knows which decisions exist without loading them. Prints nothing when the
repository has no docs/adr/.

Reads the hook input on stdin for the working directory. Registered by the SDLC
plugin's hooks.json. Run with --self-test to check it.
"""
import json, os, re, subprocess, sys

MAX = 40
# "Superseded by: x" (this skill), "Status: Superseded by x" and a Nygard "## Status" body line "Superseded by [3](0003.md)"
SUPERSEDED = re.compile(r"^\W*(status\W*)?superseded\b", re.M | re.I)
NOT_ADR = re.compile(r"^(readme|index)\.md$|template", re.I)


def root(cwd):
    try:
        out = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip() or cwd
    except (OSError, subprocess.SubprocessError):
        return cwd


def heading(text):
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("# "):
            return line[2:].strip()
    return ""


def index(top):
    base = os.path.join(top, "docs", "adr")
    rows = []
    for d, _, files in os.walk(base):
        for f in sorted(files):
            if not f.endswith(".md") or NOT_ADR.search(f):
                continue
            path = os.path.join(d, f)
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            if SUPERSEDED.search(text):
                continue
            title = heading(text) or f[:-3]
            rows.append(f"- {title}: {os.path.relpath(path, top)}")
    return sorted(rows, key=lambda r: r.rsplit(": ", 1)[1])


def render(rows):
    if not rows:
        return ""
    lines = ["Decisions in force (docs/adr/). Read the one that applies before choosing "
             "a library, a data shape or a boundary:"] + rows[:MAX]
    if len(rows) > MAX:
        lines.append(f"- and {len(rows) - MAX} more under docs/adr/")
    return "\n".join(lines)


def main():
    try:
        cwd = json.load(sys.stdin).get("cwd") or os.getcwd()
    except (ValueError, AttributeError):
        cwd = os.getcwd()
    out = render(index(root(cwd)))
    if out:
        print(out)


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        assert render(index(t)) == "", "no docs/adr prints nothing"
        a = os.path.join(t, "docs", "adr", "architecture")
        os.makedirs(a)
        open(os.path.join(a, "use-redis.md"), "w").write("# Use Redis\n\n**Supersedes:** none.\n")
        open(os.path.join(a, "use-memcached.md"), "w").write("# Use Memcached\n\n**Superseded by:** docs/adr/architecture/use-redis.md\n")
        open(os.path.join(a, "notes.txt"), "w").write("# Not an ADR\n")
        open(os.path.join(a, "README.md"), "w").write("# Index\n")
        open(os.path.join(a, "0000-template.md"), "w").write("# Template\n")
        open(os.path.join(a, "0002-nygard.md"), "w").write("# Old\n\n## Status\n\nSuperseded by [3](0003.md)\n")
        open(os.path.join(a, "0003-status.md"), "w").write("# Older\nStatus: superseded by 0004\n")
        open(os.path.join(a, "fenced.md"), "w").write("```text\n# not this\n```\n# Fenced title\n**Supersedes:** none.\n")
        out = render(index(t))
        assert "- Use Redis: docs/adr/architecture/use-redis.md" in out, out
        for gone in ("Memcached", "Not an ADR", "Index", "Template", "Old", "not this"):
            assert gone not in out, (gone, out)
        assert "- Fenced title: docs/adr/architecture/fenced.md" in out, out
        for i in range(MAX + 2):
            open(os.path.join(a, f"d{i:02}.md"), "w").write(f"# D{i}\n**Supersedes:** none.\n")
        out = render(index(t))
        assert out.endswith("- and 4 more under docs/adr/"), out
    print("self-test passed")


if __name__ == "__main__":
    self_test() if sys.argv[1:] == ["--self-test"] else main()
