---
description: Generate or refresh the build task plan — each task assigned to its owning skill
argument-hint: "[optional: phase, e.g. 'MVP only']"
---

Invoke the **foundry** skill to produce the task plan.

- Use `templates/docs/task-plan.md`. Run **after** the skill hierarchy exists.
- Walk `02-scope-phases.md` (MVP/v1) + `04-domains.md`; break capabilities into
  PR-sized tasks; assign each an **owning skill** (leaf path) or a `new_leaf` marker.
- Set `depends_on` ordering; verify every MVP/v1 capability maps to ≥1 task.
- **Weight every task 1–10** via the formula in `templates/docs/task-plan.md`
  (factors: hardness H, complexity C, bigness B, importance I); record as
  `weight (H·C·B·I)`.
- **Re-run / modify = append-only (task immutability).** Never edit, renumber, or
  delete a `done` task — supersede it with a NEW task. An `in-progress` task is
  changed only after **asking the user**; `todo` tasks may be edited in place. See
  *Re-run / modify — task immutability* in `templates/docs/task-plan.md`.

Scope: $ARGUMENTS
