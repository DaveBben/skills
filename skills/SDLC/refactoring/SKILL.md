---
name: refactoring
description: "Use this skill whenever code's structure must change while its behaviour stays the same, or code must be judged for smells, mess or readability, even one rename, extract, inline, move, guard clause or magic number. Use it on: 'refactor X', 'let's do that refactor', 'critique my approach to this refactor', 'what smells are in this code', 'clean up this file', 'simplify this function', 'reduce the duplication', 'split this file', 'merge these two packages', 'remove dead code', 'delete the leftover experiment code', 'where is our tech debt', and a story's refactor step. Load it before reading the code. Names each smell, refactors in small steps with tests green, and commits structure apart from behaviour. Not for reviewing a diff; that is `review-code`. Not for changing behaviour; that is `story` or `bug`."
license: MIT
metadata:
  version: "1.3.0"
---
# Refactoring

A refactoring changes the structure of code and leaves its observable behaviour unchanged. Refactor code you are about to change, code you struggled to understand, and hotspots. Leave the rest alone.

## Words used here

* **Smell:** a surface sign that usually points to a design problem. It is a reason to look, never a verdict.
* **Observable behaviour:** return values, raised errors, writes to files, databases, networks and logs, public names and signatures, and any ordering a caller can see.
* **Hotspot:** a file that is both complex and often changed. Rank files by change count with `git log --format= --name-only | sort | uniq -c | sort -rn`, then read the top ones for complexity.
* **Characterization test:** a test that pins what the code does now, its expected values taken from running the code.
* **Structure commit:** a commit that holds only refactorings. A **behaviour commit** holds only changes a caller can observe.

## Decide whether to refactor

Refactor when one of these holds:

* **Preparatory:** a change you are about to make is awkward in the current shape. Make the change easy, then make the easy change.
* **Comprehension:** you had to trace the code to understand it. Put that understanding into names and structure.
* **Rule of three:** a rule, a schema or a constant is copied a third time, and the copies change for the same reason.
* **Hotspot:** the user asks where to clean up, or a scheduled run starts this skill. Rank by change frequency first.

Leave it alone when:

* **No change touches it.**
* **It is due for deletion,** or a rewrite of it is already agreed.
* **The duplication is coincidental:** the copies serve rules that change for different reasons. An extraction that needs a flag or mode argument to serve its callers is the wrong abstraction.
* **Length is the only complaint:** keep a long function that reads top to bottom at one level of abstraction. Split only where each piece has a simple interface and reads without the others.

When the user asks whether code should be refactored, answer in this order: what is good and stays, each smell with the lines that show it and the refactoring that cures it, when to do each (now, when a named change next touches it, or never), and what not to do.

## Find the smells

Look first for these, the costliest to leave:

* **Shotgun Surgery or Scattered Cleanup:** one concept changed in many places, or one resource opened in one function and closed in several others.
* **Hidden Side Effect:** a function that does something its name does not say, such as a builder that closes another object.
* **Duplicated Code:** the same rule or constant written twice.
* **Middle Man:** a function or class that only forwards its arguments to another.
* **Speculative Generality:** a parameter, hook or interface with one implementation and no second caller.
* **Global Data:** shared mutable state written from several places.
* **Flag Argument:** a boolean that switches a function between two jobs.
* **Comments as deodorant:** a comment that explains an ordering or a workaround the structure could enforce. A comment that explains why stays.

The full catalogue, with how to see each smell and the named refactorings that cure it, is in [references/smells.md](references/smells.md). Name each smell and its refactoring by their catalogue names in your report and commit messages.

## Readability

* **Names:** full words, specific to the role (`unseen_articles`, not `data` or `ua`). Use the term `docs/glossary.md` gives a concept when it gives one.
* **One meaning per line:** no assignment or increment used as a value, no `&&` or `or` used as control flow, braces on every block, one role per variable, explicit conditions (`if count != 0`, not `if count` when `count` is a number).
* **Guard clauses** in place of nested conditionals.
* **Deep modules:** a small interface that hides a lot.
* **Comments:** state only what the code cannot show: why, units, invariants, ordering constraints. Delete a comment that repeats the code, and keep each explanation in one place.
* **Metrics:** complexity and readability scores are hints, never gates. Judge by whether a reader can predict what the code does without jumping elsewhere.

## Refactor safely

* **Green first:** run the tests before the first step. Code the refactoring touches that no test covers gets characterization tests first, committed alone.
  * **Prove each one can fail:** break the code it pins once, such as by flipping a branch or changing a returned value, see the test go red, and revert.
* **Two hats:** never change behaviour in a refactoring step. Note a bug found mid-refactoring, finish or revert the step, then fix the bug in its own commit by the `bug` skill.
* **Small named steps:** apply one named refactoring, run the tests, commit. On a red test, revert the step; do not debug forward.
* **Tools first:** use the language server's or IDE's rename, extract and move where one is available.
* **Keep what callers rely on:** public names and signatures (migrate them by parallel change), error handling, assertions, logging, and comments that explain why. Before each commit, read the diff for deleted lines and justify each one.
* **Thin tests:** where tests are thin, run the old and new code on the same inputs and compare the outputs.
* **Scope:** touch only the files the change needs. Add no abstraction with one implementation and no config with one value.
* **Commits:** each structure commit alone, never mixed with a behaviour change, its message naming the refactoring, such as `refactor: inline _classify_articles (Middle Man)`.

## Large refactorings

A change that cannot be one commit on main (an interface with many callers, a dependency swap, a subsystem replacement, unknown prerequisites): [references/large.md](references/large.md).

## Scheduled run

A scheduled run (a Claude Code routine or a CI cron job) follows [references/scheduled-run.md](references/scheduled-run.md): it proposes one refactoring as an issue and changes no code.

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
