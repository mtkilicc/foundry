---
name: rules-gen
description: >-
  Standalone orchestrator for generating or auditing rule packs (always-on or
  scoped policy). Use directly for any rules-only request: conventions,
  design consistency on every page, preventing a past LLM mistake.
---

# rules-gen — L2 orchestrator (standalone-capable)

If invoked without the router: run `../templates/intake/standalone.md`.

## Pick the specialist

| Trigger | Read |
|---|---|
| "bootstrap rules", rule pack for a repo, repo-wide rule audit | `full-pack/SKILL.md` |
| project UI/backend structure rules, per-repo design identity | `identity-rules/SKILL.md` |
| one incident → one law, one new convention | `single-rule/SKILL.md` |

## Shared laws
- Rule file location + format + frontmatter dialect come from the
  adapter profile (`../adapter/SKILL.md`). Never hardcode a vendor
  folder or vendor-only syntax.
- One file/section per concern; body ≤50 lines (anti-pattern registry
  exempt — a table that only grows).
- Concrete + actionable: mapping tables, do/don't examples, what TO
  DO. Framework idioms context7-verified, never from memory.
- Rules own policy; skills own domain knowledge. After any rule
  change, grep all skills for restatements.
