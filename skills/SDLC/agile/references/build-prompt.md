# Build Prompt

Issue one instruction per slice. The accepted rows already exist as failing tests. The builder makes them pass and may add tests for cases the table missed, in the same turn as the implementation. It never rewrites an accepted row.

```text
CONTRACT
<the accepted acceptance test, verbatim. Does not change.>

IMPLEMENT
Only what makes the contract test pass.
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
as slow>
<the architecture's name where the root instructions file records one, and the
layer this slice's code lives in: two facts, no description>
Do not modify anything outside <directory>.

EDGE CASES
<the accepted table's Type and Cardinality rows, already failing>
Test behaviour, not implementation. No assertion on a private function, on
internal call order, or on a log line.
List any test you added that is not in the table, and say why.
```

* **Name specifics in the prohibition list.** "Keep it simple" produces nothing. Extend the list as the model's defaults become apparent.
* **Name the search, not only the prohibition.** A model told not to duplicate still duplicates; a model told to grep first reports what it found.
* **Keep the last line.** Unasked-for tests are often the best in the suite. Requesting them separately means they get read rather than skimmed.
* **Pin load-bearing files with a hash test.** A request is advice; a test is a fact.
