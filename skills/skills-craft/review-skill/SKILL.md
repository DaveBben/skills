---
name: review-skill
description: "Use this skill when an agent skill or a subagent prompt must be reviewed, trimmed or tightened: a SKILL.md, its reference files, or an agent prompt file. Use it on: 'review this skill', 'review my SKILL.md', 'is this skill too long', 'tighten this skill', 'cut this skill down', 'make this skill shorter', 'why does the agent ignore this rule in my skill', 'will this skill work on Opus 5.5', 'audit the skills in this repo'. Reviews a skill and reports what to cut, change or add; edits only when asked."
license: MIT
compatibility: any-agent
metadata:
  version: "0.2.0"
---
# Review a skill

A skill is a set of instructions an agent loads into its context when a task matches the skill's `description`. Review it for one outcome: the agent that loads it does the task better than an agent without it, for fewer tokens. Every line is read on every run, so every line must change what the agent does.

## Read first

* **Read everything that loads together.** Read `SKILL.md`, each file it links, and any hook that injects text into the same session. Rules from all of these compete for the same attention.
* **Find what the skill prevents.** Name the task and the mistakes a capable model makes on it without the skill. When the skill does not say and the user cannot, ask. A line cannot be judged without knowing which mistake it prevents.
* **Check the format contract.** `name` is 1 to 64 lowercase letters, digits and hyphens, and matches its directory. `description` is at most 1,024 characters. `SKILL.md` is under 500 lines. Reference files sit one level deep, and a reference file over 100 lines opens with a table of contents.

## Cut

* **Knowledge the model already has:** general practice (write tests, handle errors, name things clearly), definitions of standard terms, and how common tools work. Ask whether a capable model would do it unprompted. When it would, the line costs tokens and changes nothing.
* **Anything the agent can read:** file trees, architecture overviews, and command lists that already sit in the repository. Measured: repository overviews in context files did not raise task success, and the files raised cost by more than 20%.
* **Generic rules:** "be careful", "write clean code", "avoid a generic look". A generic rule swaps one default for another. Replace it with the specific patterns it means, or delete it.
* **Checklists run on every task:** an agent treats a checklist as mandatory steps, including on tasks where a step does not apply. Excessive verification was the most common skill-caused failure in a study of 307. Keep a step only when skipping it caused a real failure, and state the case it applies to.
* **Effort and verification prompts:** "think carefully", "think step by step", "double-check your work", "think less" and "only use tools when strictly necessary" (Anthropic's Sonnet 5.5 guide says to remove that one). Current Claude models check their own work, and the effort setting controls thinking more reliably than prompt text. Removing these lines measured no loss in quality.
* **Emphasis:** ALL CAPS, CRITICAL, IMPORTANT, MUST, and stacked bold. Current models follow a plain instruction, and emphasis makes them apply the rule to cases it was not meant for. Write "Use X when Y." Keep one strong word only on a rule that testing shows is still missed.
* **Repeats:** the same rule in `SKILL.md` and a reference file, or in the skill and an always-loaded hook. Keep one copy, in the file that loads when the rule is needed.
* **Rationale written for a human:** design history, credits, and why the author changed their mind. Move it to the README, which no agent loads.
* **Perspective leak:** a line that describes the system the agent runs inside instead of the agent's own task, written from the view of whoever designed or launches it. Example: "You are review agent `<n>`, one of three working blind to each other." An agent launched by another agent starts with no memory and no colleagues, so the line prevents nothing, and telling it others share the work can lead it to skip what it assumes they cover. Keep only what the agent acts on: "Your number is `<n>`; it names your files." The same leak appears as what happens to the agent's output afterwards, who launched it, or why the design has this shape. Test each such line by deleting it: when the agent would act the same, cut it.

## Keep or add

* **Conventions that differ from defaults:** house naming, commit-message prefixes, file locations, and which of two tools to use. Agents measurably follow these, and cannot infer them. Measured: on release day, Opus 5.5 without a skill scored 0.30 on commit-message prefixes, and with the skill it matched Opus 5.
* **Named failure patterns:** list the exact wrong outputs, such as "stopping to report progress before the task is done" or "starting another review round after the reviewer passed". Name the right behaviour beside them. Named patterns change behaviour, and general warnings do not.
* **Explicit scope:** Claude 5-series models apply an instruction to what it names and do not extend it to similar items. List every case a rule covers. A filter such as "only report high-severity issues" is followed literally and lowers recall, so name what to report instead.
* **A reason where the rule has edges:** one clause of why lets the agent handle cases the rule does not list. Leave it out when the rule has no edge cases. This rests on vendor guidance, not a measurement.
* **Examples of the wanted output:** a few varied examples of the right result work better than a list of prohibitions or a catalogue of edge cases.
* **Complete sentences with correct punctuation:** shorten by deleting lines, never by compressing sentences. Measured: cutting agent instructions to 75% of their length cost 2 points, and cutting to 35% halved the score. A missing closing quote or a missing colon before a list dropped Opus 5.5 to 33% and 67% on the affected tasks, where typos had no effect.

## Size and structure

* **Count the rules:** add up the rules that load together across the skill, its references and any hooks. Adherence falls as the count rises. In a 2026 test, no model followed every rule once there were 80. Models also favour earlier rules, so put the rules most often broken first. Anthropic also suggests repeating one key constraint at the end of a long prompt.
* **Split by when it is needed:** `SKILL.md` holds what every run needs. Material only some runs need goes in a reference file that `SKILL.md` names, with the condition for reading it. Measured: focused skills with at most three modules beat larger bundles.
* **Write the description for triggering:** it is the only part loaded before the skill fires. Lead with the condition and the user's own phrases, then state what the skill does in one sentence. Leave the procedure out of it.
* **Distrust model-drafted lines:** skills a model wrote for itself scored at or below no skill in a 2026 benchmark. Check each line a model drafted against a failure the user actually saw.

## Model notes, September 2026

* **Opus 5.5:** effort defaults to medium and controls thinking. A paragraph at the end of the system prompt naming the early stops to avoid and the stops to make is followed.
* **Sonnet 5.5:** one paragraph telling it not to start extra review rounds cut session cost by about a third with no change in quality.

## Report

List findings ranked by expected effect on behaviour, then by tokens saved. Give each finding its location as `file:line`, the line, the action (cut, change or add), the replacement text for a change, and a one-sentence reason. Say when the reason rests on vendor guidance instead of a measurement. Example: `SKILL.md:26 — "Emphasis: ALL CAPS, CRITICAL..." — change — "Use X when Y." — current models over-apply emphasis. Vendor guidance.` End with the rule count and line count before and after the proposed changes.

Edit the skill only when the user asks. Only running the skill on real tasks with and without the change shows its effect.
