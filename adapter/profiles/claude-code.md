# Profile: Claude Code

| key | value |
|---|---|
| profile | claude-code |
| canonical_skills_root | agent/skills/ |
| skills_root (rendered) | .claude/skills/ |
| rules_root | .claude/rules/ |
| docs_root | docs/ |
| entry_wiring | CLAUDE.md (`@AGENTS.md` + routing mandate) |
| sync_script | scripts/foundry_sync.py |

## Canonical authoring (generators write here)

```yaml
tier: root | orchestrator | leaf
scope: <glob — orchestrator/leaf>
```

## Rendered skill frontmatter (sync output — do not hand-edit)

| tier | rendered fields |
|---|---|
| root | `name`, `description` only (auto-invokable, unscoped) |
| orchestrator | + `paths: <scope>` |
| leaf | + `disable-model-invocation: true` + `paths: <scope>` |

| rule format | .mdc; `description` + exactly one of `alwaysApply: true` XOR `globs:` |
| discovery | nested folders; SKILL.md per folder; name must equal folder |
| notes | descriptions are the trigger mechanism — make them pushy |

Single-tool repos still use `agent/skills/` as SSOT; run sync after edits.
