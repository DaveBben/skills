# Build Prompt

Issue one instruction per story.

```text
CONTRACT
<every acceptance test of the story, verbatim. They do not change.>

IMPLEMENT
Only what makes the accepted rows pass.
Commit after each row goes green; the message is the row's Test cell.
List every choice made between alternatives no row fixed: what was chosen,
why, the tradeoff.
Do NOT add: config with one value, an interface with one implementation, a
parameter only ever passed its default, retry, backoff, caching,
error handling for cases no test names, logging no one asked to read,
a class where a function does, docstrings describing future extensions,
a feature flag no row names.
If something above is genuinely required to pass the test, say so and stop.
If a row cannot be satisfied as written, because it asserts through a seam that
does not exist or holds an impossible value, stop and report the row and why.
Never change the row.

REUSE
Before writing a helper, a type, a fixture or a client, grep this directory
and its siblings for one that exists, and report every match. A second
way to do what the codebase already does is a finding, not a feature.

NON-NEGOTIABLE
<environment facts a model cannot infer and will improve into something wrong:
pinned addresses, concurrency limits, byte-frozen files, query shapes measured
as slow. Every value from the code, with its file and line, never from a spec
or README; where the two disagree, say so>
<from the module map in `AGENTS.md`, or in the chat before the first story writes it there: the module this story's code lives in, its pattern where one is set, and the modules it may depend on;
three facts, no description>
Do not modify anything outside <paths>.

EDGE CASES
<every other accepted row, already failing>
Test behaviour, not implementation. No assertion on a private function, on
internal call order, or on a log line.
List every added test that is not in the table, why it was added, and its Killed by.
```

* **Name specifics in the prohibition list,** never "keep it simple". Extend the list as the model's defaults become apparent.
* **Pin load-bearing files with a hash test,** not with a request in the prompt.
