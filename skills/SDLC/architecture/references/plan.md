# Plan a system: sections 2, 3, 4, 6 and 7

Load this for the plan path and the new-application path in `SKILL.md` section 1, and section 4 alone for the map path. Section 5, Decide, is in `SKILL.md`.

## 2. Crossings and exploration

A crossing is a place the walking skeleton's outcome passes from one running piece into another: a database, a third-party API, a host, a device, a queue, another repository.

* **List every crossing** the walking skeleton makes.
* **Ask which crossings someone has already made work** in this stack. The user decides which count as tried.
* **Run a spike on each untried crossing before section 3.** Frame its falsifiable question, finish line and timebox with the user, such as "the app can read Health data while the phone is locked". Then run the `spike` skill in a subagent with that frame, the feature's slug and the spike's number on `Stories:`. It commits its findings where the plan is committed and returns its verdict and its decision table; put the table to the user and record each row marked `record`. Sections 3 to 5 use the findings.

## 3. Numbers and sensitive data

Skip any answer `AGENTS.md` already records. Ask the rest in one message:

* How many people or requests at once.
* How long a response may take, and for what share of requests.
* How much downtime is acceptable, per month.
* How much data there is now, and how fast it grows.
* Which data is sensitive (health, personal, financial, credentials), where it may be stored, and whether it must be encrypted on disk and on the wire. Sensitive data in a log line or an error message counts as stored.

Write each answer as a constraint with its enforcer: under Critical Constraints in `AGENTS.md` when it holds for the whole system, or on the feature header's `Constraints:` line when it holds for one feature. Before `AGENTS.md` exists, write every number on the feature header. A number goes only into the repository whose Budget test asserts it. The enforcer is a Budget row: a test asserting the number, which the `story` skill proposes for every change that touches it. Accept "unknown" and write it as unknown. An unknown number defers every decision that depends on it and never blocks the walking skeleton.

## 4. Map

Propose three tables, only for what the outcome touches, and stop. The user edits them in one turn; a row not changed is accepted.

```text
| Process | Repository | Machine | Copies | Started by |
|---|---|---|---|---|
| <name> | <a repository from the Repositories: line, or "-" for a service someone else runs> | <the machine it runs on, or "external: <address>"> | <1, one per <thing>, or n threads> | <boot, a request, a schedule, an event> |

| Module | Process | Owns |
|---|---|---|
| <name, in the domain's nouns> | <a process from the first table> | <the one thing it is responsible for> |

| From -> To | What crosses | How | When To fails | Who else reaches To |
|---|---|---|---|---|
| <caller> -> <callee> | <the data sent, and the data returned> | <in-process call, HTTP, queue, file or event, and whether From waits for the answer> | <what the person sees when To is down or slow, or "-" for an in-process call> | <who else can send to To, and how To checks the caller is From; "-" for an in-process call> |
```

* **Ask who else reaches To** for every flow that crosses a machine, a database included: the local network, the internet, another app on the device. Then ask how To checks the caller: a credential, a certificate, or where it sits on the network. For a database, also ask which account From uses and what that account may do. "Only the home network can reach it" is an answer the user may choose; record it as an accepted risk. Each answer is a section 5 decision, and its test sends the call without the check and expects a refusal.

* **Copies times connections is a number to check.** The copies of each process times the connections each holds must stay under the limit of whatever it connects to. A scheduled process running beside request traffic can hold locks the requests wait on.
* **A module owns one thing.** When its Owns cell needs "and", a list or an arrow, it is two modules or a flow. State existing modules from the code, with their directory. Propose new ones.
* **Map only what the outcome touches.** Leave out files, libraries, story numbers, behaviour details and deletions. The build decides files and libraries. A schema change is a decision for section 5.
* **Flows point one way.** From depends on To. A cycle is a finding, not a row. When To must call back into From, From defines a port, and the port is its own module that To depends on.
* **A flow that crosses a process, a machine or a repository is a decision.** Its How and When To fails cells go to section 5 unless the code or an ADR already settles them.
* **Name a pattern only for a flow that needs one.** Use a port when To must be faked in tests or swapped. Use a queue when From must not wait for To. Write the pattern in the flow's How cell with the one rule it enforces, e.g. "port: listener imports the display port, never display.py". Never walk the user through a pattern catalogue. The builder picks the simplest thing that passes the tests for every other flow.
* **The walking skeleton crosses every flow with real code.** It hardcodes data, never a crossing. A module the walking skeleton does not reach stays off the map until the story that needs it.
* **Contract first at a shared boundary.** Where To is called by another team, another service or another repository, write the executable contract (OpenAPI, Protobuf, strict interface types) and assert it in a test before any code sits behind it.

## 6. Record and revise

* **Write the tables into `AGENTS.md`** under a `### Architecture` heading inside Tech Stack and Codebase Map. Before `AGENTS.md` exists, write them into the feature log below the feature header; the `orient` skill moves them, and the numbers, into `AGENTS.md` when it writes that file. Commit them with the plan. Each repository's `AGENTS.md` holds the processes whose Repository cell names it, the modules whose process runs in it, and the flows whose From module is in it. Keep every table cell under 40 characters.
* **A flow inside one process leaves the Flows table** once the `guardrails` skill has written its dependency contract ("From may import To"), so a reversed dependency fails the build. Hand the in-process flows to `guardrails` in a subagent once the tables are recorded. `AGENTS.md` stays under its 100-line cap this way.
* **Ask which modules the user reads on every change:** those deciding who may do what, or touching secrets, money, health or personal data, schema migrations or deploys. The user reads other code only when a pull request points to it. Hand those modules' directories to `guardrails` with the flows, as `# owner reads: data` lines of `CODEOWNERS`.
* **Rewrite the tables in the last commit of any story's branch** that changes a process, a module's name or Owns cell, or a flow.

## 7. A new application: stand up and hand on

Once each new repository's language is decided and every other item the walking skeleton needs is in one of the four states, run the `greenfield` skill in a subagent once per repository marked `new:` on `Repositories:`. It takes the name and directory from that line, rewrites the line to the remote URL or local path, and returns the `orient` skill's interview questions for that repository; ask them and reissue it with the answers. Then return to `deliver` when it called this skill, or run it; it starts at the walking skeleton.
