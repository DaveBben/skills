#!/usr/bin/env python3
"""Derive YNAB category targets from the user's own spending.

* Fixed bills (roles.fixed): the latest bill, spread over its billing period.
* Everything else: last-12-month net spend / 12 x (1 + the category's 12-month
  CPI change from FRED). Funds that spend fewer than twice in 12 months use a
  longer window.
* Goal type: replay the window from a $0 balance as refill-up-to and as
  set-aside; set-aside only when it leaves fewer months uncovered.

Report-only by default; the report goes to <config dir>/history/. --apply
writes goal_target, goal_needs_whole_amount and goal_frequency for the
categories named with --only (or confirmed one by one on a terminal), and
snapshots before and after to history/. Stdlib only.
"""
import argparse, csv, datetime as dt, io, json, os, re, statistics as st, subprocess, sys
import tomllib, urllib.error, urllib.request
from collections import defaultdict
from pathlib import Path

API = "https://api.ynab.com/v1"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
INTERNAL_GROUPS = {"Credit Card Payments", "Internal Master Category"}
INTERNAL_CATS = {"Inflow: Ready to Assign", "Deferred Income SubCategory", "Uncategorized"}
BY_HAND = {"emergency_fund", "surprise_fund", "savings_goals", "trial_category", "retirement"}
MERGED = re.compile(r"\s*\((?:->|→)\s*(.+?)\s*\)\s*$")     # "Clothing (-> Personal Care)"
STEADY = {"steady", "wants"}                                # purchase decisions, for the threshold


# ---- settings and data --------------------------------------------------
def config_dir():
    return Path(os.environ.get("FINANCE_CONFIG_DIR") or "~/.config/finance").expanduser()


def load_config(d):
    p = d / "config.toml"
    if not p.exists():
        sys.exit(f"No settings at {p}. Create it with the keys listed in the budget-targets SKILL.md.")
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


def call(tok, method, path, body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {tok}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"  !! {e.code} {method} {path}: {e.read().decode()[:200]}", file=sys.stderr)
        return None


def fetch(budget, service, cache, fresh):
    """Three GETs, cached under the config dir so personal data never lands in a repo."""
    cache.mkdir(parents=True, exist_ok=True)
    out, tok = {}, None
    for key, path in (("categories", "/categories"), ("accounts", "/accounts"),
                      # since_date is mandatory: without it YNAB returns one year
                      ("transactions", "/transactions?since_date=2000-01-01")):
        f = cache / f"{key}.json"
        if fresh or not f.exists():
            tok = tok or token(service)
            r = call(tok, "GET", f"/budgets/{budget}{path}")
            if r is None:
                sys.exit(f"Could not fetch {key}.")
            f.write_text(json.dumps(r["data"]))
        out[key] = json.loads(f.read_text())
    out["fetched"] = dt.date.fromtimestamp((cache / "transactions.json").stat().st_mtime).isoformat()
    return out


def build(data):
    """Live categories, archived names, and net lines (date, category, signed $).

    DT-3: history under an archived "X (-> Y)" name is folded into Y, so a merge
    does not drop the merged category's past spending.
    """
    cname, live, archived = {}, [], set()
    for g in data["categories"]["category_groups"]:
        for c in g["categories"]:
            cname[c["id"]] = c["name"]
            if g["name"] in INTERNAL_GROUPS or c["name"] in INTERNAL_CATS:
                continue
            if g["hidden"] or c["hidden"] or c["deleted"]:
                archived.add(c["name"])
            else:
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
            lines.append((t["date"], home(cname.get(s.get("category_id"), "(uncategorized)")),
                          s["amount"] / 1000))
    return live, archived, lines


def monthly(lines):
    """Net spend per category per month, positive is spending. Not clamped: a payback
    landing a month after its purchase makes that month negative, and the rate keeps it."""
    net = defaultdict(lambda: defaultdict(float))
    for d, n, a in lines:
        net[n][d[:7]] -= a
    return {n: dict(ms) for n, ms in net.items()}


