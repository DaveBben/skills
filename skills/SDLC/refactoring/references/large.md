# Large refactorings

Keep the build releasable at every step, on main, never on a long-lived branch:

* **Parallel change** for an interface: add the new form beside the old, move callers one at a time, then delete the old form.
* **Branch by abstraction** for a dependency: put an abstraction over it, move callers onto the abstraction, build the replacement behind it, switch, delete the old one.
* **Strangler fig** for a subsystem: grow the replacement beside it and move behaviour across piece by piece.
* **Mikado method** when the prerequisites are unknown: attempt the goal naively, record each failure as a prerequisite, revert, then do the prerequisites leaves first.
* **Hundreds of mechanical edits:** write a codemod or script, not hand edits.
