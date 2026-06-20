---
description: Generate or refresh the build task plan — each task assigned to its owning skill
argument-hint: "[optional: phase, e.g. 'MVP only']"
---

Invoke the **foundry** skill to produce the task plan.

- Use `templates/docs/task-plan.md`. Run **after** the skill hierarchy exists.
- Walk `02-scope-phases.md` (MVP/v1) + `04-domains.md`; break capabilities into
  PR-sized tasks; assign each an **owning skill** (leaf path) or a `new_leaf` marker.
- Set `depends_on` ordering; verify every MVP/v1 capability maps to ≥1 task.
- Re-run appends only tasks for new scope; never regenerates completed rows.

Scope: $ARGUMENTS
