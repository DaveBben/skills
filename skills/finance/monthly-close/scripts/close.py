#!/usr/bin/env python3
"""Month-end close for a YNAB budget.

  close.py scan [--month YYYY-MM]          read-only report as JSON (default: the current month)
  close.py apply plan.json [--confirm]     move assigned money and append note lines
  close.py delete-txn <id> [--confirm]     delete one transaction (a confirmed duplicate)
  close.py --selftest                      check the cover logic offline

Settings: $FINANCE_CONFIG_DIR/config.toml, default ~/.config/finance/config.toml.
Token: $YNAB_ACCESS_TOKEN, else the macOS keychain service named in [ynab] keychain_service.
Writes run only with --confirm; without it they print what they would do.
Run on the last day or two of the month: once a month has rolled over, YNAB has already turned
its uncovered overspending into card debt or a cut to next month's Ready to Assign.
"""
import argparse
import datetime as dt
import functools
import json
import os
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

API = "https://api.ynab.com/v1"
DEFAULT_ORDER = ["wants", "trial_category", "emergency_fund", "bill_funds"]
CARD_GROUP = "Credit Card Payments"


def config_dir():
    return Path(os.environ.get("FINANCE_CONFIG_DIR") or "~/.config/finance").expanduser()


def load_config():
    path = config_dir() / "config.toml"
    if not path.exists():
        sys.exit(f"No settings file at {path}. Create it or set FINANCE_CONFIG_DIR.")
    return tomllib.loads(path.read_text())


@functools.cache
def token(service):
    if os.environ.get("YNAB_ACCESS_TOKEN"):
        return os.environ["YNAB_ACCESS_TOKEN"]
    r = subprocess.run(["security", "find-generic-password", "-s", service, "-w"],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"Could not read the YNAB token from keychain service {service!r}; set YNAB_ACCESS_TOKEN.")
    return r.stdout.strip()


def api(cfg, method, path, body=None):
    req = urllib.request.Request(
        f"{API}/budgets/{cfg['ynab']['budget_id']}{path}", method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {token(cfg['ynab']['keychain_service'])}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)["data"]
    except urllib.error.HTTPError as e:
        sys.exit(f"YNAB {method} {path} failed: {e.code} {e.read().decode()[:300]}")


def names(cfg, role):
    v = cfg.get("roles", {}).get(role, [])
    return [v] if isinstance(v, str) else list(v)


def money(m):
    return f"${m / 1000:,.2f}"


def by_name(cats):
    """Name -> category. A visible category wins over a hidden one of the same name."""
    out = {}
    for c in cats:
        if c.get("deleted"):
            continue
        if c["name"] not in out or out[c["name"]].get("hidden"):
            out[c["name"]] = c
    return out


def protected_names(cfg, card_names):
    """Categories that are never a cover source."""
    return (set(names(cfg, "surprise_fund")) | set(names(cfg, "retirement"))
            | set(names(cfg, "paused")) | set(card_names))


def this_month(today=None):
    return (today or dt.date.today()).strftime("%Y-%m")


def rollover_warning(month, today=None):
    """A warning when the month has already rolled over, else None."""
    if month >= this_month(today):
        return None
    return (f"{month} has already rolled over. YNAB advises against editing a past month: its uncovered "
            "cash overspending was already taken from the next month's Ready to Assign, and its uncovered "
            "credit-card overspending is now card debt. Fund that debt in the current month's card payment "
            "category instead of covering inside the past month.")


