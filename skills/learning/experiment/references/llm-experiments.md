# Experiments with LLMs and agents

These rules add to the core rules whenever an arm, a task, or a judge involves a language model or an agent.
They follow the 2025 guidelines for empirical studies involving LLMs ([arXiv 2508.15503](https://arxiv.org/abs/2508.15503)).

## Report and pin

* **Model:** record the exact model ID and version string for every role.
  Record the sampling settings, such as temperature, even when the harness hides them.
* **Harness:** pin the agent command line, SDK, or harness version, and the tools each session may use.
* **Prompts:** commit every prompt as the exact text sent, so others can vary it.
* **Traces:** keep the full transcript and tool calls of every session, unedited.
* **Cost:** record tokens and spend for each run.

## Isolation and sessions

* **New session per run:** every run of every arm starts a new session, so no run inherits another's context.
* **Isolated inputs:** run each arm in a new directory that holds only its permitted inputs.
  Confirm with a script that the transcript reads no other file.
* **No path to the answer:** remove every path to the reference solution from each arm's environment, such as git history, cached build outputs, and network access, unless the design permits it.
* **Shared artifacts leak:** text that one arm writes and another arm reads can carry the manipulation across.
  Docstrings, comments, and file names are examples.
  Keep the artifact when a real workflow would pass it, and measure how much leaks.
* **Fresh context is a treatment too:** a fresh session differs from a continuing one in context length as well as in what it knows.
  Separate the 2 with an extra arm, or state that the experiment tests both together.
* **Same model, shared blind spots:** 2 sessions of 1 model are not independent writers.
  Independently written programs still fail on the same inputs ([Knight and Leveson, IEEE TSE 1986](https://doi.org/10.1109/TSE.1986.6312924)).
  Consider an arm on a different model when independence is the hypothesis.

## Variance and order

* **Repeated runs:** model output varies between runs, so give each unit several runs per arm and average them.
  Justify the count with the pilot, as in [statistics.md](statistics.md).
* **Drift:** a hosted model or its API can change during a long experiment.
  Randomize the order of units with a seed, run paired arms back to back, record each session's start time, and plot the score against time.

## Benchmarks and contamination

* **Training data:** a benchmark published before the model's training cutoff may be memorised, which can shrink or fake a difference.
* **Fresh items:** add a small set of items written for the experiment and never published before the run.
  Report them separately.
* **Examples in specs:** strip worked examples from task specs when they double as ready-made answers or test cases that would narrow the difference between arms.

## Comparisons

* **Baselines:** use suitable baselines, benchmarks, and metrics.
  Include a human or state-of-the-art reference on the same measure when one exists.
* **Open model:** the guidelines recommend an open-weight model as a baseline, so results do not depend on 1 closed model.
* **Human validation:** check LLM-judged or LLM-labelled outputs against human judgment on a sample.
* **Limitations:** state them plainly, including the single model, prompt sensitivity, and contamination.
