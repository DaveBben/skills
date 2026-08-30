#!/usr/bin/env python3
"""Assert that the blocks deliberately duplicated across skills stay identical.

Only one skill body loads at a time and no skill may read another skill's
references directory, so a rule every phase needs has to be copied into each
skill that needs it. This compares the copies and fails when they drift.

    python3 tools/check-shared-blocks.py
"""
import re
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "plugins/sdlc/skills"

# name -> (anchor that starts the block, how many lines it runs, which skills carry it)
BLOCKS = {
    # Empty: the six stage skills were merged into `engineering`, so no prose block is
    # duplicated across skills any more. Re-populate if a second skill ever repeats one.
    # Not covered here: references/adr.md, byte-identical in engineering and bootstrapping.
}


def extract(skill: str, anchor: str, lines: int) -> list[str] | None:
    body = (SKILLS / skill / "SKILL.md").read_text().splitlines()
    for i, line in enumerate(body):
        if re.search(anchor, line):
            return [l.rstrip() for l in body[i : i + lines] if l.strip()]
    return None


def main() -> int:
    if not BLOCKS:
        print("INERT  no block is duplicated across skills.")
        print("       See the module docstring before treating this as a pass.")
        return 0

    failed = False
    for name, (anchor, lines, skills) in BLOCKS.items():
        found = {s: extract(s, anchor, lines) for s in skills}

        missing = [s for s, v in found.items() if v is None]
        if missing:
            print(f"FAIL  {name}: not found in {', '.join(missing)}")
            failed = True
            continue

        reference_skill = skills[0]
        reference = found[reference_skill]
        for skill in skills[1:]:
            if found[skill] != reference:
                print(f"FAIL  {name}: {skill} differs from {reference_skill}")
                for a, b in zip(reference, found[skill]):
                    if a != b:
                        print(f"        {reference_skill}: {a}")
                        print(f"        {skill}: {b}")
                        break
                failed = True

        if not failed:
            print(f"ok    {name}: identical across {', '.join(skills)}")

    if failed:
        print("\nThese blocks are duplicated on purpose because each skill must stand")
        print("alone. Change one, change them all.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
