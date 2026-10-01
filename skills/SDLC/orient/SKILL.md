---
name: orient
description: "Use this skill when a repository's AGENTS.md or CLAUDE.md must be written, rewritten, trimmed or checked, or when an agent must orient itself in an unfamiliar repository. Use it on: 'write AGENTS.md', 'write a CLAUDE.md', 'set up CLAUDE.md', 'review my CLAUDE.md', 'our CLAUDE.md is too long', 'trim AGENTS.md', 'what should go in CLAUDE.md', 'orient yourself', 'familiarize yourself with this codebase'. Writes AGENTS.md at the repository root, with CLAUDE.md a symlink to it, holding only what an agent cannot learn by reading the repository. Not for enforcing a rule with a linter, hook or commit check; that is `guardrails`."
license: MIT
metadata:
  version: "1.0.0"
# Claude Code only: registered when the skill runs, for the rest of the session.
# scripts/size_guard.py stops an AGENTS.md or CLAUDE.md growing past the cap. Without python3, it exits 0.
hooks:
  PreToolUse:
    - matcher: "Edit|Write|MultiEdit"
      hooks:
        - type: command
          command: 'f="${CLAUDE_PLUGIN_ROOT}/skills/orient/scripts/size_guard.py"; [ -f "$f" ] && command -v python3 >/dev/null 2>&1 || exit 0; python3 "$f"'
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          if: "Bash(*.md*)"
          command: 'f="${CLAUDE_PLUGIN_ROOT}/skills/orient/scripts/size_guard.py"; [ -f "$f" ] && command -v python3 >/dev/null 2>&1 || exit 0; python3 "$f"'
---
# Orient

`AGENTS.md` at the repository root loads into every session before its first message. Every line costs every session, and the agent reads the README, the manifest and the code on its own. Keep a line only when deleting it would cause a mistake nothing else in the repository prevents.

## What goes in

* **Commands the repository does not make obvious,** exact and copy-pasteable: the check commands (`Check:`, run at turn end, and `Full check:`, run before a pull request), how to run one test, the red-commit command (how to commit failing tests before their code when a hook runs the tests), and any tool choice the agent would otherwise get wrong ("run Python through `uv run`; never `pip install`"). Run each test, lint and check command once; one that fails is not listed.
* **Constraints no program checks,** each stated as the mechanism: what happens and what breaks. "Never hold a worker longer than one HTTP round trip; the pool has 5 and a full pool returns 502 to every user", not "keep the pool safe". When the reason is not known, write "cause not established".
* **Traps,** one line per trap, such as a generated file changed only through its generator, a test that needs a running service, a directory that looks unused and is loaded at runtime, a test that already fails on main.
* **Architecture:** one `Architecture:` line with the path of the document that describes the system's shape (its processes, stores and flows), when the repository has one.
* **Pointers** to a document the agent would not find on its own: the path and when to read it.
* **Boundaries:** one `Boundaries:` line naming each system the product reads, writes or runs inside, and who writes the data in each store it reads: this product, a person through its own screens, or something outside. The security review treats data from an outside writer as untrusted.

Other skills write or read these lines; keep each as found, and exempt it from the findings below: the `Check:` and `Full check:` lines, the red-commit command, a number of stories built at once, and every line `guardrails` wrote under Constraints.

## What stays out

* **What a check enforces:** formatter settings, lint rules, type rules. A rule that must hold and has no check goes to the `guardrails` skill.
* **What the repository already says:** the purpose and stack the README and manifest give, a directory map, a feature list, an architecture description.
* **Advice the agent follows unprompted:** write tests, handle errors, keep functions small.
* **Words that cannot fail:** improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable, modern.

## Shape

No fixed template. Put the `Boundaries:` and `Architecture:` lines first, then only the headings that have content, in this order: Commands, Constraints, Traps, Pointers. Most repositories need under 40 lines; cap it at 100 lines and 8 KB; in Claude Code, `scripts/size_guard.py` refuses an edit that takes the file past it. To add a line, rewrite the file by these rules rather than appending. A module's own conventions go in a nested `AGENTS.md` inside that module.

Symlink `CLAUDE.md`, and any other instructions-file name the repository carries, to `AGENTS.md`, and commit them together.

## Writing it

Ask the user only what the repository cannot answer, in one message of draft lines to correct; usually that is the constraints and the traps. In the same message, ask which of these hold for every change, and write each that does as a constraint with its number or list: response time and volume; supported locales (time zones, date, number and currency formats); supported browsers, devices and screen sizes; and the regulations that apply, such as GDPR, HIPAA, PCI or SOX.

When an instructions file exists (`AGENTS.md`, a real `CLAUDE.md`, or both), read each whole, then show one table: each line, and whether it is kept, moved to a check by `guardrails`, or dropped, with the reason. Ask once. On yes, write `AGENTS.md` from the kept lines and replace a real `CLAUDE.md` with the symlink. On no, touch nothing.

## Orienting

Report in one message: what the repository is for (from the README), the commands, the constraints and traps, and every finding below. Rewrite nothing unless the user accepts a finding. With no `AGENTS.md`, offer to write one.

**Findings,** each quoting its line: a line a check enforces or the repository already shows; a line that cannot fail; a command that does not run; a constraint with no mechanism; a file over 100 lines or 8 KB; no check command, with the `guardrails` skill offered once.