def cover_plan(cats, cfg, card_names=()):
    """Cover each negative category from the cover_order steps. Amounts in milliunits."""
    order = cfg.get("cover_order", {}).get("steps", DEFAULT_ORDER)
    bad = [s for s in order if s not in DEFAULT_ORDER]
    if bad:
        raise ValueError(f"cover_order steps {bad} are not allowed cover sources; "
                         f"use only {DEFAULT_ORDER}")
    cat = by_name(cats)
    protected = protected_names(cfg, card_names)
    avail = {}
    for step in order:
        for n in names(cfg, step):
            c = cat.get(n)
            if c is None or n in protected or n in avail:
                continue
            a = min(c["balance"], c["budgeted"]) if step == "trial_category" else c["balance"]
            avail[n] = (max(a, 0), step)
    negatives = sorted((c for c in cat.values() if c["balance"] < 0 and c["name"] not in card_names),
                       key=lambda c: c["balance"])
    moves, uncovered = [], []
    for neg in negatives:
        need = -neg["balance"]
        for src, (a, step) in avail.items():
            if need == 0:
                break
            if src == neg["name"] or a <= 0:
                continue
            amt = min(a, need)
            avail[src] = (a - amt, step)
            need -= amt
            moves.append({"from": src, "to": neg["name"], "amount": amt, "step": step})
        if need:
            uncovered.append({"category": neg["name"], "amount": need})
    return moves, uncovered


def find_duplicates(txns, since):
    """Pairs in one account on one date with opposite amounts, both imported: likely sign-flipped imports."""
    seen = defaultdict(list)
    pairs = []
    for t in txns:
        if t.get("deleted") or t["date"] < since or not t.get("import_id") or t.get("transfer_account_id"):
            continue
        for u in seen[(t["account_id"], t["date"], -t["amount"])]:
            pairs.append([u, t])
        seen[(t["account_id"], t["date"], t["amount"])].append(t)
    return [[{k: x.get(k) for k in ("id", "date", "amount", "payee_name", "import_id", "account_name")}
             for x in p] for p in pairs if p[0]["amount"]]


def monthly_spend(txns, id_to_name):
    """(category name, YYYY-MM) -> net outflow in milliunits (refunds reduce it)."""
    out = defaultdict(int)
    for t in txns:
        if t.get("deleted"):
            continue
        parts = [s for s in t.get("subtransactions") or [] if not s.get("deleted")] or [t]
        for p in parts:
            n = id_to_name.get(p.get("category_id"))
            if n:
                out[(n, t["date"][:7])] -= p["amount"]
    return out


def month_list(end, count):
    y, m = map(int, end.split("-"))
    out = []
    for _ in range(count):
        out.append(f"{y:04d}-{m:02d}")
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    return out[::-1]


def note_cover_count(note, months):
    hits = {ln[:7] for ln in (note or "").splitlines() if re.match(r"\d{4}-\d{2}: .*covered", ln)}
    return len(hits & set(months))


