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

`AGENTS.md` at the repository root loads into every session before its first message. Every line costs every session. The agent reads the README, the manifest and the code on its own.

Keep a line only when deleting it would cause a mistake nothing else in the repository prevents.

## What goes in

* **Commands the repository does not make obvious:** exact and copy-pasteable, as listed below.
  * **`Check:`** the check command, run at turn end.
  * **`Full check:`** the full check command, run before a pull request.
  * **How to run one test.**
  * **The red-commit command:** how to commit failing tests before their code when a hook runs the tests.
  * **Tool choices the agent would get wrong:** "run Python through `uv run`; never `pip install`".
  * **Verified:** run each test, lint and check command once; list none that fails.
* **Constraints no program checks:** state each as the mechanism, what happens and what breaks.
  * **Good:** "Never hold a worker longer than one HTTP round trip; the pool has 5 and a full pool returns 502 to every user".
  * **Bad:** "keep the pool safe".
  * **Reason unknown:** write "cause not established".
* **Traps:** one line each, such as these.
  * A generated file changed only through its generator.
  * A test that needs a running service.
  * A directory that looks unused and is loaded at runtime.
  * A test that already fails on main.
* **Architecture:** one `Architecture:` line with the path of the document that describes the system's shape (processes, stores, flows), when the repository has one.
* **Pointers:** the path of a document the agent would not find on its own, and when to read it.
* **Boundaries:** one `Boundaries:` line naming each system the product reads, writes or runs inside.
  * **Writers:** for each store the product reads, name who writes the data: this product, a person through its own screens, or something outside.
  * **Why:** the security review treats data from an outside writer as untrusted.

Other skills write or read these lines. Keep each as found and exempt it from the findings below.

* The `Check:` and `Full check:` lines.
* The red-commit command.
* A number of stories built at once.
* Every line `guardrails` wrote under Constraints.

## What stays out

* **What a check enforces:** formatter settings, lint rules, type rules. A rule that must hold and has no check goes to the `guardrails` skill.
* **What the repository already says:** the purpose and stack the README and manifest give, a directory map, a feature list, an architecture description.
* **Advice the agent follows unprompted:** write tests, handle errors, keep functions small.
* **Words that cannot fail:** improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable, modern.

## Shape

There is no fixed template.

* **First:** the `Boundaries:` and `Architecture:` lines.
* **Then:** only the headings that have content, in this order: Commands, Constraints, Traps, Pointers.
* **Size:** most repositories need under 40 lines. Cap the file at 100 lines and 8 KB.
* **Cap enforcement:** in Claude Code, `scripts/size_guard.py` refuses an edit that takes the file past the cap.
* **Adding a line:** rewrite the file by these rules rather than appending.
* **Module conventions:** put them in a nested `AGENTS.md` inside that module.
* **Symlinks:** link `CLAUDE.md`, and any other instructions-file name the repository carries, to `AGENTS.md`, and commit them together.

## Writing it

1. **Ask only what the repository cannot answer,** in one message of draft lines to correct. Usually that is the constraints and the traps.
2. **In the same message,** ask which of these hold for every change, and write each that does as a constraint with its number or list.
   * Response time and volume.
   * Supported locales: time zones, date, number and currency formats.
   * Supported browsers, devices and screen sizes.
   * Applicable regulations, such as GDPR, HIPAA, PCI or SOX.
3. **When an instructions file exists** (`AGENTS.md`, a real `CLAUDE.md`, or both), read each whole.
4. **Show one table:** each line, whether it is kept, moved to a check by `guardrails`, or dropped, and the reason.
5. **Ask once.**
   * **Yes:** write `AGENTS.md` from the kept lines and replace a real `CLAUDE.md` with the symlink.
   * **No:** touch nothing.

## Orienting

Report in one message:

* What the repository is for, from the README.
* The commands.
* The constraints and traps.
* Every finding below.

Rewrite nothing unless the user accepts a finding. With no `AGENTS.md`, offer to write one.

**Findings,** each quoting its line:

* A line a check enforces or the repository already shows.
* A line that cannot fail.
* A command that does not run.
* A constraint with no mechanism.
* A file over 100 lines or 8 KB.
* No check command: offer the `guardrails` skill once.
