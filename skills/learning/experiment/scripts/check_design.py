#!/usr/bin/env python3
"""Checks an experiment design document, for the experiment skill.

  * the 13 required `##` sections are present, in order, and none is empty;
  * the Status section starts with design only, piloted, running, or done;
  * every relative link resolves, including a #heading anchor;
  * the 1 `sample-size:` line recomputes: its n is at least the formula's n, or
    equals a stated cap and the design calls a null result inconclusive;
  * with --ready, the Open decisions section is empty or says None: the gate for the pilot.

Usage: check_design.py [--ready] [EXPERIMENT.md]
Prints each failure and exits 1, or prints "design check passed". Run with --self-test to check it.
"""
import math, os, re, sys, tempfile
from statistics import NormalDist

SECTIONS = ["Status", "Why this question is open", "Hypotheses", "Arms", "Controlled variables",
            "Measures", "Objects", "Procedure", "Analysis", "Assumptions", "Threats to validity",
            "Reproducibility and audit", "Open decisions"]
STATES = ("design only", "piloted", "running", "done")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
EXAMPLE = "sample-size: alpha=0.05 power=0.80 delta=5 sigma=10 are=0.864 n=37"


def sections(text):
    """Each `##` section's title mapped to its body lines, ignoring code fences."""
    out, name, fence = {}, None, False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        if not fence and line.startswith("## "):
            name = line[3:].strip()
            out.setdefault(name, [])
        elif name is not None:
            out[name].append(line)
    return out


def slugs(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return {re.sub(r"[^\w\- ]", "", m.lower()).replace(" ", "-")
            for m in re.findall(r"^#{1,6} +(.+?) *$", text, re.M)}


def links(path, text):
    errs, base = [], os.path.dirname(os.path.abspath(path))
    for target in LINK.findall(re.sub(r"```.*?```", "", text, flags=re.S)):
        if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I):
            continue
        file, _, anchor = target.partition("#")
        full = os.path.join(base, file) if file else os.path.abspath(path)
        if not os.path.exists(full):
            errs.append(f"broken link: {target}")
        elif anchor and full.endswith(".md") and anchor.lower() not in slugs(open(full, encoding="utf-8").read()):
            errs.append(f"broken anchor: {target}")
    return errs


def sample_size(text):
    found = [s for s in (l.strip(" *`\t") for l in text.splitlines()) if s.startswith("sample-size:")]
    if len(found) != 1:
        return [f"expected 1 sample-size line, found {len(found)}: write one such as '{EXAMPLE}'"], []
    p = {k: float(v) for k, v in re.findall(r"(\w+)=([\d.]+)", found[0])}
    try:
        z = NormalDist().inv_cdf
        need = math.ceil(((z(1 - p["alpha"] / 2) + z(p["power"])) * p["sigma"] / p["delta"]) ** 2 / p.get("are", 1))
        n = p["n"]
    except (KeyError, ValueError, ZeroDivisionError) as e:
        return [f"the sample-size line needs alpha, power, delta, sigma, and n as numbers ({e!r}): '{EXAMPLE}'"], []
    if n >= need:
        return [], []
    if n == p.get("cap"):
        msg = f"n={n:g} is capped below the {need} units the power analysis needs"
        if "inconclusive" not in text.lower():
            return [msg + ", and the design never says a null result is then inconclusive"], []
        return [], [msg + ": a null result is inconclusive"]
    return [f"n={n:g} is below the {need} units the formula gives for these values"], []


