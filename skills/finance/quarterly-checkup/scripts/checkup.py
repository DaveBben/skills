#!/usr/bin/env python3
"""Read-only numbers for the quarterly checkup of a YNAB budget.

  checkup.py scan       JSON: essential spend and emergency-fund months, recurring payees,
                        tracking-account outflows in the last 60 days, bill-fund and
                        retirement balances, categories covered often enough to re-price
  checkup.py --selftest offline check

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
from collections import defaultdict
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


def api(cfg, path):
    req = urllib.request.Request(f"{API}/budgets/{cfg['ynab']['budget_id']}{path}",
                                 headers={"Authorization": f"Bearer {token(cfg['ynab']['keychain_service'])}"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)["data"]
    except urllib.error.HTTPError as e:
        sys.exit(f"YNAB GET {path} failed: {e.code} {e.read().decode()[:300]}")


def names(cfg, role):
    v = cfg.get("roles", {}).get(role, [])
    return [v] if isinstance(v, str) else list(v)


def money(m):
    return f"${m / 1000:,.2f}"


def month_list(end, count):
    y, m = map(int, end.split("-"))
    out = []
    for _ in range(count):
        out.append(f"{y:04d}-{m:02d}")
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    return out[::-1]


def parts(t):
    return [s for s in t.get("subtransactions") or [] if not s.get("deleted")] or [t]


def recurring_payees(txns, id_to_name, min_months):
    """Payees with outflows in at least `min_months` distinct months, largest yearly cost first."""
    hits = defaultdict(lambda: {"months": set(), "total": 0, "categories": set(), "last": ""})
    for t in txns:
        if (t.get("deleted") or t.get("transfer_account_id") or t["amount"] >= 0 or not t.get("payee_name")
                or t["payee_name"].startswith("Reconciliation")):
            continue
        h = hits[t["payee_name"]]
        h["months"].add(t["date"][:7])
        h["total"] -= t["amount"]
        h["last"] = max(h["last"], t["date"])
        h["categories"] |= {id_to_name.get(p.get("category_id"), "?") for p in parts(t)}
    out = [{"payee": p, "months_charged": len(h["months"]), "total": h["total"], "last": h["last"],
            "categories": sorted(h["categories"])}
           for p, h in hits.items() if len(h["months"]) >= min_months]
    return sorted(out, key=lambda r: -r["total"])


def scan(cfg):
    sc = cfg.get("scripts", {})
    window = sc.get("months", 12)
    today = dt.date.today()
    last_full = (today.replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")
    months = month_list(last_full, window)
    groups = api(cfg, "/categories")["category_groups"]
    cats = {}
    for g in groups:
        for c in g["categories"]:
            if not c.get("deleted") and (c["name"] not in cats or cats[c["name"]].get("hidden")):
                cats[c["name"]] = c
    id_to_name = {c["id"]: c["name"] for g in groups for c in g["categories"]}
    accounts = {a["id"]: a for a in api(cfg, "/accounts")["accounts"]}
    txns = api(cfg, f"/transactions?since_date={months[0]}-01")["transactions"]
    in_window = [t for t in txns if t["date"][:7] in months]

    spend = defaultdict(int)
    for t in in_window:
        if not t.get("deleted"):
            for p in parts(t):
                spend[id_to_name.get(p.get("category_id"))] -= p["amount"]
    wants = set(names(cfg, "wants"))
    essential = (set(names(cfg, "fixed")) | set(names(cfg, "steady")) | set(names(cfg, "bill_funds"))) - wants
    ess = sum(spend[n] for n in essential) / len(months)
    ef = cats.get(next(iter(names(cfg, "emergency_fund")), ""), {}).get("balance", 0)

    cutoff = (today - dt.timedelta(days=60)).isoformat()
    tracking_out = [{"date": t["date"], "account": accounts[t["account_id"]]["name"], "amount": money(t["amount"]),
                     "payee": t.get("payee_name"),
                     "day_60": (dt.date.fromisoformat(t["date"]) + dt.timedelta(days=60)).isoformat()}
                    for t in txns if not t.get("deleted") and t["date"] >= cutoff and t["amount"] < 0
                    and not accounts[t["account_id"]]["on_budget"]
                    and "Reconciliation" not in (t.get("payee_name") or "")]

    lookback = month_list(last_full, sc.get("cover_lookback_months", 6))
    covered = {}
    for n, c in cats.items():
        hits = {ln[:7] for ln in (c.get("note") or "").splitlines() if re.match(r"\d{4}-\d{2}: .*covered", ln)}
        if len(hits & set(lookback)) >= sc.get("cover_raise_count", 3):
            covered[n] = len(hits & set(lookback))

    year = str(today.year)
    print(json.dumps({
        "window": [months[0], months[-1]],
        "essential_monthly_mean": money(int(ess)),
        "emergency_balance": money(ef),
        "emergency_months": round(ef / ess, 1) if ess > 0 else None,
        "recurring_payees": [{**r, "total": money(r["total"])}
                             for r in recurring_payees(in_window, id_to_name, sc.get("recurring_min_months", 3))],
        "tracking_account_outflows_last_60_days": tracking_out,
        "bill_funds": {n: {"balance": money(cats[n]["balance"]), "target": money(cats[n].get("goal_target") or 0)}
                       for n in names(cfg, "bill_funds") if n in cats},
        "retirement_categories_ytd": {n: money(sum(-p["amount"] for t in txns if t["date"].startswith(year)
                                                   and not t.get("deleted") for p in parts(t)
                                                   if p.get("category_id") == cats[n]["id"]))
                                      for n in names(cfg, "retirement") if n in cats},
        "covered_often_raise_target": covered,
    }, indent=2))


def selftest():
    tx = [{"date": f"2026-0{m}-05", "amount": -10_000, "payee_name": "Stream", "category_id": "s"} for m in (1, 2, 3)]
    tx += [{"date": "2026-01-09", "amount": -90_000, "payee_name": "Once", "category_id": "s"},
           {"date": "2026-02-09", "amount": 5_000, "payee_name": "Stream", "category_id": "s"},
           {"date": "2026-03-01", "amount": -1_000, "payee_name": "Card", "category_id": None, "transfer_account_id": "x"}]
    got = recurring_payees(tx, {"s": "Subscriptions"}, 3)
    assert [(r["payee"], r["months_charged"], r["total"]) for r in got] == [("Stream", 3, 30_000)], got
    assert month_list("2026-01", 2) == ["2025-12", "2026-01"]
    print("selftest ok")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--selftest", action="store_true", help="offline check, no network")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("scan")
    args = p.parse_args()
    if args.selftest:
        return selftest()
    if not args.cmd:
        p.error("choose a command")
    scan(load_config())


if __name__ == "__main__":
    main()
