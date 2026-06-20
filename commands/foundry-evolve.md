---
description: Post-feature evolution — drift scan, then update lagging skills and re-sync
argument-hint: "[optional: feature just shipped]"
---

Invoke the **foundry** skill for skill evolution after feature work.

- Agent runs `python scripts/foundry_skill_drift.py <repo> --git --enqueue`.
- If proposals → route to `skills-gen/post-job-update` (patch canonical only),
  then `foundry_sync.py` → `foundry_check.py sync`.
- This is the same loop a leaf's **Evolution self-check** self-triggers; use this
  command to run it explicitly. If drift is clean, do nothing.

Feature context: $ARGUMENTS
