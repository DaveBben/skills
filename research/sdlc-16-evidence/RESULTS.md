# SDLC plugin vs plain prompting: experiment results (2026-09-30)

## Method

Five real changes merged upstream after the model's training cutoff (June 2026), each rebuilt as a story and given to Opus 5.5 (high effort) in headless Claude Code sessions:

| Task | Upstream PR | Kind |
|---|---|---|
| chi | go-chi/chi #1148 (2026-08-20) | Go bugfix: Walk()/Routes() hide a handler that shares a Mount() pattern |
| attrs | python-attrs/attrs #1592 (2026-08-01) | Python feature: generator on_setattr hooks |
| cli | urfave/cli #2393 (2026-08-16) | Go feature: required single-value arguments, usage errors, help rendering |
| zod | colinhacks/zod #6582 (2026-09-09) | TypeScript bugfix: discriminated unions with defaulted tags |
| llama | ggml-org/llama.cpp #29161 (2026-09-20) | C++ bugfix: PEG parser tolerates invalid UTF-8, U+FFFD maximal-subpart replacement, backtracking de-dup, streaming |

Every arm of a task gets the identical story text and working conditions (no tracker, user away, commit locally, no push). Checkout is the commit before the upstream merge, with no remote and no later history. All other plugins, MCP servers and memory are off.

Arms:

* **plain:** the story only.
* **careful:** the story plus one paragraph: list behaviours and edge cases, write failing tests and commit them, implement, then have a fresh subagent review the diff, fix what it confirms, run the full suite.
* **sdlc:** `/SDLC:deliver` plus the story, with the SDLC plugin 15.2.0 loaded (setup, build, refactor, review, security, refute, worker subagents; story.sh; hooks).
* **careful+harness (llama only):** the careful prompt on a checkout where `SDLC:guardrails` first ran every setup stage (AGENTS.md rewrite, `./check`, agent hooks, pre-commit gate; built once, 44 min, $8.92).

Grading: the upstream PR's tests laid over each run's final code ("hidden tests"; stories specify public API and exact error strings, edge cases are left out), the full suite, diff size, cost and wall time from the session logs, and a blind Opus 5.5 judge that sees all candidate diffs of a task anonymized plus the upstream diff, scoring correctness, tests, design and scope 1-5 and ranking them (two orderings per task; the untouched base is in each pool as a floor, so ranks are out of 7).

## Results per task (2 runs per arm)

| task | arm | hidden tests passed | src lines +/- | test lines + | mean cost $ | mean wall min | judge mean rank (of 7) |
|---|---|---|---|---|---|---|---|
| chi | plain | 3/3 3/3 | 15/5 | 162 | 0.48 | 2.7 | 3.0 |
| chi | careful | 3/3 3/3 | 36/15 | 459 | 1.81 | 10.1 | 3.0 |
| chi | sdlc | 3/3 3/3 | 62/15 | 725 | 12.03 | 71.4 | 4.5 |
| attrs | plain | 8/8 8/8 | 151/10 | 408 | 1.21 | 4.1 | 2.75 |
| attrs | careful | 8/8 8/8 | 157/14 | 769 | 2.54 | 9.6 | 2.25 |
| attrs | sdlc | 8/8 8/8 | 170/12 | 1241 | 14.15 | 61.0 | 5.5 |
| cli | plain | 7/8 7/8 | 86/15 | 248 | 1.04 | 3.2 | 4.0 |
| cli | careful | 7/8 7/8 | 94/22 | 525 | 2.57 | 9.6 | 2.0 |
| cli | sdlc | 7/8 7/8 | 72/18 | 395 | 4.72 | 22.1 | 4.5 |
| zod | plain | 4/6 4/6 | 23/8 | 56 | 1.21 | 4.6 | 4.5 |
| zod | careful | 5/6 4/6 | 30/20 | 101 | 2.92 | 9.6 | 4.0 |
| zod | sdlc | 4/6 3/6 | 28/26 | 122 | 9.67 | 45.9 | 2.0 |
| llama | plain | 10/10 10/10 | 147/73 | 114 | 3.08 | 24.5 | 6.0 (of 9) |
| llama | careful | 10/10 10/10 | 170/91 | 364 | 10.61 | 32.4 | 3.75 (of 9) |
| llama | sdlc | 10/10 10/10 | 143/39 | 347 | 19.45 | 92.0 | 4.75 (of 9; sdlc-1 ranked 1st and 2nd, sdlc-2 8th twice) |
| llama | careful + guardrails harness | 10/10 10/10 | 165/41 | 341 | 14.41 (+ $8.92 one-time harness build) | 43.6 | 3.5 (of 9) |

