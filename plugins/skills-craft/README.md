# skills-craft

Skills for writing instructions an agent reads.

| Skill | Fires on |
|---|---|
| `review-skill` | "review this skill", "is this skill too long", "tighten this skill", "why does the agent ignore this rule in my skill", "will this skill work on Opus 5.5", "audit the skills in this repo" |

## `review-skill`

Reviews a `SKILL.md`, its reference files or a subagent prompt, line by line, and reports each finding ranked by its expected effect on behaviour. It edits only when asked.

The skill came from one question: should writing for an agent use fewer words? The research says to use fewer lines the model does not need, not fewer words overall. Cutting what the model already knows, generic advice, repeats and checklists helps. Cutting project-specific facts, the scope of a rule, or the names of specific failures hurts.

### Evidence

Measured results:

* Adherence falls with rule count. No model, Sonnet 5 included, got every rule right once a prompt held 80 simultaneous rules. No format won across the board. ([Prompt Design at Scale, arXiv 2607.19257](https://arxiv.org/abs/2607.19257))
* IFScale found that models favour earlier instructions, and that omitting an instruction is the main failure. ([arXiv 2507.11538](https://arxiv.org/abs/2507.11538))
* Context files (AGENTS.md) did not raise task success and raised cost by more than 20%. Files written by an LLM lowered success by about 3%. Repository overviews did not help. Non-standard conventions were followed. ([arXiv 2602.11988](https://arxiv.org/abs/2602.11988))
* In SkillsBench, curated skills raised pass rates by 16.6 points. Skills the model wrote for itself scored at or below having no skill. Focused skills with at most three modules beat larger bundles. ([arXiv 2602.12670](https://arxiv.org/abs/2602.12670))
* Among 307 failures caused by skills, the top cause was excessive verification. Agents turn checklists into mandatory procedure. ([arXiv 2608.11888](https://arxiv.org/abs/2608.11888))
* A skill whose rules had piled up over many revisions scored worse than a regularized one. 6k tokens scored 47%, against 59% for 2.3k tokens. ([SkillEvoReg, arXiv 2609.30861](https://arxiv.org/abs/2609.30861))
* Few-shot prompts were cut by 65% with the same output. Larger models needed less scaffolding. ([arXiv 2609.36289](https://arxiv.org/abs/2609.36289))
* Cutting agent instructions to 75% of their length took the score from 94% to 92%. At 35%, it fell to 47% when sections were cut and to 20% when the text was rewritten generically. ([arXiv 2608.01056](https://arxiv.org/abs/2608.01056))
* Guidance tuned against real tasks resolved 33.0% of them, against 28.3% for fixed guidance and 25.5% with none. ([arXiv 2606.20512](https://arxiv.org/abs/2606.20512))
* Typos did not hurt Claude models. A missing closing quote dropped Opus 5.5 to 33% on that task. A missing colon before a list dropped it to 67%. ([prompt-noise-test](https://dev.to/vadim_albarov/typos-dont-break-llm-prompts-one-missing-quote-mark-does-d7d))
* On release day, Opus 5.5 without a skill scored 0.30 on commit-message prefixes, against 0.765 for Opus 5. With the skill loaded, the two showed no difference. The sample was small. ([Driftproof](https://dev.to/driftproofhq/opus-55-shipped-at-1631-utc-within-15-hours-we-had-receipts-on-whether-three-agent-skills-still-38kb))

Vendor guidance, with no numbers published unless noted:

* Opus 5.5: "Existing Claude Opus 5 prompts should perform well without changes."
* Opus 5.5: "Lowering effort reduces thinking, and with it cost and latency, more reliably than prompt instructions do."
* Opus 5.5: a general instruction "mostly swaps one default for another"; name the specific patterns instead.
* Opus 5.5: removing "think carefully" from a chat prompt made replies start sooner "with no clear decline in the quality" (Anthropic, internal measurement).
* ([Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5))
* Sonnet 5.5: "Asking it in the system prompt to think less doesn't reliably reduce its thinking." Remove wording that discourages tool use. One paragraph against extra review rounds cut session cost by about a third, with no change in quality (Anthropic, internal measurement). ([Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5))
* Sonnet 5 "does not silently generalize an instruction from one item to another". State the scope. ([Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5))
* Anthropic says to replace "CRITICAL: You MUST use this tool when..." with "Use this tool when...". It says explaining why lets Claude generalize. Its own sources disagree on emphasis: one guide suggests "MUST" when a rule keeps being missed. ([Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices))
* Anthropic's skill-authoring guidance says: "Only add context Claude doesn't already have." It sets a 500-line limit for `SKILL.md`, keeps references one level deep, and wants a table of contents in any reference file over 100 lines. ([Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))

No controlled study was found that isolates the effect of removing the reason behind a rule. The skill's advice to keep a reason where a rule has edge cases rests on vendor guidance alone.

Sources were gathered on 2026-09-30.

## Installing

**Claude Code:**

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install skills-craft@davebben-skills
```

**Any other agent** (Codex, Cursor, Windsurf, and more), via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add DaveBben/davebben-skills --skill review-skill
```

The canonical `SKILL.md` lives at `skills/skills-craft/` in the repo root.

MIT.
