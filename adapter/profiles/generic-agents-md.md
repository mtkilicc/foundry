# Profile: generic AGENTS.md

| key | value |
|---|---|
| profile | generic-agents-md |
| canonical_skills_root | agent/skills/ |
| skills_root | agent/skills/ (no render — canonical is the deliverable) |
| rules_root | AGENTS.md (single file, one section per concern) |
| docs_root | docs/ |
| sync_script | none (enable claude-code and/or cursor in agent-tooling.md to add renders) |

## When to use
- Codex, Windsurf, Aider, custom agents, or "I don't use Claude/Cursor"
- Fallback when the tool is unlisted

## Skill frontmatter (canonical)

```yaml
name, description
tier: root | orchestrator | leaf
scope: <glob or omit>
```

Body: leaf line `Read only when routed here`; scoping also in prose
`Applies to: ...` when the tool has no path field.

| rule format | AGENTS.md sections; keep each ≤50 lines |
| discovery | none — AGENTS.md must link `agent/skills/SKILL.md` |
| notes | add Claude and/or Cursor later by enabling render targets in agent-tooling.md and running sync — no skill rewrite needed |
