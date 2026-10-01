# Evidence for SDLC 16

Source material for the SDLC 16.0.0 rewrite. Nothing here loads into an agent.

* `RESULTS.md`: plain prompting, a one-paragraph "careful" prompt and the SDLC 15.2.0 plugin on five upstream changes merged after the model's training cutoff, graded by the upstream PR's own tests and a blind judge; plus a guardrails-harness arm.
* `EVIDENCE.md`: every SDLC 15 mechanism matched against published and measured evidence for 2026-generation models, with a keep, cut, simplify or untested verdict.
* `FOLLOWUP.md`: the follow-up experiments `EVIDENCE.md` proposed, and what each changed in SDLC 16.
* The per-run data the write-ups cite (`runs/`, each run's `grade.json`, the judge JSON files) stayed in the experiment directory and is not included here.
* `harness/`: the scripts that ran them. `run.sh <task> <arm> <rep>` prepares a checkout of the commit before the upstream merge and runs one headless session; `grade.py <run-id>` grades it; `judge.py <task> <seed>` runs the blind judge. Paths are absolute to the machine the experiment ran on; edit `env.sh`. Each `tasks/<task>/task.env` names the upstream repository, the base and merge commits and the hidden tests.