Base (untouched) code: chi 2/3, attrs 0/8, cli 0/8, zod 0/6, llama 0/10.

## Totals over chi, attrs, cli, zod

| | plain | careful | sdlc |
|---|---|---|---|
| hidden tests passed | 44/50 (88%) | 45/50 (90%) | 43/50 (86%) |
| judge mean rank | 3.6 | 2.8 | 4.1 |
| mean cost per run | ~$1.0 | ~$2.5 | ~$10.1 |
| mean wall time | ~4 min | ~10 min | ~50 min |

## Observations

* Correctness is a tie. Every arm misses the same hidden cases, all edge cases the stories did not state (cli: destination untouched when a required arg is missing; zod: nested-union metadata, and duplicate defined tags in every path). SDLC's attack tests, property tests and refute rounds did not find them.
* On llama, 3 of 4 plain/careful runs also changed the single-character `any` parser to accept invalid bytes, breaking 3 of upstream's existing tests; both SDLC runs and one plain run kept upstream's behaviour. This is the one place SDLC avoided a regression the cheaper arms made.
* The judge marks SDLC down on design and scope: chi-sdlc-2 rewrote routing internals with a pattern-normalizing shadow table (scope 1/5) for a fix plain made in ~15 lines; attrs-sdlc runs added ExitStack-style cleanup machinery with exception-handling flaws; attrs-sdlc-2 wrote 1402 test lines.
* SDLC's one judge win is zod (rank 2.0), yet that same zod-sdlc-2 run scored lowest on hidden tests (3/6, broke nested encoding).
* The skill ran as designed: every SDLC run loaded deliver, called story.sh 9-16 times and ran setup > build > refactor > review > refute. chi-sdlc-2 ran six full review rounds; the skill says a second round of blocking findings is a split or a question.
* No run in any arm needed the "decide yourself" resume prompt to finish.
* Limits: 2 runs per arm per task; stories were well specified (favours plain prompting; SDLC's criteria step may matter more on vague requests, untested); review artifacts' value to a human reviewer is not measured.

Raw data: `runs/<task>-<arm>-<rep>/grade.json`, `result.diff`, `log/turn*.jsonl`; judge output `judge-<task>-<seed>.json`; stories `tasks/<task>/story.md`.

## Guardrails harness arm (llama)

* Hidden tests 10/10 in both runs. Both made the same `any` change as the careful runs, breaking 3 of upstream's existing tests, so the harness did not prevent that divergence.
* No tool call was refused in either run. A probe with `--include-hook-events` shows the hooks do fire (PreToolUse:Bash on every Bash call, Stop, UserPromptSubmit, SessionStart) and pass silently.
* Why nothing blocked: both runs branched before their first edit, so the main-branch guard never saw an edit on main. The accepted-test guard only acts on red commits recorded by deliver's story.sh, so it is inert without deliver. Most code was written through Bash (117 and 115 Bash calls against 15 and 3 Edit calls, about 500 changed lines each), which the Edit/Write-matched hooks (main guard, tests guard, fast-check) never see. Claude Code's auto permission mode tells the model it may change files with sed, heredocs or scripts. The turn-end check (build and tests) ran and was green.
* So this arm shows the harness mostly inert on this task, not tested and found unhelpful. It does show a coverage gap: Edit-matched hooks miss Bash writes.
* The harness's UserPromptSubmit hook tells every session to run the deliver skill, which was not loaded; the runs noted it and continued.
