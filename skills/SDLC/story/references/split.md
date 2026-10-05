# Split a request into stories

* **Steps:** write the steps a person takes, in order.
* **Stories:** under each step, draft the stories that let a person do it, each with a title naming what the person can do and an outcome line.
* **Acceptance criteria:** write them for the first story only. Write each later story's when it starts, since building the first changes what the others need.
* **Reduce:** find the variation that makes the story big and reduce it to one.

Split a story that covers more than one path or variation with the first pattern that works:

1. The simplest path through every workflow step first; each extra step or branch its own story.
2. Create, then read, update, delete.
3. The simplest business rule first, each further rule its own story.
4. One kind of data first.
5. The plainest interface first.
6. The simplest version first, each complication its own story.
7. A timeboxed spike when something unknown blocks every pattern: the `spike` skill runs it, and its one acceptance criterion is the question it must answer. A second unknown is a second spike.

Rules for the stories:

* **Cut across layers, never along them:** a story that only adds a table or only adds an endpoint ships nothing a person can see.
* **Not stories:** a requirement on how well a story behaves, an enabler nobody perceives alone, and a task are acceptance criteria on the story that needs them.
* **Hardening:** fold it into the story that creates the exposure.
* **Order:** each story can be built and shipped without waiting on a later one.
* **Check before showing:** no two stories share a rule, and none needs a later one to ship.
* **Between two working splits:** prefer the one that lets the user drop a story, then the one with stories of roughly equal size.
* **Something new:** mark as the first story the thinnest slice across all the steps that a real person can use end to end, with hard-coded data where that keeps it thin.

Then agree it:

* **Show the user** the steps, the stories in their proposed order, and the owning story with its proposed `Outcome:` and `Measure:` in one message. Read the measure's value now with a tool where one reaches it, else ask the user for it.
* **Write the stories** only after the user confirms: as issues by the `using-trackers` skill, each blocked by the one before it, or as the feature file in build order.
* **An open decision a story waits on:** goes under that story's `Open questions`.
* **A story found while building:** add it after the stories already ordered, unless the user moves it.
* **Feature acceptance test:** when the user wants one, they write it, marked strictly expected-to-fail. Build each story from its own acceptance criteria.
