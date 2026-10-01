# Follow-up experiments (2026-10-01)

Eight of the nine experiments `EVIDENCE.md` section 4 proposed, on the same harness as `RESULTS.md`: Opus 5.5 at high effort, headless, identical story text per task, hidden tests from the upstream PR, and a blind Opus 5.5 judge with two orderings per pool. Three runs per arm unless noted; `EVIDENCE.md` asked for five, so a difference of one hidden test or about one rank position is within noise.

Arm prompts are in `arms/<arm>.txt`, appended to the working conditions. `careful` is the arm from `RESULTS.md`: list the behaviours and edge cases, write failing tests and commit them, implement, have a fresh subagent review the diff, fix what it confirms, and run the full suite.

## 1. Underspecified stories

The story replaced by the upstream issue text as filed (`tasks/chiv`, `cliv`, `zodv`). Arms: `plain`, `careful`, and `story` (plain plus "before any code, write the cases this change must handle as a numbered list with concrete values, and a Not doing list").

| task | full story (plain) | issue text: plain | careful | story |
|---|---|---|---|---|
| chi | 3/3 | 3, 3, 3 | 3, 3, 3 | 3, 3, 3 |
| cli | 7/8 | 5, 5, 5 | 5, 5, 5 | 5, 5, 5 |
| zod | 4/6 | 3, 3, 3 | 2, 2, 2 | 3, 2, 3 |

* The vague request costs 2 of 8 hidden tests on cli and 1 of 6 on zod, in every arm.
* An agent writing its own numbered case list recovers none of it. The lost cases (the plural error message, the destination left untouched, ambiguous-lookup wording) are information only the person asking has; listing cases from the same vague text does not create it.
* So a story's value is the person's answers, written down as concrete cases. Asking where readings diverge, which a headless run cannot test, is the mechanism left.

## 2. Test author in a fresh context (`carefulsplit`)

A fresh subagent writes the failing tests from the request and the case list alone, then the session implements.

| task | hidden | judge rank | judge tests score | cost |
|---|---|---|---|---|
| cli | 7, 7, 7 (careful 7, 7, 7) | 8.67 of 12 (careful 4.83) | 4.5 (careful 4.0) | $3.55 (careful $2.53) |
| zod | 4, 4, 4 (careful 4, 4, 5) | 5.5 of 9 (careful 6.83) | 4.17 (careful 3.33) | $3.16 (careful $2.70) |
| llama | 10, 10, 10 | | | $16.12 (careful $10.61) |

* No hidden-test gain. The judge scored its tests higher on both tasks; its overall rank was mixed (worse on cli, better on zod), with lower design and scope scores, at about $0.50-$1 more per run on the small tasks.

## 3. Locked tests plus stop-and-report (`carefullock`, llama)

A pre-commit hook refused commits that changed a test file the recorded red commit held, and the prompt said a test that cannot be satisfied is a stop.

* Test lines changed after the red commit: 0, 0, 0. Without the lock, the fresh-test-author runs changed 30 and 18 lines after theirs, and the AGENTS.md-only runs 63 and 139.
* Hidden tests 10/10 in all three. The lock did not prevent the `any` parser change, because that edit to existing tests happens inside the red commit itself.

## 4. Mutation pass (`carefulmutate`)

| task | hidden | judge rank (cli) | cost |
|---|---|---|---|
| attrs | 8, 8, 8 | | $3.85 (careful $2.54) |
| cli | 7, 7, 7 | 5.5 of 12 (careful 4.83) | $4.08 (careful $2.53) |

* No hidden-test or rank gain, at about $1.50 more per run.

## 5. Review ablation (cli and zod, one judge pool of 12 per task)

| arm | cli hidden | zod hidden | cli rank | zod rank | mean rank | mean cost |
|---|---|---|---|---|---|---|
| `noreview` | 7, 7, 7 | 4, 4, 4 | 10.0 | 9.5 | 9.75 | $1.58 |
| `careful` (one review) | 7, 7, 7 | 4, 4, 5 | 5.33 | 6.33 | 5.83 | $2.62 |
| `verify` (one review, then a numbered pass that drops findings with no supporting line or test) | 7, 7, 7 | 4, 4, 4 | 6.83 | 2.67 | **4.75** | $2.35 |
| `tworounds` | 8, 7, 7 | 4, 4, 4 | 3.83 | 7.5 | 5.67 | $3.56 |

* Removing the review is clearly worst on judge rank on both tasks.
* One review with a verification pass has the best mean rank at below-careful cost; a second round costs more and swings between tasks.

## 6. Guardrails separated (llama, two runs each)

| arm | hidden | upstream `any` tests broken | cost |
|---|---|---|---|
| AGENTS.md only | 10, 10 | 3, 3 | $7.10, $6.69 |
| hooks and gate only | 10, 10 | 3, 3 | $8.41, $5.82 |
| both (`llamah`, from `RESULTS.md`) | 10, 10 | 3, 3 | $21.66, $7.15 |

* With `--include-hook-events`, the hooks-only runs fired the Bash hooks 162 and 268 times and the Edit hooks 10 and 12 times, with no denial. Neither part, nor both, changed a measured outcome on this task.

## 7. Writing rules (`writing`: careful plus only the plugin's SessionStart and SubagentStart writing hooks)

| task | hidden | judge rank | cost |
|---|---|---|---|
| cli | 7, 7, 7 | 7.0 of 12 (careful 4.83) | $2.03 |
| zod | 5, 5, 3 | 2.67 of 9 (careful 6.83) | $2.86 |

* No consistent effect on code; one task better, one worse.

## 8. Judge validity

* Source-only judging (every test file stripped from the diffs) left SDLC's ranks where they were: chi 4.5 to 4.25, attrs 5.5 to 5.5 (of 7). The penalty is on SDLC's source changes, not its test volume.
* The human half (the user ranking `blind-cli/` without the key) has not been done.

## 9. Characterization first (`pin`, llama)

* Hidden 10/10 in all three; upstream's `any` tests broken in 2 of 3 runs. Only SDLC (2 of 2) and one plain run kept upstream's `any` behaviour. Why SDLC did is not established.

## 10. SDLC 16 smoke runs

One headless run each of the rewritten `deliver` (`sdlc16` arm), same story text and working conditions. Each ran the `test-author` agent once and the `review` agent once, then stopped for the user's confirmation.

| task | hidden | cost | wall min | SDLC 15 (same task) |
|---|---|---|---|---|
| cli | 7/8 | $3.58 | 14.7 | 7, 7 of 8; $4.72; 22.1 min |
| zod | 4/6 | $3.07 | 10.8 | 4, 3 of 6; $9.67; 45.9 min |

* On zod, no accepted test changed after the red commit. On cli the grader could not identify the red commit, because it also held source stubs.
* One run per task: this shows the loop works without a person and costs about what the careful prompt does, not that it beats it.

## What this changed in SDLC 16

* **Kept:** one fresh review that writes attack tests before reading the code, then a verification pass over its own findings (section 5); the accepted-test lock with a stop-and-report rule, enforced at commit so shell edits are caught (section 3); a fresh test-author agent, for its higher test scores (section 2); stories as concrete cases with questions asked only where readings diverge (section 1).
* **Cut:** a second review round, the refute agent on another model, the mutation pass (section 4), and writing rules injected into the SDLC subagents (section 7).
* **Left as is:** guardrails' AGENTS.md and hooks, with one fix: every rule that must hold also runs at commit or turn end, since edit hooks see a fraction of the writes (section 6).
