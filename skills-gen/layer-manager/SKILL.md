---
name: layer-manager
description: >-
  Dynamic depth manager for the skill hierarchy. Use when a specialist grew
  too big, the user wants specific sub-skills under an existing specialist,
  a domain needs an extra orchestration layer, or layers should merge.
  Handles inserting, splitting, and merging layers and propagating updates
  to every affected skill.
---

# layer-manager (leaf — read only when routed here)

## Depth policy (when a new layer is justified)
Split a leaf into a mini-orchestrator + deeper leaves when ANY holds:
- body would exceed ~80 lines after the new content;
- it anchors leaf docs from >1 distinct responsibility;
- its decision logic has >2 genuinely different workflows;
- the user explicitly names sub-skills they want under it.
MERGE a layer back when an orchestrator routes to a single child, or
siblings' "owns" sections overlap. Depth is per-branch: one domain may
be 3 tiers while another is 5. Never add a layer "for symmetry".

## Method — SPLIT (leaf → orchestrator + children)
1. Read the target skill; partition its content: routing → new
   mini-orchestrator (decision table, same template as L2); per-
   responsibility content → one new leaf each
   (`../../templates/skills/canonical-leaf.md`); shared invariants →
   stay in the orchestrator.
2. Scoping: children get narrower scopes that UNION to the parent's
   old scope (per adapter profile; prose if unsupported).
3. PROPAGATE — the critical step:
   - parent's parent decision table: row now points at the new
     orchestrator;
   - grep ALL skills for links to the old leaf; repoint to the correct
     new child;
   - leaf docs anchored by the old skill: re-home each to exactly one
     new child;
   - update the hierarchy diagram/index if one exists.
4. Verify: full-hierarchy verify block on the touched branch + routing
   dry-run that reaches every NEW leaf.

## Method — INSERT (new intermediate layer) / MERGE
Same propagation discipline: every inbound link, decision-table row,
and doc anchor is re-pointed; nothing may reference a deleted node.
Run the boundary grep after.

## Hand-offs
- New leaves needing the interview/test loop →
  `../single-skill/SKILL.md` per leaf.
- Depth decisions worth standardizing repo-wide → append a
  `layer_change` event to .foundry/queue.json.