def window(today, n):
    """DT-6: the n complete months before today's month. Judged by the calendar,
    not by the data, so a run on the 1st keeps last month."""
    y, m, out = today.year, today.month, []
    for _ in range(n):
        y, m = (y - 1, 12) if m == 1 else (y, m - 1)
        out.append(f"{y:04d}-{m:02d}")
    return out[::-1]


def month_gap(a, b):
    return (int(b[:4]) - int(a[:4])) * 12 + int(b[5:7]) - int(a[5:7])


# ---- CPI (DT-4) ----------------------------------------------------------
def yoy(csv_text):
    """12-month change of the latest observation in a FRED CSV."""
    rows = [(r[0], float(r[1])) for r in csv.reader(io.StringIO(csv_text))
            if len(r) > 1 and r[0][:1].isdigit() and r[1] not in ("", ".")]
    last, v = rows[-1]
    prior = dict(rows).get(f"{int(last[:4]) - 1}{last[4:]}")
    if not prior:
        raise ValueError("no observation 12 months before the latest")
    return v / prior - 1, last


def cpi(series, cache, fresh):
    f = cache / f"fred-{series}.csv"
    if fresh or not f.exists():
        req = urllib.request.Request(FRED.format(series), headers={"User-Agent": "budget-targets"})
        with urllib.request.urlopen(req) as r:
            f.write_text(r.read().decode())
    return yoy(f.read_text())


# ---- the rules -----------------------------------------------------------
def uncovered(vals, target, set_aside):
    """Months whose spend exceeded the available balance, replayed from $0.
    Cash overspending resets the category to 0 next month."""
    bal, miss = 0.0, 0
    for s in vals:
        bal = bal + target if set_aside else max(bal, target)
        bal -= s
        if bal < -0.005:
            miss, bal = miss + 1, 0.0
    return miss


def goal_type(vals, target):
    """R12 (DT-2): set-aside only if it leaves fewer months uncovered."""
    return "set-aside" if uncovered(vals, target, True) < uncovered(vals, target, False) else "refill-up-to"


def to5(x):
    return round(x / 5) * 5


def derive(name, role, ser, today, months, long_months, change):
    """One category's recommendation. `change` is its 12-month CPI change."""
    r = {"name": name, "role": role or "-", "note": ""}
    if role in BY_HAND:
        return dict(r, kind="by hand", note=f"{role}: a balance or dated goal, not derivable from spending")
    if role == "fixed":                                   # R10 (DT-1)
        hits = [(m, ser.get(m, 0.0)) for m in window(today, long_months) if ser.get(m, 0.0) > 0]
        if len(hits) < 2:
            return dict(r, kind="by hand", note="fewer than two bills on record; set from the contract")
        gaps = [month_gap(a[0], b[0]) for a, b in zip(hits, hits[1:])]
        period = max(1, round(st.median(gaps)))
        last_m, bill = hits[-1]
        r.update(kind="fixed", target=to5(bill / period) if bill >= 5 else round(bill, 2),
                 type="refill-up-to" if period == 1 else "set-aside", largest=bill, miss=0.0,
                 note=f"latest bill ${bill:,.2f} in {last_m}, every {period} mo; confirm against the contract")
        return r
    raw = [ser.get(m, 0.0) for m in window(today, months)]
    if sum(1 for v in raw if v > 0) < 2:                  # DT-1: rare funds need a longer window
        raw = [ser.get(m, 0.0) for m in window(today, long_months)]
        if sum(1 for v in raw if v > 0) < 2:
            return dict(r, kind="by hand", note=f"fewer than two spending months in {long_months}; "
                        "set from the expected bill and its date")
        r["note"] = f"{long_months}-month window (rare spending)"
    # R11: the rate sums unclamped months, so a payback in a later month offsets its purchase;
    # the replay and largest month use months clamped at 0
    target = to5(max(0.0, sum(raw)) / len(raw) * (1 + change))
    vals = [max(0.0, v) for v in raw]
    first = next(i for i, v in enumerate(vals) if v > 0)
    if first >= len(vals) // 3:
        r["note"] += (f"; first spend in month {first + 1} of {len(vals)}: if the category is newer "
                      "than the window, this rate is too low")
    kind = goal_type(vals, target)
    r.update(kind="derived", target=target, type=kind, largest=max(vals),
             miss=sum(abs(v - target) for v in vals) / len(vals), cpi=change)
    if kind == "refill-up-to" and target < max(vals):      # DT-6: never cap a lumpy fund
        r["refuse"] = (f"refill-up-to ${target:,.0f} is below the largest month ${max(vals):,.0f}; "
                       "choose the type by hand, or split off the lumpy part (R13)")
    return r


