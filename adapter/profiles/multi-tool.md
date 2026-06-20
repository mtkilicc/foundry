# Profile: multi-tool (recommended default)

| key | value |
|---|---|
| profile | multi-tool |
| canonical_skills_root | agent/skills/ |
| rules_root | AGENTS.md (canonical law) + per-target rule renders |
| docs_root | docs/ |
| render_targets | claude-code, cursor (generic needs no render) |
| sync_script | scripts/foundry_sync.py |

## Render map

| target | skills output | policy rules | always-on router |
|---|---|---|---|
| claude-code | `.claude/skills/**/SKILL.md` | `.claude/rules/*.mdc` | `CLAUDE.md` imports `@AGENTS.md` + routing mandate |
| cursor | `.cursor/skills/**/SKILL.md` | `.cursor/rules/*.mdc` (policy only) | `.cursor/rules/00-routing.mdc` (`alwaysApply: true`) |
| openharness | `.openharness/skills/**/SKILL.md` | `AGENTS.md` (+ prose scope) | root SKILL.md description (on-demand load) |
| generic / other | canonical only (`agent/skills/`) | `AGENTS.md` sections | `AGENTS.md` links `agent/skills/SKILL.md` |

## Canonical skill frontmatter (authoring dialect)

All generators write HERE first. Tool-specific frontmatter is **rendered**, never hand-edited.

```yaml
---
name: <folder-name>
description: >-
  <Third person. WHAT + WHEN.>
tier: root | orchestrator | leaf
scope: <glob or empty for unscoped>
---
```

| tier | meaning |
|---|---|
| `root` | L1 router — every task |
| `orchestrator` | L2 domain router — scoped |
| `leaf` | L3+ specialist — routed only |

## Sync law (non-negotiable)

1. **Edit only** `agent/skills/` (and `AGENTS.md` for policy).
2. After every skill create/update/split: agent runs `foundry_sync.py <repo>`.
3. **Never hand-edit** `.claude/skills/`, `.cursor/skills/`, or generated routing files.
4. `foundry_check.py sync <repo>` fails if renders are stale.

Updating Claude-side content automatically updates Cursor-side (and vice versa) because both are renders of the same canonical tree.

## Interview default

When the user names more than one tool, or says "both Claude and Cursor", select this profile and record all targets in `docs/stack/agent-tooling.md`.
