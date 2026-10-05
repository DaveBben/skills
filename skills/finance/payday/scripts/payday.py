#!/usr/bin/env python3
"""Assign a paycheck that has landed in YNAB, by priority.

  payday.py plan --amount 1234.56 [--kind regular|third|bonus] [--month YYYY-MM]   read-only
  payday.py assign plan.json [--confirm]                                          add to assigned
  payday.py --selftest                                                            offline check

regular: fixed and steady gaps -> bill funds -> emergency-fund repayment -> savings goals (trial first)
         -> retirement -> wants.
third / bonus: emergency-fund gap (repayment) -> the rest to the first savings goal (trial first).
Gaps are each category's goal_under_funded this month. Categories in [roles] paused get nothing.
Never plans more than Ready to Assign: money not yet received cannot be assigned.

Settings: $FINANCE_CONFIG_DIR/config.toml, default ~/.config/finance/config.toml.
Token: $YNAB_ACCESS_TOKEN, else the macOS keychain service named in [ynab] keychain_service.
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
    out = {}
    for c in cats:
        if c.get("deleted"):
            continue
        if c["name"] not in out or out[c["name"]].get("hidden"):
            out[c["name"]] = c
    return out


def tiers(cfg, kind):
    goals = names(cfg, "trial_category") + [n for n in names(cfg, "savings_goals") if n not in names(cfg, "trial_category")]
    if kind == "regular":
        return [("fixed and steady", names(cfg, "fixed") + names(cfg, "steady")),
                ("bill funds", names(cfg, "bill_funds")),
                ("emergency fund repayment", names(cfg, "emergency_fund")), ("savings goals", goals),
                ("retirement", names(cfg, "retirement")), ("wants", names(cfg, "wants"))]
    return [("emergency fund repayment", names(cfg, "emergency_fund")), ("savings goals", goals)]


def allocate(cats, cfg, amount, kind):
    """Return [(tier, category, milliunits)] for `amount` milliunits."""
    cat = by_name(cats)
    paused = set(names(cfg, "paused"))
    left, out, seen = amount, [], set()
    for tier, members in tiers(cfg, kind):
        for n in members:
            if left <= 0:
                return out
            if n in seen or n in paused or n not in cat:
                continue
            seen.add(n)
            gap = cat[n].get("goal_under_funded") or 0
            if gap > 0:
                amt = min(gap, left)
                out.append((tier, n, amt))
                left -= amt
    if left > 0 and kind != "regular":
        dest = next((n for n in tiers(cfg, kind)[-1][1] if n in cat and n not in paused), None)
        if dest:
            out.append(("savings goals", dest, left))
    return out


def plan(cfg, amount, kind, month):
    mdata = api(cfg, "GET", f"/months/{month}-01")["month"]
    rta = mdata["to_be_budgeted"]
    want = round(amount * 1000)
    use = min(want, max(rta, 0))
    lines = allocate(mdata["categories"], cfg, use, kind)
    print(json.dumps({
        "month": month, "kind": kind, "ready_to_assign": money(rta), "paycheck": money(want),
        "warning": None if use == want else
        f"Only {money(use)} is in Ready to Assign; plan covers that much. Check the paycheck has landed.",
        "lines": [{"tier": t, "category": n, "amount": a / 1000} for t, n, a in lines],
        "left_unassigned": money(use - sum(a for _, _, a in lines)),
    }, indent=2))


def assign(cfg, p, confirm):
    month = p["month"]
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        sys.exit("plan month must be YYYY-MM")
    mdata = api(cfg, "GET", f"/months/{month}-01")["month"]
    cat = by_name(mdata["categories"])
    paused = set(names(cfg, "paused"))
    total = sum(round(ln["amount"] * 1000) for ln in p["lines"])
    if total > mdata["to_be_budgeted"]:
        sys.exit(f"Refusing: plan assigns {money(total)} but Ready to Assign is {money(mdata['to_be_budgeted'])}.")
    for ln in p["lines"]:
        if ln["category"] not in cat:
            sys.exit(f"No category named {ln['category']!r}.")
        if ln["category"] in paused:
            sys.exit(f"Refusing: {ln['category']} is paused in the settings file.")
    for ln in p["lines"]:
        amt = round(ln["amount"] * 1000)
        print(f"assign {money(amt)} to {ln['category']} in {month}")
        if confirm:
            cid = cat[ln["category"]]["id"]
            cur = api(cfg, "GET", f"/months/{month}-01/categories/{cid}")["category"]["budgeted"]
            api(cfg, "PATCH", f"/months/{month}-01/categories/{cid}", {"category": {"budgeted": cur + amt}})
    if not confirm:
        sys.exit("Dry run. Re-run with --confirm after the user approves.")


def selftest():
    cfg = {"roles": {"fixed": ["Rent"], "steady": ["Food"], "bill_funds": ["Tax"], "wants": ["Food", "Fun"],
                     "savings_goals": ["House", "Car"], "trial_category": "House", "retirement": ["IRA"],
                     "emergency_fund": "EF", "paused": ["IRA"]}}
    cats = [{"name": "Rent", "goal_under_funded": 800_000}, {"name": "Food", "goal_under_funded": 200_000},
            {"name": "Tax", "goal_under_funded": 100_000}, {"name": "House", "goal_under_funded": 500_000},
            {"name": "IRA", "goal_under_funded": 300_000}, {"name": "Fun", "goal_under_funded": 50_000},
            {"name": "EF", "goal_under_funded": 0}, {"name": "Car", "goal_under_funded": 0}]
    got = [(n, a) for _, n, a in allocate(cats, cfg, 1_500_000, "regular")]
    assert got == [("Rent", 800_000), ("Food", 200_000), ("Tax", 100_000), ("House", 400_000)], got
    got = [(n, a) for _, n, a in allocate(cats, cfg, 3_000_000, "regular")]
    assert ("IRA", 300_000) not in got and ("Fun", 50_000) in got, got
    cats[6]["goal_under_funded"] = 100_000
    got = [(n, a) for _, n, a in allocate(cats, cfg, 1_000_000, "bonus")]
    assert got == [("EF", 100_000), ("House", 500_000), ("House", 400_000)], got
    got = [(n, a) for _, n, a in allocate(cats, cfg, 1_500_000, "regular")]
    assert got == [("Rent", 800_000), ("Food", 200_000), ("Tax", 100_000), ("EF", 100_000), ("House", 300_000)], got
    print("selftest ok")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--selftest", action="store_true", help="offline check, no network")
    sub = p.add_subparsers(dest="cmd")
    pl = sub.add_parser("plan")
    pl.add_argument("--amount", type=float, required=True)
    pl.add_argument("--kind", choices=["regular", "third", "bonus"], default="regular")
    pl.add_argument("--month", default=dt.date.today().strftime("%Y-%m"))
    a = sub.add_parser("assign")
    a.add_argument("plan")
    a.add_argument("--confirm", action="store_true")
    args = p.parse_args()
    if args.selftest:
        return selftest()
    if not args.cmd:
        p.error("choose a command")
    cfg = load_config()
    if args.cmd == "plan":
        plan(cfg, args.amount, args.kind, args.month)
    else:
        assign(cfg, json.loads(Path(args.plan).read_text()), args.confirm)


if __name__ == "__main__":
    main()
