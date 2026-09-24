# Failure Modes

When working inside a constraint, ask whether it was chosen or inherited.

* **Developer-written stories.** The feature header lists what the agent could see, not what the user wants. Cause: the proposed stories were accepted unread, or named what the agent found in the code instead of what the user will do. Tell: story titles name mechanisms or read like tasks.
* **Inherited scope.** Every story shipped, nothing about the user's day changed. Cause: a spike's boundary became the project's boundary, or the delivering work sits behind a repo edge with no story. Tell: the feature header is precise about internals and silent about the user's day.
* **Unowned correctness.** All green, still not what was wanted. Two causes: a requirement with no test, fixed by mapping stories to tests in both directions; and a passing suite that never encoded the thing that matters, which only observing the shipped behaviour catches.
