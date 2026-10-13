---
name: refactoring
description: "Use this skill whenever code's structure must change while its behaviour stays the same, or code must be judged for smells, mess or readability. Use it even for one small named refactoring: a rename, an extract, an inline, a move, guard clauses, a constant for a magic number. Use it on: 'refactor X', 'should this be refactored', 'what smells are in this code', 'clean up this file', 'this code is messy', 'make this more readable', 'simplify this function', 'reduce the duplication', 'split this file', 'remove dead code', 'where is our tech debt', and a story's refactor step. Load it before reading the code. Names each smell with the lines that show it, refactors only what a change in hand or a hotspot justifies, in small steps with the tests green after each, and commits structure apart from behaviour. Not for reviewing a diff or a pull request; that is `review-code`. Not for changing behaviour; that is `story` or `bug`."
license: MIT
metadata:
  version: "1.1.0"
---
# Refactoring

A refactoring changes the structure of code and leaves its observable behaviour unchanged. It pays only when it makes a change cheaper, so refactor code you are about to change, code you had to struggle to understand, and hotspots, and leave the rest alone.

## Words used here

* **Smell:** a surface sign that usually points to a design problem. It is a reason to look, never a verdict.
* **Observable behaviour:** return values, raised errors, writes to files, databases, networks and logs, public names and signatures, and any ordering a caller can see.
* **Hotspot:** a file that is both complex and often changed. Rank files by change count with `git log --format= --name-only | sort | uniq -c | sort -rn`, then read the top ones for complexity.
* **Characterization test:** a test that pins what the code does now, written by running the code and asserting the output it gave.
* **Structure commit:** a commit that holds only refactorings. A **behaviour commit** holds only changes a caller can observe.

## Decide whether to refactor

Refactor when one of these holds:

* **Preparatory:** a change you are about to make is awkward in the current shape. Make the change easy, then make the easy change.
* **Comprehension:** you had to trace the code to understand it. Put that understanding into names and structure so the next reader does not trace it.
* **Duplicated knowledge:** a rule, a schema or a constant is copied in a third place, and the copies change for the same reason.
* **Hotspot:** the user asks where to clean up, or a scheduled run starts this skill. Rank by change frequency first; unhealthy code nobody changes costs little.

Leave it alone when:

* **No change touches it:** working code that nobody edits pays back no refactoring.
* **It is due for deletion,** or a rewrite of it is already agreed.
* **The duplication is coincidental:** the same text serves rules that change for different reasons. Duplication costs less than the wrong abstraction. An extraction that needs a flag or mode argument to serve its callers is the wrong abstraction.
* **Length is the only complaint:** a long function that reads top to bottom at one level of abstraction beats pieces a reader must jump between. Split only where each piece has a simple interface and reads without the others.

When the user asks whether code should be refactored, answer in this order: what is good and stays, each smell with the lines that show it and the refactoring that cures it, when to do each (now, when a named change next touches it, or never), and what not to do.

## Find the smells

Look first for the smells that cost the most to leave:

* **Scattered responsibility:** one concept changed in many places, or one resource opened in one function and closed in several others.
* **A name that misleads:** a function that does something its name does not say, such as a builder that closes another object.
* **Duplicated knowledge:** the same rule or constant written twice.
* **A pass-through:** a function or class that only forwards its arguments to another.
* **Speculative generality:** a parameter, hook or interface with one implementation and no second caller.
* **Shared mutable state** written from several places.
* **A flag argument** that switches a function between two jobs.
* **A comment that explains an ordering or a workaround** the structure could enforce instead. A comment that explains why is not a smell.

The full catalogue, with how to see each smell and the named refactorings that cure it, is in [references/smells.md](references/smells.md). Name each smell and its refactoring by their catalogue names in your report and commit messages.

## Readability

* **Names:** full words, specific to the role (`unseen_articles`, not `data` or `ua`). Use the term `docs/glossary.md` gives a concept when it gives one. Follow the repository's case convention.
* **One meaning per line:** no assignment or increment used as a value, no `&&` or `or` used as control flow, braces on every block, one role per variable, explicit conditions (`if count != 0`, not `if count` when `count` is a number).
* **Nesting:** replace nested conditionals with guard clauses that return early.
* **Deep modules:** a small interface that hides a lot. A method or variable that only passes through a layer is a smell.
* **Comments:** state what the code cannot show: why, units, invariants, ordering constraints. Delete a comment that repeats the code, and keep each explanation in one place.
* **Metrics:** complexity and readability scores are hints, never gates. Judge by whether a reader can predict what the code does without jumping elsewhere.

## Refactor safely

* **Green first:** run the tests before the first step. Code the refactoring touches that no test covers gets characterization tests first, committed alone.
* **One hat at a time:** never change behaviour in a refactoring step. A bug found mid-refactoring is noted, the step finished or reverted, and the bug fixed afterwards in its own commit by the `bug` skill.
* **Small named steps, never outrunning your headlights:** apply one named refactoring, run the tests, commit. A red test means revert the step; do not debug forward.
* **Tools first:** use the language server's or IDE's rename, extract and move where one is available; a refactoring engine checks what hand edits miss.
* **Keep what callers rely on:** public names and signatures (migrate them with parallel change), error handling, assertions, logging, and comments that explain why. Read the diff for deleted lines before each commit, and justify each one.
* **Tests are not proof:** passing tests bound what changed, they do not prove nothing did. Where tests are thin, run the old and new code on the same inputs and compare the outputs.
* **Scope:** touch only the files the change needs. Add no abstraction with one implementation and no config with one value.
* **Commits:** each structure commit alone, its message naming the refactoring, such as `refactor: inline _classify_articles (Middle Man)`. Never mix it with a behaviour change.

## Large refactorings

Keep the build releasable at every step, on main, never on a long-lived branch:

* **Parallel change** for an interface: add the new form beside the old, move callers one at a time, then delete the old form.
* **Branch by abstraction** for a dependency: put an abstraction over it, move callers onto the abstraction, build the replacement behind it, switch, delete the old one.
* **Strangler fig** for a subsystem: grow the replacement beside it and move behaviour across piece by piece.
* **Mikado method** when the prerequisites are unknown: attempt the goal naively, record each failure as a prerequisite, revert, then do the prerequisites leaves first.
* **Hundreds of mechanical edits:** write a codemod or script, not hand edits.

## Scheduled run

A scheduled run (a Claude Code routine or a CI cron job, for example) proposes one refactoring and changes no code.

1. **Rank** files by changes in the last 90 days: `git log --since=90.days --format= --name-only | sort | uniq -c | sort -rn`. Drop files that no longer exist and files that hold no code, such as docs, lockfiles and JSON.
2. **Skip** a file named in the title of an open issue labelled `refactor`.
3. **Read** the top files for complexity and take the first that has a smell from the catalogue.
4. **Propose** one refactoring for it, written as the Report's `Smells:` line.
5. **File** it as one issue labelled `refactor`, titled `refactor: <path>: <smell>`, by the `using-trackers` skill, or print it when the repository has no tracker.

Once the user approves the issue, build it by Build it, below.

## Build it

* **Inside a story or a bug fix:** refactor at step 6 of the `story` skill's implement path, inside that branch's diff, by the rules above.
* **On its own:** build it through the `story` skill's implement path for a change with no behaviour change, `../story/references/implement.md` from this skill's folder.

## Report

```text
Keep: <what is good and stays, and why>
Smells: <file:line — smell — evidence — refactoring — when: now | when <named change> | never>
Done: <each structure commit and the refactoring it applied>; tests: <green before and after>
Not done: <what was left, and why>
```
