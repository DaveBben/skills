# Implementing an experiment

Contents: before building, testing the instrument, writing the analysis first, running, performance benchmarks, provenance, pilot, checking transcripts by hand, and reporting.

Implementing means building the harness, running the pilot and the experiment, and producing the results from a committed design.
Most failures at this stage come from a measurement instrument that is silently wrong, or from a decision made after seeing data.
The design document is the specification.
When the harness and the design disagree, change the design in its own commit with the reason, and do it before the pilot.

## Before building

* **Freeze the design:** commit the design document and tag it, such as `design-v1`, before writing the harness.
* **Settle open decisions:** the pilot cannot start while the design's open-decisions list has entries.
* **Draw by script:** every random draw runs from a committed script with a seed committed before it runs.
  The script prints its selection, and the selection is committed too.

## Testing the instrument

The instrument is everything that turns a run into a number: the scorer, the test runner, the mutation tool, and the analysis script.
Test it on inputs whose answers are known before trusting any score it gives.

* **Known extremes:** an empty output scores the minimum, and a reference output scores the maximum the design expects.
* **Planted faults:** a deliberately wrong item is caught by the guard measure.
  An example is a test that fails on the reference implementation, which must be marked invalid.
* **Reference sanity:** a published reference result lands in a plausible range.
  An example is a benchmark's own tests killing a sensible share of mutants.
* **Determinism:** scoring the same output twice gives the same number.
  When it does not, find the source before the pilot.
* **Flaky items:** any check that can pass and fail on the same input is unreliable.
  Run each check several times on the reference.
  Treat any check whose result changes as invalid, and record how many were flaky.
  Tests that depend on time, randomness, ordering, or the network are the usual cause.
* **A/A run:** during the pilot, run the control arm in the treatment arm's place for a few units, through the same harness path, assignment, and scorer.
  Pre-set a tolerance from the pilot's run-to-run spread.
  A mean difference outside it means the harness, the assignment, or the scorer favours 1 arm position, such as running first.
  The A/A run checks the harness only: it estimates no effect and does not change the decision rule.

## Writing the analysis first

Write the analysis script before experiment data exists, and test it on pilot or synthetic data.
Lock it with a commit.
Where practical, have it label the arms with neutral codes, such as X and Y, until the results are final, so no one tunes the analysis toward an arm.

## Running

* **No peeking:** do not look at the primary result until the run is complete.
  Stopping early, or adjusting, once a result looks good inflates false positives.
* **Monitor only operations:** watch failures, cost, throughput, and completeness during the run.
* **Completeness:** check that every planned unit has every arm for every run.
  A gap or an imbalance between arms means the harness or the logging is broken, and the result is not trusted until it is explained.
  This is the equivalent of the sample ratio check in an A/B test.
* **Failure types:** decide in advance how each failure is handled.
  An infrastructure failure, such as an API error, a timeout of the harness, or a crashed container, is rerun.
  A scientific failure, such as an agent producing poor output, is data and is kept.
  Log every rerun with its reason.
* **Budget:** set a hard stop on spend and compute, estimated from the pilot's cost per session and per scoring run.

## Performance benchmarks

These apply when the primary measure is time, throughput, or resource use:

* **Warm-up:** pre-set how steady state is detected, such as JIT compilation finished and caches filled, and discard the iterations before it.
  When cold start is what matters, measure it as its own measure.
* **Stable machine:** fix CPU frequency scaling and turbo where the host allows, and stop background jobs.
  Record the hardware, kernel, and runtime versions in the manifest.
* **Interleaved arms:** run the arms in randomized order within each pair of runs, or in ABBA blocks, never all of 1 arm then all of the other.
  Thermal throttling, noisy neighbours on a shared cloud host, and drift then hit both arms.
* **Microbenchmarks:** use a benchmark harness, such as JMH, pyperf, or Criterion.
  It handles warm-up and stops the compiler from removing code whose result is never used.
* **Open-loop load:** send requests at a fixed rate that does not wait for responses.
  A load generator that waits for each response sends fewer requests while the system is slow, so the slow period barely appears in the results.
  This is called **coordinated omission**.
* **Percentiles:** report latency as percentiles, such as p50, p95, and p99, with a plot of the full distribution, because a mean hides the tail.
  Pre-specify which percentile is the primary measure, compute it per run, and bootstrap its confidence interval over runs.

## Provenance

* **Manifest per run:** each run writes the harness commit, the image digest, the model ID or weights revision, the seed, timestamps, and token counts.
* **Append-only outputs:** raw outputs are never overwritten.
  Record a content hash for each one.
* **Rerunnable results:** 1 command recomputes every reported number from the raw outputs.
  Run that command inside a pinned environment too.

## Pilot

The pilot tests the harness and supplies variance estimates.
Its effect is never analysed.

1. Run the pilot exactly as the design specifies.
2. Fix every harness bug it finds, and log each fix.
3. Set the sizes that the design fixes after the pilot, such as the unit count and the run count, by its pre-set rules, and commit them.
4. Tag the harness version, such as `harness-v1`, and keep it unchanged for the main run.

Pilot data is never mixed into the experiment's results.

## Checking transcripts by hand

Read a random sample of transcripts per arm, with the sample size and seed fixed in advance.
Look for anomalies that scripts miss, such as reading forbidden files, misreading the prompt, or a harness error the agent worked around.
Log what you find, and report it.

## Reporting

* **Surprises checked first:** treat an effect far outside what prior work or the A/A run makes plausible, in either direction, as a harness bug until a check rules that out.
  Read the transcripts or raw outputs behind the largest wins and the largest losses before reporting, and log every check and its result.
* **Everything pre-specified:** report every pre-specified analysis, including null and inconclusive results.
* **Results separate from interpretation:** keep the results section free of speculation.
* **Deviations:** include the deviation log, with the effect of each deviation on the result.
* **Raw data:** publish the raw outputs, the scripts, and the per-run scores, so others can check the numbers.