def changes(rec, cat):
    """What differs from the target set today."""
    if rec["kind"] not in ("fixed", "derived"):
        return []
    if cat.get("goal_type") in ("TB", "TBD", "MF", "DEBT"):
        return [f"type is {cat['goal_type']}: change it to a NEED target in the app first"]
    if not cat.get("goal_type"):
        return ["new target"]
    cur, out = (cat.get("goal_target") or 0) / 1000, []
    if cat.get("goal_cadence") not in (None, 1):
        out.append("cadence")
    if abs(cur - rec["target"]) >= max(10, cur * 0.10):
        out.append("amount")
    if cat.get("goal_needs_whole_amount") is not None and cat["goal_needs_whole_amount"] != (rec["type"] == "set-aside"):
        out.append("type")
    return out


def threshold(amounts, share):
    """Smallest purchase among the largest that together make `share` of the total."""
    amts = sorted(amounts, reverse=True)
    total, cum = sum(amts), 0.0
    for i, a in enumerate(amts):
        cum += a
        if cum >= total * share:
            return a, i + 1, len(amts), total
    return 0.0, 0, 0, 0.0


# ---- report --------------------------------------------------------------
def report(recs, cats, lines, archived, roles, win, fetched, today):
    lo, hi = win[0], win[-1]
    L = [f"# Targets, {today.isoformat()}", "",
         f"Run {today.isoformat()} on data fetched {fetched}. Spend window {lo} to {hi} "
         "(complete months). Amounts are net of reimbursements; merged history is folded "
         "into the category it moved to.", "",
         "| Category | Role | Type | Current | Recommended | CPI | Typical miss | Change | Note |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in recs:
        c = cats[r["name"]]
        cur = (f"{c.get('goal_type') or 'none'} ${(c.get('goal_target') or 0) / 1000:,.0f}"
               + ("" if c.get("goal_needs_whole_amount") is None else
                  " set-aside" if c["goal_needs_whole_amount"] else " refill"))
        rec = f"**${r['target']:,.0f}**" if "target" in r else r["kind"]
        chg = "REFUSED: " + r["refuse"] if "refuse" in r else ", ".join(r.get("changes", [])) or "none"
        L.append(f"| {r['name']} | {r['role']} | {r.get('type', '-')} | {cur} | {rec} | "
                 f"{r['cpi']:+.1%} | ${r['miss']:,.0f} | {chg} | {r['note'].lstrip('; ')} |"
                 if "cpi" in r else
                 f"| {r['name']} | {r['role']} | {r.get('type', '-')} | {cur} | {rec} | - | - | "
                 f"{chg} | {r['note']} |")

    buys = [-a for d, n, a in lines if a < 0 and lo <= d[:7] <= hi and roles.get(n) in STEADY]
    L += ["", "## Purchase-decision threshold", ""]
    if buys:                                               # DT-5: steady and want categories only
        amt, k, n_all, total = threshold(buys, 0.5)
        L.append(f"Across steady and want categories, the {k} largest of {n_all:,} purchases "
                 f"({100 * k / n_all:.1f}%) carry half of ${total:,.0f}. The smallest of them is "
                 f"${amt:,.0f}: the purchase size above which checking the budget first covers half the money.")
    else:
        L.append("No category has role `steady` or `wants` in config.toml, so no threshold.")

    leak = defaultdict(float)
    last = {}
    for d, n, a in lines:
        if (n in archived or n == "(uncategorized)") and lo <= d[:7] <= hi and a < 0:
            leak[n] -= a
            last[n] = max(last.get(n, ""), d)
    if leak:
        L += ["", "## Spending in archived or uncategorized categories", "",
              "This money counts toward no target above. A recent date is a routing fault "
              "worth fixing; rename an archived category `Old (-> New)` to fold its history into New.", ""]
        L += [f"- {n}: ${v:,.0f} (last {last[n]})" for n, v in sorted(leak.items(), key=lambda x: -x[1])]
    return L


# ---- apply (DT-6) --------------------------------------------------------
def choose(patches, only, ask):
    """Only categories the user approved: named with --only, or confirmed one by one."""
    if only:
        unknown = set(only) - {p["name"] for p in patches}
        if unknown:
            sys.exit(f"Not patchable (no change, refused or by hand): {', '.join(sorted(unknown))}")
        return [p for p in patches if p["name"] in only]
    if ask is None:
        sys.exit("Refusing to apply: pass --only NAME for each category the user approved.")
    return [p for p in patches if ask(f"{p['name']}: {p['type']} ${p['target']:,.0f}? [y/N] ").strip().lower() == "y"]


def apply(budget, service, chosen, cats, history, today):
    tok = token(service)
    stamp = f"{today.isoformat()}-budget-targets"
    (history / f"{stamp}-before.json").write_text(json.dumps([cats[p["name"]] for p in chosen], indent=1))
    after, log = [], []
    for p in chosen:
        body = {"goal_target": int(round(p["target"] * 1000)),
                "goal_needs_whole_amount": p["type"] == "set-aside", "goal_frequency": "monthly"}
        r = call(tok, "PATCH", f"/budgets/{budget}/categories/{cats[p['name']]['id']}", {"category": body})
        if r:
            c = r["data"]["category"]
            after.append(c)
            log.append(f"- {p['name']}: {p['type']} ${c['goal_target'] / 1000:,.2f} "
                       f"(was {cats[p['name']].get('goal_type')} ${(cats[p['name']].get('goal_target') or 0) / 1000:,.2f})")
    (history / f"{stamp}-after.json").write_text(json.dumps(after, indent=1))
    with open(history / f"{stamp}.md", "a") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log), file=sys.stderr)


