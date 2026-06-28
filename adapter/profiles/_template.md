# Profile: <tool name>

| key | value |
|---|---|
| profile | <name> |
| canonical_skills_root | agent/skills/ |
| skills_root | <render path or same as canonical> |
| rules_root | <where policy lives> |
| docs_root | docs/ |
| sync_script | scripts/foundry_sync.py (if renders exist) |
| skill frontmatter | canonical: `tier`, `scope`; rendered dialect per target |
| rule format | <extension + frontmatter> |
| discovery | <nested folders? index rule?> |
| notes | <quirks> |

Prefer extending `multi-tool.md` when the user names more than one IDE.
After creating a new profile: append `new_profile` to queue; record in
`docs/stack/agent-tooling.md`.
