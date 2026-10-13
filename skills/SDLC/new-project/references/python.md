# Python projects

The template is the GitHub template repository `DaveBben/claude-ready-python-codebase`.
It is a src-layout package named `example_project`, managed by uv, with `./check`, Claude Code hooks, pre-commit and CI already wired.
Its `README.md` holds the authoritative rename steps under "Rename the template".
Follow them rather than any copy of them, because they change with the template.

## Names

Derive 3 names from the repository name, such as `invoice-sync`, one per placeholder name:

* **Distribution name:** `invoice-sync`, replacing `example-project`.
* **Import name:** `invoice_sync`, replacing `example_project`.
* **Exception prefix:** `InvoiceSync`, replacing `ExampleProject` in `ExampleProjectError`.

## Requirements

The template needs 2 tools beyond Python:

* **uv 0.9.17 or later:** when `uv --version` is older, ask the user to update it, such as with `uv self update`, and wait.
* **gitleaks on the `PATH`:** needed only by `./check --full`.
  When it is missing, name it to install and continue.

## Create

1. Create the repository from the template and clone it, from the parent directory.
   With the GitHub CLI:

   ```bash
   gh repo create <name> --template DaveBben/claude-ready-python-codebase --private --description "<purpose>" --clone
   cd <name>
   ```

   Pass `--public` instead when the user chose public.
   Without the GitHub CLI or a GitHub host, run `git clone --depth 1 https://github.com/DaveBben/claude-ready-python-codebase.git <name>`, delete its `.git` directory, then run `git init -b main`, `git add -A` and `git commit -m "Start from claude-ready-python-codebase"`, because the rename steps act only on tracked files.
   Create an empty repository on the user's host and add it as `origin`.
2. Follow every step of the cloned README's "Rename the template" section with the 3 names.
   In its step for the project's own text, write the `description` and the module docstring from the purpose, and replace `README.md` with the project's name, its purpose, and the setup and check commands from `AGENTS.md`.
   When a step of `./check` fails, the README missed a rename: fix it, and tell the user so the template's README can be corrected.
3. Set up the clone:

   ```bash
   uv sync
   uv run pre-commit install
   ```

4. Stage the rename with `git add -u`, which takes every renamed, edited and deleted tracked file and no stray file.
   Commit it and push with `git push -u origin main`.
