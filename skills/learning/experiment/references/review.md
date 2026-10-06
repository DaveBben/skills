# Reviewing an experiment

Contents: choosing the standards, checklist, gaps that recur, and reporting.

Read the whole design before judging any part, because a gap in one section is often closed in another.
Report findings and do not edit the design until the user asks.
The exception is reviewing your own draft while creating one: fix each gap that needs no choice from the user.
When the design uses this skill's outline, run `scripts/check_design.py` on it first and report each failure as an essential gap.
When a fix needs the user's choice, such as adding an arm or accepting a confound, ask with the options instead of picking one.

## Choosing the standards

These are the ACM SIGSOFT Empirical Standards and related guidelines:

* **General standard:** applies to every study.
* **Experiments standard:** written for experiments with human participants, but its method items fit any controlled experiment.
  When there are no human participants, skip the participant and incentive items and say so.
* **Benchmarking standard:** applies when the objects come from a benchmark or the measure is performance on one.
* **Engineering Research standard:** applies only when the study proposes and evaluates a new artifact, such as a tool, method, or algorithm.
  It sends evaluations of existing approaches back to the Experiments standard, so state which framing the design takes.
* **LLM guidelines:** apply when a model or agent is involved, as listed in [llm-experiments.md](llm-experiments.md).

Items about results and discussion cannot be checked on a design that has no data yet.
Mark them not yet applicable, and check that the design plans for them.

## Checklist

### Essential items

* **Hypotheses:** formal hypotheses.
  Sidedness is consistent across H0, the test, the confidence interval, and the power analysis.
  A one-sided test needs a justification.
* **Dependent variable:** described with its unit and instrument, and justified as a measure of the construct, with a citation.
* **Independent variable:** described, with how it is manipulated.
* **Extraneous variables:** listed, each controlled physically, statistically, or explicitly not at all.
* **Sample size:** justified by a power analysis at a stated smallest effect of interest.
  Repeated runs per unit are justified too.
* **Construct mapping:** how the real phenomenon maps onto the manipulation and the measure.
* **Design and protocol:** treatments, materials, tasks, the named design, allocation, sequence, and logistics.
* **Assignment:** random assignment with its mechanism, or a justification for not using it and how unequal groups or a fixed order is mitigated.
* **Objects:** described by size and type, with their selection justified and any object-treatment confound acknowledged.
* **Analysis:** described in detail.
  Tests match the design, such as a paired test for paired data, and are justified.
  Their assumptions are listed with how each is checked.
* **Effect sizes:** reported with confidence intervals.
* **Validity:** construct, internal, external, and conclusion validity are each discussed.
  Alternative interpretations of the result are given.
* **Methodology named:** the method is named and fits the question.
* **Terms defined:** jargon and abbreviations are defined.
* **Benchmark:** the benchmark choice is justified.
  The setup and workload are described in enough detail to replicate.
  Arms compete without artificial limits, and repetitions are enough to judge stability.
* **Artifact, Engineering Research only:** the artifact is described, its need justified, and its strengths and weaknesses discussed.
  State-of-the-art alternatives are compared, or the design argues that comparison is impractical.
  Assumptions are explicit and consistent, and notation is used consistently.

### Desirable items

* **Materials:** the full protocol, materials, raw data, and analysis scripts are supplied.
* **Hypothesis basis:** hypotheses are justified from prior studies and theory.
* **Alternative designs:** the design says which alternatives it considered and why it rejected them.
* **Plots:** the design plans plots of data distributions.
* **Statistics citations:** unusual statistical choices cite their source.
* **Deviations:** they are logged with their date, reason, and consequence.
* **Manipulation checks:** they are planned and reported.
* **Preregistration:** the design is committed or registered before data, ideally with a public timestamp.
* **Raters:** subjective coding uses more than 1 rater, with agreement reported.
* **Realism:** the design discusses how realistic the setup is and how sensitive the result is to that.
* **Theory and examples:** a theoretical basis and a running example are given.
  The evaluation uses an industry-relevant context, for Engineering Research.

