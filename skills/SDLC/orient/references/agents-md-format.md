# AGENTS.md format

Guidance for each section of the template in `SKILL.md`. Omit a section that would be empty.

### 1. Project Identity

The product charter. Purpose in one sentence naming an actor and an observable result, Users and what they do with the output, Not doing as checkable statements, and the three to five Nouns. Technology belongs in Tech Stack, never here.

### 2. Tech Stack and Codebase Map

Language and version, framework and version, package manager, any code generation tool, and the top-level directories only, each with a one-line purpose.

End the section with Boundaries: every external system the product reads from, writes to, or runs inside, by name and address. Then the Backlog block. Its first line lists the tracker, the project and the access methods in order. The lines under it hold what an agent cannot look up: the criteria field, the checked blocking-link direction, the status names. Record methods, never which one worked in one session. With no tracker: `Backlog: none; stories live in docs/delivery/`.

For an in-house tracker, one line per operation, with the command or endpoint and `{epic}`, `{key}`, `{file}` placeholders. The commands below are illustrative, not a real tool:

```markdown
Backlog:   Acme Tickets at https://tickets.acme.internal; `tix` CLI
  list:     tix list --parent {epic} --json   (order is rank; blockers in .blocked_by)
  read:     tix show {key} --comments --json
  create:   tix new --parent {epic} --type {story|bug|spike} --title "{title}" --body-file {file}
  describe: tix edit {key} --body-file {file}
  block:    tix link {blocker} blocks {blocked}
  comment:  tix comment {key} --body-file {file}
  status:   tix move {key} "{status}"
  rank:     none; the user ranks by hand
  pr:       tix link-url {key} {url}
```

The section ends with a `### Architecture` heading, after Boundaries and Backlog, holding the three tables the `architecture` skill writes: processes, modules and flows. A flow inside one process leaves the table once the `guardrails` skill has written its dependency contract.

### 3. Operational Commands

The exact command for install, build, test, lint, format, run and deploy, whichever apply, each with a one-line purpose. Write the command, never the instruction to find it.

### 4. Critical Constraints

Two kinds belong here: a checkable statement that ends with its enforcer (a Budget row in the test table, a check in the commit gate, an ADR), and a rule no tool can see. Leave out a constraint with neither.

### 5. Pointers to Deeper Docs

One line per document that exists: its exact path, a dash, and its purpose, such as `docs/adr/` for decision records and `docs/delivery/` for the feature logs. Never copy a pointed-to document's content into `AGENTS.md`.
