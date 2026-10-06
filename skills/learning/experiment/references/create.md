# Creating an experiment

Draft the design document from what the user has said, then ask only for the choices that are theirs: budget, model, which arms to run, and what effect would matter to them.
Put any choice still unmade in the open-decisions section rather than stalling on it.

## Steps

1. **Find the gap.** Search for the nearest published studies when a search tool is available.
   For each one, record its numbers and what it confounds, such as a comparison that changes 2 things at once.
   State the question that no study isolates.
   That is the "why this question is open" section.
2. **State hypotheses.** H1 is directional and names the measure and the comparison.
   H0 is "the difference is zero".
   Justify the direction from prior work, and test two-sided, so a difference in the other direction is still detected and reported.
   Write a theory section when 2 plausible mechanisms predict opposite results, because the result then tells the reader which one held.
3. **Name the method and design.** Name the method, such as "a controlled benchmarking experiment without human participants".
   Name the design, such as paired with each task as a block, between-groups, 2x2 factorial, or crossover.
4. **Define the arms.** Give each arm's treatment and exactly what it sees, in a table.
   Name the **manipulation**: the single thing that differs between arms.
   Then list every other difference as a confound.
   A common one is a treatment that bundles 2 differences.
   For example, a fresh agent lacks the designer's notes and also starts with a shorter, fresh context.
   For each confound, remove it, add an arm that separates it, measure it, or state that the experiment tests the bundle.
   When units were chosen for an extreme score, such as the slowest endpoints, they move toward the average on their own, which is called **regression to the mean**.
   Randomize the selected units between arms, or in a paired design run every arm on each selected unit.
   Measure again rather than reusing the score that selected them, so no arm is compared with the units' own earlier score.
   Look for leak paths, where an artifact passed between arms carries part of the manipulation, and measure how much leaks.
5. **Handle assignment and order.** Randomize allocation of units to arms when units receive 1 arm each.
   When every unit receives every arm, say so.
   When arm order is fixed by a dependency, such as arm B needing arm A's output, state the reason and the mitigation.
   The mitigations are to run paired arms back to back and to randomize the order of units with a seed.
6. **List controlled variables.** These are everything held constant: model and version, materials, prompts, tools, limits, framework, and settings.
   Say how each is controlled: physically, statistically, or not at all.
7. **Define measures.**
   * **Primary:** 1 measure, with its unit, its instrument, and a citation that it measures the construct.
     Check whether that evidence weakens under a covariate, and record that covariate.
   * **Guard:** a measure that must not get worse, with a pre-set margin, such as an invalid-test rate.
   * **Secondary:** context such as downstream outcomes, reported and not used in the decision rule.
   * **Reference:** a human or state-of-the-art result on the same measure, such as a benchmark's own human-written tests, so readers can see the scale.
   * **Covariate:** any size or volume that could inflate the primary measure on its own, such as the number of tests in a suite.
   * **Manipulation check:** confirm in every run that the manipulation happened and that the other arm did not receive it.
     Pre-specify a rerun-once-then-exclude rule, and report every exclusion with its reason.
8. **Choose objects.** Objects are the tasks, programs, or datasets the arms run on.
   Name the source and pin its version.
   Respect its licence, for example by downloading it with a script instead of committing a copy.
   Justify the choice and say why simpler alternatives would not exercise the manipulation.
   Plan to report each object's size, such as its method count, line count, and number of items scored.
   Filter broken objects first, then draw pilot objects and experiment objects with separate seeds.
   Commit each seed before the draw that uses it.
9. **Check for contamination.** When the objects are public, add a few fresh objects written for this experiment and never published before the run.
   Report them separately as a contamination check.
   Too few of them can decide nothing.
10. **Set the sample size.** Follow [statistics.md](statistics.md).
    Use the larger of the pilot's estimate of spread and a conservative planning value, set a budget cap, and say that a capped null result is inconclusive.
    Justify the number of repeated runs per unit with a pre-set rule that uses the pilot's run-to-run variance.
11. **Write the procedure.** List numbered steps for 1 run of 1 unit, including where each check runs.
    Record the start time of each session so drift can be plotted.
    When the primary measure is time, throughput, or resource use, write the warm-up rule, machine settings, arm interleaving, load model, and primary percentile from the performance-benchmarks section of [implement.md](implement.md).
12. **Plan the pilot.** Run the pilot with the planned number of runs per unit.
    When the pre-set rule then changes k, rescale σ as [statistics.md](statistics.md) describes.
    It checks the harness and supplies variance estimates.
    Include an A/A run, as in the A/A item of [implement.md](implement.md).
    Its effect is never analysed.
    Publish 1 pilot run as a worked example.
13. **Plan the analysis.** Give the paired difference and its confidence interval, the test with its justification and assumption checks, wins, ties, and losses, and the guard, covariate, and size-adjusted analyses.
    Plot the distribution of differences.
    Label the exploratory analyses as exploratory.
14. **Write the decision rule.** Give the conditions that must all hold for H1, including the SESOI and the guard margin.
    Read the decision-rule section of [statistics.md](statistics.md) before fixing it.
15. **List the assumptions.** Make each assumption the design rests on explicit, and check that no 2 contradict each other or the status line.
    For example, settings the plan fixes after the pilot must be marked as planned, not as deviations.
16. **Group the threats.** Group them under construct, internal, external, and conclusion validity.
    Give each its check or mitigation, and include alternative interpretations of a positive result.
17. **Plan for reproducibility.** List the pinned inputs, all seeds, committed prompts and materials, raw outputs, the analysis script, logged hand edits, cost per run, and the deviation log.
    A git commit before the pilot fixes the design locally.
    A public timestamp, such as an OSF registration or a push to a public repository, is stronger.
    That publishes the design, so ask the user first.

## Document outline

Use these sections in this order, and omit a section only when it cannot apply:

1. Title as a question, then 3 to 5 sentences giving the question, the arms, the primary measure, and the method.
2. Status: design only, piloted, running, or done, and what must happen before the next stage.
3. Why this question is open: the nearest studies with their numbers, the gap, and the theory.
4. Hypotheses: H1, H0, sidedness, and a pointer to the decision rule.
5. Arms: the arm table, the manipulation, the design and arm order, and alternatives not compared with the reason.
6. Controlled variables.
7. Measures: primary, guard, secondary, reference, covariate, and manipulation check.
8. Task set or objects: source and pin, justification, filters and draws, fresh objects, and sample size.
9. Procedure: run order, per-run steps, and the pilot.
10. Analysis: primary, test choice, exploratory, and the decision rule.
11. Assumptions.
12. Threats to validity, in 4 groups.
13. Reproducibility and audit.
14. Open decisions.

## Checking the draft

Before handing the draft over, review it with [review.md](review.md) and fix every essential gap you can fix without the user's choice.
Confirm that every internal link resolves and that every number in the sample-size section recomputes from its formula.