def check(path, ready=False):
    text = open(path, encoding="utf-8").read()
    secs, errs = sections(text), []
    missing = [s for s in SECTIONS if s not in secs]
    if missing:
        errs.append("missing sections: " + ", ".join(missing))
    elif [s for s in secs if s in SECTIONS] != SECTIONS:
        errs.append("sections out of order, expected: " + ", ".join(SECTIONS))
    for s in SECTIONS[:-1]:
        if s in secs and not any(l.strip() for l in secs[s]):
            errs.append(f"section '{s}' is empty: write it, or write 'Not applicable: <reason>'")
    status = next((l.strip().lower() for l in secs.get("Status", []) if l.strip()), "")
    if "Status" in secs and not status.startswith(STATES):
        errs.append("Status must start with one of: " + ", ".join(STATES))
    if ready:
        items = [l for l in (x.strip(" *-.\t").lower() for x in secs.get("Open decisions", [])) if l and l != "none"]
        if items:
            errs.append(f"{len(items)} open decisions remain: the pilot waits until the list is empty")
    errs += links(path, text)
    size_errs, warns = sample_size(text)
    return errs + size_errs, warns


def main(argv):
    paths = [a for a in argv if a != "--ready"] or ["EXPERIMENT.md"]
    errs, warns = check(paths[0], "--ready" in argv)
    for w in warns:
        print("warning:", w)
    for e in errs:
        print("FAIL:", e)
    print(f"{len(errs)} failures" if errs else "design check passed")
    return 1 if errs else 0


def self_test():
    d = tempfile.mkdtemp()
    open(os.path.join(d, "other.md"), "w").write("# Other\n\n## Some part\n\nText.\n")
    path = os.path.join(d, "EXPERIMENT.md")

    def run(ready=False, order=SECTIONS, **over):
        body = {s: "Text." for s in SECTIONS}
        body.update(Status="Design only: the pilot waits.", **{"Open decisions": "None."},
                    Objects=EXAMPLE + "\n\nSee [the part](other.md#some-part).")
        body.update({k.replace("_", " "): v for k, v in over.items()})
        open(path, "w").write("# Does X beat Y?\n\n" + "\n\n".join(f"## {s}\n\n{body[s]}" for s in order if s in body))
        return check(path, ready)

    assert run() == ([], []), run()
    assert run(Objects=EXAMPLE.replace("n=37", "n=36"))[0], "36 is below the 37 units at ARE 0.864"
    assert run(Objects=EXAMPLE.replace("are=0.864 n=37", "n=32")) == ([], []), "32 units for the t-test"
    assert run(Objects=EXAMPLE.replace("n=37", "n=30 cap=30"))[0], "a cap with no inconclusive clause fails"
    capped = run(Objects=EXAMPLE.replace("n=37", "n=30 cap=30") + "\n\nA null result is inconclusive.")
    assert not capped[0] and capped[1], "a stated cap warns"
    assert run(Objects=EXAMPLE + "\n\n" + EXAMPLE)[0], "2 sample-size lines"
    assert run(Objects="No sample size.")[0], "no sample-size line"
    assert run(Objects="sample-size: alpha=0.05 power=0.80 delta=5 n=37")[0], "sigma missing"
    assert run(order=[s for s in SECTIONS if s != "Assumptions"])[0], "missing section"
    assert run(order=SECTIONS[1:2] + SECTIONS[:1] + SECTIONS[2:])[0], "out of order"
    assert run(Measures="")[0], "empty section"
    assert run(Measures="Not applicable: no measures.") == ([], []), "not applicable passes"
    assert run(Status="Draft")[0], "unknown status"
    assert not run(Open_decisions="* Which model to run")[0], "open decisions pass without --ready"
    assert run(True, Open_decisions="* Which model to run")[0], "open decisions block --ready"
    assert run(True) == ([], []), "None passes --ready"
    assert run(Arms="[x](other.md#nope)")[0], "broken anchor"
    assert run(Arms="[x](missing.md)")[0], "broken link"
    assert run(Arms="[x](https://example.com/a.md)") == ([], []), "URLs are not checked"
    assert run(Arms="```text\n## Status\n[x](missing.md)\n```") == ([], []), "code fences are ignored"
    print("self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    else:
        sys.exit(main(sys.argv[1:]))
