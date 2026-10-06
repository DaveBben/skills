# Statistics for experiment design

## Sample size for a paired design

```text
n = ((z(1 − α/2) + z(1 − β)) × σ / δ)² / ARE
```

* **α:** the significance level, two-sided.
  At 0.05, z(1 − α/2) = 1.96.
* **1 − β:** the power.
  At 0.80, z(1 − β) = 0.84.
* **δ:** the smallest effect size of interest (SESOI), in the measure's units.
* **σ:** the standard deviation of the per-unit paired differences, on the scale the analysis uses.
  If each unit's score is a mean of k runs, σ is the spread of those means.
* **ARE:** the asymptotic relative efficiency of the planned test against the paired t-test.
  For the Wilcoxon signed-rank test, use 0.864, its minimum over all distributions.
  It is 0.955 under normality, so 0.864 is the conservative choice.
  Use 1 for the t-test itself.

Recompute every example number with a script before writing it down.
At α = 0.05 two-sided, power 0.80, δ = 5, and σ = 10, the formula gives n = 31.4 for the t-test (ARE 1), so 32 units, and n = 36.3 for the Wilcoxon test (ARE 0.864), so 37 units.
The normal approximation understates n for small samples.
The exact paired t-test needs 34 units here, so add z(1 − α/2)² / 2, about 2 units, or compute power with the noncentral t distribution.

### Choosing σ

* **Planning value:** take the larger of the pilot's estimate and a conservative planning value.
  A pilot of 3 to 5 units estimates σ poorly.
* **Matching scale:** run the pilot with the planned runs per unit, so its σ is on the scale the analysis uses.
  When the rule below changes k, rescale with σ² − s²w / k_pilot + s²w / k_new.
* **Budget cap:** when n exceeds the cap, run the cap and state in advance that a null result is then inconclusive.

### Repeated runs per unit

Let s²w be the run-to-run variance of a unit's paired difference, measured in the pilot.
With k runs per unit, run noise contributes s²w / k to σ².
Pre-set a rule, such as raising k from 3 to 5 when s²w / k is more than half of σ².

## Tests

* **Paired data:** use a paired test.
  An independent-samples test on paired data is a recognised antipattern.
* **Wilcoxon signed-rank:** suits bounded or non-normal paired differences.
  It assumes the differences are roughly symmetric.
  Check this with a histogram, and report a sign test beside it when they are clearly skewed.
* **Ties:** bounded scores often produce zero differences.
  Keep them with Pratt's method, for example `scipy.stats.wilcoxon(d, zero_method="pratt")`.
  The default method drops them, which shrinks n silently.
* **Confidence interval:** use a bootstrap over units for the mean paired difference.
  Use at least 10,000 resamples with a fixed seed, percentile or BCa.
* **Several primary tests:** correct for multiplicity, or pick 1 primary test.
  With k tests decided separately, Bonferroni runs each at α / k, and the sample size is computed at that level.
  Holm's method is less conservative when the tests are decided together.
* **Clustered units:** when units share a source, such as tasks from 1 repository, limit the units per cluster in the draw.
  Then repeat the bootstrap with whole clusters resampled, and report it beside the primary interval.

## Decision rule

* **Support:** the confidence interval lies entirely on the side of zero that H1 predicts, the guard measure stays within its margin, and the interval is compared with the SESOI as the threshold-trap item below describes.
  An interval entirely on the other side is reported as an effect opposite to H1.
* **Threshold trap:** requiring the observed mean to reach the SESOI gives about 50% power when the true effect equals the SESOI.
  Either power the study for a larger true effect and say so, or require the confidence interval to exclude zero and compare the interval with the SESOI.
* **Claiming no effect:** a non-significant result is not evidence of no effect.
  To claim the effect is smaller than the SESOI, pre-specify an equivalence test (TOST) with bounds ±SESOI.
  Without one, a null result is reported as inconclusive.

## Controlled experiments with users

These apply when live users or traffic are split between arms, as in an A/B test:

* **Sample ratio mismatch:** test the observed split against the planned split with a chi-squared test on every experiment.
  A mismatch means the assignment or logging is broken, and the result is not trusted.
* **Unit of analysis:** analyse at the unit that was randomized.
  When users are randomized and the metric is per request, 1 user's requests are not independent, and a per-request test gives intervals that are too narrow.
  Aggregate to 1 value per user, or bootstrap over users.
* **Interference:** arms that share a resource, such as a database, a cache, or a rate limit, change each other's measures.
  A treatment that loads the shared database slows the control too.
  Partition the resource, or randomize by cluster such as region and analyse 1 value per cluster with power computed on the cluster count, or measure the load on the shared resource.
* **Fixed split:** keep the allocation ratio fixed for the analysis window.
  Pooling a ramp from 1% to 50% mixes periods with different ratios, which can reverse the direction of the effect (Simpson's paradox).
  Analyse only the period at the final ratio, or stratify by period.
* **Guardrail metrics:** set the metrics that must not degrade, such as latency or error rate, before launch.
* **Novelty effects:** a short test can measure novelty rather than a lasting change.
  Run long enough, or keep a holdout group.
