# personalize

Skills that make an agent act as you.

| Skill | Fires on |
|---|---|
| `sound-like-me` | "reply to this for me", "draft a text to", "answer this comment", "comment on the MR", "comment on the Confluence page", "write this doc in my voice", "write a script for my video" |
| `setup-my-env` | "set up my environment", "set up my new Mac", "make my terminal readable", "configure VS Code for readability", "make Obsidian easier to read", "the colors look off in light mode" |

## `setup-my-env`

Configures your apps for readable text and records how, so a new machine or a new app gets the same result.
`SKILL.md` holds the working rules: back up first, find where the app really stores its settings, change one app at a time, and verify by reading the value back and measuring a screenshot.
The detail loads only when readability work starts, from `references/readability.md`: the targets with their evidence labels, the size and line-width formulas, a procedure for any app, the exact values applied to iTerm2, zsh, Claude Code, VS Code and Obsidian on 2026-10-02, and the mistakes made that day.
`scripts/contrast.py` computes WCAG contrast and fixes a failing color by lightness while keeping its hue.

The targets come from reading research: text size by visual angle (Legge and Bigelow 2011), light-mode advantage tied to screen brightness (Buchner, Mayr and Brandt 2009; Piepenbrock et al. 2014; Dobres et al. 2017), line length on screen (Dyson 2004), and contrast thresholds from WCAG 2.2.

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
npx skills add DaveBben/davebben-skills --skill sound-like-me --skill setup-my-env
```

The canonical `SKILL.md` files live at `skills/personalize/` in the repo root.

MIT.
