# Guide for agents

This file explains how to change `davebben-skills` without breaking a plugin, a skill, or the way agents install them.

## What this repo contains

`davebben-skills` is a collection of agent skills written in Markdown, grouped into one plugin per area of focus.

Skills work with any skills-compatible agent. Keep them portable. Do not write instructions that limit a skill to one agent's tools; name a tool as an example, not a requirement.

Plugins are independent. A user installs only the area they want, and one plugin's triggers never load alongside another's. Do not merge them or let one plugin's skill reference another's.

## Key files

- `skills/<area>/<skill>/SKILL.md` is the source of truth for a skill, with its reference files one level deep in `references/` beside it. This is the only place to edit a skill.
- `plugins/<area>/` is a thin Claude Code wrapper: a `plugin.json`, a README, and a `skills` symlink to `../../skills/<area>`. The symlink means one copy, not two. Do not replace it with real files.
- `.claude-plugin/marketplace.json` lets users add this repo as a Claude marketplace and lists every plugin.
- `README.md` explains installation and indexes the plugins. Rationale for a design lives here, not in a skill.
- `research/` holds source material and never loads into an agent.

## Rules for changes

- **Adding a plugin:** create canonical skills under `skills/<area>/`, a wrapper under `plugins/<area>/`, and one appended entry in `marketplace.json`. Full steps are in `README.md`.
- **Renaming a plugin** must update five things together: the `skills/<area>/` directory, the `plugins/<area>/` directory, the `name` in `plugin.json`, the entry in `marketplace.json`, and the README. The plugin `name` is the slash-command prefix, so a skill invokes as `/<plugin>:<skill>`.
- **Skill paths** in `marketplace.json` must be `./skills/<skill>`, relative to the plugin `source`, with no `..`. The schema forbids `..`; the symlink is what reaches the canonical files.
- **Version:** keep the version in a plugin's `plugin.json` equal to its `marketplace.json` entry, and bump both together.
- **Runtime reach:** nothing outside `skills/<area>/` reaches an agent, not this file, the READMEs, or `research/`. Every term a skill uses must be defined inside that skill.

## Writing a skill

Every skill must follow the [Agent Skills specification](docs/agent-skills-spec.md): a `SKILL.md` with valid `name` and `description` frontmatter, references one level deep, kept under 500 lines. That doc is the format contract; the rules below are how this repo writes within it.

A skill orients a capable agent; it is not a step-by-step procedure. Assume the agent is smart and give it the knowledge and conventions it lacks, not instructions it already knows.

- Write for the agent, not a human reader.
- Prefer precise terms over slang or vague description; agents misread ambiguity and human jargon.
- Keep the YAML metadata valid, and lead its `description` with the trigger.
- Treat the prose below the metadata as the product.
- Prefer one short, clear instruction over another exception or repeated explanation.