### Antipatterns

* **Bad proxy:** the measure stands in for something it does not track.
* **Wrong analysis:** an independent-samples test is used on paired data.
* **Flat threats:** threats are listed without linking each to a check or to the results.
* **Underpowered study:** the sample is too small, with no power analysis.
* **HARKing:** hypothesizing after the results are known.
* **P-hacking:** only the significant tests are reported.
* **Aggregates only:** aggregated measurements are kept instead of raw results.
* **Tailored benchmark:** the benchmark is tailored to favour 1 arm.
* **Overreach:** conclusions overreach the limitations the design admits.

## Gaps that recur

Check each of these that applies to the design's kind, and name those that do not apply.
Report one as essential when it can change the direction of the result or the decision, and as desirable otherwise:

* **Threshold power trap:** the decision rule needs the observed effect to reach the SESOI, which passes only about half the time when the true effect equals the SESOI.
* **Pilot too small for its job:** σ estimated from 3 units is used as if it were reliable, or from 1 run per unit while the analysis averages several.
* **Unstated cap consequence:** the budget caps the sample below the power analysis, and the design still reads a null result as "no effect".
* **Size confound:** a volume, such as suite size or output length, inflates the primary measure on its own.
* **Bundled treatment:** the treatment arm differs in 2 ways, and the design attributes the effect to 1.
* **Leak path:** an artifact passed between arms carries part of the manipulation.
* **Fixed order with drift:** arm order is fixed, and unit order is not randomized, so drift over time lines up with units.
* **Contamination:** public benchmark items may be in a model's training data, and there is no fresh, unpublished check set.
* **No manipulation check:** nothing confirms the manipulation happened or stayed isolated.
* **No reference point:** there is no human or state-of-the-art result on the same measure.
* **Implicit assumptions:** assumptions are unstated, or planned post-pilot settings contradict a "no changes after the pilot" rule.
* **Seeds after the fact:** seeds are not committed before the draws that use them.
* **Flaky instrument:** a measure built on test outcomes never reruns the tests, so a test that fails at random counts as catching faults.
* **No concurrent control:** the comparison is before and after a change, so every other change made over that period is mixed into the effect.
* **Regression to the mean:** units chosen for an extreme score are compared with their own earlier score, with no control drawn from the same selected set.
* **No A/A run:** nothing measures what the harness reports when both arms are the same.
* **Unit mismatch:** randomization is by 1 unit, such as a user, and the analysis treats a smaller unit, such as a request, as independent.
* **Interference:** arms share a resource, so 1 arm's load changes the other arm's measure.
* **Benchmark noise:** a performance measure has no warm-up rule, runs the arms in blocks instead of interleaved, uses a load generator that waits for responses, or makes mean latency primary.
  See the performance-benchmarks section of [implement.md](implement.md).
* **Reachable answer:** the reference solution can be reached by an arm that should not see it, for example through git history in the environment or network access.
* **Clustered units:** many units share a source, such as tasks from 1 repository, and the analysis treats them as independent.

## Reporting

Lead with a 1-sentence verdict and the count of essential and desirable gaps.
State which standards were applied and which items do not apply, with the reason.

List the essential gaps as numbered items, each with what is missing, why it matters for the result, and the concrete fix.
List the desirable gaps briefly the same way.
Then give 1 paragraph on what the design already meets.

Name specific missing details, never "lacks detail".
Do not ask for a different methodology, an arbitrary minimum sample, or analyses unrelated to the question.
Do not mark a gap that another section already closes.
Cite each standard with a link:

* [General](https://github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/GeneralStandard.md)
* [Experiments](https://github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/Experiments.md)
* [Benchmarking](https://github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/Benchmarking.md)
* [Engineering Research](https://github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/EngineeringResearch.md)
