---
name: post-job-update
description: >-
  Post-feature skill refresh. Use AFTER docs/code changed for a shipped feature
  but the canonical skill still lags — when foundry_skill_drift.py reports gaps,
  queue has skill_drift events, or the user says "update the skill for this
  feature". Validates proposals against skill-creation rules, patches
  agent/skills/, runs sync to Claude/Cursor renders.
---

# post-job-update (leaf — run at end of feature work)

## When this runs
End of any feature job that touched `docs/**/domain/*.md` or added routes,
endpoints, or modules. The implementing agent does NOT patch skills inline
during the feature unless the change is trivial (one code-map line).

Trigger the pipeline (agent runs):

`python scripts/foundry_skill_drift.py . --git --enqueue`

## Step 1 — Load proposals
1. Read `.foundry/skill-drift-report.json`
2. Read `.foundry/config.json` — note enabled `render_targets`
3. Pending `skill_drift` events in `.foundry/queue.json`

If all dispositions are `auto_rejected` and queue is green → stop.

## Step 2 — Validate each proposal (is it real? allowed?)

| Check | Reject if |
|---|---|
| Real | doc artifact is gone, duplicate, or typo-only |
| Belongs in skill | fact belongs in doc only (move to docs-gen, not skill) |
| Belongs in rule | policy not domain knowledge (route to rules-gen/single-rule) |
| New leaf needed | `new_leaf_candidate` — parent domain exists but no leaf slot |
| Size budget | patch would push leaf >80 lines → `layer-manager` first |
| Rule boundary | sentence restates AGENTS.md policy → delete, don't add |

**Approve** when: routing, code map, description triggers, or orchestrator
decision row must reflect new capability for the next prompt to route correctly.

## Step 3 — Apply (canonical only)

| kind | action |
|---|---|
| `code_map_gap` | Add path/endpoint to **Code map** or **Owns** in the anchoring leaf |
| `trigger_gap` | Extend `description` with pushy WHEN terms (third person) |
| `orchestrator_row` | Add row to parent L2 decision table |
| `new_leaf_candidate` | STOP → `../single-skill/SKILL.md` for a new leaf, then return |
| `identity_kit_gap` | Update `docs/stack/design-identity.md` or `backend-identity.md` via `../../docs-gen/stack-identity/SKILL.md`, then `../project-talent/SKILL.md` |

Use `../../templates/skills/canonical-leaf.md` shape. Edit **only**
`agent/skills/` — never `.claude/` or `.cursor/`.

## Step 4 — Sync all enabled targets

Read `render_targets` from config; agent runs for each enabled tool:

`foundry_sync.py` → `foundry_check.py sync` → `foundry_check.py structure agent/skills`

Confirm renders exist for every enabled target (claude-code, cursor, …).

## Step 5 — Close queue
Set each handled `skill_drift` event: `status: approved`, `routed_to`:
`skills-gen/post-job-update`. Rerun `foundry_check.py queue`.

## Laws
- Docs own facts; skills own map (anchors + triggers + hand-offs).
- One feature job → one drift scan → minimal skill diff.
- If drift check is clean, do not touch skills.
