---
name: sound-like-me
version: "0.1.0"
description: "Use this skill whenever the text you are composing will go out as the user's own words, in their voice: a text or DM to a friend, family member or partner; a reply, review comment or chat message to a coworker; documentation, a README, a design doc, a wiki page or a blog post written as the user; or a script, voiceover, talk or video narration the user will read aloud. Use it on: 'reply to this for me', 'draft a text to', 'write back to', 'answer this comment', 'leave a review comment', 'write this doc in my voice', 'write a blog post', 'write a script for my video', 'what should I say'. Load it before drafting, even for a one-line reply. Not for text in your own voice, such as explanations, summaries or code comments you author as the agent."
license: MIT
compatibility: any-agent
---
# Sound like me

The user's voice is described in private profile files that live outside this skill. Pick the profile that fits the message, read the whole file, and compose the text by following it. The profile is the style authority for this text, and it overrides your default prose habits and any general writing rules loaded in the session. It applies only to the text written as the user. Your own replies to the user keep your normal voice.

## Where the profiles are

The profiles are in the directory named by the `SOUND_LIKE_ME_DIR` environment variable. When that is unset, they are in `~/.config/sound-like-me/`. List the directory first. Each Markdown file there is one profile, and its filename and first lines say which situation it covers.

The expected files are:

| File | Use it for |
|---|---|
| `casual.md` | Texts, DMs and social replies to friends, family or a partner |
| `professional-chat.md` | Short work messages to coworkers: code review and merge-request comments, team chat, quick work replies |
| `writing.md` | Informational writing: documentation, READMEs, design docs, wiki pages, how-tos, blog posts and essays |
| `speaking.md` | Words the user will say aloud: video scripts, voiceovers, talks, presentation narration |

When the directory or the fitting file is missing, tell the user the path you checked and ask them to point you at a profile. Do not improvise their voice without one.

## Choosing a profile

Choose by audience and medium, not by topic. A technical question from a friend in a text thread is `casual.md`. A joke in a merge-request thread is `professional-chat.md`.

When no profile covers the medium, such as email, pick the nearest one and tell the user which one you used:
- A short work email → `professional-chat.md`.
- A long explanatory work email → `writing.md`.
- A personal email → `casual.md`.

When a message mixes registers, such as a coworker who is also a close friend, follow the register the thread itself is already in.

## Composing

- **Mirror the thread.** When replying, read the whole thread or document you are replying into, and match its energy, length and register as the profile directs.
- **Content comes from the user.** Never invent facts, plans, times, commitments, opinions or personal details the user has not given you or that the thread does not establish. When the message needs a fact you lack, ask for it, or leave a clearly marked placeholder such as `[time?]` and point it out.
- **No simulated typos or grammar slips**, even if the profile describes the user as making them.
- **Output only the message.** Put nothing inside it except the words the user would send or say. No preamble, alternatives or commentary. When a reply is several separate texts, show each one on its own line and say that they are separate messages.

## Sending

Composing is not sending. Show the draft to the user. Send, post or publish it on their behalf only when they tell you to, in this conversation, for this message.

## Privacy

The profiles are private. Never copy, quote or summarize a profile into any output, file, commit, pull request or public location. Never move or copy profile files into a repository.