def scan(cfg, month):
    sc = cfg.get("scripts", {})
    window = sc.get("months", 12)
    lookback = sc.get("cover_lookback_months", 6)
    warning = rollover_warning(month)
    if warning:
        print(f"WARNING: {warning}", file=sys.stderr)
    mdata = api(cfg, "GET", f"/months/{month}-01")["month"]
    cats = [c for c in mdata["categories"] if not c.get("deleted")]
    groups = api(cfg, "GET", "/categories")["category_groups"]
    accounts = api(cfg, "GET", "/accounts")["accounts"]
    months = month_list(month, window)
    txns = api(cfg, "GET", f"/transactions?since_date={months[0]}-01")["transactions"]

    card_now = {c["name"]: c for g in groups if g["name"] == CARD_GROUP
                for c in g["categories"] if not c.get("deleted")}
    cards = []
    for a in accounts:
        if a["type"] in ("creditCard", "lineOfCredit") and a["on_budget"] and not a["closed"] and not a["deleted"]:
            c = card_now.get(a["name"])
            owed = -a["balance"]
            cards.append({"card": a["name"], "owed": money(owed),
                          "payment_category": money(c["balance"]) if c else None,
                          "ok": bool(c) and c["balance"] >= owed})

    cat = by_name(cats)
    moves, uncovered = cover_plan(cats, cfg, card_now.keys())
    first_step = cfg.get("cover_order", {}).get("steps", DEFAULT_ORDER)[0]
    notes = []
    for mv in moves:
        c = cat[mv["to"]]
        notes.append({"category": mv["to"], "line": f"{month}: target {money(c.get('goal_target') or 0)}, "
                      f"spent {money(-c['activity'])}, covered {money(mv['amount'])} from {mv['from']}"})

    id_to_name = {c["id"]: c["name"] for c in cats}
    spend = monthly_spend(txns, id_to_name)
    wants = set(names(cfg, "wants"))
    essential = (set(names(cfg, "fixed")) | set(names(cfg, "steady")) | set(names(cfg, "bill_funds"))) - wants
    ess_month = sum(spend[(n, m)] for n in essential for m in months) / len(months)
    ef = cat.get(next(iter(names(cfg, "emergency_fund")), ""), {}).get("balance", 0)

    trial = None
    tname = next(iter(names(cfg, "trial_category")), None)
    if tname and tname in cat:
        t = cat[tname]
        trial = {"category": tname, "assigned": money(t["budgeted"]), "target": money(t.get("goal_target") or 0),
                 "under_funded": money(t.get("goal_under_funded") or 0), "activity": money(t["activity"]),
                 "month_income": money(mdata["income"]),
                 "base_monthly": money(int(cfg["income"]["base_monthly"] * 1000)),
                 "covers_beyond_step_1": [m["from"] for m in moves if m["step"] != first_step]}

    report = {
        "month": month,
        "rollover_warning": warning,
        "ready_to_assign": money(mdata["to_be_budgeted"]),
        "negative_categories": [{"category": c["name"], "balance": money(c["balance"]), "hidden": c.get("hidden")}
                                for c in cats if c["balance"] < 0],
        "proposed_plan": {"month": month,
                          "moves": [{**m, "amount": m["amount"] / 1000} for m in moves],
                          "notes": notes},
        "uncovered": [{**u, "amount": money(u["amount"])} for u in uncovered],
        "cards": cards,
        "bill_funds_under_target": [n for n in names(cfg, "bill_funds")
                                    if n in cat and (cat[n].get("goal_under_funded") or 0) > 0],
        "trial": trial,
        "covered_months_in_lookback": {mv["to"]: note_cover_count(cat[mv["to"]].get("note"),
                                                                  month_list(month, lookback)) + 1
                                       for mv in moves},
        "possible_duplicate_imports": find_duplicates(txns, f"{months[-1]}-01"),
        "r29": {"discretionary_last_3_months": money(sum(spend[(n, m)] for n in wants for m in months[-3:])),
                "essential_monthly_mean": money(int(ess_month)),
                "emergency_balance": money(ef),
                "emergency_months": round(ef / ess_month, 1) if ess_month > 0 else None},
    }
    print(json.dumps(report, indent=2))


def apply(cfg, plan, confirm):
    month = plan["month"]
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        sys.exit("plan month must be YYYY-MM")
    warning = rollover_warning(month)
    if warning:
        print(f"WARNING: {warning}", file=sys.stderr)
    groups = api(cfg, "GET", "/categories")["category_groups"]
    cards = {c["name"] for g in groups if g["name"] == CARD_GROUP for c in g["categories"]}
    cat = by_name([c for g in groups for c in g["categories"]])
    protected = protected_names(cfg, cards)
    for mv in plan.get("moves", []):
        if mv["from"] in protected:
            sys.exit(f"Refusing: {mv['from']} is a surprise, retirement, card payment or paused category.")
        for n in (mv["from"], mv["to"]):
            if n not in cat:
                sys.exit(f"No category named {n!r}.")
    for mv in plan.get("moves", []):
        amt = round(mv["amount"] * 1000)
        print(f"move {money(amt)} from {mv['from']} to {mv['to']} in {month}")
        if confirm:
            for n, delta in ((mv["from"], -amt), (mv["to"], amt)):
                cid = cat[n]["id"]
                cur = api(cfg, "GET", f"/months/{month}-01/categories/{cid}")["category"]["budgeted"]
                api(cfg, "PATCH", f"/months/{month}-01/categories/{cid}", {"category": {"budgeted": cur + delta}})
    for nt in plan.get("notes", []):
        if nt["category"] not in cat:
            sys.exit(f"No category named {nt['category']!r}.")
        print(f"append to {nt['category']} note: {nt['line']}")
        if confirm:
            cid = cat[nt["category"]]["id"]
            note = api(cfg, "GET", f"/categories/{cid}")["category"].get("note") or ""
            api(cfg, "PATCH", f"/categories/{cid}", {"category": {"note": (note.rstrip() + "\n" + nt["line"]).strip()}})
    if not confirm:
        sys.exit("Dry run. Re-run with --confirm after the user approves.")


