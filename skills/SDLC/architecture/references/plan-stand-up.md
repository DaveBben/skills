# Plan step: stand up a repository

For each new repository, run this skill's `scripts/scaffold.sh` `<template> <name> <directory> <test command>`. It clones the template, strips its history, renames `example_project`, runs the tests and commits each step. The Python template is `https://github.com/DaveBben/claude-ready-python-codebase`, tested with `uv run pytest`. With no template for the language, run the platform's own generator (`cargo new`, `npm init`) and add one passing test. Then replace the README with the project name and one sentence, delete docs that describe the template, remove sample modules and the dependencies only they used, keeping anything ambiguous, and run the tests again, then commit. Rewrite the `new:` line to the remote URL or path. Then run the `guardrails` skill for `AGENTS.md` and the checks.

Once every new repository stands, read `plan-record.md` in this folder.
