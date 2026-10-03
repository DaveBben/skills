#!/usr/bin/env python3
"""Decide whether a YNAB category should be added, split, merged, retired or kept.

    check_category.py                                   sweep: dead, merge, under-spend, surprise-fund leaks
    check_category.py --add "Pet Care" --match "vet|petco"
    check_category.py --split "Personal Care" --match "clothing|shoes"
    check_category.py --remove "Gifts"
    check_category.py --selftest                        offline check

Report-only: nothing is written to YNAB. Reads the same three GETs as
budget-targets, cached under <config dir>/cache/. Stdlib only.
"""
import argparse, datetime as dt, json, os, re, statistics as st, subprocess, sys
import tomllib, urllib.error, urllib.request
from collections import defaultdict
from pathlib import Path

API = "https://api.ynab.com/v1"
INTERNAL_GROUPS = {"Credit Card Payments", "Internal Master Category"}
INTERNAL_CATS = {"Inflow: Ready to Assign", "Deferred Income SubCategory", "Uncategorized"}
BY_HAND = {"emergency_fund", "surprise_fund", "savings_goals", "trial_category", "retirement"}
MERGED = re.compile(r"\s*\((?:->|→)\s*(.+?)\s*\)\s*$")

# Household choices, not findings. Change them here.
SINK_ANNUAL = 400            # C.1: a lumpy fund carries at least this much a year
SINK_MAX_HITS = 6            # C.1: at most this many payments a year
SINK_CONCENTRATION = 0.25    # C.1: the largest payment is at least this share of the year
MERGE_R = 0.7                # merge candidates move together at least this closely
MERGE_MIN_ACTIVE = 6         # months both must spend in before r means anything
MERGE_OVERRUNS = 2           # each side overran its target in at most this many months
DEAD_MONTHS, DEAD_BALANCE = 6, 25
UNDER_RATIO, UNDER_MONTHS = 0.70, 3          # R18
RECUR_MONTHS, RECUR_TOL, RECUR_DAYS = 3, 0.05, 3


# ---- settings and data (same contract as budget-targets) -----------------
def config_dir():
    return Path(os.environ.get("FINANCE_CONFIG_DIR") or "~/.config/finance").expanduser()


def load_config(d):
    p = d / "config.toml"
    if not p.exists():
        sys.exit(f"No settings at {p}. Create it with the keys listed in the category-fit SKILL.md.")
    with open(p, "rb") as f:
        return tomllib.load(f)


def role_map(cfg):
    out = {}
    for role, v in cfg.get("roles", {}).items():
        if role in ("paused", "medical"):   # flags; the category keeps its real role
            continue
        for n in ([v] if isinstance(v, str) else v):
            if n:
                out[n] = role
    return out


def token(service):
    t = subprocess.run(["security", "find-generic-password", "-s", service, "-w"],
                       capture_output=True, text=True).stdout.strip()
    if not t:
        sys.exit(f"No YNAB token in the keychain under service '{service}'.")
    return t


def fetch(budget, service, cache, fresh):
    cache.mkdir(parents=True, exist_ok=True)
    out, tok = {}, None
    for key, path in (("categories", "/categories"), ("accounts", "/accounts"),
                      ("transactions", "/transactions?since_date=2000-01-01")):
        f = cache / f"{key}.json"
        if fresh or not f.exists():
            tok = tok or token(service)
            req = urllib.request.Request(f"{API}/budgets/{budget}{path}",
                                         headers={"Authorization": f"Bearer {tok}"})
            try:
                with urllib.request.urlopen(req) as r:
                    f.write_text(json.dumps(json.load(r)["data"]))
            except urllib.error.HTTPError as e:
                sys.exit(f"Could not fetch {key}: {e.code}")
        out[key] = json.loads(f.read_text())
    out["fetched"] = dt.date.fromtimestamp((cache / "transactions.json").stat().st_mtime).isoformat()
    return out


