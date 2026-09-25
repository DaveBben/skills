---
name: greenfield
description: "Use this skill when a project does not exist yet and the user wants one stood up, or asks for a template, scaffolding, a bootstrap or a walking skeleton. Use it on: 'let's set up a new project', 'I want to start a new python/javascript project', 'create scaffolding for an iOS app', 'put together the walking skeleton for a new repo', 'python project template', 'template project', 'bootstrap a codebase'. Use it too when the ask names a feature, endpoint, test or CI setup but the repository has no application yet, since those need code first. Clones a language template, renames it, proves its default state passes tests, then removes what this project does not need, committing every step. Not for a codebase that already has an application (`deliver`), or throwaway code (`spike`)."
license: MIT
compatibility: any-agent
metadata:
  version: "0.5.0"
---
# Greenfield Codebase Setup

Stand up a new project from a known-good template instead of an empty directory.

Never rebuild the toolchain, test runner, linting, or CI from scratch.

## Select the Template

Only clone a template that exists for the project's primary language.

| Language | Template |
| --- | --- |
| Python | https://github.com/DaveBben/claude-ready-python-codebase |

If the user's language has no template listed, halt. State that no template exists for that language and ask the user whether to add one or proceed without a template. Do not substitute a different language's template.

## Confirm Before Cloning

Ask the user for two facts before touching the filesystem:
* **Project name:** The kebab-case or snake_case name that replaces `example_project` throughout the clone.
* **Target directory:** Where the new repository lives. Default to a sibling of the current working directory named after the project.

## The Setup Sequence

Commit at the end of each numbered step with the stated message.

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

* Install dependencies using the template's declared toolchain. If that toolchain's command is not installed, halt and name the missing command. Do not substitute a different package manager.
* Run the full test suite.
* If tests fail before any removal, halt.
* **Commit:** only if install or the rename produced lockfile or config changes — `chore: verify default state passes`

### 4. Remove template docs

* Replace the template `README.md` with this shape and nothing else:

```markdown
# <project-name>

<one sentence naming what the project does>
```

* Run the `orient` skill to write `AGENTS.md`, with `CLAUDE.md` symlinked to it.
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

* **Green at every commit:** The test suite passes before step 4 and after step 5.
* **Do not add features:** Do not write business logic, add new dependencies, or design architecture here. Hand off to `deliver` once the skeleton is clean.
* **Preserve the toolchain:** Do not remove the test runner, linter, formatter, or CI configuration.
