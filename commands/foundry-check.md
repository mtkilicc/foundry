---
description: Run Foundry's deterministic checks (structure / sync / drift / blueprint / queue / all)
argument-hint: "[scope: all | structure | sync | drift | blueprint | queue]"
---

Invoke the **foundry** skill to run close-out checks.

- Agent runs `python scripts/foundry_check.py $1 <repo>` (default `all`).
- `structure` validates `agent/skills/`; `sync` flags stale renders; `drift`
  checks doc/skill lag; `blueprint` is the bootstrap gate; `queue` confirms the
  `.foundry/queue.json` is green-or-known.
- Report results as a short table; anything `needs_review` → `/foundry-review-queue`.

Scope (default all): $ARGUMENTS