def build(data):
    """Live categories and net lines (date, category, signed $, payee, payee+memo text).

    CF-6: on-budget accounts only, transfers dropped, inflows kept so refunds
    net against spending, and "Old (-> New)" history folded into New.
    """
    cname, live = {}, []
    for g in data["categories"]["category_groups"]:
        for c in g["categories"]:
            cname[c["id"]] = c["name"]
            if g["name"] in INTERNAL_GROUPS or c["name"] in INTERNAL_CATS:
                continue
            if not (g["hidden"] or c["hidden"] or c["deleted"]):
                live.append(dict(c, group=g["name"]))
    names = {c["name"] for c in live}

    def home(n):
        m = MERGED.search(n)
        return m.group(1) if m and m.group(1) in names else n

    on_budget = {a["id"] for a in data["accounts"]["accounts"] if a["on_budget"] and not a["deleted"]}
    lines = []
    for t in data["transactions"]["transactions"]:
        if t["deleted"] or t["transfer_account_id"] or t["account_id"] not in on_budget:
            continue
        for s in (t.get("subtransactions") or [t]):
            if s.get("deleted") or s.get("transfer_account_id"):
                continue
            payee = t.get("payee_name") or "(no payee)"
            text = " ".join(filter(None, (payee, t.get("memo"), s.get("memo") if s is not t else None)))
            lines.append((t["date"], home(cname.get(s.get("category_id"), "(uncategorized)")),
                          s["amount"] / 1000, payee, text))
    return live, lines


def window(today, n):
    """The n complete calendar months before today's month."""
    y, m, out = today.year, today.month, []
    for _ in range(n):
        y, m = (y - 1, 12) if m == 1 else (y, m - 1)
        out.append(f"{y:04d}-{m:02d}")
    return out[::-1]


def series(lines, win):
    """Net monthly spend over the window, positive is spending. Not clamped, so a payback
    landing a month after its purchase offsets it in every rate."""
    net = defaultdict(float)
    for d, _, a, *_ in lines:
        net[d[:7]] -= a
    return [net[m] for m in win]


# ---- tests ---------------------------------------------------------------
def uncovered(vals, target, set_aside):
    bal, miss = 0.0, 0
    for s in vals:
        bal = bal + target if set_aside else max(bal, target)
        bal -= s
        if bal < -0.005:
            miss, bal = miss + 1, 0.0
    return miss


def goal_type(vals):
    """R12 at the spend rate: set-aside if it leaves fewer months uncovered, refill-up-to
    if refill leaves none, otherwise "undecided" (both types miss the same months)."""
    rate = max(0.0, sum(vals)) / len(vals) if vals else 0.0
    if not rate:
        return None
    vals = [max(0.0, v) for v in vals]       # the replay spends no negative month
    sa, rf = uncovered(vals, rate, True), uncovered(vals, rate, False)
    return "set-aside" if sa < rf else "refill-up-to" if rf == 0 else "undecided"


def pearson(a, b):
    n = len(a)
    if n < 3:
        return 0.0
    ma, mb = sum(a) / n, sum(b) / n
    va, vb = sum((x - ma) ** 2 for x in a), sum((y - mb) ** 2 for y in b)
    if va <= 0 or vb <= 0:
        return 0.0
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (va * vb) ** 0.5


def recurring(lines):
    """CF-5: same payee, amount within 5%, day of month within 3 days, in 3+ months.
    Returns (payee, months, amount) for the first payee that qualifies."""
    by_payee = defaultdict(list)
    for d, _, a, payee, _ in lines:
        if a < 0:
            by_payee[payee].append((d, -a))
    for payee, hits in by_payee.items():
        if len({d[:7] for d, _ in hits}) < RECUR_MONTHS:
            continue
        amt = st.median(a for _, a in hits)
        day = st.median(int(d[8:10]) for d, _ in hits)
        if all(abs(a - amt) <= amt * RECUR_TOL and abs(int(d[8:10]) - day) <= RECUR_DAYS for d, a in hits):
            return payee, len({d[:7] for d, _ in hits}), amt
    return None


