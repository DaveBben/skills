# Split a request into stories

Write the steps a person takes, in order. Under each step, draft the stories that let a person do it, each with a title naming what the person can do and an outcome line. Write cases only for the first story; each later story's cases are written when it starts, since building the first one changes what the others need.

Split a story that covers more than one step or variation with the first pattern that works:

1. One story per workflow step.
2. Create, then read, update, delete.
3. The simplest business rule first, each further rule its own story.
4. One kind of data first.
5. The plainest interface first.
6. The simplest version first, each complication its own story.
7. Make it work, then make it fast.
8. A timeboxed spike when something unknown blocks every pattern: the `spike` skill runs it.

Cut across layers, never along them: a story that only adds a table or only adds an endpoint ships nothing a person can see. A requirement on how well a story behaves, an enabler nobody perceives alone, and a task are cases on the story that needs them, not stories. Fold hardening into the story that creates the exposure.

When something new is being built, mark the thinnest slice across all the steps that a real person can use end to end as the first story, with hard-coded data where that keeps it thin.

Put the steps, the stories and the proposed `Order:` to the user in one message. Write the feature file, or the epic and its child issues, only after the user confirms. A story that building reveals later is normal: add it to the feature, after the stories already ordered unless the user moves it.

When the user wants one acceptance test for the whole feature, they write it, marked strictly expected-to-fail, and `deliver` runs it as a check after each story. It is a check to run, not the specification: build each story from its own cases.