# ---- selftest ------------------------------------------------------------
def selftest():
    today = dt.date(2026, 10, 1)
    # DT-6: a run on the 1st keeps last month; the current month is excluded
    assert window(today, 12)[-1] == "2026-09" and window(today, 12)[0] == "2025-10"
    assert window(dt.date(2026, 10, 31), 1) == ["2026-09"]
    m12 = window(today, 12)

    # DT-3: merged history folds into the live category
    data = {"categories": {"category_groups": [
                {"name": "Spend", "hidden": False, "categories": [
                    {"id": "pc", "name": "Personal Care", "hidden": False, "deleted": False}]},
                {"name": "Old", "hidden": True, "categories": [
                    {"id": "cl", "name": "Clothing (-> Personal Care)", "hidden": True, "deleted": False}]}]},
            "accounts": {"accounts": [{"id": "chk", "on_budget": True, "deleted": False},
                                      {"id": "ira", "on_budget": False, "deleted": False}]},
            "transactions": {"transactions": [
                {"date": "2026-03-04", "account_id": "chk", "category_id": "cl", "amount": -300000,
                 "deleted": False, "transfer_account_id": None, "subtransactions": []},
                {"date": "2026-03-09", "account_id": "chk", "category_id": "pc", "amount": -50000,
                 "deleted": False, "transfer_account_id": None, "subtransactions": []},
                {"date": "2026-03-10", "account_id": "ira", "category_id": "pc", "amount": -999000,
                 "deleted": False, "transfer_account_id": None, "subtransactions": []}]}}
    live, archived, lines = build(data)
    assert monthly(lines)["Personal Care"]["2026-03"] == 350.0, "merged history and off-budget filter"

    # DT-1 / R10: fixed bill uses the latest bill, not the average
    rent = {m: (1050.0 if m < "2026-06" else 1000.0) for m in window(today, 36)}
    r = derive("Rent", "fixed", rent, today, 12, 36, 0.0)
    assert r["target"] == 1000 and r["type"] == "refill-up-to"
    annual = {"2024-11": 1200.0, "2025-11": 1200.0}
    r = derive("Insurance", "fixed", annual, today, 12, 36, 0.0)
    assert r["target"] == 100 and r["type"] == "set-aside"

    # DT-1: a fund with one hit in 12 months uses the long window
    car = {"2024-02": 600.0, "2025-01": 900.0, "2026-04": 1500.0}
    r = derive("Car Repair", "bill_funds", car, today, 12, 36, 0.0)
    assert r["target"] == to5(3000 / 36) and "36-month" in r["note"]
    assert derive("Rare", None, {"2026-04": 50.0}, today, 12, 36, 0.0)["kind"] == "by hand"

    # DT-2 / R12: a small monthly fee does not turn a lumpy fund into refill-up-to
    lumpy = {m: 10.0 for m in m12}
    lumpy[m12[5]] = lumpy[m12[11]] = 400.0
    r = derive("Surprises", "bill_funds", lumpy, today, 12, 36, 0.0)
    assert r["type"] == "set-aside" and "refuse" not in r
    # set-aside never leaves more months uncovered, so refill-up-to wins only on a tie
    r = derive("Phone plan", "steady", {m: 400.0 for m in m12}, today, 12, 36, 0.0)
    assert r["type"] == "refill-up-to" and "refuse" not in r

    # DT-6: refuse to cap a lumpy fund when the replay cannot tell the types apart
    first_hit = {m: 0.0 for m in m12}
    first_hit[m12[0]] = 1200.0
    first_hit[m12[1]] = 1.0
    r = derive("Lumpy", None, first_hit, today, 12, 36, 0.0)
    assert r["type"] == "refill-up-to" and "refuse" in r

    # DT-3: no trimming to the first spend; a late first spend is flagged instead
    late = {m: (100.0 if m >= "2026-06" else 0.0) for m in m12}
    r = derive("New", "steady", late, today, 12, 36, 0.0)
    assert r["target"] == to5(400 / 12) and "first spend" in r["note"]

    # R11: a payback landing the month after its purchase offsets it in the rate
    dining = {m: 100.0 for m in m12}
    dining[m12[5]], dining[m12[6]] = 300.0, -100.0       # $200 paid back next month
    r = derive("Dining", "wants", dining, today, 12, 36, 0.0)
    assert r["target"] == 100 and r["largest"] == 300.0, r

    # DT-4: CPI from a FRED CSV raises the target
    fred = "observation_date,X\n2025-08-01,100.0\n2025-09-01,.\n2026-08-01,103.0\n"
    ch, last = yoy(fred)
    assert abs(ch - 0.03) < 1e-9 and last == "2026-08-01"
    assert derive("Dining", "wants", {m: 200.0 for m in m12}, today, 12, 36, ch)["target"] == 205

    # DT-5: the threshold ignores fixed bills
    lines = [("2026-09-01", "Rent", -1000.0)] + [("2026-09-02", "Dining", -a) for a in (100.0, 20.0, 10.0)]
    roles = {"Rent": "fixed", "Dining": "wants"}
    buys = [-a for d, n, a in lines if roles.get(n) in STEADY]
    assert threshold(buys, 0.5)[0] == 100.0

    # DT-6: --apply needs an allow-list or per-category confirmation
    patches = [{"name": "A", "type": "set-aside", "target": 10}, {"name": "B", "type": "set-aside", "target": 20}]
    assert [p["name"] for p in choose(patches, ["B"], None)] == ["B"]
    assert [p["name"] for p in choose(patches, [], lambda q: "y" if q.startswith("A") else "n")] == ["A"]
    for args in ((patches, [], None), (patches, ["Z"], None)):
        try:
            choose(*args)
            raise AssertionError("choose should refuse")
        except SystemExit:
            pass
    assert changes({"kind": "derived", "target": 100, "type": "set-aside"},
                   {"goal_type": "TB", "goal_target": 5000000}) and \
        changes({"kind": "derived", "target": 100, "type": "set-aside"},
                {"goal_type": "NEED", "goal_target": 100000, "goal_cadence": 1,
                 "goal_needs_whole_amount": True}) == []
    print("selftest ok: DT-1 DT-2 DT-3 DT-4 DT-5 DT-6 R11-payback")


