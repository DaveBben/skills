# AGENTS.md format

## Template

Write these five sections in this order. Omit a section that would be empty and needs no placeholder:

```markdown
## Project Identity

<!-- Purpose (one sentence: actor, observable result), Users, Not doing (checkable lines), Nouns (3-5 domain terms) -->

## Tech Stack and Codebase Map

<!-- Language, framework versions, package manager, directory layout, Boundaries (external systems), Backlog -->

## Operational Commands

<!-- Exact shell commands for build, test, lint, format, run -->

## Critical Constraints

<!-- Checkable statements, each ending with its enforcer (Budget row, gate check, ADR) or being a rule no tool can see -->

## Pointers to Deeper Docs

<!-- Descriptive file references — e.g., `spec.md` — product requirements and acceptance criteria -->
```

---

## Section-by-Section Guidance

### 1. Project Identity

The product charter. Purpose in one sentence naming an actor and an observable result, Users and what they do with the output, Not doing as checkable statements, and the three to five Nouns the code must use.

**Good:**
> Internal billing reconciliation service that pulls invoices from Stripe and NetSuite nightly,
> detects discrepancies, and opens tickets in Linear for the finance team to review. Exists because
> manual reconciliation was missing ~3% of mismatches each quarter.

**Bad:**
> This is a Python project that uses AWS CDK and boto3.

Technology belongs in Tech Stack, not here.

---

### 2. Tech Stack and Codebase Map

**Include:**
- Language and version (e.g., "Python 3.11")
- Framework and version if applicable (e.g., "AWS CDK 2.198.0")
- Package manager (e.g., "uv", "npm", "pnpm", "cargo")
- Top-level directory tree with one-line purposes
- Code generation tools if any (e.g., "XcodeGen generates .xcodeproj from project.yml")

**Good:**
```markdown
- Language: Python 3.11
- Infrastructure: AWS CDK 2.198.0 (via aws-cdk-lib)
- Package Manager: uv (with uv.lock, workspace mode)
- Formatting: black (line-length 88), isort
- Linting: flake8, ruff
- Testing: unittest, coverage

### Directory Layout
**Good:**
- `infra/` — CDK infrastructure definitions
- `src/functions/` — Lambda function handlers
- `src/layers/python/` — Shared Lambda layers
- `test/unit/` — Unit tests
- `test/integration/` — Integration tests
- `scripts/` — Utility scripts
- `bin/` — Shell scripts (deploy, test, lint, format)
- `app.py` — CDK app entry point
```

Keep the directory layout to top-level directories only. The module map `deliver` writes goes after the layout, as its modules table and its flows table.

End the section with Boundaries: every external system the product reads from, writes to, or runs inside, by name and address. Then the Backlog block. Its first line lists the tracker, the project and the access methods in order. The lines under it hold what an agent cannot look up: the criteria field, the checked blocking-link direction, the status names. Record methods, never which one worked in one session.

```markdown
Backlog:   Jira project PAY at https://acme.atlassian.net; Atlassian MCP server, else `acli jira`
  Criteria: field "Acceptance criteria"
  Blocks:   link type "Blocks"; `--out PAY-1 --in PAY-2` makes PAY-1 block PAY-2
  Status:   To Do, In Progress, In Review, Done
```

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

With no tracker: `Backlog: none; stories live in docs/delivery/`.

---

### 3. Operational Commands

**Include:** build, test, lint, format, run/deploy — whatever applies to the project.

**Good:**
```markdown
- `uv sync` — install dependencies
- `./bin/test.sh` — run linting + unit tests with coverage
- `./bin/test.sh -s` — run unit tests only (skip linting)
- `./bin/lint.sh` — run black (check), isort (check), flake8
- `./bin/format.sh` — auto-format with black + isort
- `coverage run -m unittest discover -v -s ./test/unit` — run unit tests directly
- `coverage report -m --omit="./test/*"` — show coverage report
```

**Bad:**
```markdown
- Run the tests before committing
- Make sure linting passes
- Install dependencies first
```

Write the command, never the instruction to find it.

---

### 4. Critical Constraints

Two kinds belong here: a checkable statement that ends with its enforcer (a Budget row in the test
table, a check in the commit gate, an ADR), and a rule no tool can see. Leave out a constraint with
neither.

**Good:**
- Never commit `.env` files or credentials
- All database migrations must be reversible
- Public API endpoints require authentication — no anonymous access
- Do not modify files in `vendor/` — they are managed by the dependency tool

**Bad:**
- Write good code
- Follow best practices
- Be careful with the database

With no hard constraints, leave the HTML comment placeholder.

---

### 5. Pointers to Deeper Docs

One line per document: file path + dash + purpose. Never copy a pointed-to document's content into
AGENTS.md.

**Good:**
```markdown
- `docs/specs/spec.md` — project spec, architecture, and spec index for all subsystem/feature specs
- `docs/architecture.md` — system architecture and component design
- `docs/api.md` — REST API endpoint reference
- `CONTRIBUTING.md` — pull request process and code review standards
```

Only list docs that exist, each by its exact path.
