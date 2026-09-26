#!/usr/bin/env python3
"""Assert that the text deliberately duplicated across skills stays identical.

Only one skill body loads at a time and no skill may read another skill's
files, so a rule several skills need has to be copied into each skill that
needs it. This compares the copies and fails when they drift.

    python3 tools/check-shared-blocks.py
"""
import re
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "skills/SDLC"

# name -> (anchor that starts the block, how many lines it runs, which skills carry it)
BLOCKS = {
    # Empty: no prose block inside a SKILL.md is duplicated across skills.
    # Re-populate if a second skill ever repeats one.
}

# name -> the same file, byte for byte, in each of these skills
FILES = {
    "writing rules": ["deliver/references/writing.md",
                      "spike/references/writing.md",
                      "reviewing/references/writing.md",
                      "architecture/references/writing.md"],
}


def extract(skill: str, anchor: str, lines: int) -> list[str] | None:
    body = (SKILLS / skill / "SKILL.md").read_text().splitlines()
    for i, line in enumerate(body):
        if re.search(anchor, line):
            return [l.rstrip() for l in body[i : i + lines] if l.strip()]
    return None


def check_blocks() -> bool:
    failed = False
    for name, (anchor, lines, skills) in BLOCKS.items():
        found = {s: extract(s, anchor, lines) for s in skills}
        missing = [s for s, v in found.items() if v is None]
        if missing:
            print(f"FAIL  {name}: not found in {', '.join(missing)}")
            failed = True
            continue
        reference = found[skills[0]]
        for skill in skills[1:]:
            if found[skill] != reference:
                print(f"FAIL  {name}: {skill} differs from {skills[0]}")
                failed = True
        if not failed:
            print(f"ok    {name}: identical across {', '.join(skills)}")
    return failed


def check_files() -> bool:
    failed = False
    for name, paths in FILES.items():
        missing = [p for p in paths if not (SKILLS / p).is_file()]
        if missing:
            print(f"FAIL  {name}: missing {', '.join(missing)}")
            failed = True
            continue
        reference = (SKILLS / paths[0]).read_bytes()
        differs = [p for p in paths[1:] if (SKILLS / p).read_bytes() != reference]
        if differs:
            print(f"FAIL  {name}: {', '.join(differs)} differ from {paths[0]}")
            failed = True
        else:
            print(f"ok    {name}: identical across {', '.join(paths)}")
    return failed


def main() -> int:
    failed = check_blocks() | check_files()
    if failed:
        print("\nThese copies are duplicated on purpose because each skill must stand")
        print("alone. Change one, change them all.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
