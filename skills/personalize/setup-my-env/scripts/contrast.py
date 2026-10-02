#!/usr/bin/env python3
"""WCAG 2 contrast between two colors, and a hue-keeping fix to reach a target ratio.

  contrast.py FG BG                 print the ratio of FG on BG
  contrast.py --fix FG BG [TARGET]  print FG moved in lightness until it reaches TARGET (default 4.6) on BG
  contrast.py --self-test           run the checks

Colors are hex: #RRGGBB, RRGGBB or #RGB.
"""
import colorsys
import sys


def rgb(hexstr):
    h = hexstr.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6 or any(c not in "0123456789abcdefABCDEF" for c in h):
        sys.exit(f"not a hex color: {hexstr}")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hexstr(c):
    return "#%02X%02X%02X" % tuple(round(v * 255) for v in c)


def luminance(c):
    f = lambda v: v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def fix(fg, bg, target=4.6):
    """Lighten fg on a dark bg, darken it on a light bg, until contrast >= target. 4.6 leaves margin over WCAG AA's 4.5."""
    h, l, s = colorsys.rgb_to_hls(*fg)
    step = 0.005 if luminance(bg) < 0.18 else -0.005
    c = fg
    while contrast(rgb(hexstr(c)), bg) < target and (l < 1 if step > 0 else l > 0):
        l = min(1, max(0, l + step))
        c = colorsys.hls_to_rgb(h, l, s)
    return rgb(hexstr(c))


def self_test():
    assert round(contrast(rgb("#000000"), rgb("#FFFFFF")), 1) == 21.0
    assert round(contrast(rgb("#686868"), rgb("#15191F")), 2) == 3.16
    fixed = fix(rgb("#686868"), rgb("#15191F"))
    assert contrast(fixed, rgb("#15191F")) >= 4.6 and luminance(fixed) > luminance(rgb("#686868"))
    fixed = fix(rgb("#FFFFFF"), rgb("#FAFAFA"))  # starts at lightness 1, must still darken
    assert contrast(fixed, rgb("#FAFAFA")) >= 4.6
    assert rgb("#FFF") == (1.0, 1.0, 1.0)
    fixed = fix(rgb("#ECE100"), rgb("#FAFAFA"))
    assert contrast(fixed, rgb("#FAFAFA")) >= 4.6 and luminance(fixed) < luminance(rgb("#ECE100"))
    print("self-test passed")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
    elif args[0] == "--self-test":
        self_test()
    elif args[0] == "--fix" and len(args) >= 3:
        fg, bg = rgb(args[1]), rgb(args[2])
        target = float(args[3]) if len(args) > 3 else 4.6
        new = fix(fg, bg, target)
        print(f"{hexstr(fg)} {contrast(fg, bg):.2f}:1 -> {hexstr(new)} {contrast(new, bg):.2f}:1")
        if contrast(new, bg) < target:
            sys.exit(f"target {target}:1 not reachable on this background by changing lightness")
    elif len(args) != 2:
        sys.exit(__doc__)
    else:
        print(f"{contrast(rgb(args[0]), rgb(args[1])):.2f}:1")