# ---- main ----------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fresh", action="store_true", help="re-fetch YNAB and FRED instead of using the cache")
    p.add_argument("--out", help="report path (default history/<date>-targets.md)")
    p.add_argument("--no-cpi", action="store_true", help="skip FRED; targets get no price change")
    p.add_argument("--apply", action="store_true", help="write the approved targets (always re-fetches)")
    p.add_argument("--only", action="append", default=[], metavar="NAME",
                   help="category the user approved; repeat per category")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()

    d = config_dir()
    cfg = load_config(d)
    budget, service = cfg["ynab"]["budget_id"], cfg["ynab"]["keychain_service"]
    sc = cfg.get("scripts", {})
    months, long_months = int(sc.get("months", 12)), int(sc.get("long_months", 36))
    cache, history = d / "cache", d / "history"
    history.mkdir(parents=True, exist_ok=True)
    today = dt.date.today()

    data = fetch(budget, service, cache, a.fresh or a.apply)
    live, archived, lines = build(data)
    ser, roles = monthly(lines), role_map(cfg)
    cats = {c["name"]: c for c in live}

    changes_by_series = {}
    def change_for(name):
        sid = cfg.get("cpi", {}).get(name, sc.get("cpi_default", "CPIAUCSL"))
        if a.no_cpi or not sid:
            return 0.0
        if sid not in changes_by_series:
            try:
                changes_by_series[sid] = cpi(sid, cache, a.fresh)[0]
            except (OSError, ValueError) as e:
                sys.exit(f"CPI series {sid} unavailable ({e}). Re-run with --no-cpi to skip prices.")
        return changes_by_series[sid]

    recs = []
    for c in sorted(live, key=lambda c: -sum(ser.get(c["name"], {}).values())):
        n, role = c["name"], roles.get(c["name"])
        if not ser.get(n) and role not in BY_HAND:
            continue
        r = derive(n, role, ser.get(n, {}), today, months, long_months,
                   change_for(n) if role != "fixed" else 0.0)
        r["changes"] = changes(r, c)
        recs.append(r)

    L = report(recs, cats, lines, archived, roles, window(today, months), data["fetched"], today)
    out = Path(a.out) if a.out else history / f"{today.isoformat()}-targets.md"
    out.write_text("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n--- report written to {out} ---", file=sys.stderr)

    patches = [r for r in recs if r.get("changes") and "refuse" not in r
               and not r["changes"][0].startswith("type is")]
    if a.apply:
        chosen = choose(patches, a.only, input if sys.stdin.isatty() else None)
        if chosen:
            apply(budget, service, chosen, cats, history, today)
    elif patches:
        print(f"{len(patches)} categories have a patchable change. Confirm each with the user, "
              "then re-run with --apply --only NAME ...", file=sys.stderr)


if __name__ == "__main__":
    main()
