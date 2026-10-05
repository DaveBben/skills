#!/usr/bin/env python3
"""Cover overspent YNAB categories in the current month, before the month rolls over.

  cover.py scan                         read-only: negatives and a proposed cover plan as JSON
  cover.py apply plan.json [--confirm]  move assigned money and append one note line per cover
  cover.py --selftest                   check the cover logic offline

Works on the current calendar month only. Sources follow [cover_order] steps
(default wants -> trial_category -> emergency_fund -> bill_funds) and never include the
surprise fund, a retirement category, a credit-card payment category or a [roles] paused category.

Settings: $FINANCE_CONFIG_DIR/config.toml, default ~/.config/finance/config.toml.
Token: $YNAB_ACCESS_TOKEN, else the macOS keychain service named in [ynab] keychain_service.
Writes run only with --confirm; without it they print what they would do.
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
from pathlib import Path

API = "https://api.ynab.com/v1"
DEFAULT_ORDER = ["wants", "trial_category", "emergency_fund", "bill_funds"]
CARD_GROUP = "Credit Card Payments"
WARN = {"trial_category": "Draw from the trial category: this month fails practice-payment criterion c (every overspend covered from the first source).",
        "emergency_fund": "Draw from the emergency fund: schedule a repayment from next month, ranked above every want."}


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


def this_month(today=None):
    return (today or dt.date.today()).strftime("%Y-%m")


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


def cover_plan(cats, cfg, card_names=()):
    """Cover each negative category from the cover_order steps. Amounts in milliunits."""
    order = cfg.get("cover_order", {}).get("steps", DEFAULT_ORDER)
    bad = [s for s in order if s not in DEFAULT_ORDER]
    if bad:
        raise ValueError(f"cover_order steps {bad} are not allowed cover sources; use only {DEFAULT_ORDER}")
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


def check_moves(moves, protected, known):
    """Return the reason to refuse a plan, or None."""
    for mv in moves:
        if mv["from"] in protected:
            return f"Refusing: {mv['from']} is a surprise, retirement, card payment or paused category."
        for n in (mv["from"], mv["to"]):
            if n not in known:
                return f"No category named {n!r}."
    return None


def note_line(month, c, amount, source):
    return (f"{month}: target {money(c.get('goal_target') or 0)}, spent {money(-c['activity'])}, "
            f"covered {money(amount)} from {source}")


def card_names(groups):
    return {c["name"] for g in groups if g["name"] == CARD_GROUP for c in g["categories"] if not c.get("deleted")}


def scan(cfg):
    month = this_month()
    mdata = api(cfg, "GET", f"/months/{month}-01")["month"]
    cats = [c for c in mdata["categories"] if not c.get("deleted")]
    cards = card_names(api(cfg, "GET", "/categories")["category_groups"])
    cat = by_name(cats)
    moves, uncovered = cover_plan(cats, cfg, cards)
    print(json.dumps({
        "month": month,
        "negative_categories": [{"category": c["name"], "balance": money(c["balance"]), "hidden": c.get("hidden")}
                                for c in cats if c["balance"] < 0 and c["name"] not in cards],
        "proposed_plan": {"month": month,
                          "moves": [{**m, "amount": m["amount"] / 1000} for m in moves],
                          "notes": [{"category": m["to"], "line": note_line(month, cat[m["to"]], m["amount"], m["from"])}
                                    for m in moves]},
        "uncovered": [{**u, "amount": money(u["amount"])} for u in uncovered],
        "warnings": sorted({WARN[m["step"]] for m in moves if m["step"] in WARN}),
    }, indent=2))


def apply(cfg, plan, confirm):
    month = plan["month"]
    if month != this_month():
        sys.exit(f"Plan is for {month}; this skill covers only the current month ({this_month()}). "
                 "Run a fresh scan.")
    groups = api(cfg, "GET", "/categories")["category_groups"]
    cat = by_name([c for g in groups for c in g["categories"]])
    moves = plan.get("moves", [])
    err = check_moves(moves, protected_names(cfg, card_names(groups)), cat)
    if err:
        sys.exit(err)
    for nt in plan.get("notes", []):
        if nt["category"] not in cat:
            sys.exit(f"No category named {nt['category']!r}.")
    for mv in moves:
        amt = round(mv["amount"] * 1000)
        print(f"move {money(amt)} from {mv['from']} to {mv['to']} in {month}")
        if WARN.get(mv.get("step")):
            print(f"  {WARN[mv['step']]}")
        if confirm:
            for n, delta in ((mv["from"], -amt), (mv["to"], amt)):
                cid = cat[n]["id"]
                cur = api(cfg, "GET", f"/months/{month}-01/categories/{cid}")["category"]["budgeted"]
                api(cfg, "PATCH", f"/months/{month}-01/categories/{cid}", {"category": {"budgeted": cur + delta}})
    for nt in plan.get("notes", []):
        print(f"append to {nt['category']} note: {nt['line']}")
        if confirm:
            cid = cat[nt["category"]]["id"]
            note = api(cfg, "GET", f"/categories/{cid}")["category"].get("note") or ""
            api(cfg, "PATCH", f"/categories/{cid}", {"category": {"note": (note.rstrip() + "\n" + nt["line"]).strip()}})
    if not confirm:
        sys.exit("Dry run. Re-run with --confirm after the user approves.")


def selftest():
    cfg = {"roles": {"wants": ["Fun", "Food", "Gear"], "trial_category": "Trial", "emergency_fund": "EF",
                     "bill_funds": ["Bills"], "surprise_fund": "Oops", "retirement": ["IRA"], "paused": ["Gear"]}}
    cats = [{"name": "Food", "balance": -50_000, "budgeted": 100_000, "activity": -150_000, "goal_target": 100_000},
            {"name": "Gear", "balance": 70_000, "budgeted": 0},
            {"name": "Fun", "balance": 20_000, "budgeted": 20_000},
            {"name": "Trial", "balance": 500_000, "budgeted": 10_000},
            {"name": "EF", "balance": 900_000, "budgeted": 0},
            {"name": "Oops", "balance": 99_000, "budgeted": 0},
            {"name": "IRA", "balance": 99_000, "budgeted": 0},
            {"name": "Card", "balance": 99_000, "budgeted": 0},
            {"name": "Food", "balance": 5_000, "budgeted": 0, "hidden": True}]
    moves, unc = cover_plan(cats, cfg, card_names=["Card"])
    assert [(m["from"], m["amount"]) for m in moves] == [("Fun", 20_000), ("Trial", 10_000), ("EF", 20_000)], moves
    assert not unc
    # Protected and paused categories are never chosen, even when listed in a cover step.
    cfg2 = {"roles": {**cfg["roles"], "wants": ["Oops", "IRA", "Card", "Gear", "Fun"]}}
    moves, unc = cover_plan(cats, cfg2, card_names=["Card"])
    assert moves[0]["from"] == "Fun" and {m["from"] for m in moves} <= {"Fun", "Trial", "EF"}, moves
    # Only the emergency fund has money: it is the first configured role that can pay.
    empty = [{**c, "balance": 0} if c["name"] in ("Fun", "Trial") else c for c in cats]
    moves, _ = cover_plan(empty, cfg, card_names=["Card"])
    assert [(m["from"], m["step"]) for m in moves] == [("EF", "emergency_fund")], moves
    try:
        cover_plan(cats, {**cfg, "cover_order": {"steps": ["surprise_fund"]}})
        raise AssertionError("surprise fund accepted as a cover step")
    except ValueError:
        pass
    protected = protected_names(cfg, ["Card"])
    known = by_name(cats)
    for src in ("Oops", "Card", "IRA", "Gear"):
        assert check_moves([{"from": src, "to": "Food", "amount": 1}], protected, known), src
    assert check_moves([{"from": "Fun", "to": "Food", "amount": 1}], protected, known) is None
    assert note_line("2026-01", cats[0], 20_000, "Fun") == \
        "2026-01: target $100.00, spent $150.00, covered $20.00 from Fun"
    assert re.match(r"\d{4}-\d{2}: .*covered", note_line("2026-01", cats[0], 1, "Fun"))
    assert this_month(dt.date(2026, 10, 31)) == "2026-10"
    print("selftest ok")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--selftest", action="store_true", help="offline check, no network")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("scan")
    a = sub.add_parser("apply")
    a.add_argument("plan")
    a.add_argument("--confirm", action="store_true")
    args = p.parse_args()
    if args.selftest:
        return selftest()
    if not args.cmd:
        p.error("choose a command")
    cfg = load_config()
    if args.cmd == "scan":
        scan(cfg)
    else:
        apply(cfg, json.loads(Path(args.plan).read_text()), args.confirm)


if __name__ == "__main__":
    main()
