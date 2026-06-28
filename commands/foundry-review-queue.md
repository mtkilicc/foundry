---
description: Handle needs_review queue items with judgment (MCP proposals, drift, findings)
argument-hint: ""
---

Invoke the **foundry** skill, routing to `evaluator` — **only** for items the
script marked `needs_review` in `.foundry/queue.json`.

- Per item, apply the evaluator method (restate need → score → decide → route).
- Never re-verify what `foundry_check.py` already verified; never implement —
  set `routed_to` and let the owning skill implement.
- After handling, rerun `foundry_check.py queue`; summarize event → decision → routed_to.

$ARGUMENTS
