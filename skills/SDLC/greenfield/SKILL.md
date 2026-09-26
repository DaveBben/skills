---
name: greenfield
description: "Use this skill when a new repository must be stood up from a language template, usually called by `architecture` once it has decided the repository's language. Use it on: 'python project template', 'template project', 'create scaffolding for this repository', 'bootstrap a codebase from a template'. Clones a language template, or runs the language's own project generator when no template exists, renames it, proves its default state passes tests, then removes what this project does not need, committing every step. Not for planning a new application or work asked for in an empty repository (`architecture`), a codebase that already has an application (`deliver`), or throwaway code (`spike`)."
license: MIT
compatibility: any-agent
metadata:
  version: "0.6.0"
---
# Greenfield Codebase Setup

Stand up a new project from a known-good template instead of an empty directory.

Never rebuild the toolchain, test runner, linting, or CI from scratch.

## Select the Template

The language is a decision that is expensive to reverse. Take it from its ADR (architecture decision record), the file the `architecture` skill wrote under `docs/adr/` in the first repository on the `Repositories:` line. That line is in the feature header, the `## Feature` block at the top of `docs/delivery/{slug}.md`, where `{slug}` is the work's short name. When the user named the language in this request, continue, and record it as an ADR in the new repository, on main, right after step 1, with the `architecture` skill's path for recording one decision. Otherwise, with no such ADR, run the `architecture` skill first; it owns a new application's path and calls this skill back. This skill runs once per repository that line marks `new: <name> <directory>`.

Only clone a template that exists for the project's primary language.

| Language | Template |
| --- | --- |
| Python | https://github.com/DaveBben/claude-ready-python-codebase |

If the language has no template listed, say so and ask the user whether to add one or proceed without a template. Do not substitute a different language's template. Without a template, step 1 runs the platform's own project generator for the kind of app being built (`cargo new`, `npm init` are examples) into the target directory; when the platform has no command-line generator, as for an iOS app, ask the user to create the project and continue from step 2. Step 1 also adds a test runner with one passing test when the generator creates none. Steps 2 to 6 then run as written.

## Confirm Before Cloning

Take both facts from the `new:` line when `architecture` called this skill. Otherwise ask the user for them before touching the filesystem:
* **Project name:** The kebab-case or snake_case name that replaces `example_project` throughout the clone.
* **Target directory:** Where the new repository lives. Default to a sibling of the current working directory named after the project.

## The Setup Sequence

Commit at the end of each numbered step with the stated message.

### 1. Clone and detach

* Clone the template into a scratch directory and remove its `.git` directory to sever its history.
* When the target directory already holds a repository, as it does after the `architecture` skill created one for the feature log and ADRs, copy the template's files into it beside `docs/`. Otherwise run `git init -b main` in the target directory and copy the template in.
* Stage the full template as the initial state.
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

### 6. Hand back

* Rewrite the repository's `new:` line to its remote URL, or its local path when it has no remote, and commit that in the first repository on `Repositories:`.
* Return to `architecture` when it called this skill; otherwise hand off to `deliver` once the template is clean.

## Guardrails

* **Green at every commit:** The test suite passes before step 4 and after step 5.
* **Do not add features:** Do not write business logic, add new dependencies, or design architecture here. The `architecture` skill decides the shape.
* **Preserve the toolchain:** Do not remove the test runner, linter, formatter, or CI configuration.