def sinking_test(lines, n_months):
    """C.1 on an annual basis (CF-1): totals and counts are scaled by 12 / window months."""
    outs = [-a for _, _, a, *_ in lines if a < 0]
    scale = 12 / n_months
    total = max(0.0, -sum(a for _, _, a, *_ in lines)) * scale    # net of refunds
    hits = len(outs) * scale
    largest = max(outs, default=0.0)
    conc = largest / (total / scale) if total else 0.0
    ok = total >= SINK_ANNUAL and hits <= SINK_MAX_HITS and conc >= SINK_CONCENTRATION
    return ok, total, hits, largest, conc


def monthly_target(c):
    if c.get("goal_type") != "NEED" or c.get("goal_cadence") not in (None, 1):
        return 0.0
    return (c.get("goal_target") or 0) / 1000


def merge_partner(name, by_cat, cats, win, roles):
    """Best merge partner, or None. R13: the two must give the same goal type.
    CF-3: each side may overrun its own target in at most MERGE_OVERRUNS months."""
    def eligible(n):
        return n in cats and roles.get(n) not in BY_HAND and roles.get(n) != "fixed"
    if not eligible(name):
        return None
    mine = series(by_cat.get(name, []), win)
    kind = goal_type(mine)
    if sum(1 for v in mine if v > 0) < MERGE_MIN_ACTIVE or kind == "undecided":
        return None
    best = None
    for other in cats:
        if other == name or not eligible(other):
            continue
        theirs = series(by_cat.get(other, []), win)
        if sum(1 for v in theirs if v > 0) < MERGE_MIN_ACTIVE or goal_type(theirs) != kind:
            continue
        r = pearson(mine, theirs)
        if r <= MERGE_R:
            continue
        if any(sum(1 for v in vals if t and v > t) > MERGE_OVERRUNS
               for vals, t in ((mine, monthly_target(cats[name])), (theirs, monthly_target(cats[other])))):
            continue
        if best is None or r > best[1]:
            best = (other, r, kind)
    return best


def is_dead(c, vals, role):
    """No outflow in 6 months, nothing assigned this month, balance under $25."""
    return (role not in BY_HAND and not any(v > 0 for v in vals[-DEAD_MONTHS:])
            and not c.get("budgeted") and (c.get("balance") or 0) / 1000 < DEAD_BALANCE)


def underspending(c, vals):
    """R18: a refill-up-to target spent under 70% for 3 straight months. Never set-aside."""
    t = monthly_target(c)
    if not t or c.get("goal_needs_whole_amount") is not False:
        return False
    return all(v < UNDER_RATIO * t for v in vals[-UNDER_MONTHS:])


def split_test(part, rest, win):
    """R13: split when the parts need different goal types."""
    a, b = series(part, win), series(rest, win)
    return goal_type(a), goal_type(b), sum(a) / len(win), sum(b) / len(win), pearson(a, b)


# ---- verdicts ------------------------------------------------------------
UNDECIDED = ("Replayed from a $0 balance, both goal types leave the same months uncovered, usually "
             "because a large month comes early in the window. Judge the type with the user: an "
             "expense that arrives in lumps needs set-aside.")


