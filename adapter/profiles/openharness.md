# Profile: OpenHarness

[HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) — a local-LLM agent
harness (tool-use, skills, memory, multi-agent). Its skills system reads
`SKILL.md` files and is **compatible with the Anthropic / Claude skills format**,
so Foundry renders to it with the same canonical tree — only the output path
differs.

| key | value |
|---|---|
| profile | openharness |
| canonical_skills_root | agent/skills/ |
| skills_root (rendered) | .openharness/skills/ |
| rules_root | AGENTS.md (+ `.openharness/` settings if used) |
| docs_root | docs/ |
| sync_script | scripts/foundry_sync.py |

## Skill discovery (OpenHarness)

- Loads `SKILL.md` from `<project>/.openharness/skills/<skill>/SKILL.md` (also
  `~/.openharness/skills/` and `~/.claude/skills/`).
- Skills are **on-demand knowledge** — the `description` is the load trigger.
  Keep it pushy (WHAT + WHEN), like Claude.
- Frontmatter is `name` + `description`. Foundry's render also carries the
  canonical `tier`/scope hints; OpenHarness ignores unknown keys harmlessly.

## Rendered skill frontmatter (sync output — do not hand-edit)

Same render as Claude (`name`, `description`, and tier-derived fields). Leaves
stay routed-only; root stays auto-loadable via its description.

## What this profile controls

- `skills_root` → `.openharness/skills/` (set by sync's `TARGET_SKILLS`).
- Policy law lives in `AGENTS.md` (canonical); scoped rules render as prose in
  the skill body if OpenHarness lacks path scoping.
- Plugins/commands/hooks (`.openharness/plugins/**`, `settings.json`) are
  out of scope for Foundry generation today — note as a future surface.

## Interview default

Select when the user runs OpenHarness for local LLMs. Combine with Claude/Cursor
via `multi-tool.md`; enable all chosen targets in
`docs/stack/agent-tooling.md` (Render targets table).
