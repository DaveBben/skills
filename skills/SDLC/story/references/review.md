# Review stories someone wrote

Read the stories from the tracker, the feature file, or what the user pasted. Change nothing without the owner's agreement. For each story, look for:

* **No outcome:** no role, nothing a person would notice once it ships, a `so that` that restates the feature, or no `Out of scope` lines.
* **Solution as need:** an `I want` that names a control or a design (a dropdown, a modal, a new table). Restate it as what the person can do.
* **Not testable:** an acceptance criterion with no concrete value, a vague word (better, faster, properly, handled), or a mechanism instead of what a person sees.
* **Not a story:** something a person cannot perceive alone (an enabler such as a column or a service, a property of another story's behaviour, a task). Name the story it folds into as an acceptance criterion.
* **Too big:** more than one path or variation, an `I want` joined by "and" or "or", or an acceptance criterion whose `when` is a different action or person. Propose the split by [split.md](split.md).
* **Dependent:** a story that cannot be built until another ships. Reorder, or fold the shared part into the earlier story, so each ships alone.
* **Dependent, still waiting:** name the blocker in `Order:`.
* **Duplicates:** two stories that are one. Search for one distinctive sentence and merge the stories containing it.
* **Missing paths:** a failure path or, for outside input, an abuse path the change can break, whose outcome no acceptance criterion states and the code does not settle.
* **Stale:** an acceptance criterion naming a route, a module or a design the code no longer has. Grep for it.

Check every candidate against the quoted text of its story. Keep it only when the text shows it. Report:

```text
<story>: <finding kind> — "<the quoted text>" — <what to change>
Ready to build: <stories with no finding>
```
