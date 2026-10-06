---
name: experiment
description: "Use this skill when the user wants to design, plan, preregister, review, audit, critique, or implement and run a controlled experiment whose result must be trusted: arms compared with hypotheses, measures, a sample size, and a decision rule. It covers experiments on LLMs, agents, prompts, or workflows, A/B tests, and benchmark studies. Use it on: 'design an experiment to test X', 'help me design an expirement', 'what are the steps to designing a good experiment', 'how many runs do I need', 'review my EXPERIMENT.md', 'check this against the SIGSOFT empirical standards', 'poke holes in my study design', 'build the harness for my experiment', 'run the pilot'. Load it before drafting, reading, or running a design. Writes a design document that fixes every decision before data exists, reviews one against published standards with a fix for each gap, or implements one with a tested instrument and no peeking. Not for a timeboxed prototype that answers a feasibility question with throwaway code."
license: MIT
metadata:
  version: "0.1.0"
---
# Experiment

An experiment is trustworthy when every decision that could bend its result is fixed before any data exists.
This skill has 3 parts: creating a design document, reviewing one, and implementing one.
All 3 rest on the same rules, so read the core rules below, then load the reference file for the part the user asked for.

## Choosing the part

* **Creating:** the user wants an experiment designed, or a question turned into a test.
  Read [references/create.md](references/create.md).
* **Reviewing:** the user has a design, plan, protocol, or preregistration and wants it checked, audited, or improved.
  Read [references/review.md](references/review.md).
  When the user then asks to apply the findings, edit the design as creating would.
* **Implementing:** the user has a committed design and wants the harness built, the pilot run, the experiment run, or the results produced.
  Read [references/implement.md](references/implement.md).
* **Statistics:** read [references/statistics.md](references/statistics.md) when setting or checking a sample size, a test, a confidence interval, or a decision rule, or when live users or traffic are split between arms.
* **LLM or agent experiments:** read [references/llm-experiments.md](references/llm-experiments.md) when any arm, task, or judge involves a language model or an agent.

## Core rules

* **Fix decisions before data:** hypotheses, measures, analysis, the decision rule, and the sample size or the pre-set rule that computes it from the pilot are written and committed before the pilot.
  A choice the user has not made yet goes in an open-decisions list, and the pilot waits until that list is empty.
* **Vary one thing:** each comparison between 2 arms differs in exactly 1 manipulation.
  A factorial design varies several factors and crosses each with the others.
  List every other difference between arms as a confound, then remove it, add an arm that separates it, measure it as a covariate, or state that the experiment tests the bundle.
  Arms run over the same period, because time is a difference too: a before-and-after comparison mixes in every other change made over that period.
* **One primary measure:** 1 primary measure decides the result.
  Guard measures catch a win that is really a cheat, secondary measures add context, and covariates expose confounds.
  None of those decide the result.
* **Size from the smallest effect of interest:** the **smallest effect size of interest** (SESOI) is the smallest difference that would change a decision.
  The sample size comes from a power analysis at the SESOI, and never from an effect size reported in earlier studies, which publication bias inflates.
* **Pre-specified versus exploratory:** an analysis not written before data is labelled exploratory and never decides the result.
* **Every threat has a check:** each threat to validity names the check or mitigation that addresses it, or says plainly that nothing does.
* **Reproducible from the repository:** pinned inputs and seeds, committed prompts and materials, raw outputs kept unedited, 1 script that computes every reported number, and a dated log of every deviation from the design.

## The design document

The design lives in 1 Markdown file, `EXPERIMENT.md` at the repository root unless the user names another path.
[references/create.md](references/create.md) gives its section outline.
A review reads that file, or whatever design the user supplies, in full before judging it.

## Checks

3 scripts in this skill's `scripts/` directory turn gates into commands.
Run each with Python 3 from the experiment's repository: they need no packages.
Each prints every failure and exits 1, and `--self-test` checks the script itself.
A failure blocks the gate it guards.
A pass proves structure, order, and counts only: whether the design is sound stays a judgement.

* **[scripts/check_design.py](scripts/check_design.py):** run on the design after every draft.
  With `--ready`, it is the gate for the pilot.
* **[scripts/check_order.py](scripts/check_order.py):** run before reporting.
  It proves from git history that the design tag, each seed, the analysis script, and the harness tag came before the data.
* **[scripts/check_run.py](scripts/check_run.py):** run after the main run.
  It proves every planned run has its output and manifest, and that no raw output changed since its hash was recorded.
