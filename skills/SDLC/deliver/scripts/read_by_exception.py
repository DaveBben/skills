#!/usr/bin/env python3
"""Usage: read_by_exception.py <base> [<red commit>] | --self-test

Run from the repository root. Prints one line per signal that makes the user
read code, and exits 0; no output means no signal. <base> is the merge target
(main). <red commit> is the story's latest red commit: test lines removed after
it are a weakened test, and its message holds the criteria.

Signals:
  owner-reads <label>: <path>   a changed file matches a line under a
                                `# owner reads: <label>` heading in CODEOWNERS
                                (the section ends at a blank line)
  suppression: <path>: <line>   an added line skips a test or silences a check
  test lines removed after red commit: <path>
  test value in production code: <path>: <literal>
                                a string of 8+ characters from an added test line
                                appears in added production code and not in the
                                criteria
Edit TEST and SUPPRESS to the project's test paths and tools."""
import fnmatch, re, subprocess, sys

TEST = ["tests/*", "*/tests/*", "*test_*.py", "*.test.*", "*.spec.*"]
SUPPRESS = re.compile(r"noqa|type:\s*ignore|nosemgrep|eslint-disable|@ts-ignore|"
                      r"pytest\.mark\.(skip|xfail)|\.skip\(|\.only\(|t\.Skip\(")
LITERAL = re.compile(r"[\"']([^\"'\n]{8,})[\"']")


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def is_test(path):
    return any(fnmatch.fnmatch(path, g) for g in TEST)


def owner_reads(cwd=None):
    """`# owner reads: <label>` sections of CODEOWNERS -> [(pattern, label)]."""
    try:
        text = open(f"{cwd or '.'}/CODEOWNERS").read()
    except FileNotFoundError:
        return []
    out, label = [], None
    for line in text.splitlines():
        m = re.match(r"#\s*owner reads:\s*(.+)", line)
        if m:
            label = m.group(1).strip()
        elif not line.strip() or line.startswith("#"):
            label = None
        elif label:
            out.append((line.split()[0].lstrip("/"), label))
    return out


def matches(path, pat):
    return path.startswith(pat) if pat.endswith("/") else fnmatch.fnmatch(path, pat)


def added(base, cwd=None):
    """{path: [added lines]} for base...HEAD."""
    out, path = {}, None
    for line in git("diff", "-U0", f"{base}...HEAD", cwd=cwd).splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line != "+++ /dev/null" else None
        elif line.startswith("+") and path:
            out.setdefault(path, []).append(line[1:])
    return out


def signals(base, red=None, cwd=None):
    found, adds = [], added(base, cwd)
    for path in git("diff", "--name-only", f"{base}...HEAD", cwd=cwd).split():
        for pat, label in owner_reads(cwd):
            if matches(path, pat):
                found.append(f"owner-reads {label}: {path}")
    for path, lines in adds.items():
        for text in lines:
            if SUPPRESS.search(text):
                found.append(f"suppression: {path}: {text.strip()}")
    if red:
        for line in git("diff", "--numstat", f"{red}..HEAD", cwd=cwd).splitlines():
            a, r, path = line.split("\t", 2)
            if is_test(path) and r not in ("0", "-"):
                found.append(f"test lines removed after red commit: {path}")
    test_literals = {m for p, ls in adds.items() if is_test(p) for t in ls for m in LITERAL.findall(t)}
    criteria = git("log", "-1", "--format=%B", red, cwd=cwd) if red else ""
    for path, lines in adds.items():
        if is_test(path):
            continue
        for text in lines:
            for lit in LITERAL.findall(text):
                if lit in test_literals and lit not in criteria:
                    found.append(f"test value in production code: {path}: {lit}")
    return found


def self_test():
    import os, tempfile
    with tempfile.TemporaryDirectory() as d:
        w = lambda p, s: (os.makedirs(os.path.dirname(f"{d}/{p}") or d, exist_ok=True), open(f"{d}/{p}", "w").write(s))
        c = lambda m: (git("add", "-A", cwd=d), git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", m, cwd=d))
        git("init", "-q", "-b", "main", cwd=d)
        w("CODEOWNERS", "# owner reads: data\n/migrations/ @owner\n\n* @team\n")
        w("src/app.py", "x = 1\n")
        w("tests/test_app.py", "def test_a():\n    assert f(2) == 4\n")
        c("base")
        git("checkout", "-qb", "story", cwd=d)
        w("tests/test_app.py", "def test_a():\n    assert f(2) == 4\n\ndef test_b():\n    assert f('cust-000042') == 0\n")
        c("red: criteria")
        red = git("rev-parse", "HEAD", cwd=d).strip()
        assert signals("main", red, d) == [], "a red commit alone fires nothing"
        w("src/app.py", "x = 1\nif user == 'cust-000042': return 0  # noqa\n")
        w("migrations/0002.sql", "alter table t add c int;\n")
        w("tests/test_app.py", "def test_b():\n    assert f('cust-000042') == 0\n")
        c("build")
        got = "\n".join(signals("main", red, d))
        for want in ["owner-reads data: migrations/0002.sql", "suppression: src/app.py",
                     "test lines removed after red commit: tests/test_app.py",
                     "test value in production code: src/app.py: cust-000042"]:
            assert want in got, f"missing: {want}\n{got}"
        assert "src/app.py" not in [l.split(": ")[-1] for l in got.splitlines() if l.startswith("owner-reads")], \
            "a path outside every owner-reads section must not fire"
    print("read_by_exception self-test passed")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    for s in signals(*sys.argv[1:3]):
        print(s)
