---
description: Sync canonical skills to all render targets (Claude, Cursor, OpenHarness) and verify
argument-hint: ""
---

Invoke the **foundry** skill to sync renders.

- Agent runs `python scripts/foundry_sync.py <repo>` then
  `python scripts/foundry_check.py sync <repo>`.
- Renders canonical `agent/skills/` → every enabled target in
  `docs/stack/agent-tooling.md`: `.claude/skills/`, `.cursor/skills/` +
  `00-routing.mdc`, `.openharness/skills/`, `CLAUDE.md`.
- Never hand-edit rendered copies — edit `agent/skills/` and re-sync.

$ARGUMENTS
