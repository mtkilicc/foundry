---
name: foundry
description: >-
  Automation starter: blueprint → docs, skills, and rules for agent-ready repos.
  Users invoke foundry only — the agent runs scripts. Use for bootstrap, one
  page/skill/rule jobs, seed import, MVP/v1 agreement, talented project identity,
  or "document the … flow".
---

# foundry — L1 router

**Users talk to Foundry. The agent runs `scripts/*.py` via Shell** — users do
not run Python themselves. See `scripts/README.md`.

Users may invoke a `/foundry-*` slash command (see `commands/`) **or** plain
language — both land here. A command just pre-states the task; routing is the same.

THE MAIN FLOW IS THE SMALL JOB. Ceremony scales with job size. See
`examples/sample-project/walkthrough-small-job.md`.

## Step −1 — Run mode (detect BEFORE anything else)

A repo reaches Foundry in one of three modes / **project states** (what the user
brings). Detect by what exists, then route:

| signal | mode | project state | what Foundry does |
|---|---|---|---|
| no `agent/skills/` AND no real code | **greenfield** | **Empty** (idea / docs only) | full bootstrap from an idea — generative design + sizing (no code to mine). *Blueprint state = greenfield + prune + dynamic UI redesign.* |
| code exists, no `.foundry/config.json` / `agent/skills/` | **brownfield-first** | **Running** (existing app) | bootstrap from reality — mine code, consolidate legacy docs; current-state + requested-state docs |
| `.foundry/config.json` **and** `agent/skills/SKILL.md` exist | **re-run (maintenance)** | **Running** (foundryized) | **do NOT re-bootstrap** — incremental update only |

Detection: `agent/skills/SKILL.md` + `.foundry/config.json` present → re-run.
Else, code present (lockfiles/apps) → brownfield-first. Else → greenfield. When
ambiguous, confirm with the user (question bank Area 0 `situation`).

**Re-run rules:** keep the existing identity/fingerprint and blueprint; touch
only what the request changes. Re-run the blueprint gate **only** if the job
promotes a phase or changes intent. Apply every Foundry capability
incrementally (intake gap-scan on the delta, master-expert + self-evolution,
sync to all targets incl. OpenHarness, task generation for the new scope).
Greenfield + brownfield-first → **BIG PATH** bootstrap below.

## Step 0 — Blueprint gate (bootstrap only)

Before **BIG PATH** or first full bootstrap, **agent runs**
`foundry_blueprint_check.py <repo>`.

Exit 1 → read `docs-gen/project-blueprint/SKILL.md`. Run its **Intake &
normalization** step first: clarify situation, normalize any input (one sentence
or a folder of docs) onto `templates/intake/question-bank.md`, then **ask the
user for every gap** — Foundry fills gaps from defaults/its own decisions **only
if the user explicitly delegates** (design/creativity slots excepted). Then fill
TBDs and record MVP/v1 in `.foundry/blueprint-agreement.json`. **Stop.**

Exit 0 → adapter + generation.

Fast-path jobs skip re-agreement unless they **promote a phase** or change
blueprint intent.

## Step 1 — Adapter (once per repo, cached)

Load `docs/stack/agent-tooling.md` or read `adapter/SKILL.md`. Copy seeds from
`templates/config/` and `templates/docs/agent-tooling.md` when missing.

## Step 2 — Triage: FAST PATH or BIG PATH?

FAST PATH (default):
- One line: "Small job: <what>. Proceeding."
- Route to leaf; append queue event if needed.
- **Agent close-out:** `foundry_skill_drift.py --git --enqueue` → if proposals,
  `skills-gen/post-job-update` → `foundry_sync.py` → `foundry_check.py queue`.

BIG PATH:
- Fill `templates/intake/work-order.md`; get approval.
- Order: blueprint → rules → docs(stack) → docs(domain) → skills → project-talent
  → **task-plan** (`templates/docs/task-plan.md`: every MVP/v1 task assigned to
  its owning skill — generated last, after skills exist).
- **Agent close-out:** `foundry_sync.py` → `foundry_check.py all agent/skills <repo>`.

## Step 3 — Dispatch table

| User request | Read |
|---|---|
| blueprint, MVP/v1, seed folder, start docs | `docs-gen/project-blueprint/SKILL.md` |
| documentation | `docs-gen/SKILL.md` |
| skills | `skills-gen/SKILL.md` |
| talented / unique UI | `skills-gen/project-talent/SKILL.md` |
| rules | `rules-gen/SKILL.md` |
| library / MCP | `toolkit/SKILL.md` |
| needs_review queue | `evaluator/SKILL.md` |

## Template index

`templates/README.md` — all source paths (blueprint/, config/, skills/, …).

## Invariant

Docs = contract · Rules = law · Skills = map. One fact, one layer; others link.