def do_add(name, pattern, lines, by_cat, win, roles):
    rx = re.compile(pattern, re.I)
    rows = [l for l in lines if rx.search(l[4]) and win[0] <= l[0][:7] <= win[-1]]
    L = [f"# Add `{name}`?", "", f"Matched `{pattern}` against payee and memo, {win[0]} to {win[-1]}.", ""]
    net = -sum(a for _, _, a, *_ in rows)
    if net <= 0:
        return L + ["## Verdict: REJECT", "", "No net spending matches in the window. If it starts, "
                    "it lands in an existing category; re-run once there is history."]
    where = defaultdict(float)
    for _, c, a, *_ in rows:
        where[c] -= a
    ranked = sorted(where.items(), key=lambda kv: -kv[1])
    L += ["| Lands in today | Net | Share |", "|---|---|---|"]
    L += [f"| {c} | ${v:,.0f} | {v / net:.0%} |" for c, v in ranked] + [""]
    home = ranked[0][0]

    rec = recurring(rows)
    if rec:
        payee, months, amt = rec
        return L + ["## Verdict: RAISE A TARGET, do not add", "",
                    f"`{payee}` bills about ${amt:,.2f} on the same day in each of {months} months. "
                    f"That is a fixed bill: add it to **{home}**'s target at the current bill and "
                    "name the payee in its note."]

    if len(ranked) == 1:
        rest = [l for l in by_cat.get(home, []) if not rx.search(l[4])]
        ta, tb, ra, rb, r = split_test(rows, rest, win)
        if not tb:
            return L + ["## Verdict: REJECT, it is already a category", "",
                        f"Every dollar in **{home}** matches. Rename **{home}** or rewrite its note instead."]
        if "undecided" in (ta, tb):
            return L + ["## Verdict: UNDECIDED", "", UNDECIDED]
        if ta != tb:
            return L + [f"## Verdict: ADD by splitting it out of {home}", "",
                        f"The matched part needs **{ta}** (${ra:,.0f}/mo); the rest of {home} needs "
                        f"**{tb}** (${rb:,.0f}/mo). One category carries one target, so the parts "
                        "need separate categories. Write a note on each: what it includes, what it excludes."]
        return L + ["## Verdict: REJECT, it already has a home", "",
                    f"Both the matched part and the rest of **{home}** need {ta}. A separate category "
                    f"would carry the same kind of target; fix {home}'s target instead if it runs short."]

    ok, total, hits, largest, conc = sinking_test(rows, len(win))
    if ok:
        return L + ["## Verdict: ADD as a set-aside fund", "",
                    f"Per year: ${total:,.0f} net, {hits:.0f} payments, largest ${largest:,.0f} "
                    f"({conc:.0%} of the window's total). Set aside **${total / 12:,.0f}/month**. "
                    "Move the matching payees' future transactions into it and write its note "
                    "before the first one lands."]
    fails = [f"${total:,.0f}/yr < ${SINK_ANNUAL}" if total < SINK_ANNUAL else "",
             f"{hits:.0f} payments/yr > {SINK_MAX_HITS}" if hits > SINK_MAX_HITS else "",
             f"largest only {conc:.0%} of the total" if conc < SINK_CONCENTRATION else ""]
    surprise = next((n for n, r in roles.items() if r == "surprise_fund"), "the surprise fund")
    return L + ["## Verdict: DO NOT ADD; leave it where it lands", "",
                "Not a lumpy expense worth its own fund: " + "; ".join(f for f in fails if f) + ".",
                "", f"Keep it in **{home}** and raise that target at its next re-derivation if it "
                f"runs short. Only an unforeseeable charge belongs in {surprise}."]


def do_split(name, pattern, by_cat, win):
    rx = re.compile(pattern, re.I)
    lines = by_cat.get(name)
    if lines is None:
        return [f"# Split `{name}`?", "", "No live category by that name."]
    part = [l for l in lines if rx.search(l[4])]
    rest = [l for l in lines if not rx.search(l[4])]
    ta, tb, ra, rb, r = split_test(part, rest, win)
    L = [f"# Split `{name}`?", "", f"Part matching `{pattern}`: {ta or 'no spending'}, ${ra:,.0f}/mo. "
         f"Rest: {tb or 'no spending'}, ${rb:,.0f}/mo. Correlation r = {r:.2f}.", ""]
    if "undecided" in (ta, tb):
        return L + ["## Verdict: UNDECIDED", "", UNDECIDED]
    if ta and tb and ta != tb:
        return L + ["## Verdict: SPLIT", "", "The parts need different goal types, and one category "
                    "carries one target. Create the new category, write a note on each saying what it "
                    "includes and excludes, and re-derive both targets."]
    return L + ["## Verdict: KEEP TOGETHER", "", "Both parts need the same goal type (or one part has "
                "no spending), so a split changes no target."]


