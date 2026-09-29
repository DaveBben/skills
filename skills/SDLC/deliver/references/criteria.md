# Story setup: criteria, test table and red commit

The setup subagent follows this file in the story's worktree. It gets the story's issue key, the feature header's `Outcome:`, `Not doing:`, `Constraints:`, `Context:` and `Decided:` lines, the worktree path, and `AGENTS.md`. It talks to nobody: every question goes back in its return.

Before writing, search the epic's comments for `Learned`, `Observed` and `Not caught by` lines, fetch the requirements document the epic links, when it links one, and read each ADR (decision record) on `Decided:` by its title, `Decision:` and `Detector:` lines, opening one in full only when its Decision names what this story touches. When the story spans repositories, read each one's `AGENTS.md`, else its `CLAUDE.md`, and keep its rules.

## 1. The card

```text
<Title: what the person will be able to do, five to eight words>
Outcome:  <what a person observes once this story is done>
Why:      <what stays broken for them without it>
Scope:    <what this story covers, and what it leaves to which other story>
Criteria:
  a. Given <a concrete starting state>, when <a concrete action>, then <what the person sees, with real values>
  b. <a boundary, a failure path or an abuse path, same form>
Open:     <each undecided value, who decides it, and which criterion waits on it; "none">
Interpreted: <each input this story adds and what interprets it as instructions: a query, a shell, a template, a parser; omit when none>
```

A criterion records a product choice when it holds a number, a rule a person could argue with, or what happens at a boundary the requirements leave open, or when it touches a data shape, a trust boundary, an interface another team calls, a value a person sees, personal or health data, or a record lost or half stored.

## 2. Write the criteria

* **Write in what the observer sees.** A person sees a screen, a message, a file. A service sees status codes, the error code in the body and the response shape; add what a repeated identical request returns and what a field of the wrong type returns.
* **Criterion a is the outcome,** or for a bug the reproduction: the starting state, the action, and what the person should see instead.
* **Use concrete values and a number in every limit.** Never write improve, better, faster, seamless, robust, correct, properly, handled, intuitive, flexible, scalable or modern; write the number or the event. A limit with no number is marked not testable.
* **One outcome per criterion,** from the observer's side, naming the interface, in the nouns the code and `AGENTS.md` already use.
* **Walk the failure paths** and give each that can happen a criterion or a line in `Not doing`: empty or malformed input; input past a limit; the same action twice; two at the same moment; a half-completed action and what clears it; a dependency down; a step with no time limit; the person abandoning the flow.
* **Walk the abuse paths:** acting as another person, bulk repetition, a response revealing a third party, sending to an address the requester chose, personal data entering the system. Each that matters gets a criterion with a number in it.
* **Fold in what constrains the story:** each header constraint this story could break, a rate limit or pagination, an enabler such as a new column, a flag when the story ships half a behaviour, and the contract of an interface this story defines.
* **Keep standards out.** A criterion is something a reasonable person could choose against and the user would notice. Anything else is an engineering standard: list its inputs on `Interpreted` and write no criterion.
* **Never settle an open value.** Mark it on `Open`, write its question in the return, and never guess it into a criterion or a test.

Ready when every criterion names what a person sees in checkable values, every failure and abuse path has a criterion or a non-goal, the story leaves a person able to do something new, and its product-choice criteria are within the limit `AGENTS.md` states, else 8. More than one step or variation, or over the limit, is several stories: say so, propose the split, and stop before the red commit.

## 3. The test table

One index table, then one block per row. Keep index cells under forty characters.

```text
| # | Test | Level | Generator | Killed by |
|---|---|---|---|---|
| 1 | <what the person can do> | Acceptance | Requirement | <the one-line change, or observable change, that turns it red> |

**1. <title>**
**Given** <a concrete state>  **When** <an action>  **Then** <what the person sees>
**Prevents** <the failure a person would see>
```

Generate rows in this order; a generator with nothing to fire on adds none.

* **Requirement:** one acceptance row per criterion, through the interface the person uses: a browser test for a screen, a request to a running service for an API, the command for a CLI. It is never cut.
* **Seam:** one row per boundary crossed (a database, a queue, a third-party API), pinned against a recorded exchange where the real one is unreachable.
* **Type:** for each field touched, empty, null, zero, negative, the delimiter, each enum value, and the wrong type for data written outside this system.
* **Cardinality:** zero, one and many for each collection, page or retry.
* **Both sides:** a negative test from the attacker's seat for each authorisation check.
* **Invariant:** a round trip, ordering or conservation law becomes one property test.
* **Budget:** each number in `AGENTS.md` or the header this story touches, asserted.

Cut a row that asserts a private function, call order, a log line or an unstated order; one that only fails when another does; and one that prevents nothing a person would see. A row already green on the current code stays only when it is a Requirement row; mark it `characterizes existing behaviour`. A row that exposes a product decision nothing records goes back as a question, and stays out of the red commit.

## 4. Before the red commit

* **Pin untested code** this story changes with characterization tests, committed first.
* **Add a seam** where the code offers no point to test through, as its own commit, with the suite green before and after.
* **Do each open `Proposed refactor`** this story touches as its own commit, suite green before and after.
* **A bug's table is two rows:** the failing test at the level of the report, then a unit test isolating the fault. A review finding handed back is a bug's table on this story. Grep every caller of the function about to change.

## 5. Red

Write every row as a failing test, the acceptance tests first, new rows in new files. Run them: a row not marked `characterizes existing behaviour` that passes, or fails for a reason other than the missing behaviour, means the story's assumption is wrong; report it. Delete or rewrite existing tests that assert behaviour this story removes, in the same commit. Add stubs whose only body raises where the tests name symbols that do not exist.

Commit the tests and stubs alone with the red-commit command `AGENTS.md` records (with pre-commit, `SKIP=tests,e2e git commit`; with none, `git commit`, and when a hook refuses the failing tests, skip that hook alone by its id and return the command for `AGENTS.md`), with the criteria, the index table and each row's failure line in the message. Then run [story.sh](../scripts/story.sh) `red` in the worktree. Never skip the whole gate.

## Return

```text
Criteria: <letter> <criterion in the user's words> [product choice]   (one line each)
Card: <path of card.md in the worktree's git directory, holding the card text>
Paths: <the source paths the story may change>
Red: <hash per repository>; tests: <paths>; red rows: <n>, green rows: <n>
Non-negotiable: <pinned values, limits and frozen files from the code, with file:line; one "Rejected: <alternative>, because <reason>." per ADR on this module>
Assumes: <each fact read from a document, and how it was checked>
Questions: <each open value or product decision, one line>
Split: <proposed stories, only when the story is several>
```
