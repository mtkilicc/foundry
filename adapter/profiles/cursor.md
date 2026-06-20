# Profile: Cursor

| key | value |
|---|---|
| profile | cursor |
| canonical_skills_root | agent/skills/ |
| skills_root (rendered) | .cursor/skills/ |
| rules_root | .cursor/rules/ |
| docs_root | docs/ |
| always_on_router | .cursor/rules/00-routing.mdc (`alwaysApply: true`) |
| sync_script | scripts/foundry_sync.py |

## Canonical authoring (generators write here)

```yaml
tier: root | orchestrator | leaf
scope: <glob — orchestrator/leaf>
```

## Rendered outputs (sync — do not hand-edit)

| artifact | purpose |
|---|---|
| `.cursor/skills/**/SKILL.md` | native Agent Skills (same tree as canonical) |
| `.cursor/rules/00-routing.mdc` | L1 decision table, `alwaysApply: true` |
| `.cursor/rules/*.mdc` (other) | scoped policy rules from rules-gen |

Rendered `.cursor/skills/` use the same frontmatter dialect as Claude Code
(`disable-model-invocation`, `paths`) — Cursor's native skill format.

| rule format | .mdc; description + globs XOR alwaysApply |
| discovery | `.cursor/skills/` folder tree; verify current Cursor docs before generating |
| notes | routing decision table is duplicated into `00-routing.mdc` for every-prompt dispatch |

Single-tool repos still use `agent/skills/` as SSOT; run sync after edits.