def do_remove(name, cats, by_cat, win, roles):
    c = cats.get(name) or next((v for k, v in cats.items() if k.lower() == name.lower()), None)
    if not c:
        return [f"# Remove `{name}`?", "", "No live category by that name."]
    name, role = c["name"], roles.get(c["name"])
    vals = series(by_cat.get(name, []), win)
    L = [f"# Remove `{name}`?", "", f"Role {role or 'none'}, balance ${(c.get('balance') or 0) / 1000:,.2f}, "
         f"${sum(vals):,.0f} net spend {win[0]} to {win[-1]}.", ""]
    if role == "surprise_fund":
        return L + ["## Verdict: KEEP", "", "It is the one surprise fund. Without it every unforeseeable "
                    "cost lands in a category budgeted for something else."]
    if role in BY_HAND:
        return L + ["## Verdict: KEEP", "", f"A {role} category holds a balance toward a goal; spending "
                    "is not its measure. Change it only if the goal itself is gone."]
    if is_dead(c, vals, role):
        return L + ["## Verdict: RETIRE", "", f"No outflow in {DEAD_MONTHS} months, nothing assigned this "
                    f"month, balance under ${DEAD_BALANCE}. The API cannot hide or delete a category: "
                    "hide it in the YNAB app. First ask whether it is the only place a future expense "
                    "is written down; if so, zero its target and keep it."]
    p = merge_partner(name, by_cat, cats, win, roles)
    if p:
        other, r, kind = p
        return L + [f"## Verdict: MERGE into {other}", "", f"Both need {kind}, r = {r:.2f}, and neither "
                    f"overran its target more than {MERGE_OVERRUNS} months. Confirm with the user: if they "
                    f"can name a purchase they would decline because {other} is empty rather than {name}, "
                    "keep both."]
    if underspending(c, vals):
        return L + ["## Verdict: LOWER THE TARGET, do not remove", "", f"Under {UNDER_RATIO:.0%} of its "
                    f"refill-up-to target for {UNDER_MONTHS} straight months. Lower it to its spend rate "
                    f"(${sum(vals) / len(vals):,.0f}/mo) at the next re-derivation."]
    return L + ["## Verdict: KEEP", "", "Not dead, no merge partner with the same goal type, not under-spending."]


def do_sweep(cats, by_cat, win, roles):
    vals = {n: series(by_cat.get(n, []), win) for n in cats}
    count = defaultdict(int)
    for n in cats:
        count[roles.get(n, "no role")] += 1
    L = ["# Category sweep", "", f"Window {win[0]} to {win[-1]}. {len(cats)} live categories: "
         + ", ".join(f"{k} {v}" for k, v in sorted(count.items())) + ". Counts are information, not verdicts.", ""]
    dead = [n for n, c in cats.items() if is_dead(c, vals[n], roles.get(n))]
    L += ["## Retire candidates", ""] + ([f"- {n}" for n in dead] or ["None."])
    seen, pairs = set(), []
    for n in cats:
        p = merge_partner(n, by_cat, cats, win, roles)
        if p and frozenset((n, p[0])) not in seen:
            seen.add(frozenset((n, p[0])))
            pairs.append((n, p[0], p[1], p[2]))
    L += ["", "## Merge candidates (same goal type, moving together)", ""]
    L += [f"- {a} + {b}: r = {r:.2f}, both {k}" for a, b, r, k in sorted(pairs, key=lambda x: -x[2])] or ["None."]
    under = [n for n, c in cats.items() if underspending(c, vals[n])]
    L += ["", f"## Refill-up-to targets under-spent {UNDER_MONTHS} months running (R18)", ""]
    L += [f"- {n}: target ${monthly_target(cats[n]):,.0f}, spend rate ${sum(vals[n]) / len(win):,.0f}/mo"
          for n in under] or ["None."]
    surprise = next((n for n, r in roles.items() if r == "surprise_fund"), None)
    rec = recurring(by_cat.get(surprise, [])) if surprise else None
    L += ["", "## Recurring charges in the surprise fund", ""]
    L += [f"- `{rec[0]}` about ${rec[2]:,.2f} in {rec[1]} months: move it to its own category."] if rec else ["None."]
    return L


