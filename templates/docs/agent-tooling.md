# Agent tooling

Recorded by Foundry adapter. Generators and sync scripts read this file.

| key | value |
|---|---|
| profile | multi-tool |
| canonical_skills_root | agent/skills/ |
| rules_root | AGENTS.md |
| docs_root | docs/ |

## Render targets

| target | enabled | skills output | notes |
|---|---|---|---|
| claude-code | yes | .claude/skills/ | CLAUDE.md wired by Foundry sync |
| cursor | yes | .cursor/skills/ | 00-routing.mdc always-on |
| openharness | no | .openharness/skills/ | Claude-compatible SKILL.md; set `yes` to enable |
| generic | yes | agent/skills/ | AGENTS.md links tree |

## Sync

**Authoritative tree:** `agent/skills/` only.

After skill changes, ask Foundry to sync — agent runs `scripts/foundry_sync.py`.

Rendered paths are generated. Do not edit by hand.

## Post-job skill refresh

Copy `templates/config/foundry.json` → `.foundry/config.json`. After feature
work, ask Foundry to run drift check and post-job skill update.
