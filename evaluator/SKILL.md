---
name: evaluator
description: >-
  Judgment layer for queue items the script could not auto-resolve. Use ONLY
  when scripts/foundry_check.py marks events needs_review — never as a
  routine end-of-run step, and never to re-check what the script already
  verified.
---

# evaluator — judgment for needs_review items only

Division of labor: `scripts/foundry_check.py` does ALL deterministic
checking (structure, links, registries, duplicates, artifact
existence). This skill spends tokens exclusively on items the script
marked `needs_review` in `.foundry/queue.json`. If the queue is green,
this skill is never read.

## Per-item method (handle each needs_review event, then stop)

mcp_proposal:
1. Restate the need as a CAPABILITY. 2. Candidates = proposal's + your
own (web-search current options) + "existing stack covers it".
3. Score: capability fit · overlap with stack (weight heavily —
near-duplicates rot stacks) · option health · auth blast radius ·
setup cost · project fit. 4. Decide; one-line reason per rejection.
5. Set status approved/rejected + routed_to: `toolkit/mcp-stack`
(catalog row + mcp-setup.md registration). Append decision to
`docs/stack/adoption-log.md`.

skill_drift (doc grew; skill map lags):
1. Read payload (`kind`, `doc`, `skill`, `artifact`, `suggested_action`).
2. Real? — confirm artifact still in doc; not typo-only.
3. Allowed? — map change only; not a rule or a doc fact restatement.
4. Approve → `routed_to: skills-gen/post-job-update` (that skill patches
   canonical + runs sync). Reject → `rejected` + one-line reason.
5. `new_leaf_candidate` → route to `../skills-gen/single-skill/SKILL.md` instead.

blueprint_change (phase or scope agreement amended):
Route to `../docs-gen/project-blueprint/SKILL.md`; update agreement JSON;
if phase promoted to shipped → notify full-tree audit for domain Status rows.

finding (a skill learned something beyond its scope):
Route by payload.kind — policy → `../rules-gen/single-rule/SKILL.md`;
fact/contract → `../docs-gen/single-doc/SKILL.md`; routing/domain →
parent orchestrator via `../skills-gen/single-skill/SKILL.md`. A
finding stays local ONLY if it truly applies to one leaf. Set
routed_to; the OWNING skill implements (you never implement).

new_profile / new_template / layer_change:
Same score-and-decide shape; check overlap with existing profiles/
templates/depth-policy; approved → route to adapter / templates owner /
layer-manager.

## After handling
Update each event's status + routed_to in queue.json, rerun
`foundry_check.py queue` to confirm green-or-known, summarize in one
table: event → decision → routed_to.

## Laws
- Never re-verify what the script verifies. Never implement — route.
- Every shared-infrastructure addition passes through the queue, not
  through chat memory.
