# `.foundry/config.json` — machine config for foundry scripts

Human-readable tool choices also live in `docs/stack/agent-tooling.md`.
**Scripts read `config.json` first**, then merge enabled flags from
`agent-tooling.md`. Keep both in sync when adding/removing tools.

## Location

```
<repo>/.foundry/config.json
```

Copy from `templates/config/foundry.json` on first bootstrap.

## Schema

| key | type | purpose |
|---|---|---|
| `version` | number | schema version |
| `canonical_skills_root` | string | SSOT skill tree (`agent/skills`) |
| `post_job.enabled` | bool | run drift check after feature work |
| `post_job.run_drift_check` | bool | call `foundry_skill_drift.py` |
| `post_job.enqueue_proposals` | bool | append `skill_drift` events to queue |
| `render_targets.<tool>.enabled` | bool | sync renders for that tool |
| `render_targets.<tool>.skills_root` | string | output path for skills |
| `drift.auto_reject_kinds` | string[] | script auto-closes as false positive |
| `drift.needs_review_kinds` | string[] | script enqueues for post-job-update |

## Drift kinds

| kind | meaning | typical action |
|---|---|---|
| `code_map_gap` | doc lists path/route/endpoint skill omits | add to Code map / Owns |
| `trigger_gap` | new feature term in doc not in description | extend description triggers |
| `orchestrator_row` | new subdomain needs L2 decision table row | edit parent orchestrator |
| `new_leaf_candidate` | new domain doc with no anchoring skill | `skills-gen/single-skill` |
| `doc_status_only` | only `Status:` changed | auto-reject |
| `already_covered` | skill already mentions artifact | auto-reject |
| `identity_kit_gap` | new UI primitive or app shape not in stack identity | `docs-gen/stack-identity` + `skills-gen/project-talent` |

## Post-job flow

```
feature work (docs updated)
  → python scripts/foundry_skill_drift.py <repo> --git [--enqueue]
  → proposals in .foundry/skill-drift-report.json (+ queue events)
  → skills-gen/post-job-update (validate + patch canonical skills)
  → python scripts/foundry_sync.py <repo>
  → python scripts/foundry_check.py all agent/skills <repo>
```

## Render targets

When `claude-code` and `cursor` are both enabled, **one canonical edit**
updates both via `foundry_sync.py`. Disable a target here to skip its
render (e.g. team uses only Cursor).

---

# `.foundry/intake.json` — enforced intake record

Seed from `templates/config/intake.json`. The blueprint gate
(`foundry_blueprint_check.py`) **fails** unless this file resolves every blocking
slot. Embodies the rule: *ask the user for every gap; Foundry guesses only when
the user delegates.*

| key | type | purpose |
|---|---|---|
| `version` | number | schema version |
| `delegated` | bool | user handed gap-filling to Foundry ("you decide / use defaults") |
| `delegated_by` | string | required when `delegated=true` |
| `delegated_at` | string | ISO timestamp (optional) |
| `slots.<key>.value` | string | the answer (non-empty) |
| `slots.<key>.source` | enum | `user` \| `seed` \| `repo` \| `derive` \| `default` \| `foundry-decided` |

**Blocking slots** (all required): `situation`, `consuming_tools`,
`project_name`, `pitch`, `archetype`, `personas`, `auth_model`, `core_flows`,
`domains`, `mvp_scope`, `v1_scope` — must match the Blocking set in
`templates/intake/question-bank.md`.

**Source rule:** `user`/`seed`/`repo`/`derive` are always accepted.
`default`/`foundry-decided` (Foundry guessed) are accepted **only** when
`delegated=true`. Design/creativity slots are non-blocking and not recorded here.

Escape: `foundry_blueprint_check.py <repo> --skip-intake` bypasses this check
(legacy repos / explicit human override only).

---

# `.foundry/blueprint-agreement.json` — state + approval

| key | type | purpose |
|---|---|---|
| `state` | enum | `empty` \| `blueprint` \| `running` (set during intake SITUATION) |
| `approval.project` | object | Empty/Blueprint approval of `docs/project/APPROVAL.md` |
| `running_approval.current_state` | object | Running: approval of `CURRENT-STATE.md` |
| `running_approval.requested_state` | object | Running: approval of `REQUESTED-STATE.md` |
| `approval.*.{approved,approved_by,approved_at,document}` | — | approval record |
| `phases.<p>.status` | enum | `empty\|draft\|agreed\|shipped\|optional` |

**Gate enforcement (`foundry_blueprint_check.py`):** Empty/Blueprint require
`approval.project.approved=true` (+ `approved_by`); Running requires **both**
`running_approval` docs approved. The consolidated doc(s) are produced by
`foundry_blueprint_assemble.py`. Approval is mandatory; revise → re-assemble →
re-present until the user approves. Escape: `--skip-approval`.
