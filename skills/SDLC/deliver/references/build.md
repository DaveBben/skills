# Build prompt

Issue one instruction per story, filled from what the setup subagent returned.

```text
CONTRACT
<the accepted test files and the red commit's hash, or only the test paths when the
user declined red commits. Read them; they do not change.>

IMPLEMENT
Only what makes the accepted rows pass. Commit after each row goes green; the
message is the row's title.
When a choice no row fixes changes what a person sees (wording, a default, an
error message, the order of a list), commit what is green, then stop and return
the question with the alternatives.
List every other choice made between alternatives no row fixed: what, why, the
tradeoff.
Do NOT add: config with one value, an interface with one implementation, a
parameter only ever passed its default, retry, backoff, caching, a feature flag
no row names, error handling for cases no test names, logging nobody reads,
a class where a function does, a comment that restates the code.
If a row cannot be satisfied as written, stop and report the row and why.
Never change a row, the user's own test under the feature-acceptance directory, or a file outside <paths>.

REUSE
Before writing a helper, a type, a fixture or a client, grep this repository for
one that exists, and report every match.

NON-NEGOTIABLE
<pinned addresses, limits, frozen files and slow query shapes, each from the
code with file:line>
<the module this story's code lives in and the flows it may call, from the
latest snapshot AGENTS.md points at>
<one line per ADR on this module: Rejected: <alternative>, because <reason>.>

EDGE CASES
Test behaviour, not implementation. List every test added beyond the table, why,
and its Killed by.
```
