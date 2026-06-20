---
name: docs-gen
description: >-
  Standalone orchestrator for generating or auditing documentation trees. Use
  directly for any docs-only request — bootstrapping docs, documenting one
  feature, integration docs with another project, registries, drift — without
  invoking the rest of foundry.
---

# docs-gen — L2 orchestrator (standalone-capable)

If invoked without the router: run `../templates/intake/standalone.md`.

## Pick the specialist

| Trigger | Read |
|---|---|
| project blueprint, MVP/v1 agreement, fill TBDs, before bootstrap | `project-blueprint/SKILL.md` |
| "bootstrap docs", whole repo/component, major restructure | `full-tree/SKILL.md` |
| one page / one flow / one registry update | `single-doc/SKILL.md` |
| design/backend identity, unique UI per project, stack personality | `stack-identity/SKILL.md` |
| "learn from X / integrate with X / mirror X's API or events" | `transplant-contract/SKILL.md` |
| page asserts library behavior | also `../toolkit/context7/SKILL.md` |

## Doc strata (all specialists honor)
- `<docs_root>/project/` — **START POINT**: vision, phased scope (MVP/v1/v2…),
  architecture, domains, constraints, open questions; user-agreed before Foundry
  bootstrap (`foundry_blueprint_check.py`).
- `<docs_root>/stack/` — inherited platform docs (Docker,
  design system, agent-tooling, mcp-setup), version-pinned.
- `<docs_root>/integration/<peer>/` — mirrored contracts; regenerable,
  never hand-edited; each page records peer source path + commit.
- `<docs_root>/<component>/domain|operations/` — capabilities with
  `Status: planned | building | shipped` headers + exhaustive
  registries (api-*.md, env-vars.md, error-codes.md...).

`<docs_root>` resolves via the adapter profile (default `docs/`).

## LLM-legibility standard (every page, every specialist)
Docs are read by agents first. Each page: lead with the **contract** (what it
owns + invariants); put **exhaustive registries** (endpoints, fields, enums, env
vars) in tables — no "see code", no "etc."; define terms on first use; prefer
tables/examples over prose; **relative links**, one fact per doc. See
`../templates/docs/domain-page.md`.

## Cross-cutting follow-ups (note, don't do)
- new leaf a skill should anchor → `../skills-gen/single-skill`
- repeated drift pattern → `../rules-gen/single-rule`
- anything new/discovered → one event in .foundry/queue.json,
  then `foundry_check.py queue`
