# Review a story the agent built

The review subagent follows this file on the story branch. It gets the story's card (criteria and `Interpreted` line), the interface each criterion names, the branch, the red commit's hash, the check command, the story's permitted paths and the feature header's `Decided:` line, and nothing from the chat. Run the steps in order and never merge them. The Done block keeps its fixed format over any writing rule.

## 1. Attack first

Before reading the test table, the builder's choices or the build commits, work from the criteria and the interfaces alone: a second reader with the builder's inputs repeats the builder's blind spots.

Write each attack as a test in the project's framework, through the interface a criterion names, under `attack/` in the worktree's git directory (`git rev-parse --git-dir`). Try the boundary values each number implies, empty and oversized input, the same request twice and at once, a caller who is not who the criterion assumes, a number arriving as a string, and a dependency that is down or slow. Take each expected value from the criterion's words. Run them on the built code and keep only the red ones, after checking each red one is not the test's own mistake. A red attack on a stated criterion is a blocking finding. A red attack on behaviour no criterion states (a timeout, what a repeat returns, an error's wording) is a question for the user.

## 2. Correctness

* **Mutate.** Run the mutation runner over the changed files where there is one. Otherwise apply each row's `Killed by` from the red commit message by hand, one at a time, and confirm that row goes red. A row that stays green asserts nothing: fix the test. List any surviving mutant that cannot change behaviour, with its reason.
* **Diff the accepted tests** against the red commit. Any change is a finding. Never edit the `feature-acceptance` directory.
* **Delete tests of incidental detail:** a private function, internal call order, a log line.

## 3. Subtraction

Delete what no row asked for: config with one value, an interface with one implementation, a parameter only ever passed its default, unrequested retry, caching or flags, error handling for cases no test names, logging nobody reads, a class where a function does, a comment that restates the code, commented-out code. When it is unclear whether something is load-bearing, delete it and run the suite; green means a missing test.

## 4. Scars

Pinned addresses, ports, limits and frozen files are unchanged. No new name collides with one at the merge target (grep it). Nothing changed outside the permitted paths.

## 5. Design

Read the latest snapshot `AGENTS.md` points at and the Decision line of each ADR on the header's `Decided:` line. List each departure: a module doing what another owns, an import the import rule forbids, a process, store or flow the snapshot lacks, a choice a decision rejected, a second copy of a helper or type that exists. Say whether this branch records it in a new snapshot or ADR.

## 6. Security

For each place the diff takes data from outside the code's control (a route, an argument, a file, a queue message, a third-party response, rows another system writes), check: its type, size and range are checked at the entry; the sink has its standard defence (a parameterized query, an argument array, template escaping, a strict deserializer); the server checks who the caller is and what it may do; sensitive data goes only where `AGENTS.md` allows and never into a log, an error or a response; no secret is written, logged or returned; an entry others reach has a size, rate or time limit; an outbound request follows no redirect to another host with credentials attached, and sends to allowed hosts only; a failure leaves no half-written record another caller sees. Each sink on the card's `Interpreted` line gets its standard defence. A path from outside to a sink without its defence, a credential sent to a host it was not issued for, or an entry with no authentication or authorization, is blocking. Read what the dependency audit and secret scan reported instead of redoing them.

## 7. Refactor while green

Rename to the domain's terms, split a function whose name needs "and", and remove duplicated knowledge this story created, committing before and after with the suite green. A refactor outside the diff goes on `Proposed refactor:` instead. Re-run the accepted-test diff after it.

## Done

Write the block to `done-block.md` in the worktree's git directory, and return only whether the review is done and the number of blocking findings. Each finding with a failure behind it is one `Findings:` row: `<file>:<line> — <what breaks> — case: <input, sequence or caller> — blocking | non-blocking`.

```text
DONE
Attack:      <n> tests; <n> red; one line per red test: criterion, what the person would see
Correctness: <runner or by hand>; per row: the mutation, red or survived; accepted tests unchanged since <red commit>, or the diff
Subtraction: <what was deleted, or "nothing">
Scars:       <each pinned value checked, or "none pinned">
Design:      <one row per departure and whether this branch records it; or "follows <snapshot>", or "no snapshot">
Security:    <one line per entry checked, or "no outside input">
Refactor:    <renames and merges, or "none">
Proposed refactor: <files and the duplication it removes, or "none">
Decided alone: <the build's choices, then the review's own: what, why, the tradeoff>
Gate:        <the check command and its result>
Criteria:    <per criterion: a few words, the exact test name, passed as seen in this run>
Changed:     <one line per new function, module or branch: what it is for and its file>
Findings:    <rows as above, or "none">
Questions:   <red attacks on behaviour no criterion states, or "none">
```

A surviving mutant neither fixed nor explained, or a check command that errors instead of passing or failing, means the block is not written: report the command, its exit status and its output, and stop.
