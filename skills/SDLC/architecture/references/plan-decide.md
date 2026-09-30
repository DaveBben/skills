# Plan step: decide

List what the outcome touches and cannot cheaply reverse: the repositories and the language and platform of each; every flow crossing a process, machine or repository; per store, what makes a record unique, the rules the data always keeps (preferring database constraints), retention and deletion, backup and a proved restore, and how the schema changes; the trust and consistency boundaries; each choice a number or the sensitive-data answer forces.

Read the latest snapshot `AGENTS.md` points at and the titles under `docs/adr/`, skipping superseded ones, and state what the code and those records already settle, with the file. Put each other item to the user one per message: the problem, the constraints, and the alternatives with their tradeoff, marking none as recommended. Ask which the user would pick, and wait. "Not sure" or "you pick" is an answer: give the recommendation and its reason, and record it. Once they answer, say in one sentence whether the agent would have picked differently and why, and in the same message any tradeoff, alternative or untested hazard the answer missed. Record each answer by `record-decision.md` in this folder before the next question and before any code that depends on it.

* **A third-party service** the tests cannot use at the volume or failure modes needed gets an ADR for a twin: a fake under `tests/twins/<service>/` whose contract suite runs against the twin in every check and against recorded real responses on a schedule.
* **Data the system cannot regenerate** puts a restore criterion on the story that first stores it.
* **A smaller choice a later story inherits** (a port, a schedule, a file format, a name that becomes a domain noun): ask, unless the ranked qualities in `docs/architecture/summary.md` pick one; then decide it and name the quality.
* **A choice nothing inherits and nobody sees:** decide alone and list it.

Each item ends Decided (an ADR on `Decided:`), Deferred (on `Deferred:` with what will force it; propose this for each item the first story does not touch), waiting on a spike (run by "Run a spike" in `SKILL.md`), or settled by the code. No story that needs an item starts before then.

When deciding one open item, stop once it has ended. Otherwise, once every item has ended, read `plan-stand-up.md` in this folder for a new application, else `plan-record.md`.
