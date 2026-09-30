# Plan step: record the shape

Write the agreed shape by "Write a snapshot" in `SKILL.md`, also giving the subagent the Map tables as the user left them, the Numbers, the `Decided:` ADR paths and the `Deferred:` lines, told to head the snapshot "planned, not yet built". The checkout is the repository, and the branch is the plan branch `story/{slug}/0-plan`, or main in a repository with no remote. On the plan branch, open one pull request holding the plan's ADRs, the snapshot and the `AGENTS.md` change, which the user merges before the first story.

Hand the in-process flows to the `guardrails` skill as dependency contracts, with the directories the user reads on every change (who may do what, secrets, money, health or personal data, migrations, deploys) as `# owner reads: data` lines for `CODEOWNERS`. A story that changes a process, a store, a module or a flow writes a new snapshot in its last commit. Then `deliver` builds, starting at the walking skeleton.
