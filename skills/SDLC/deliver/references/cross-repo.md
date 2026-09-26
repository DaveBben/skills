# A story that spans repositories

Load this when a story changes more than one repository.

Cut a branch with the same name in each repository the story changes, taken from the feature header's `Repositories:` line; for a one-story request with no header, from the request, or ask. Open one pull request per repository. Order them by parallel change (Martin Fowler, "ParallelChange", https://martinfowler.com/bliki/ParallelChange.html), which splits an incompatible interface change into expand, migrate and contract:

1. **Expand.** The pull request in the repository being called goes first. Its contract test lands first. The new form sits beside the old one, so existing callers keep working, and it merges and deploys on its own.
2. **Migrate.** The pull request in the calling repository merges after the first has merged.
3. **Contract.** When an old form exists, removing it is a later story on `Stories:`, blocked by the story that migrated the last caller.

Each pull request links the others. Setup, build, review and verify run once per repository, in expand-then-migrate order. The feature log, the ADRs and the feature acceptance test live in the first repository on `Repositories:`. The log commit goes on that repository's branch, which merges after every other pull request of the story. When the first repository's own change is the expand step, or the story does not change the first repository, the log goes in a log-only pull request there after the others merge. The story is done when all of its pull requests have merged, in every repository.
