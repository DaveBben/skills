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

NON-NEGOTIABLE
<environment facts a model cannot infer and will improve into something wrong:
pinned addresses, concurrency limits, byte-frozen files, query shapes measured
as slow>
Do not modify anything outside <directory>.

EDGE CASES
<the accepted table's Type and Cardinality rows, already failing>
Test behaviour, not implementation. No assertion on a private function, on
internal call order, or on a log line.
List any test you added that is not in the table, and say why.
```

* **Name specifics in the prohibition list.** "Keep it simple" produces nothing. Extend the list as the model's defaults become apparent.
* **Keep the last line.** Unasked-for tests are often the best in the suite. Requesting them separately means they get read rather than skimmed.
* **Pin load-bearing files with a hash test.** A request is advice; a test is a fact.
