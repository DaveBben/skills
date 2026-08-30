# context

Skills for managing an agent session's context across boundaries.

One skill today. More will follow as the ways a session runs out of context, or has to move between agents, get their own handling.

| Skill | Fires on |
|---|---|
| `handing-off` | "write a handoff", "I'm running low on context", "I want to pick this up later", "summarise this for next time" |

## `handing-off`

Writes `docs/agents/handoff/YYYY-MM-DD-NNN-slug.md`, proposing the filename and waiting for confirmation before writing anything. It records what was accomplished, the key decisions, **the dead ends and what went wrong with each**, where things stand as one concrete next step, and the context a fresh agent would otherwise re-derive.

The dead ends are the reason it beats built-in compaction: a fresh session with no record of the failed approaches will find them again. A handoff that reads as though everything went well is worse than none, because the next session trusts it.

## Installing

**Claude Code:**

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install context@davebben-skills
```

**Any other agent** (Codex, Cursor, Windsurf, and more), via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add DaveBben/davebben-skills --skill handing-off
```

The canonical `SKILL.md` lives at `skills/context/` in the repo root.

MIT.
