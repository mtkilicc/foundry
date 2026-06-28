---
name: full-pack
description: >-
  Builds or audits the complete rule pack against a coverage checklist —
  including the frontend design-system rule and the anti-pattern registry.
  Use for bootstraps and repo-wide rule audits.
---

# full-pack (leaf — read only when routed here)

## Method
1. CLARIFY — per rule: purpose, scope (always-on XOR concrete file
   patterns, expressed per adapter profile).
2. COVERAGE CHECKLIST — each box gets a rule OR a written
   "not needed because ...":
   - [ ] docs-first workflow & drift handling
   - [ ] **project identity** (stack-identity): `docs/stack/design-identity.md`
         + `backend-identity.md` + `.foundry/project-fingerprint.json`
         mined from THIS repo — never copied from another Foundry project
   - [ ] **two-tier frontend rules** (identity-rules): `frontend-structure`
         (how to compose) + `frontend-design-identity` (this project's kits);
         + `backend-structure` scoped to backend api/apps
   - [ ] legacy single "design-system" rule — replace with the above OR
         waive with "covered by design-identity + frontend-structure"
   - [ ] API conventions: one pagination style, one error envelope,
         one naming scheme, versioning policy (scoped: backend api)
   - [ ] data & migrations: safety, no destructive ops without an
         approved plan, seed-data policy
   - [ ] security: no secrets in code, authz at the boundary, input
         validation norms (always-on)
   - [ ] testing: what must be tested, where tests live, fixtures;
         frontend e2e via the project's browser-automation MCP
         (`../../toolkit/mcp-stack/SKILL.md`)
   - [ ] commit/PR hygiene (always-on)
   - [ ] anti-pattern registry (step 3)
   - [ ] transplant repos: never redefine the peer's schemas locally;
         all peer calls via the client module; integration docs
         regenerated, never hand-edited
3. ANTI-PATTERN REGISTRY — seed from
   `../../templates/rules/anti-patterns-seed.md`; mine git history (reverts,
   "fix the fix" chains), review comments, and the user's named
   incidents into incident → wrong move → required move rows.
4. WRITE — `../../templates/rules/policy.md` per concern, rendered in
   the profile's rule format; brownfield rules are MINED, not invented
   (3 pagination styles found → one rule picks the winner); greenfield
   copies the blueprint pack, tailored.
5. VERIFY — frontmatter/format valid per profile; checklist fully
   checked or waived; every rule has a table or do/don't pair; grep
   all skills for restatements → zero. Append new_artifact
   events; run `foundry_check.py queue` — evaluator only if
   needs_review.
