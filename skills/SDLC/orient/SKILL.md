---
name: orient
description: "Use this skill when a repository's AGENTS.md or CLAUDE.md must be written, rewritten, trimmed or checked, when an agent must orient itself in an unfamiliar repository, or when the user wants to see the architecture of the code they work in. Use it on: 'write AGENTS.md', 'write a CLAUDE.md', 'set up CLAUDE.md', 'review my CLAUDE.md', 'our CLAUDE.md is too long', 'trim AGENTS.md', 'what should go in CLAUDE.md', 'orient yourself', 'familiarize yourself with this codebase', 'show me the architecture', 'what's the current architecture', 'give me an updated view of the architecture', 'what calls this service', 'write an onboarding doc'. Writes AGENTS.md at the repository root, with CLAUDE.md a symlink to it, holding only what an agent cannot learn by reading the repository, and a one-page architecture snapshot in ARCHITECTURE.md, traced from the code and every system that calls it or that it calls. Not for enforcing a rule with a linter, hook or commit check; that is `guardrails`."
license: MIT
metadata:
  version: "1.1.0"
---
# Orient

`AGENTS.md` at the repository root loads into every session before its first message. Every line costs every session. The agent reads the README, the manifest and the code on its own.

Keep a line only when deleting it would cause a mistake nothing else in the repository prevents.

## What goes in

* **Commands the repository does not make obvious:** exact and copy-pasteable, as listed below.
  * **`Check:`** the check command, run at turn end.
  * **`Full check:`** the full check command, run before a pull request.
  * **How to run one test.**
  * **Tool choices the agent would get wrong:** "run Python through `uv run`; never `pip install`".
* **Constraints no program checks:** state each as the mechanism, what happens and what breaks.
  * **Good:** "Never hold a worker longer than one HTTP round trip; the pool has 5 and a full pool returns 502 to every user".
  * **Bad:** "keep the pool safe".
* **Traps:** one line each, such as these.
  * A generated file changed only through its generator.
  * A test that needs a running service.
  * A directory that looks unused and is loaded at runtime.
  * A test that already fails on main.
* **Pointers:** the path of a document the agent would not find on its own and when to read it
* **Boundaries:** one `Boundaries:` line naming each system the product reads, writes or runs inside.
  * **Writers:** for each store the product reads, name who writes the data: this product, a person through its own screens, or something outside.
* **Project Tracker:** If using a project management tool like Jira, GitHub Projects, etc - add link to the location.

Keep the `Check:` and `Full check:` lines as found and exempt them from the findings below.

## What stays out

* **What a check enforces:** formatter settings, lint rules, type rules. A rule a program could check but none does yet goes to the `guardrails` skill.
* **What the repository already says:** the purpose and stack the README and manifest give, a directory map, a feature list, an architecture description.
* **Advice the agent follows unprompted:** write tests, handle errors, keep functions small.
* **Words that cannot fail:** improve, better, seamless, robust, correct, properly, handled, intuitive, flexible, scalable, modern.

## Shape

There is no fixed template.

* **First:** the `Boundaries:` and `Architecture:` lines.
* **Then:** only the headings that have content, in this order: Commands, Constraints, Traps, Pointers.
* **Size:** most repositories need under 40 lines. Cap the file at 100 lines and 8 KB.
* **Adding a line:** rewrite the file by these rules rather than appending.
* **Module conventions:** put them in a nested `AGENTS.md` inside that module.
* **Symlinks:** link `CLAUDE.md`, and any other instructions-file name the repository carries, to `AGENTS.md`, and commit them together.

## Architecture snapshot

Every run of this skill, and every request to see the architecture, writes or refreshes `ARCHITECTURE.md` at the repository root. The snapshot traces the code, every outside system that calls into it and every system it calls, and lays them out on one page a newcomer reads in five minutes. Read [references/architecture.md](references/architecture.md) before tracing. A request only to see the architecture needs only the snapshot; leave `AGENTS.md` untouched.

## Writing it

1. **Read first:** the existing `AGENTS.md` and any real `CLAUDE.md`, each whole. Then run each test, lint and check command once, and keep none that fails.
2. **Send one message** holding:
   * a table of each existing line, whether it is kept, moved to a check by `guardrails`, or dropped, and the reason;
   * the draft of new lines;
   * only the questions the repository cannot answer, usually constraints and traps.
3. **Ask in that message about each of these only when the repository shows it applies,** and write each yes as a constraint with its number or list.
   * **Response time and volume:** the repository runs a server.
   * **Locales:** it shows dates, money or text to users.
   * **Browsers and devices:** it has a web or mobile front end.
   * **Regulations such as GDPR, HIPAA, PCI or SOX:** it holds personal, health or payment data.
4. **On yes:** write `AGENTS.md` from the kept and corrected lines, and replace a real `CLAUDE.md` with the symlink. **On no:** touch nothing.
5. **Take the architecture snapshot,** whatever the answer.

## Orienting

Take the architecture snapshot, then report in one message:

* The commands.
* The constraints and traps.
* Every finding below when the user asked to check or review the file; otherwise the count of findings and an offer to list them.

Rewrite nothing unless the user accepts a finding. With no `AGENTS.md`, offer to write one.

**Findings,** each quoting its line:

* A line a check enforces or the repository already shows.
* A line that cannot fail.
* A command that does not run.
* A constraint with no mechanism.
* A file over 100 lines or 8 KB.

With no check command, offer the `guardrails` skill once.
