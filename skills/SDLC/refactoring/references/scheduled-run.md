# Scheduled run

A scheduled run proposes one refactoring and changes no code.

1. **Rank** files by changes in the last 90 days: `git log --since=90.days --format= --name-only | sort | uniq -c | sort -rn`. Drop files that no longer exist and files that hold no code, such as docs, lockfiles and JSON.
2. **Skip** a file named in the title of an open issue labelled `refactor`.
3. **Read** the top files for complexity and take the first that has a smell from [the catalogue](smells.md).
4. **Propose** one refactoring for it, written as the Report's `Smells:` line.
5. **File** it as one issue labelled `refactor`, titled `refactor: <path>: <smell>`, by the `using-trackers` skill, or print it when the repository has no tracker.

Once the user approves the issue, build it by the Build it section of `SKILL.md`.
