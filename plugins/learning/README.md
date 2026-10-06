# learning

Skills for learning a topic in a format the reader absorbs, and for practicing code by hand.

| Skill | Fires on |
|---|---|
| `teach-like-stackoverflow` | "how do I X in Python", "why am I getting this error", "how does X work", "explain X", "what's the difference between X and Y", "teach me X" |
| `code-practice` | "I want to practice coding", "let me re-implement PR 9 myself", "give me a coding drill", "what should I practice next" |

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
```

The canonical `SKILL.md` lives at `skills/learning/` in the repo root.

MIT.
