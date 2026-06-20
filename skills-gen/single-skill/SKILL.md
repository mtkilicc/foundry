---
name: single-skill
description: >-
  Creates or updates ONE skill for a small purpose — a feature specialist at
  any depth, a standalone utility skill, or fixing a skill that won't
  trigger. Wraps the skill-creator loop with hierarchy slotting. Never
  rebuilds the hierarchy.
---

# single-skill (leaf — read only when routed here)

## Method
1. SLOT FIRST — read the root skill and walk decision tables to the
   candidate parent (any depth). Decide:
   (a) new leaf under that parent; (b) extend an existing leaf whose
   "owns" already covers this (prevent near-duplicates); (c) the
   parent leaf is already too big or the user wants sub-skills →
   `../layer-manager/SKILL.md` first, then return here; (d) standalone
   utility skill outside routing (report generators, automation);
   (e) purpose spans domains → STOP, recommend `../full-hierarchy/SKILL.md`.
2. INTERVIEW (skill-creator style, scaled) — two axes:
   - **Capability depth** (specialist questions, tech-independent): what are the
     distinct sub-capabilities/operations of this area? what does "done right"
     mean (the quality bar)? which states & edge cases must it handle? how does a
     specialist decide between options? how is this area commonly done wrong?
   - **Implementation:** trigger phrases; contract; decisions already made;
     gotchas; extension points; output format; dependencies.
   Leaf docs to anchor — missing → `../../docs-gen/single-doc/SKILL.md` FIRST.
   MCP needs → select from `../../toolkit/mcp-stack/SKILL.md` (one,
   two, or all as the task demands); not in stack → adoption protocol
   there, which pings the evaluator.
3. DRAFT — routed leaf: `../../templates/skills/canonical-leaf.md`,
   ≤80 lines, `tier: leaf` + `scope` in frontmatter. A leaf is a **senior
   specialist** on BOTH axes: fill **Capability mastery** (sub-capabilities,
   quality bar, states/edge cases, decision criteria, failure modes) AND
   **Implementation mastery** (contract, decisions, gotchas, extension points),
   plus the **Evolution self-check**. Specialize by capability, not only tech —
   never ship a generic router or a "we use <library>" stub.
   Standalone utility: lean SKILL.md + scripts/ (deterministic steps),
   references/ (load-on-demand, "read X when Y"), assets/. Bulk lives
   in references (progressive disclosure). Description: third-person,
   WHAT + WHEN, pushy triggers.
4. TEST LOOP — 3–5 substantive multi-step prompts (one-liners never
   trigger skills); run with the skill; review with the user; iterate
   description + body; assertions for checkable outputs.
5. INTEGRATE — add one row to the parent's decision table; never edit
   siblings beyond that row. Run `python ../../scripts/foundry_sync.py <repo>`.
   Append one new_artifact event; run `foundry_check.py queue`.

## Verify
name/folder match per profile; frontmatter valid; ≥1 leaf doc + ≥1
code anchor (routed case); no rule restated; no sibling overlap; test
prompts trigger reliably. **Capability check:** both Capability mastery and
Implementation mastery are filled with specifics for THIS area (concrete
sub-capabilities + quality bar + edge cases) — reject generic placeholders or a
tech-only stub.
