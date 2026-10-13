---
name: new-project
description: "Use this skill whenever a new software project, repository or codebase must be started, whether the user, the session or another agent wants it: a new app, service, CLI, library or script that will live in its own repository. Use it on: 'start a new project', 'new Python project', 'new Python repo', 'create a new repo for X', 'scaffold a project', 'bootstrap a service', 'set up the template for a new project', 'spin up a repo for this idea', 'I want to build X from scratch'. Load it before creating the first file or running a scaffolding tool such as `uv init`. Creates the repository from the user's template for its language, renames the template's placeholder names, and commits only once the checks pass. Not for adding checks to a repository that exists; that is `guardrails`. Not for a throwaway prototype; that is `spike`."
license: MIT
metadata:
  version: "1.1.0"
---
# New project

A new project starts from the user's template for its language, so it has the check command, the agent hooks, the CI workflow and `AGENTS.md` from its first commit.
Never scaffold from nothing with a language's own tool, such as `uv init`, `cargo new` or `npm create`, while a template exists for that language.

## Templates

Each language has its template and the steps to create from it in one reference file.
Read the file for the project's language before running any command.

* **Python:** [references/python.md](references/python.md).
* **Any other language:** no template exists yet.
  Tell the user so, and once the user agrees, scaffold with the language's own tool.
  Then set up the checks by the `guardrails` skill and write `AGENTS.md` by the `orient` skill.

## Ask once

Ask in one message, only for what the request does not already say.
Offer language and visibility as choices, with the harness's multiple-choice tool where it has one (Claude Code's AskUserQuestion), and ask for name and purpose as text.

* **Language:** when the request names none.
* **Name:** the repository name, in lowercase with hyphens, such as `invoice-sync`.
* **Purpose:** one sentence on what the project does, for its description and README.
* **Visibility:** private or public on GitHub, or on the user's Git host when it is another, private by default.
* **Parent directory:** the directory holding the user's other repositories, such as `~/projects`.
  Ask only when none is evident.

## Done means

The project is set up when all of these hold:

* **No placeholder left:** a case-insensitive search of every tracked file for the template's placeholder names prints nothing.
* **Checks pass:** the repository's `./check` exits 0 on the renamed project.
* **Hooks installed:** the template's commit hooks are installed in the clone's `.git/hooks`, so the rename commit ran them.
* **Pushed:** one commit holding the rename is on the host's main branch.

Report the repository's URL, its local path and anything the user must install, such as a tool version the template requires.
Tell the user to start the next session inside the new repository, because its hooks and `AGENTS.md` load only in a session started there.
Write no feature code during setup.
The project's first behaviour is a change to code that exists, so build it by the `story` skill.
Its first story is a tracer bullet: the thinnest slice a person can use end to end, kept and grown, unlike a throwaway prototype.
Offer to schedule the `refactoring` skill's scheduled run for the repository, such as a weekly Claude Code routine or a CI cron job, and set it up only on the user's yes.
A stack or library choice that costs more than a day to reverse goes to the `adr` skill.
