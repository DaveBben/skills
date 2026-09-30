#!/usr/bin/env python3
"""Mealie client for the meal plan: one request at a time, a 180 s timeout, no deletes.

    python3 mealie.py recipes --out catalog.json [--tag dinner-template] [--name "Exact name"] [--slug s] [--refresh]
    python3 mealie.py read-plan START END
    python3 mealie.py write-plan writes.json [--keep | --replace | --add]
    python3 mealie.py create-list NAME [--again]
    python3 mealie.py add-recipes LIST_ID writes.json
    python3 mealie.py read-list LIST_ID
    python3 mealie.py update-item LIST_ID ITEM_ID (--quantity Q | --checked)
    python3 mealie.py --self-test

Reads MEALIE_BASE_URL and MEALIE_API_KEY from the environment. writes.json is
what `plan-calc.py --out` writes.

recipes      fetches full recipes (by tag, exact name or slug) into a local
             catalog file, skipping any already cached, and prints each one's
             servings and per-serving kcal, protein and fiber.
write-plan   refuses when entries already exist in the range, until told
             --keep (skip filled slots), --replace (overwrite the first entry
             in each filled slot) or --add (write alongside). Re-reads the
             range afterwards and fails on any slot whose count is off.
create-list  refuses a name that already exists unless --again.
add-recipes  refuses a list that already holds recipes, since a second add
             doubles every quantity.
update-item  lowers a quantity or checks an item off; never removes one.

After a failed write, every command re-reads before retrying once, because a
timed-out write may already be stored.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT = 180  # the server is slow and stalls under concurrent requests


def fail(msg):
    raise SystemExit(f"mealie: {msg}")


def http(method, path, body=None):
    base, key = os.environ.get("MEALIE_BASE_URL"), os.environ.get("MEALIE_API_KEY")
    if not base or not key:
        fail("set MEALIE_BASE_URL and MEALIE_API_KEY, or ask the user for them")
    req = urllib.request.Request(base.rstrip("/") + path, method=method,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def write(method, path, body, saved):
    """Send one write; after a failure, saved() re-reads and returns the stored result or None."""
    for _ in range(2):
        try:
            return http(method, path, body)
        except urllib.error.HTTPError as e:
            if e.code < 500:
                fail(f"{method} {path}: HTTP {e.code} {e.read().decode(errors='replace')[:300]}")
            err = e
        except OSError as e:  # timeouts and connection errors
            err = e
        found = saved()
        if found:
            return found
    fail(f"{method} {path} failed twice ({err}); re-read before any further attempt")


# recipes

def recipes(out, tags, names, slugs, refresh):
    cache = json.load(open(out)) if os.path.exists(out) else {}
    want = list(slugs)
    for tag in tags:
        want += [r["slug"] for r in http("GET", f"/api/recipes?page=1&perPage=2000&tags={urllib.parse.quote(tag)}")["items"]]
    if names:
        summary = http("GET", "/api/recipes?page=1&perPage=2000")["items"]
        for name in names:
            hit = [r["slug"] for r in summary if r["name"].lower() == name.lower()]
            if not hit:
                fail(f"no recipe named '{name}'; stop and ask the user")
            want.append(hit[0])
    for slug in dict.fromkeys(want):
        if refresh or slug not in cache:
            cache[slug] = http("GET", f"/api/recipes/{slug}")
            with open(out, "w") as f:  # save after each fetch: a full fetch takes minutes
                json.dump(cache, f)
    for slug in dict.fromkeys(want):
        r, n = cache[slug], cache[slug].get("nutrition") or {}
        print(f"{slug}: {r['name']} | serves {r.get('recipeServings')} | {n.get('calories')} kcal, "
              f"{n.get('proteinContent')} protein, {n.get('fiberContent')} fiber | "
              + ", ".join(t["name"] for t in r.get("tags") or []))


# meal plan

def read_plan(start, end):
    return http("GET", f"/api/households/mealplans?start_date={start}&end_date={end}&perPage=500")["items"]


def show(e):
    name = (e.get("recipe") or {}).get("name") or e.get("title") or e.get("recipeId")
    return f"{e['date']} {e['entryType']:9} {name} | {e.get('text') or ''} [{e['id']}]"


def matches(item, body):
    return all((item.get(k) or "") == (body.get(k) or "") for k in ("date", "entryType", "recipeId", "title", "text"))


def write_plan(w, mode):
    existing = read_plan(w["start"], w["end"])
    if existing and not mode:
        print("\n".join(show(e) for e in existing))
        fail(f"{len(existing)} entries exist from {w['start']} to {w['end']}; show them, ask the user "
             "whether to keep, replace or add alongside, then pass --keep, --replace or --add")
    slots = {}
    for e in existing:
        slots.setdefault((e["date"], e["entryType"]), []).append(e)
    expected = {}
    for new in w["entries"]:
        key = (new["date"], new["entryType"])
        old = slots.get(key, [])
        expected[key] = len(old) + (1 if mode == "add" or not old else 0)
        saved = lambda: next((i for i in read_plan(new["date"], new["date"]) if matches(i, new)), None)
        if old and mode == "keep":
            continue
        if old and mode == "replace":
            body = {k: v for k, v in old[0].items() if k != "recipe"}
            body.update(new)
            write("PUT", f"/api/households/mealplans/{old[0]['id']}", body, saved)
            for extra in old[1:]:
                print("still present, remove in Mealie if unwanted: " + show(extra))
            continue
        write("POST", "/api/households/mealplans", new, saved)
    # re-read: a slot with more entries than expected is a duplicate
    after = {}
    for e in read_plan(w["start"], w["end"]):
        after[(e["date"], e["entryType"])] = after.get((e["date"], e["entryType"]), 0) + 1
    off = [f"{d} {t}: {after.get((d, t), 0)} entries, expected {n}" for (d, t), n in sorted(expected.items())
           if after.get((d, t), 0) != n]
    if off:
        fail("after writing:\n" + "\n".join(off))
    print(f"wrote {w['start']} to {w['end']}: every slot has the expected entry count")


# shopping list

def read_list(list_id):
    return http("GET", f"/api/households/shopping/lists/{list_id}")


def create_list(name, again):
    same = lambda: [l for l in http("GET", "/api/households/shopping/lists?perPage=500")["items"] if l["name"] == name]
    before = same()
    if before and not again:
        fail(f"a list named '{name}' exists ({before[0]['id']}); ask the user before creating another, then pass --again")
    made = write("POST", "/api/households/shopping/lists", {"name": name},
                 lambda: next((l for l in same() if l["id"] not in {b["id"] for b in before}), None))
    print(made["id"])


def add_recipes(list_id, w):
    if read_list(list_id).get("recipeReferences"):
        fail(f"list {list_id} already holds recipes; adding again doubles every quantity")
    write("POST", f"/api/households/shopping/lists/{list_id}/recipe", w["shopping"],
          lambda: read_list(list_id).get("recipeReferences") or None)
    print(f"added {len(w['shopping'])} recipe items to {list_id}")


def show_item(i):
    return (f"{'x' if i.get('checked') else ' '} {i.get('quantity')} {(i.get('unit') or {}).get('name') or ''} "
            f"{(i.get('food') or {}).get('name') or ''} | {i.get('note') or ''} [{i['id']}]")


def update_item(list_id, item_id, quantity, checked):
    item = next((i for i in read_list(list_id)["listItems"] if i["id"] == item_id), None)
    if not item:
        fail(f"no item {item_id} on list {list_id}")
    if quantity is not None:
        if quantity <= 0:
            fail("a quantity must stay above 0; check the item off instead")
        item["quantity"] = quantity
    if checked:
        item["checked"] = True
    want = {k: item[k] for k in ("quantity", "checked")}
    write("PUT", f"/api/households/shopping/items/{item_id}", item,
          lambda: next((i for i in read_list(list_id)["listItems"]
                        if i["id"] == item_id and all(i.get(k) == v for k, v in want.items())), None))
    print(show_item(item))


def main(argv):
    ap = argparse.ArgumentParser(prog="mealie.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("recipes")
    s.add_argument("--out", required=True)
    s.add_argument("--tag", action="append", default=[])
    s.add_argument("--name", action="append", default=[])
    s.add_argument("--slug", action="append", default=[])
    s.add_argument("--refresh", action="store_true")
    s = sub.add_parser("read-plan")
    s.add_argument("start")
    s.add_argument("end")
    s = sub.add_parser("write-plan")
    s.add_argument("writes")
    g = s.add_mutually_exclusive_group()
    for m in ("keep", "replace", "add"):
        g.add_argument(f"--{m}", dest="mode", action="store_const", const=m)
    s = sub.add_parser("create-list")
    s.add_argument("name")
    s.add_argument("--again", action="store_true")
    s = sub.add_parser("add-recipes")
    s.add_argument("list_id")
    s.add_argument("writes")
    s = sub.add_parser("read-list")
    s.add_argument("list_id")
    s = sub.add_parser("update-item")
    s.add_argument("list_id")
    s.add_argument("item_id")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--quantity", type=float)
    g.add_argument("--checked", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "recipes":
        recipes(a.out, a.tag, a.name, a.slug, a.refresh)
    elif a.cmd == "read-plan":
        print("\n".join(show(e) for e in read_plan(a.start, a.end)))
    elif a.cmd == "write-plan":
        write_plan(json.load(open(a.writes)), a.mode)
    elif a.cmd == "create-list":
        create_list(a.name, a.again)
    elif a.cmd == "add-recipes":
        add_recipes(a.list_id, json.load(open(a.writes)))
    elif a.cmd == "read-list":
        print("\n".join(show_item(i) for i in read_list(a.list_id)["listItems"]))
    elif a.cmd == "update-item":
        update_item(a.list_id, a.item_id, a.quantity, a.checked)


def self_test():
    """Runs every command against an in-memory stand-in for the server; nothing leaves the machine."""
    import tempfile

    class Fake:
        def __init__(self):
            tag = lambda n: [{"name": n, "slug": n.lower().replace(" ", "-")}]
            self.recipes = {
                "egg-bomb": {"id": "r1", "slug": "egg-bomb", "name": "Breakfast - Protein Egg Bomb", "recipeServings": 1,
                             "tags": tag("Breakfast Template"), "nutrition": {"calories": "450", "proteinContent": "45g", "fiberContent": "6"}},
                "chicken": {"id": "r2", "slug": "chicken", "name": "Chicken", "recipeServings": 4,
                            "tags": tag("Dinner Template"), "nutrition": {"calories": "650", "proteinContent": "50", "fiberContent": "12"}},
            }
            self.plan, self.lists, self.items, self.calls = [], {}, {}, []
            self.timeout_after_save = self.double_save = False
            self.n = 0

        def new_id(self):
            self.n += 1
            return f"id{self.n}"

        def __call__(self, method, path, body=None):
            assert method in ("GET", "POST", "PUT"), f"unexpected {method}"
            self.calls.append((method, path))
            url = urllib.parse.urlsplit(path)
            q = {k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()}
            parts = url.path.strip("/").split("/")[1:]
            result = self.route(method, parts, q, body)
            if method != "GET" and self.timeout_after_save:
                self.timeout_after_save = False
                raise TimeoutError("timed out")
            return result

        def route(self, method, parts, q, body):
            if parts[0] == "recipes":
                if len(parts) == 2:
                    return self.recipes[parts[1]]
                rs = [r for r in self.recipes.values() if "tags" not in q or q["tags"] in [t["slug"] for t in r["tags"]]]
                return {"items": [{"slug": r["slug"], "name": r["name"]} for r in rs]}
            if parts[1] == "mealplans":
                if method == "GET":
                    return {"items": [e for e in self.plan if q["start_date"] <= e["date"] <= q["end_date"]]}
                if method == "POST":
                    for _ in range(2 if self.double_save else 1):
                        self.plan.append(dict(body, id=self.new_id(), recipe=None))
                    return self.plan[-1]
                e = next(e for e in self.plan if e["id"] == parts[2])
                e.update(body)
                return e
            if parts[2] == "lists":
                if len(parts) == 3 and method == "GET":
                    return {"items": list(self.lists.values())}
                if len(parts) == 3:
                    lid = self.new_id()
                    self.lists[lid] = {"id": lid, "name": body["name"], "listItems": [], "recipeReferences": []}
                    return self.lists[lid]
                lst = self.lists[parts[3]]
                if method == "GET":
                    return lst
                for add in body:  # POST .../recipe: one item per recipe, quantity = scale
                    lst["recipeReferences"].append({"recipeId": add["recipeId"]})
                    lst["listItems"].append({"id": self.new_id(), "quantity": add["recipeIncrementQuantity"],
                                             "checked": False, "food": {"name": add["recipeId"]}, "unit": None, "note": ""})
                return lst
            item = next(i for lst in self.lists.values() for i in lst["listItems"] if i["id"] == parts[3])
            item.update(body)
            return item

    def no_network(*a, **k):
        raise AssertionError("the self-test tried to reach a real server")
    urllib.request.urlopen = no_network
    fake = Fake()
    globals()["http"] = fake
    tmp = tempfile.mkdtemp()
    catalog, writes = os.path.join(tmp, "catalog.json"), os.path.join(tmp, "writes.json")

    def refused(argv, text):
        try:
            main(argv)
        except SystemExit as e:
            assert text in str(e), e
            return
        raise AssertionError(f"{argv} should have been refused")

    # recipes: by tag and exact name, cached; an unknown name stops
    main(["recipes", "--out", catalog, "--tag", "dinner-template", "--name", "breakfast - protein egg bomb"])
    assert set(json.load(open(catalog))) == {"chicken", "egg-bomb"}
    fetched = len(fake.calls)
    main(["recipes", "--out", catalog, "--slug", "chicken"])
    assert len(fake.calls) == fetched, "a cached recipe was fetched again"
    refused(["recipes", "--out", catalog, "--name", "Missing"], "no recipe named 'Missing'")

    entry = lambda d, t, rid, text: {"date": d, "entryType": t, "recipeId": rid, "title": "", "text": text}
    w = {"start": "2026-10-05", "end": "2026-10-06", "list_name": "Meal plan 2026-10-05 to 2026-10-06",
         "entries": [entry("2026-10-05", "breakfast", "r1", "2 servings (user + partner)"),
                     entry("2026-10-05", "dinner", "r2", "Cook: 2 servings tonight, 2 leftover for Tue 10/6"),
                     entry("2026-10-06", "dinner", "r2", "Leftovers from Mon 10/5")],
         "shopping": [{"recipeId": "r1", "recipeIncrementQuantity": 4}, {"recipeId": "r2", "recipeIncrementQuantity": 1}]}
    json.dump(w, open(writes, "w"))

    # an existing entry blocks the write until the user picks a mode
    fake.plan.append({"id": "old", "date": "2026-10-05", "entryType": "dinner", "recipeId": "rx", "title": "", "text": "", "recipe": {"name": "Old"}})
    refused(["write-plan", writes], "1 entries exist")
    assert not [c for c in fake.calls if c[0] != "GET" and "mealplans" in c[1]]

    # --keep skips the filled slot; a create that times out after saving is not sent twice
    fake.timeout_after_save = True
    main(["write-plan", writes, "--keep"])
    assert len([e for e in fake.plan if e["date"] == "2026-10-05" and e["entryType"] == "breakfast"]) == 1
    assert [e["recipeId"] for e in fake.plan if e["date"] == "2026-10-05" and e["entryType"] == "dinner"] == ["rx"]

    # --replace overwrites the old entry in place
    main(["write-plan", writes, "--replace"])
    old = next(e for e in fake.plan if e["id"] == "old")
    assert old["recipeId"] == "r2" and old["text"].startswith("Cook:")
    assert len(fake.plan) == 3

    # the post-write re-read catches a duplicate the server made
    fake.plan.clear()
    fake.double_save = True
    refused(["write-plan", writes], "2 entries, expected 1")
    fake.double_save = False

    # shopping list: a name in use needs --again; a timed-out bulk add is not sent twice
    main(["create-list", w["list_name"]])
    lid = next(iter(fake.lists))
    refused(["create-list", w["list_name"]], "exists")
    fake.timeout_after_save = True
    main(["add-recipes", lid, writes])
    assert len(fake.lists[lid]["recipeReferences"]) == 2
    refused(["add-recipes", lid, writes], "already holds recipes")

    # items are lowered or checked off, never removed
    item = fake.lists[lid]["listItems"][0]["id"]
    refused(["update-item", lid, item, "--quantity", "0"], "check the item off")
    main(["update-item", lid, item, "--quantity", "2.5"])
    main(["update-item", lid, item, "--checked"])
    got = fake.lists[lid]["listItems"][0]
    assert got["quantity"] == 2.5 and got["checked"] is True and len(fake.lists[lid]["listItems"]) == 2
    main(["read-list", lid])
    main(["read-plan", "2026-10-05", "2026-10-06"])
    assert all(m in ("GET", "POST", "PUT") for m, _ in fake.calls)
    print("\nself-check passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    else:
        main(sys.argv[1:])
