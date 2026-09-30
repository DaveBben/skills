#!/usr/bin/env python3
"""Meal plan arithmetic: per-day totals, plan averages, servings, scale, entry text.

    python3 plan-calc.py plan.json [--out writes.json]
    python3 plan-calc.py --self-test

Prints the review: the dinner table, per-day totals for the user, plan averages
against TARGETS, servings made and scale per recipe, and granola batches to buy.
With no dinners in plan.json it prints the dinner budget instead. --out writes
the meal plan entries and the shopping-list payload that `mealie.py write-plan`
and `mealie.py add-recipes` send, plus the list name.

plan.json, every date inside the plan period:

    {"start": "2026-10-05", "days": 5, "catalog": "catalog.json",
     "fixed": {"breakfast": "<name or slug>", "drink": "...", "lunch": "..."},
     "bowls_left": 2, "partner_berries": true,
     "changes": [{"date": "...", "slot": "lunch", "recipe": "<name or slug>"},
                 {"date": "...", "slot": "breakfast", "title": "Eating out"},
                 {"date": "...", "slot": "drink"}],
     "dinners": [{"date": "...", "recipe": "...", "seafood": false},
                 {"date": "...", "recipe": "...", "seafood": false, "days": 2},
                 {"date": "...", "title": "Eating out"}]}

`catalog` is the file `mealie.py recipes` writes: {slug: full recipe JSON}.
A change with `title` is an entry with no recipe; its day has no nutrition and
drops out of the averages. A change with neither `recipe` nor `title` plans
nothing in that slot. A dinner with `recipe` is a cook; its batch covers
floor(recipeServings / 2) days (at least 1), cut by `days`, the next dinner,
or the end of the plan period. Servings not eaten in the period are not bought.
Seafood is cooked fresh each day it covers.
"""
import json
import math
import re
import sys
from datetime import date, timedelta

# the user's daily averages; a plan passes inside these
TARGETS = {"kcal_max": 2050, "protein_min": 110, "fiber_min": 25}
TARGET_POINT = {"kcal": 2000, "protein": 120, "fiber": 30}
# servings made per day in each fixed slot; the user eats 1 of each
FIXED_SERVINGS = {"breakfast": 2, "drink": 2, "lunch": 1}
DINNER_SERVINGS = 2
SLOTS = ["breakfast", "drink", "lunch", "dinner"]
NUTRIENTS = [("kcal", "calories"), ("protein", "proteinContent"), ("fiber", "fiberContent")]


def fail(msg):
    raise SystemExit(f"plan-calc: {msg}")


def find(catalog, ref):
    if ref in catalog:
        return catalog[ref]
    for r in catalog.values():
        if r.get("name", "").lower() == ref.lower():
            return r
    fail(f"no recipe '{ref}' in the catalog; fetch it or ask the user")


def servings(r):
    s = r.get("recipeServings")
    if not s:
        fail(f"{r['name']} has no recipeServings")
    return s


def nutrition(r):
    out = {}
    for key, field in NUTRIENTS:
        m = re.match(r"\s*(\d+(?:\.\d+)?)", str((r.get("nutrition") or {}).get(field) or ""))
        if not m:
            fail(f"{r['name']} has no stored {field}; stop and ask the user")
        out[key] = float(m.group(1))
    return out


def label(d):
    return f"{d:%a} {d.month}/{d.day}"


def joined(days):
    names = [label(d) for d in days]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def split_rows(r):
    """(batch rows, other rows): a row belongs to the last section title at or above it."""
    batch, rest, title = [], [], ""
    for row in r.get("recipeIngredient") or []:
        title = row.get("title") or title
        (batch if "batch" in title.lower() else rest).append(row)
    return batch, rest


def is_berry(row):
    return "berr" in (((row.get("food") or {}).get("name") or "") + " " + (row.get("note") or "")).lower()


