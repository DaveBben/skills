---
name: greenfield
description: "Use this skill whenever a project does not exist yet and the user wants one stood up, or asks for a template, scaffolding, a blueprint, a bootstrap or a walking skeleton. Use it on: 'let's setup a new project', 'I want to start a new python/javascript project', 'let's create scaffolding for an iOS app', 'let's put together the walking skeleton', 'python project template', 'template project', 'bootstrap a codebase'. Use it even on a bare two-word ask like 'template project': a new codebase is never the one-step answer it sounds like. Use it too when the ask names a feature, endpoint, test or CI setup but the repo has no application yet. A health check, test or CI run needs code first, so spot an empty or app-less repo before reading the ask as `agile`, and stand up the project first. Clone a language template, rename it, prove the default state passes tests, then strip it to what this project needs, committing every step. Do not use it to change a codebase that already exists; that is `agile`."
license: MIT
compatibility: any-agent
metadata:
  version: "0.4.0"
---
# Greenfield Codebase Setup

Stand up a new project from a known-good template instead of an empty directory. Clone the template for the project's language, rename it, prove the default state passes, then remove everything the project clearly will not use. Commit after every discrete change so the history shows the reduction from template to project.

The template supplies the toolchain, test harness, linting, and CI already wired and passing. Do not rebuild these from scratch. Start from green and subtract.

## Select the Template

Match the project's primary language to a template repository. Only clone a template that exists for that language.

| Language | Template |
| --- | --- |
| Python | https://github.com/DaveBben/claude-ready-python-codebase |

If the user's language has no template listed, halt. State that no template exists for that language and ask the user whether to add one or proceed without a template. Do not substitute a different language's template.

## Confirm Before Cloning

Ask the user for two facts before touching the filesystem:
* **Project name:** The kebab-case or snake_case name that replaces `example_project` throughout the clone.
* **Target directory:** Where the new repository lives. Default to a sibling of the current working directory named after the project.

## The Setup Sequence

Execute these steps in order. Commit at the end of each numbered step with the stated message. Never batch multiple steps into one commit.

### 1. Clone and detach

* Clone the template into the target directory.
* Remove the template's `.git` directory to sever its history.
* Run `git init` and stage the full template as the initial state.
* **Commit:** `chore: import <language> template`

### 2. Rename the project

* Replace every occurrence of `example_project` (and any case variants like `ExampleProject` or `EXAMPLE_PROJECT`) with the project name across file contents and file/directory paths.
* Grep the tree afterward to prove zero occurrences of the template name remain.
* **Commit:** `chore: rename example_project to <name>`

### 3. Prove the default state passes

* Install dependencies using the template's declared toolchain.
* Run the full test suite. It must pass on the unmodified template.
* If tests fail before any removal, halt. A failing default state is a template defect or an environment problem — do not proceed to strip files against a broken baseline. Report the failure to the user.
* **Commit:** only if install or the rename produced lockfile or config changes — `chore: verify default state passes`

### 4. Strip docs to the project

* Replace the template `README.md` with a minimal one stating the project name and its one-line purpose.
* Run the `orient` skill to write `CONTEXT.md` and `AGENTS.md`, with `CLAUDE.md` symlinked to it. These are the files every later session reads first; when the template shipped an instructions file, `orient` shows the mapping and asks before rewriting it.
* Remove template-authored docs that describe the template itself rather than the project (contributing guides, changelogs, example docs).
* Preserve `LICENSE`, CI config, and any doc the project will keep filling in.
* **Commit:** `docs: reset template docs for <name>`

### 5. Remove clearly unneeded files and dependencies

* Remove sample or demo modules the project will not build on.
* Remove dependencies that only served the removed samples. Edit the dependency manifest, not just the imports.
* Remove optional tooling the project has explicitly declined.
* **Only remove what is clearly unneeded.** When a file's necessity is ambiguous, keep it and ask the user rather than guessing.
* Re-run the full test suite after removal. It must still pass.
* **Commit:** `chore: remove unused template files and dependencies`

## Guardrails

* **Green at every commit:** The test suite passes before step 4 and after step 5. Never commit a state where the suite is red.
* **Subtract, do not add features:** This skill scaffolds. Do not write business logic, add new dependencies, or design architecture here. Hand off to `agile` once the skeleton is clean.
* **Ask on ambiguity:** Removing a file is easy to reverse in git but easy to get wrong. When unsure whether the project needs a file or dependency, keep it and ask.
* **Preserve the toolchain:** Do not remove the test runner, linter, formatter, or CI configuration. These are the reason to start from a template.
