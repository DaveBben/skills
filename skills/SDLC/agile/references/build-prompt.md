# Build Prompt

Issue one instruction per slice. Implementation and unit tests arrive in the same turn. Tests written after the code are derived from it, pass by construction, and pin its accidents.

```text
CONTRACT
<the accepted acceptance test, verbatim. Does not change.>

IMPLEMENT
Only what makes the contract test pass.
Do NOT add: config options, feature flags, retry or backoff, a logging
framework, abstract classes or interfaces, plugin points, CLI flags, caching,
error handling for cases not in the accepted table, docstrings describing
future extensions, a class where a function does.
If something above is genuinely required to pass the test, say so and stop.

NON-NEGOTIABLE
<environment facts a model cannot infer and will improve into something wrong:
pinned addresses, concurrency limits, byte-frozen files, query shapes measured
as slow>
Do not modify anything outside <directory>.

EDGE CASES
<the accepted table's Type and Cardinality rows>
Test behaviour, not implementation. No assertion on a private function, on
internal call order, or on a log line.
List anything you tested that is not in the table, and say why.
```

* **Name specifics in the prohibition list.** "Keep it simple" produces nothing. Extend the list as the model's defaults become apparent.
* **Keep the last line.** Unasked-for tests are often the best in the suite. Requesting them separately means they get read rather than skimmed.
* **Pin load-bearing files with a hash test.** A request is advice; a test is a fact.
