# learning

Skills for learning a topic in a format the reader absorbs, for practicing code by hand, and for designing experiments whose results can be trusted.

| Skill | Fires on |
|---|---|
| `teach-like-stackoverflow` | "how do I X in Python", "why am I getting this error", "how does X work", "explain X", "what's the difference between X and Y", "teach me X" |
| `code-practice` | "I want to practice coding", "let me re-implement PR 9 myself", "give me a coding drill", "what should I practice next" |
| `experiment` | "design an experiment to test X", "how many runs do I need", "review my EXPERIMENT.md", "check this against the SIGSOFT empirical standards" |

## `teach-like-stackoverflow`

Answers a programming or computer-science question as a mock Stack Overflow thread on one HTML page, served on the local network when you read it on a phone.

The format came from one experiment. The same topic, logistic regression over 768-number sentence embeddings, was taught six ways in one session:

* A prose walkthrough lost the reader's attention.
* A problem to solve before the explanation took too much time and effort.
* One-line comments on every code line were too busy.
* Static charts didn't click.
* An interactive chart was better, but not quite there.
* The Stack Overflow thread worked.

Four features of the thread plausibly did the work. They were not tested separately:

* **Someone else makes the mistake.** People learn from watching a tutee's errors get corrected (Chi, Roy & Hausmann, 2008), and from a misconception stated and then refuted (Muller et al., 2008).
* **Explanations come as short answers to specific questions.** The comments break the material into segments, and each segment is introduced by the question it answers.
* **The mechanism is code.** A further answer writes the library call out in the layer beneath it, such as `fit` written as a numpy loop, so the reader learns it in a format they already read.
* **The layout is familiar.** A developer already knows where the fix, the accepted answer and the side questions sit.

What the skill insists on:

* **Every code block is run** before it goes on the page, and error text is copied from the run.
* **Further answers each take a different technique:** the call written out one layer lower, an alternative with its trade-off, or a popular approach with a flaw a comment exposes.
* **Follow-up questions go onto the page** as new comments or answers, so the thread stays the one place to read.

`assets/thread.html` carries the page layout and styles, with one example of every element.

## `code-practice`

Has you re-implement one slice of a change that is already merged, such as a pull request an agent wrote, so you keep writing code yourself.

A session runs in this order:

1. The agent picks a slice with real logic and creates a `practice/<number>-<slice>` branch at the commit before the change.
2. You write the slice's interface and list the test cases you would write, and the agent compares both with the merged version.
3. The agent brings in the rest of the change and the merged tests, fitted to your interface, and checks they fail.
4. You write the implementation.
   The agent answers conceptual questions fully but gives only graded hints on the slice: a question, then the place to look, then the idea, then code for one step only when you ask for it.
5. The agent critiques your code against the merged version: correctness beyond the tests, data structures, Big-O time, memory, design and patterns, and any better approach with why it is better.
6. An optional debugging drill plants one bug for you to find.
7. A log at `~/.code-practice/log.md` records where you got stuck and a redo date 2 to 3 weeks out.

The design follows the research on practice:

* **Writing beats reading:** producing an answer from memory builds more skill than studying a worked one, so the agent never writes the slice.
* **Help fades:** faded worked examples move a learner from full help to none, which the hint levels do inside one session.
* **Delegation costs learning:** in [Anthropic's 2026 randomized trial](https://www.anthropic.com/research/AI-assistance-coding-skills), 52 developers learned a new library.
  Those with AI averaged about 50% on a later quiz, against about 67% for those coding by hand, with the largest gap on debugging.
  Developers who asked the AI only conceptual questions scored 65% or more, so the skill answers those in full and adds a debugging drill.
* **Spacing:** the log's redo date brings the same slice back after a gap.

The agent writes the tests, because in a story the design lives in the interface and acceptance criteria.
The tests mostly turn those into examples, so writing them by hand is setup work more than design practice.
Listing the cases keeps the part that is practice.

## `experiment`

Designs a controlled experiment as one design document, `EXPERIMENT.md`, reviews an existing design and lists each gap with its fix, or implements a committed design.
It was built from one session that researched experiment design, then designed and repeatedly audited an experiment on whether a fresh agent writes stronger failing tests than the agent that designed the interface.

The skill uses progressive disclosure.
`SKILL.md` holds the core rules and routes to 1 reference file per job:

* **`references/create.md`:** 17 design steps and the document outline.
* **`references/review.md`:** a checklist condensed from the ACM SIGSOFT Empirical Standards and the gaps that recur.
  It uses the General, Experiments, Benchmarking, and Engineering Research standards.
* **`references/implement.md`:** testing the measuring instrument, flaky checks, writing the analysis before the data, no peeking, completeness checks, provenance, and freezing the harness after the pilot.
* **`references/statistics.md`:** sample size for a paired design, test choice, and decision-rule traps.
* **`references/llm-experiments.md`:** pinning, isolation, contamination, and drift for experiments on models and agents.
* **`scripts/`:** 3 standard-library Python checks that replace judgement at the gates.
  `check_design.py` checks the outline, open decisions, links, and sample size before the pilot, `check_order.py` proves from git history that decisions came before data, and `check_run.py` proves the run is complete and its raw outputs unchanged.
  Each has a `--self-test`.

The sources:

* **Classical design of experiments:** randomization, replication, and blocking.
* **Preregistration practice:** hypotheses, the smallest effect size of interest, and an analysis plan fixed before data.
* **Kohavi, Tang, and Xu's _Trustworthy Online Controlled Experiments_:** guardrail metrics and sample ratio mismatch.
* **The [ACM SIGSOFT Empirical Standards](https://github.com/acmsigsoft/EmpiricalStandards):** the review checklist.
* **The [2025 guidelines for empirical studies involving LLMs](https://arxiv.org/abs/2508.15503):** the LLM-specific rules.

The list of recurring gaps comes from the audits in that session.
It includes a one-sided null hypothesis under a two-sided test, and a decision rule with only 50% power at its own threshold.
It also includes a size covariate that inflates the primary measure, a treatment that bundles 2 differences, and a leak path between arms.

## Installing

**Claude Code:**

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install learning@davebben-skills
```

**Any other agent** (Codex, Cursor, Windsurf, and more), via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add DaveBben/davebben-skills --skill teach-like-stackoverflow
npx skills add DaveBben/davebben-skills --skill code-practice
npx skills add DaveBben/davebben-skills --skill experiment
```

The canonical `SKILL.md` lives at `skills/learning/` in the repo root.

MIT.
