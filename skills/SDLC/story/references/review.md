# Review stories someone wrote

Read the stories from the tracker, the feature file, or what the user pasted. Change nothing without the owner's agreement. For each story, look for:

* **No outcome:** nothing a person would notice once it ships, or no `Not doing` lines.
* **Not testable:** a case with no concrete value, a vague word (better, faster, properly, handled), or a mechanism instead of what a person sees.
* **Not a story:** something a person cannot perceive alone (an enabler such as a column or a service, a property of another story's behaviour, a task). Say which story it folds into as a case.
* **Too big:** more than one workflow step or variation. Propose the split by [split.md](split.md).
* **Duplicates:** two stories that are one. Search for one distinctive sentence; the stories containing it are the ones to merge.
* **Missing paths:** a failure path or, for outside input, an abuse path with neither a case nor a `Not doing` line.
* **Stale:** a case naming a route, a module or a design the code no longer has. Grep for it.

Then check every candidate against the quoted text of the story it is about: keep it only when the text shows it, and drop it otherwise. Report:

```text
<story>: <finding kind> — "<the quoted text>" — <what to change>
Ready to build: <stories with no finding>
```
