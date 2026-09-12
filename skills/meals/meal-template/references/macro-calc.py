#!/usr/bin/env python3
"""Per-serving macro calculation for a meal template.

Extend FOODS with USDA FoodData Central values per 100 g, list the recipe's
ingredients in grams for the whole recipe, and divide by the serving count.
Grams, never volume: volume measures for solids are the largest error source.

Run directly to see the worked example.
"""

# name: (kcal, protein_g, fiber_g, fat_g, carb_g) per 100 g
FOODS = {
    "cod_raw":            (82, 17.8, 0.0, 0.67, 0.0),
    "artichoke_jarred":   (45, 2.6, 5.5, 0.2, 9.0),
    "kalamata":           (160, 1.0, 3.3, 17.3, 4.0),
    "olive_oil":          (884, 0.0, 0.0, 100.0, 0.0),
    "cannellini_canned":  (114, 7.3, 4.8, 0.4, 21.0),
    "spinach_raw":        (23, 2.9, 2.2, 0.4, 3.6),
    "lentils_cooked":     (116, 9.0, 7.9, 0.4, 20.1),
    "shrimp_cooked":      (99, 24.0, 0.0, 0.3, 0.2),
    "chicken_breast":     (165, 31.0, 0.0, 3.6, 0.0),
    "egg_white_raw":      (52, 10.9, 0.0, 0.2, 0.7),
}

TARGETS = {"kcal_max": 600, "protein_min": 40, "fiber_min": 10}


def per_serving(rows, servings, targets=TARGETS):
    """rows: [(food_key, grams_for_whole_recipe), ...]. Prints a table, returns totals."""
    total = [0.0] * 5
    print(f"{'ingredient':22}{'g/serv':>8}{'kcal':>7}{'P':>7}{'F':>7}{'fat':>7}{'carb':>7}")
    for key, grams in rows:
        vals = [x * grams / 100 / servings for x in FOODS[key]]
        total = [a + b for a, b in zip(total, vals)]
        print(f"{key:22}{grams/servings:8.0f}{vals[0]:7.0f}{vals[1]:7.1f}"
              f"{vals[2]:7.1f}{vals[3]:7.1f}{vals[4]:7.1f}")
    print(f"{'PER SERVING':22}{'':8}{total[0]:7.0f}{total[1]:7.1f}"
          f"{total[2]:7.1f}{total[3]:7.1f}{total[4]:7.1f}")
    print(f"  kcal    {total[0]:6.0f}  vs <= {targets['kcal_max']}"
          f"   headroom {targets['kcal_max'] - total[0]:+.0f}")
    print(f"  protein {total[1]:6.1f}  vs >= {targets['protein_min']}"
          f"   {total[1] - targets['protein_min']:+.1f}")
    print(f"  fiber   {total[2]:6.1f}  vs >= {targets['fiber_min']}"
          f"   {total[2] - targets['fiber_min']:+.1f}")
    return total


def demo():
    """Template 1: roasted cod with artichokes, cannellini, and spinach. 4 servings."""
    base = [("cod_raw", 792), ("artichoke_jarred", 510),
            ("kalamata", 67), ("olive_oil", 27)]
    print("=== base recipe alone ===")
    base_total = per_serving(base, 4)
    assert base_total[1] < 40, "base should fall short on protein"
    assert base_total[2] < 10, "base should fall short on fiber"

    print("\n=== base + cannellini and spinach add-on ===")
    full = base + [("cannellini_canned", 500), ("spinach_raw", 400), ("olive_oil", 14)]
    t = per_serving(full, 4)
    assert t[0] <= TARGETS["kcal_max"], "over the calorie ceiling"
    assert t[1] >= TARGETS["protein_min"], "under the protein floor"
    assert t[2] >= TARGETS["fiber_min"], "under the fiber floor"
    print("\nall targets clear")


if __name__ == "__main__":
    demo()
