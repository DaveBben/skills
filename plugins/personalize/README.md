# personalize

Skills that make an agent act as you.

| Skill | Fires on |
|---|---|
| `sound-like-me` | "reply to this for me", "draft a text to", "answer this comment", "comment on the MR", "comment on the Confluence page", "write this doc in my voice", "write a script for my video" |

## `sound-like-me`

Composes text that goes out as your own words. It picks one voice profile by audience and medium:
- casual texting;
- professional chat;
- informational writing;
- speaking.

It then writes by that profile. It never invents facts or commitments, never simulates typos, and shows you the draft instead of sending it.

### A reminder in every session

In Claude Code, the plugin's `SessionStart` and `SubagentStart` hooks print one line into every session and subagent. The line tells the agent to load `sound-like-me` before it drafts a merge request comment, a thread reply, or a comment on a Confluence, wiki or Google Docs page. Another plugin's skill that writes those comments, such as a code review, then picks up your voice without naming this plugin. Other agents rely on the skill's description alone.

### Your profiles stay private

The skill carries no voice of its own. It reads Markdown profiles from `$SOUND_LIKE_ME_DIR`, or `~/.config/sound-like-me/` when that variable is unset. They are kept outside this repo on purpose: a voice profile is built from your private messages and is unique to you, so it never belongs in a public repository. The skill also refuses to copy profiles into repos or outputs.

Expected files: `casual.md`, `professional-chat.md`, `writing.md`, `speaking.md`. Any file you leave out is simply unavailable, and the skill asks for it rather than guessing your voice.

### Building a profile

Build a profile from your own sent messages, docs or transcripts. Write it as concise, directive rules an LLM can follow: frequencies instead of quirk lists, a "default is plain" baseline, and do and don't pairs for the tells that give away LLM text.

Then check it blind:
1. Hold out real samples.
2. Have a model write from content-only briefs, once with the profile and once without.
3. Have a separate model score both against the real text.

Rules beat pasted examples in these tests. Expect a ceiling below "indistinguishable", because real replies carry context only you know.

## Installing

**Claude Code:**

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install personalize@davebben-skills
```

**Any other agent** (Codex, Cursor, Windsurf, and more), via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add DaveBben/davebben-skills --skill sound-like-me
```

The canonical `SKILL.md` lives at `skills/personalize/` in the repo root.

MIT.
