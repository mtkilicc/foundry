---
name: skills-gen
description: >-
  Standalone orchestrator for generating or auditing agent skill hierarchies.
  Use directly for any skills-only request: bootstrapping the hierarchy,
  adding one skill, adding or splitting layers, fixing triggering or routing.
---

# skills-gen — L2 orchestrator (standalone-capable)

If invoked without the router: run `../templates/intake/standalone.md`.

## Pick the specialist

| Trigger | Read |
|---|---|
| "bootstrap/redesign skills", new major domain, hierarchy-wide audit | `full-hierarchy/SKILL.md` |
| "talented skills", unique UI, enrich from project, not generic | `project-talent/SKILL.md` |
| "add/extend ONE skill", small purpose, utility skill, "won't trigger" | `single-skill/SKILL.md` |
| "this skill is too big", "I want sub-skills under X", insert/split/merge a layer, depth changes | `layer-manager/SKILL.md` |
| feature shipped, docs updated, skill lags / drift report / skill_drift queue | `post-job-update/SKILL.md` |

## Shared laws (all specialists)
- **Canonical SSOT:** write all skills under `agent/skills/` with `tier`
  (`root` | `orchestrator` | `leaf`) and `scope` in frontmatter — see
  `../templates/skills/canonical-leaf.md`. Never write tool-specific
  frontmatter (`disable-model-invocation`, `alwaysApply`) into canonical files.
- After every create/update: `python ../scripts/foundry_sync.py <repo>` then
  `python ../scripts/foundry_check.py sync <repo>`.
- After feature work that changed domain docs: `python ../scripts/foundry_skill_drift.py <repo> --git --enqueue`; if proposals → `post-job-update/SKILL.md`.
- Resolve render paths and dialect through the adapter profile
  (`../adapter/SKILL.md`). Never hardcode vendor folders in canonical files.
- Read every rule file first — skills MUST NOT restate rules. Boundary:
  rules own policy; skills own routing, leaf-doc links, code anchors,
  domain invariants, hand-offs. A sentence that could move into a rule
  without losing meaning gets deleted from the skill.
- Every leaf specialist anchors ≥1 LEAF doc and ≥1 code file; missing
  doc → create via `../docs-gen/single-doc/SKILL.md` first.
- **Master-expert standard (two axes):** every leaf is a senior specialist in
  its area on BOTH **capability** and **implementation**. Fill **Capability
  mastery** (sub-capabilities · quality bar · states/edge cases · decision
  criteria · failure modes — tech-independent) AND **Implementation mastery**
  (contract · decisions · gotchas · extension points). Specialize by domain
  capability, not only by technology — never a generic router or a "we use X" stub.
- **Skill-owned evolution:** every leaf carries the **Evolution self-check**;
  after feature work it self-decides whether to evolve and self-triggers
  `foundry_skill_drift.py` → `post-job-update` → `foundry_sync.py`.
- Descriptions: third-person, WHAT + WHEN, pushy trigger phrases
  (under-triggering is the common failure).
- Depth is DYNAMIC — the N-tier policy lives in
  `layer-manager/SKILL.md`; full-hierarchy and single-skill both defer
  to it whenever depth questions arise.