def delete_txn(cfg, tid, confirm):
    t = api(cfg, "GET", f"/transactions/{tid}")["transaction"]
    print(f"delete {t['date']} {t.get('payee_name')} {money(t['amount'])} in {t.get('account_name')} "
          f"(import_id {t.get('import_id')})")
    if not confirm:
        sys.exit("Dry run. Re-run with --confirm after the user has checked the bank balance.")
    api(cfg, "DELETE", f"/transactions/{tid}")


def selftest():
    cfg = {"roles": {"wants": ["Fun", "Food", "Gear"], "trial_category": "Trial", "emergency_fund": "EF",
                     "bill_funds": ["Bills"], "surprise_fund": "Oops", "retirement": ["IRA"], "paused": ["Gear"]}}
    cats = [{"name": "Food", "balance": -50_000, "budgeted": 100_000},
            {"name": "Gear", "balance": 70_000, "budgeted": 0},
            {"name": "Fun", "balance": 20_000, "budgeted": 20_000},
            {"name": "Trial", "balance": 500_000, "budgeted": 10_000},
            {"name": "EF", "balance": 900_000, "budgeted": 0},
            {"name": "Oops", "balance": 99_000, "budgeted": 0},
            {"name": "Card", "balance": 99_000, "budgeted": 0},
            {"name": "Food", "balance": 5_000, "budgeted": 0, "hidden": True}]
    moves, unc = cover_plan(cats, cfg, card_names=["Card"])
    assert [(m["from"], m["amount"]) for m in moves] == [("Fun", 20_000), ("Trial", 10_000), ("EF", 20_000)], moves
    assert not unc
    try:
        cover_plan(cats, {**cfg, "cover_order": {"steps": ["surprise_fund"]}})
        raise AssertionError("surprise fund accepted as a cover source")
    except ValueError:
        pass
    tx = [{"id": "a", "account_id": "x", "date": "2026-01-02", "amount": 5_000, "import_id": "YNAB:5000:2026-01-02:1"},
          {"id": "b", "account_id": "x", "date": "2026-01-02", "amount": -5_000, "import_id": "YNAB:-5000:2026-01-02:1"},
          {"id": "c", "account_id": "y", "date": "2026-01-02", "amount": -5_000, "import_id": "z"}]
    assert [[p[0]["id"], p[1]["id"]] for p in find_duplicates(tx, "2026-01-01")] == [["a", "b"]]
    assert month_list("2026-02", 3) == ["2025-12", "2026-01", "2026-02"]
    assert note_cover_count("2026-01: target $1, spent $2, covered $1 from Fun\nother", ["2026-01"]) == 1
    today = dt.date(2026, 10, 30)
    assert this_month(today) == "2026-10"
    assert rollover_warning("2026-10", today) is None
    assert "rolled over" in rollover_warning("2026-09", dt.date(2026, 10, 1))
    assert build_parser().parse_args(["scan"]).month == this_month()
    print("selftest ok")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--selftest", action="store_true", help="offline check, no network")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("scan")
    s.add_argument("--month", default=this_month(), help="month to close, default the current month")
    a = sub.add_parser("apply")
    a.add_argument("plan")
    a.add_argument("--confirm", action="store_true")
    d = sub.add_parser("delete-txn")
    d.add_argument("id")
    d.add_argument("--confirm", action="store_true")
    return p


def main():
    p = build_parser()
    args = p.parse_args()
    if args.selftest:
        return selftest()
    if not args.cmd:
        p.error("choose a command")
    cfg = load_config()
    if args.cmd == "scan":
        scan(cfg, args.month)
    elif args.cmd == "apply":
        apply(cfg, json.loads(Path(args.plan).read_text()), args.confirm)
    else:
        delete_txn(cfg, args.id, args.confirm)


if __name__ == "__main__":
    main()
