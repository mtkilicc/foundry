---
name: full-tree
description: >-
  Builds or audits an entire docs tree so an LLM can act on the system
  without reading source. Use for full bootstraps, new components, or
  repo-wide doc audits — not single pages.
---

# full-tree (leaf — read only when routed here)

## Method
1. INVENTORY — read `docs/project/` (blueprint) for phases + domains FIRST;
   map runtime components via parallel explore subagents
   (tables only, no source dumps); list existing docs + drift.
2. STRUCTURE — root `<docs_root>/README.md` maps EVERY doc file
   (table, 1-line purpose); the three strata from `../SKILL.md`;
   per-component README indexes; exhaustive reference registries.
3. CONTENT — every endpoint/field/enum/error/env-var BY NAME; never
   "see code"; tables for exhaustive lists; relative links only;
   cross-link the LEAF owning each concept; library assertions
   verified via `../../toolkit/context7/SKILL.md`, never from memory.
   - **Business flows** — materialize `docs/project/business-flows.md` from
     `../../templates/docs/business-flows.md`, expanding the blueprint
     `core_flows`/`flow_detail` into one detail block per flow (actor → trigger →
     steps → outcome → touches domains/skills → acceptance). This page OWNS flow
     detail; `04-domains.md` only indexes it. Every MVP flow must appear.
4. SCENARIO DELTAS
   - greenfield: domain docs are **intent** for agreed phase only (`Status: planned`);
     blueprint `01-scope-phases.md` is the scope authority.
   - brownfield: code is truth; accidental-looking behavior documented
     as-is PLUS "⚠ Drift" callout with suspected intent — never
     silently canonized, never wishfully "fixed".
   - transplant: integration/ pages come ONLY from
     `../transplant-contract/SKILL.md` output.
5. SYNC CONTRACT — behavior-changing code edits update the matching
   doc in the same change; statuses flip planned→building→shipped.

## Verify
- Every link resolves; every README lists its whole subtree.
- No TODO / "see source" placeholders.
- No `shipped` status the code map cannot confirm.
- Read-through test: one feature, docs only — endpoints, data model,
  flows statable? If not, the tree failed.

## Hand-offs
- single pages later → `../single-doc/SKILL.md`; doc-workflow policy
  lives in rules, not here.
