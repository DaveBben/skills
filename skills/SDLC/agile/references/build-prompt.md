# Build Prompt

Issue one instruction per slice. The accepted rows already exist as failing tests.

```text
CONTRACT
<the accepted acceptance test, verbatim. Does not change.>

IMPLEMENT
Only what makes the contract test pass.
Commit after each row goes green; the message is the row's Test cell.
Do NOT add: config with one value, an interface with one implementation, a
parameter only ever passed its default, retry, backoff, caching, feature
flags, error handling for cases no test names, logging no one asked to read,
a class where a function does, docstrings describing future extensions.
If something above is genuinely required to pass the test, say so and stop.

REUSE
Before writing a helper, a type, a fixture or a client, grep this directory
and its siblings for one that exists, and report what you found. A second
way to do what the codebase already does is a finding, not a feature.

NON-NEGOTIABLE
<environment facts a model cannot infer and will improve into something wrong:
pinned addresses, concurrency limits, byte-frozen files, query shapes measured
as slow. Every value from the code, with its file and line, never from a spec
or README; where the two disagree, say so>
<the architecture's name where the root instructions file records one, and the
layer this slice's code lives in: two facts, no description>
Do not modify anything outside <paths>.

KEEP FOR THE USER
Leave <function> unwritten: its signature, a one-line contract, and a body
that only raises. Make every other row green; the acceptance row stays red
until the user writes this body. Name the function in your report.

EDGE CASES
<the accepted table's Type and Cardinality rows, already failing>
Test behaviour, not implementation. No assertion on a private function, on
internal call order, or on a log line.
List any test you added that is not in the table, why, and its Killed by.
```

* **Name specifics in the prohibition list,** never "keep it simple". Extend the list as the model's defaults become apparent.
* **Name the search, not only the prohibition.** Tell the builder to grep first and report what it found.
* **Keep the last line,** so an unasked-for test is listed and read rather than skimmed.
* **Pin load-bearing files with a hash test,** not with a request in the prompt.