def calc(p, catalog):
    start = date.fromisoformat(p["start"])
    dates = [start + timedelta(i) for i in range(p["days"])]

    def day_index(s):
        d = date.fromisoformat(s)
        if d not in dates:
            fail(f"{s} is outside the plan period")
        return dates.index(d)

    # slot plan: plan[i][slot] = {"recipe": r, "servings": n, "text": ..., "kind": ...} or {"title": t}
    plan = [{} for _ in dates]
    def check_slot(slot):
        if slot not in FIXED_SERVINGS:
            fail(f"unknown slot '{slot}'; use one of {', '.join(FIXED_SERVINGS)} (dinners go in 'dinners')")

    for slot, ref in p["fixed"].items():
        check_slot(slot)
        r = find(catalog, ref)
        for day in plan:
            day[slot] = {"recipe": r, "servings": FIXED_SERVINGS[slot]}
    for c in p.get("changes", []):
        day, slot = plan[day_index(c["date"])], c["slot"]
        check_slot(slot)
        if "recipe" in c:
            day[slot] = {"recipe": find(catalog, c["recipe"]), "servings": c.get("servings", FIXED_SERVINGS[slot])}
        elif "title" in c:
            day[slot] = {"title": c["title"]}
        else:
            day.pop(slot, None)
    for day in plan:
        for slot in FIXED_SERVINGS:
            if "recipe" in day.get(slot, {}):
                n = day[slot]["servings"]
                day[slot]["text"] = "1 serving (user)" if n == 1 else f"{n} servings (user + partner)"

    dinners = sorted(p.get("dinners", []), key=lambda d: d["date"])
    for k, c in enumerate(dinners):
        i = day_index(c["date"])
        nxt = day_index(dinners[k + 1]["date"]) if k + 1 < len(dinners) else len(dates)
        if nxt == i:
            fail(f"two dinners on {c['date']}")
        if "title" in c:
            plan[i]["dinner"] = {"title": c["title"]}
            continue
        r = find(catalog, c["recipe"])
        span = dates[i:i + min(max(1, int(servings(r)) // 2), c.get("days", len(dates)), nxt - i)]
        for j, d in enumerate(span):
            if j == 0:
                kind = "cook"
                text = f"Cook: {DINNER_SERVINGS} servings tonight"
                if len(span) > 1 and not c.get("seafood"):
                    text += f", {DINNER_SERVINGS * (len(span) - 1)} leftover for {joined(span[1:])}"
            elif c.get("seafood"):
                kind, text = "cook fresh", f"Cook fresh: {DINNER_SERVINGS} servings from the same recipe (seafood, not reheated)"
            else:
                kind, text = "leftover", f"Leftovers from {label(span[0])}"
            if j >= 2:
                kind += ", day 3+ of a batch: ask whether to cut"
            plan[i + j]["dinner"] = {"recipe": r, "servings": DINNER_SERVINGS, "text": text, "kind": kind}

    # per-day totals for the user: 1 serving of each planned recipe
    totals, left_out = [], []
    for d, day in zip(dates, plan):
        if dinners and "dinner" not in day:
            fail(f"no dinner on {d}; add a cook or a title entry such as 'Eating out'")
        if any("title" in e for e in day.values()):
            left_out.append(d)
            continue
        t = {k: 0.0 for k, _ in NUTRIENTS}
        for e in day.values():
            for k, v in nutrition(e["recipe"]).items():
                t[k] += v
        totals.append((d, t))
    if not totals:
        fail("every day has an entry without nutrition; nothing to average")
    avg = {k: sum(t[k] for _, t in totals) / len(totals) for k, _ in NUTRIENTS}
    passed = {"kcal": avg["kcal"] <= TARGETS["kcal_max"],
              "protein": avg["protein"] >= TARGETS["protein_min"],
              "fiber": avg["fiber"] >= TARGETS["fiber_min"]}

    # servings made per recipe: a template planned twice sums its servings
    made, user_days = {}, {}
    for day in plan:
        for slot, e in day.items():
            if "recipe" in e:
                rid = e["recipe"]["id"]
                made[rid] = made.get(rid, 0) + e["servings"]
                user_days[rid] = user_days.get(rid, 0) + 1
    by_id = {e["recipe"]["id"]: e["recipe"] for day in plan for e in day.values() if "recipe" in e}
    breakfast_id = find(catalog, p["fixed"]["breakfast"])["id"] if "breakfast" in p["fixed"] else None
    lunch_id = find(catalog, p["fixed"]["lunch"])["id"] if "lunch" in p["fixed"] else None
    scales, shopping, batches = [], [], 0
    for rid, n in made.items():
        r = by_id[rid]
        S = servings(r)
        scale = n / S
        # only the lunch recipe has a batch section; elsewhere "batch" is just a title
        batch_rows, other_rows = split_rows(r) if rid == lunch_id else ([], r.get("recipeIngredient") or [])
        if batch_rows:
            # granola: per-bowl rows for each bowl eaten; whole batches only for bowls not already made
            batches = max(0, math.ceil((n - p.get("bowls_left", 0)) / S))
            shopping.append({"recipeId": rid, "recipeIncrementQuantity": round(scale, 4), "recipeIngredients": other_rows})
            if batches:
                shopping.append({"recipeId": rid, "recipeIncrementQuantity": batches, "recipeIngredients": batch_rows})
            scales.append((r["name"], n, f"{scale:.4g} per-bowl rows, {batches} batch(es)"))
            continue
        berries = [row for row in other_rows if is_berry(row)]
        if rid == breakfast_id and not p.get("partner_berries", True) and berries:
            user_scale = user_days[rid] / S
            shopping.append({"recipeId": rid, "recipeIncrementQuantity": round(scale, 4),
                             "recipeIngredients": [row for row in other_rows if not is_berry(row)]})
            shopping.append({"recipeId": rid, "recipeIncrementQuantity": round(user_scale, 4), "recipeIngredients": berries})
            scales.append((r["name"], n, f"{scale:.4g}, berry rows {user_scale:.4g}"))
            continue
        shopping.append({"recipeId": rid, "recipeIncrementQuantity": round(scale, 4)})
        scales.append((r["name"], n, f"{scale:.4g}"))

    entries = []
    for d, day in zip(dates, plan):
        for slot in SLOTS:
            e = day.get(slot)
            if e and "recipe" in e:
                entries.append({"date": d.isoformat(), "entryType": slot, "recipeId": e["recipe"]["id"], "title": "", "text": e["text"]})
            elif e:
                entries.append({"date": d.isoformat(), "entryType": slot, "title": e["title"], "text": ""})

    return {"dates": dates, "plan": plan, "totals": totals, "left_out": left_out, "avg": avg,
            "passed": passed, "scales": scales, "batches": batches,
            "writes": {"start": dates[0].isoformat(), "end": dates[-1].isoformat(),
                       "list_name": f"Meal plan {dates[0]} to {dates[-1]}",
                       "entries": entries, "shopping": shopping}}


def left(key, nutrient, fixed, table=TARGETS):
    """What the dinner must still supply; never below 0."""
    return max(0, table[key] - fixed[nutrient])


def report(res, has_dinners=True):
    if not has_dinners:
        fixed = {k: sum(t[k] for _, t in res["totals"]) / len(res["totals"]) for k, _ in NUTRIENTS}
        print(f"fixed meals per day: {fixed['kcal']:.0f} kcal, {fixed['protein']:.0f} g protein, {fixed['fiber']:.0f} g fiber")
        print(f"dinner budget: {TARGET_POINT['kcal'] - fixed['kcal']:.0f} to {TARGETS['kcal_max'] - fixed['kcal']:.0f} kcal, "
              f">= {left('protein_min', 'protein', fixed):.0f} g protein (target {left('protein', 'protein', fixed, TARGET_POINT):.0f}), "
              f">= {left('fiber_min', 'fiber', fixed):.0f} g fiber (target {left('fiber', 'fiber', fixed, TARGET_POINT):.0f})")
        return
    print("date        dinner                                    day")
    for d, day in zip(res["dates"], res["plan"]):
        e = day.get("dinner", {})
        print(f"{label(d):11} {e.get('title') or e['recipe']['name']:41} {e.get('kind', '')}")
    print("\nper day, user     kcal  protein  fiber")
    for d, t in res["totals"]:
        print(f"{label(d):15} {t['kcal']:6.0f} {t['protein']:8.0f} {t['fiber']:6.0f}")
    if res["left_out"]:
        print("left out (an entry has no nutrition): " + ", ".join(label(d) for d in res["left_out"]))
    a, ok = res["avg"], res["passed"]
    print(f"\nplan average: {a['kcal']:.0f} kcal (<= {TARGETS['kcal_max']}) {'pass' if ok['kcal'] else 'FAIL'}, "
          f"{a['protein']:.0f} g protein (>= {TARGETS['protein_min']}) {'pass' if ok['protein'] else 'FAIL'}, "
          f"{a['fiber']:.0f} g fiber (>= {TARGETS['fiber_min']}) {'pass' if ok['fiber'] else 'FAIL'}")
    print("\nservings made, scale")
    for name, n, scale in res["scales"]:
        print(f"  {name}: {n} servings, scale {scale}")


def demo():
    """Mon 2026-10-05 to Fri: chicken cooked twice (the Friday cook cut at the
    period end), salmon cooked fresh, granola with 2 bowls left, Thursday
    breakfast eaten out, partner's egg bomb without berries."""
    def recipe(slug, S, kcal, protein, fiber, rows=()):
        return {"id": slug + "-id", "slug": slug, "name": slug, "recipeServings": S,
                "nutrition": {"calories": str(kcal), "proteinContent": f"{protein}g", "fiberContent": fiber},
                "recipeIngredient": list(rows)}
    row = lambda food, title="": {"title": title, "quantity": 1, "food": {"name": food}, "note": ""}
    catalog = {r["slug"]: r for r in [
        recipe("egg-bomb", 1, 450, 45, "6", [row("egg"), row("cottage cheese"), row("blueberries")]),
        recipe("latte", 1, 180, 12, "0"),
        recipe("granola-bowl", 12, 700, 55, "18",
               [row("oats", "Granola batch"), row("walnuts"), row("greek yogurt", "Bowls"), row("protein powder")]),
        recipe("chicken", 4, 650, 50, "12"),
        recipe("salmon", 4, 600, 45, "10"),
    ]}
    p = {"start": "2026-10-05", "days": 5, "bowls_left": 2, "partner_berries": False,
         "fixed": {"breakfast": "egg-bomb", "drink": "latte", "lunch": "granola-bowl"},
         "changes": [{"date": "2026-10-08", "slot": "breakfast", "title": "Eating out"}],
         "dinners": [{"date": "2026-10-05", "recipe": "chicken"},
                     {"date": "2026-10-07", "recipe": "salmon", "seafood": True},
                     {"date": "2026-10-09", "recipe": "chicken"}]}
    res = calc(p, catalog)
    report(res)
    text = {(e["date"], e["entryType"]): e for e in res["writes"]["entries"]}
    items = res["writes"]["shopping"]
    qty = lambda rid, food=None: [i["recipeIncrementQuantity"] for i in items if i["recipeId"] == rid
                                  and (food is None or food in [r["food"]["name"] for r in i.get("recipeIngredients", [])])]

    # batch stretching and entry text
    assert text[("2026-10-05", "dinner")]["text"] == "Cook: 2 servings tonight, 2 leftover for Tue 10/6"
    assert text[("2026-10-06", "dinner")]["text"] == "Leftovers from Mon 10/5"
    assert text[("2026-10-07", "dinner")]["text"] == "Cook: 2 servings tonight"
    assert text[("2026-10-08", "dinner")]["text"].startswith("Cook fresh: 2 servings")
    assert text[("2026-10-05", "breakfast")]["text"] == "2 servings (user + partner)"
    assert text[("2026-10-05", "lunch")]["text"] == "1 serving (user)"
    assert text[("2026-10-08", "breakfast")] == {"date": "2026-10-08", "entryType": "breakfast", "title": "Eating out", "text": ""}
    # boundary cut: the Friday cook covers one day, scale 2/4; planned twice sums to 1.5
    assert text[("2026-10-09", "dinner")]["text"] == "Cook: 2 servings tonight"
    assert qty("chicken-id") == [1.5], qty("chicken-id")
    assert qty("salmon-id") == [1.0]
    # granola split: 5 bowls eaten, per-bowl rows 5/12; 2 left so 3 more need 1 batch
    assert qty("granola-bowl-id", "greek yogurt") == [0.4167]
    assert qty("granola-bowl-id", "oats") == [1] and res["batches"] == 1
    # egg bomb: 4 breakfast days (Thursday out), berries for the user only
    assert qty("egg-bomb-id", "egg") == [8.0] and qty("egg-bomb-id", "blueberries") == [4.0]
    # averages: Thursday drops out; the other 4 days are the fixed 1,330 kcal plus that day's dinner
    assert res["left_out"] == [date(2026, 10, 8)]
    assert abs(res["avg"]["kcal"] - (1330 + (650 + 650 + 600 + 650) / 4)) < 1e-9
    assert res["passed"] == {"kcal": True, "protein": True, "fiber": True}

    # a "batch" section outside the lunch recipe is not the granola split: all rows reach the list
    catalog["curry"] = recipe("curry", 4, 600, 45, "10", [row("chicken"), row("rice", "Sauce batch"), row("salt")])
    p3 = dict(p, dinners=[{"date": "2026-10-05", "recipe": "curry", "days": 2}] + [{"date": f"2026-10-0{d}", "title": "Out"} for d in (7, 8, 9)])
    res3 = calc(p3, catalog)
    curry = [i for i in res3["writes"]["shopping"] if i["recipeId"] == "curry-id"]
    assert len(curry) == 1 and curry[0]["recipeIncrementQuantity"] == 1.0 and "recipeIngredients" not in curry[0], curry
    assert res3["batches"] == 1  # still only the granola batch

    # unknown slot is a message, not a KeyError; the budget never shows a negative floor
    try:
        calc(dict(p, changes=[{"date": "2026-10-05", "slot": "snack", "recipe": "latte"}]), catalog)
        raise AssertionError("a snack slot should fail")
    except SystemExit as e:
        assert "unknown slot 'snack'" in str(e)
    import contextlib, io
    catalog["big"] = recipe("big", 1, 500, 200, "90")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        report(calc(dict(p, fixed={"breakfast": "big"}, changes=[], dinners=[]), catalog), False)
    assert ">= 0 g protein" in buf.getvalue() and ">= 0 g fiber" in buf.getvalue(), buf.getvalue()

    # enough bowls left: no batch bought; a gap in dinners is refused
    p2 = dict(p, bowls_left=6, dinners=p["dinners"][:2])
    try:
        calc(p2, catalog)
        raise AssertionError("a day with no dinner should fail")
    except SystemExit as e:
        assert "no dinner on 2026-10-09" in str(e)
    p2["dinners"] = p2["dinners"] + [{"date": "2026-10-09", "title": "Eating out"}]
    res2 = calc(p2, catalog)
    assert res2["batches"] == 0 and len([i for i in res2["writes"]["shopping"] if i["recipeId"] == "granola-bowl-id"]) == 1
    print("\nself-check passed")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "--self-test":
        demo()
    elif sys.argv[1] in ("-h", "--help"):
        print(__doc__)
    else:
        p = json.load(open(sys.argv[1]))
        catalog = json.load(open(p["catalog"]))
        res = calc(p, catalog)
        report(res, bool(p.get("dinners")))
        if "--out" in sys.argv:
            with open(sys.argv[sys.argv.index("--out") + 1], "w") as f:
                json.dump(res["writes"], f, indent=1)
