---
name: code-practice
description: "Use this skill when the user wants to practice writing code by hand, above all by re-implementing a change that is already merged, and wants it critiqued. Use it on: 'I want to practice coding', 'let me re-implement PR 9 myself', 'practice on this merge request', 'I want to make sure I still remember how to code', 'give me a coding drill', 'redo this commit by hand', 'what should I practice next'. Load it before reading the change. Branches from before the change, has the user write the interface and implementation while the agent supplies failing tests and graded hints but no implementation code, then critiques the user's design, data structures, time and memory complexity against the merged version, and logs what to redo. Not for explaining a concept with no code to write; that is teach-like-stackoverflow."
license: MIT
compatibility: Needs git and code execution in the user's repository.
metadata:
  version: "0.1.0"
---
# Code practice

The user re-implements part of a change that is already merged, to keep and grow their own coding skill.
You branch from before the change, bring in the rest of it, and supply the failing tests.
The user writes the interface and the implementation.
You give hints but never the implementation, then critique what they wrote as a senior engineer would.

Writing the code from memory is what builds the skill, so every rule below protects the user's attempt.
In a 2026 Anthropic trial, developers who delegated code to an AI scored lowest on a later quiz.
Developers who asked the AI only conceptual questions and wrote the code themselves scored highest.

## Choosing the slice

* **Read the log first:** when the practice log exists, offer any redo that is due, and prefer slices that exercise past weak points.
* **Find the change:** the user names a merged pull request, merge request, or commit.
  Read its description, linked issue, acceptance criteria, and diff.
  The **base** is the commit before it: the merge commit's first parent, or the parent of a squash commit.
* **Pick one slice:** a slice is one part of the change that holds real logic, such as a loop with a cap, a parser with validation, or a new query.
  Offer the slice most worth practicing and say why.
  The whole change is a slice too, when the user asks for it.
  Data files, docs, generated code, and config are never the slice.
* **Keep the answer hidden:** describe the slice by its behaviour and acceptance criteria.
  Do not show the merged implementation of the slice until the critique.

## The practice branch

Create a branch at the base, named `practice/<number>-<slice>`, and check it out.
When the working tree has uncommitted changes, ask the user before switching.
Commit to the practice branch locally as the session goes, so the user's work has a clean diff.
Never push it or open a pull request from it.

## Interface

On the practice branch, the user writes the slice's interface: its function signatures, types, and constants, with stub bodies.
Compare it with the merged interface.
Name each difference, say which is better and why, and let the user choose which to build against.

Then the user lists the test cases they would write, one line each.
Compare the list with the cases the merged tests cover, and name the cases each side missed.
The user does not write the tests.

## Setting up the implementation

* **Bring in the rest of the change:** copy from the merged commit every part of the change outside the slice, such as data files, config, and code the slice depends on.
  Only the slice's implementation stays missing.
* **Fit the tests:** use the merged tests.
  When the user chose their own interface, adapt the tests and the code that calls the slice to it.
  Add a test for each case the user listed that the merged tests miss.
* **Check the red:** run the tests and confirm each fails on the stub, not on an import or setup error.
  When a test needs a service, such as a database, use the repository's own test setup, and tell the user which tests cannot run here.
* **Commit the setup** so the user's implementation is the only change after it.

## While the user writes

You never write or edit the slice's implementation.
Answer conceptual questions fully and directly, such as how a heap works or what a library call returns, because those are the questions that build skill.
Answer them without writing the slice's code.

When the user asks for help with the slice, give the lowest hint that unblocks them, one level at a time:

1. **A question** that points at the gap, such as "what should happen to the next item once the cap is reached?"
2. **The place:** the file, function, or existing helper to look at.
3. **The idea** in words or pseudocode.
4. **Code for one step,** only when the user asks for code outright.

When a test fails, let the user read the failure.
When asked, explain what the failure means, not what to change.
When the user asks for the answer, ask whether to end the attempt, and on yes go to the critique and log the slice as unfinished.

## Critique

Critique when the tests pass or the user ends the attempt.
Read the user's diff against the base and the merged diff.
Write for an engineer who wants to improve, and rank the points by how much each would improve their code beyond this slice.

Cover every area below.
Give an area with no issue one line saying so.

* **Correctness beyond the tests:** inputs the tests miss that break the user's code.
  Give each input and the wrong result, from a run.
* **Data structures:** whether each collection fits the operations done on it.
  Examples are a list scanned for membership where a set gives O(1), a full sort where a heap gives the top k, or a dict rebuilt inside a loop.
* **Time complexity:** the Big-O of the user's code and the merged code, in named inputs, such as O(n·k) for n candidates and k slots, with the line that sets it.
  State the real input sizes, read from the code or the data, and whether the difference matters at those sizes.
* **Memory:** extra space as Big-O, and any copy, intermediate list, or whole-file read that a generator, view, or in-place update would avoid.
* **Design and patterns:** whether a pattern the user used or missed fits here, such as a guard clause, a pure function split from I/O, or a lookup table instead of branches.
  Name over-engineering as readily as missing structure, and name any helper already in the repository that the user re-implemented.
* **Better approach:** when one exists, show it as a short snippet, say why it is better and when that matters, and name its cost.

Compare the user's version with the merged version on each point, and say plainly where the user's is better.
When a speed or memory difference matters at real sizes, measure both versions with a short benchmark and report the numbers.
Praise only what is specifically good, with the reason.
End with the one habit to work on next.

## Debugging drill

After the critique, offer one drill.
Plant one bug in a copy of the merged slice, of a kind the critique or the user's stuck points suggest, such as a wrong boundary or a budget shared incorrectly between two loops.
Tell the user only the symptom: the failing test, or for a bug the tests miss, the wrong output.
The user finds the bug and explains it before you confirm.

## Practice log

Append one entry to `~/.code-practice/log.md`, unless the user names another file.
Record the date, the repository, the change, the slice, the hints used at each level, where the user got stuck, the critique's top points, and a redo date 2 to 3 weeks out.
Ask before deleting the practice branch, because it holds the user's code.
