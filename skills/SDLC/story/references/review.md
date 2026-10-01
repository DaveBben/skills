# Review stories someone wrote

Read the stories from the tracker, the feature file, or what the user pasted. Change nothing without the owner's agreement. For each story, look for:

* **No outcome:** no role, nothing a person would notice once it ships, a `so that` that restates the feature, or no `Out of scope` lines.
* **Solution as need:** an `I want` that names a control or a design (a dropdown, a modal, a new table) instead of what the person can do. Restate it as the need.
* **Not testable:** an acceptance criterion with no concrete value, a vague word (better, faster, properly, handled), or a mechanism instead of what a person sees.
* **Not a story:** something a person cannot perceive alone (an enabler such as a column or a service, a property of another story's behaviour, a task). Say which story it folds into as an acceptance criterion.
* **Too big:** more than one workflow step or variation, or an acceptance criterion whose `when` is a different action or person. Propose the split by [split.md](split.md).
* **Dependent:** a story that cannot be built until another ships. Reorder the stories, or fold the shared part into the earlier one, so each can ship on its own; when one still must wait, name the blocker in `Order:`.
* **Duplicates:** two stories that are one. Search for one distinctive sentence; the stories containing it are the ones to merge.
* **Missing paths:** a failure path or, for outside input, an abuse path with neither an acceptance criterion nor an `Out of scope` line.
* **Stale:** an acceptance criterion naming a route, a module or a design the code no longer has. Grep for it.

Then check every candidate against the quoted text of the story it is about: keep it only when the text shows it, and drop it otherwise. Report:

```text
<story>: <finding kind> — "<the quoted text>" — <what to change>
Ready to build: <stories with no finding>
```
