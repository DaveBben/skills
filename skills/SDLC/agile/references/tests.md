# Choosing the tests

Load this twice: when building the constraint-to-test manifest, and again before writing the first failing test of a slice.

## Which kind

The constraint decides the kind, so name it on the manifest row rather than leaving it to whoever writes the test. A row usually carries one.

- **Example-based** is the default, and covers everything not named below.
- **Property-based** wherever you can name an invariant that holds across every input: a round trip, an ordering, a bound that never moves, a total that always reconciles. Add an example beside it only for a case you want named in the suite that the property does not already cover.
- **Fuzzing** where untrusted input crosses a boundary flagged in triage.
- **An integration test at every seam this change crosses.** Not conditional on anything. A seam here is an external dependency the change talks to and does not control: a database, a queue, the filesystem, another team's service. It is not the internal seam you create by extracting an interface. Each one becomes a manifest row of its own with origin "created by the shape". A mock that agrees with itself is what lets a field-name mismatch reach production. Where the real dependency cannot be reached from a test, say so on the row and pin the contract against a recorded exchange instead.
- **One end-to-end test** for the change as a whole, through the door a real user comes in, as its own manifest row. A change small enough to be a single slice does not need one.
- **A budget assertion** on any hot path carrying a number.

The kinds are independent rather than escalating, so do not stop at the first that fits, and do not provision speculatively. Write one line where a kind does not apply. All of them assert observable behaviour, never internals.

## Then cut

Over-testing is the default failure here, and every test is something that has to keep passing while the design changes.

A row earns a test because a constraint or an acceptance criterion needs discharging, not because a function exists. Do not test the language, the framework, or a library doing what its documentation says. Do not write a second test that fails only when the first one already has. Do not add a heavier kind than the row needs: a property test on a lookup table and an integration test on a pure function are both cost with no return.

For each row, and for each failure path detector, say what user-visible bug or incident it would catch. Where the answer is nothing, it does not become a test: disposition the row `no test` with that as the reason, or, where the whole area is structurally irrelevant to this change, drop the area and name it under Not applicable in the design doc. Nothing leaves the manifest by any other route.
