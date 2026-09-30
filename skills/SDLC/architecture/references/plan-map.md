# Plan step: map

Propose three tables, only for what the outcome touches, and let the user edit them in one turn.

```text
| Process | Repository | Machine | Copies | Started by |
| Module | Process | Owns |
| From -> To | What crosses | How (and whether From waits) | When To fails, what the person sees | Who else reaches To, and how To checks the caller |
```

* **A module owns one thing.** An Owns cell that needs "and" is two modules or a flow. State existing modules from the code, with their directory.
* **Flows point one way.** A cycle is a finding. When To must call back, From defines a port that To depends on.
* **Name a pattern only where a flow needs one:** a port when To must be faked or swapped, a queue when From must not wait.
* **Copies times connections** stays under the limit of what they connect to.
* **Ask who else reaches To** for every flow that crosses a machine, and how To checks the caller. Each answer is a decision in the next step.
* **Contract first** where another team, service or repository calls To: an executable contract (OpenAPI, Protobuf, strict types) asserted in a test before code sits behind it.

The tables as the user leaves them are the agreed shape. Then read `plan-decide.md` in this folder.
