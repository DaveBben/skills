# learning

Skills for learning a topic in a format the reader absorbs.

| Skill | Fires on |
|---|---|
| `teach-like-stackoverflow` | "how do I X in Python", "why am I getting this error", "how does X work", "explain X", "what's the difference between X and Y", "teach me X" |

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

## Installing

**Claude Code:**

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install learning@davebben-skills
```

**Any other agent** (Codex, Cursor, Windsurf, and more), via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add DaveBben/davebben-skills --skill teach-like-stackoverflow
```

The canonical `SKILL.md` lives at `skills/learning/` in the repo root.

MIT.