# ---- selftest ------------------------------------------------------------
def selftest():
    today = dt.date(2026, 10, 3)
    win12, win8 = window(today, 12), window(today, 8)

    def ln(d, cat, amt, payee="Shop"):
        return (d, cat, amt, payee, payee)

    # CF-1: an 18-month window is annualised before the C.1 thresholds
    win18 = window(today, 18)
    two_vets = [ln("2025-06-10", "Pets", -450.0, "Vet"), ln("2026-06-10", "Pets", -450.0, "Vet")]
    ok, total, hits, *_ = sinking_test(two_vets, 18)
    assert abs(total - 600) < 1e-9 and abs(hits - 4 / 3) < 1e-9 and ok
    assert not sinking_test(two_vets[:1], 18)[0], "$300 a year is under the C.1 floor"

    # CF-2: an 8-month window runs without an index error
    assert len(win8) == 8 and do_sweep({}, {}, win8, {})[0] == "# Category sweep"

    # CF-3: overruns are counted per side, not pooled
    # A never overruns; B overruns 3 months (109-111 > 108). Pooled (3 <= 4) would pass.
    by_cat = {k: [ln(f"{m}-05", k, -(100.0 + i)) for i, m in enumerate(win12)] for k in "AB"}
    cats = {"A": {"name": "A", "goal_type": "NEED", "goal_cadence": 1, "goal_target": 200000},
            "B": {"name": "B", "goal_type": "NEED", "goal_cadence": 1, "goal_target": 108000}}
    assert merge_partner("A", by_cat, cats, win12, {}) is None
    cats["B"]["goal_target"] = 200000
    assert merge_partner("A", by_cat, cats, win12, {})[0] == "B"
    # R13: different goal types never merge
    lumpy = [ln(f"{m}-05", "C", -(1200.0 if i == 0 else 100.0 + i)) for i, m in enumerate(win12)]
    by_cat["C"] = lumpy
    cats["C"] = {"name": "C"}
    assert goal_type(series(lumpy, win12)) != goal_type(series(by_cat["A"], win12))
    assert merge_partner("C", by_cat, cats, win12, {}) is None

    # CF-4: no verdict depends on a category count (no band constants exist)
    assert not any(k in globals() for k in ("SINKING_BAND", "TOTAL_BAND", "GUARDRAIL_CAP"))

    # CF-5: fixed means same payee, amount and day, not a group name
    bill = [ln(f"{m}-05", "Subs", -15.0, "Stream") for m in win12[:4]]
    assert recurring(bill)[0] == "Stream"
    assert not recurring([ln(f"{m}-{d:02d}", "Subs", -15.0, "Stream") for m, d in zip(win12, (1, 9, 20, 28))])
    assert not recurring([ln(f"{m}-05", "Subs", -15.0 * (i + 1), "API") for i, m in enumerate(win12[:4])])

    # CF-6: refunds net out and off-budget accounts are dropped
    data = {"categories": {"category_groups": [{"name": "G", "hidden": False, "categories": [
                {"id": "p", "name": "Pets", "hidden": False, "deleted": False}]}]},
            "accounts": {"accounts": [{"id": "chk", "on_budget": True, "deleted": False},
                                      {"id": "brk", "on_budget": False, "deleted": False}]},
            "transactions": {"transactions": [
                {"date": "2026-05-01", "account_id": "chk", "category_id": "p", "amount": -500000,
                 "payee_name": "Vet", "memo": None, "deleted": False, "transfer_account_id": None},
                {"date": "2026-05-09", "account_id": "chk", "category_id": "p", "amount": 100000,
                 "payee_name": "Vet", "memo": "refund", "deleted": False, "transfer_account_id": None},
                {"date": "2026-05-09", "account_id": "brk", "category_id": "p", "amount": -900000,
                 "payee_name": "Vet", "memo": None, "deleted": False, "transfer_account_id": None}]}}
    _, lines = build(data)
    assert series(lines, win12)[win12.index("2026-05")] == 400.0
    assert abs(sinking_test(lines, 12)[1] - 400.0) < 1e-9

    # a payback landing the month after its purchase offsets it in the split rate
    dinner = [ln(f"{win12[4]}-28", "Food", -300.0, "Group dinner"), ln(f"{win12[5]}-02", "Food", 200.0, "Group dinner")]
    assert abs(split_test(dinner, [], win12)[2] - 100 / 12) < 1e-9

    # R13 split: a lumpy part inside a steady category splits; a steady part does not
    care = [ln(f"{m}-03", "Care", -60.0, "Pharmacy") for m in win12]
    clothes = [ln(f"{win12[i]}-15", "Care", -a, "Clothing Store") for i, a in ((5, 250.0), (11, 300.0))]
    assert do_split("Care", "clothing", {"Care": care + clothes}, win12)[4] == "## Verdict: SPLIT"
    assert do_split("Care", "pharm", {"Care": care}, win12)[4] == "## Verdict: KEEP TOGETHER"

    # R18: only refill-up-to targets are lowered
    vals = [0.0] * 12
    assert underspending({"goal_type": "NEED", "goal_target": 100000, "goal_needs_whole_amount": False}, vals)
    assert not underspending({"goal_type": "NEED", "goal_target": 100000, "goal_needs_whole_amount": True}, vals)
    print("selftest ok: CF-1 CF-2 CF-3 CF-4 CF-5 CF-6 R13 R18 payback")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--add", metavar="NAME", help="proposed new category or expense type")
    g.add_argument("--split", metavar="NAME", help="existing category to test for a split")
    g.add_argument("--remove", metavar="NAME", help="existing category to retire or merge")
    p.add_argument("--match", metavar="REGEX", help="payee/memo pattern for --add and --split")
    p.add_argument("--fresh", action="store_true", help="re-fetch; do this before acting on a verdict")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if a.split and not a.match:
        p.error("--split needs --match")

    d = config_dir()
    cfg = load_config(d)
    data = fetch(cfg["ynab"]["budget_id"], cfg["ynab"]["keychain_service"], d / "cache", a.fresh)
    live, lines = build(data)
    win = window(dt.date.today(), int(cfg.get("scripts", {}).get("months", 12)))
    lines = [l for l in lines if win[0] <= l[0][:7] <= win[-1]]
    by_cat = defaultdict(list)
    for l in lines:
        by_cat[l[1]].append(l)
    cats, roles = {c["name"]: c for c in live}, role_map(cfg)
    global UNDER_RATIO, UNDER_MONTHS
    sc = cfg.get("scripts", {})
    UNDER_RATIO = float(sc.get("underspend_ratio", UNDER_RATIO))
    UNDER_MONTHS = int(sc.get("underspend_months", UNDER_MONTHS))

    if a.add:
        L = do_add(a.add, a.match or re.escape(a.add), lines, by_cat, win, roles)
    elif a.split:
        L = do_split(a.split, a.match, by_cat, win)
    elif a.remove:
        L = do_remove(a.remove, cats, by_cat, win, roles)
    else:
        L = do_sweep(cats, by_cat, win, roles)
    print(f"Data fetched {data['fetched']}.\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
