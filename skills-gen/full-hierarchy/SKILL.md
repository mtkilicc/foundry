---
name: full-hierarchy
description: >-
  Designs and implements the full N-tier skill system (root router, domain
  orchestrators, specialists, optional deeper sub-specialists) mirroring the
  repo's code + docs. Use for bootstraps, new major domains, or
  hierarchy-wide audits.
---

# full-hierarchy (leaf — read only when routed here)

## Method
1. RESEARCH — web-search current best practice for the ACTIVE TOOL
   PROFILE (frontmatter, discovery, size limits change per tool); read
   all rules; read docs incl. stack/ and integration/.
2. MAP — one explore subagent per domain in parallel; each returns
   stack, folder purposes, per-feature module map, doc-to-code
   alignment, suggested skill boundaries. Tables only.
3. PROPOSE the hierarchy — default 3 tiers, deeper where the DEPTH
   POLICY (`../layer-manager/SKILL.md`) demands:
   - L1 root: auto-invoked, unscoped, routes ANY task incl.
     cross-cutting (loads multiple L2s).
   - L2 per major domain: auto-invoked, domain-scoped, decision table
     trigger → child. Transplant repos add `integration-with-<peer>`.
   - L3+ specialists: one per real domain responsibility (NOT per
     technical layer); leaves marked no-auto-invoke per profile,
     scoped, ≤80 lines. An L3 that the depth policy says is too big
     becomes a mini-orchestrator over L4 leaves — same templates, one
     level down. Granularity calibrated from the user's named examples.
   - Greenfield: leaves only for docs with Status building/shipped.
   - Forbidden skills: "update code", "update docs", "read docs first".
4. PLAN — mermaid routing diagram + folder layout + per-specialist
   table + rule-vs-skill boundary table + depth decisions with
   justification. Wait for approval.
5. WRITE — orchestrators: confirm scope → decision table → dispatch →
   cross-cutting list. Leaves: `../../templates/skills/canonical-leaf.md`.
   Scaffold under `agent/skills/`; write in parallel.
6. SYNC — `python ../../scripts/foundry_sync.py <repo>`; ensure
   `docs/stack/agent-tooling.md` exists with enabled targets.
7. TALENT — `../project-talent/SKILL.md` (identity docs + structure rules +
   enrich every leaf with UI composition / backend patterns).

## Verify
- name == folder everywhere (or profile equivalent); root unscoped;
  every non-leaf has a decision table; every leaf is no-auto-invoke +
  scoped (or prose-scoped per profile).
- Every leaf: ≥1 leaf doc + ≥1 code anchor.
- Boundary grep over all skills: "read docs first", "sync with code",
  doc-workflow, design-system, anti-pattern phrases → zero matches.
- Routing dry-run: 5 realistic tasks (≥1 cross-cutting, ≥1 ambiguous,
  ≥1 that must reach the DEEPEST tier) walked on paper; no dead ends,
  no double-owners.
- Append new_artifact events for created skills to .foundry/queue.json;
  run sync + `python ../../scripts/foundry_check.py all agent/skills <repo>`
  — must exit 0.
