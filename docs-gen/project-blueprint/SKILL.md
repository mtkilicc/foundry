---
name: project-blueprint
description: >-
  Creates or completes the project blueprint — the start-point docs that let an
  LLM understand the project end-to-end before Foundry generates skills, rules,
  and domain docs. Handles empty TBD sections, MVP/v1/v2 phase agreement, living
  updates during development, single-file or multi-file layout. Use before any
  Foundry bootstrap on new or existing repos.
---

# project-blueprint (leaf — START HERE for bootstrap)

Foundry **does not** run full generation until the agent runs
`foundry_blueprint_check.py` and it exits 0.

## Project states (Empty / Blueprint / Running)

The state = **what the user brings**. Record it in `blueprint-agreement.json`
`state` during SITUATION. All states run Intake & normalization, the mode choice,
and the mandatory approval; the method + addenda differ:

| state | user brings | method + state-specific steps |
|---|---|---|
| **Empty** | an idea / text / md (no app) | greenfield method below |
| **Blueprint** | a blueprint or docs (no running app) | greenfield/seed method **+ PRUNE** parts not in the agreed idea **+ dynamic UI redesign** |
| **Running** | an existing, running app | brownfield/re-run method **+ two approved docs** (current-state + requested-state) |

State addenda:
- **Blueprint — prune:** after import/normalize, **remove blueprint parts not in
  the agreed idea** (out-of-scope domains, stale sections). Keep only what the
  project needs; the remainder is the start point.
- **Blueprint — dynamic UI redesign:** do **not** inherit the blueprint's UI. Run
  `../stack-identity/SKILL.md` **greenfield (generative)** to redesign the UI fresh
  from the project idea — regenerable, not a copy of the provided design.
- **Running — current-state first:** build `docs/project/CURRENT-STATE.md` **with
  the user** — mine the code and confirm with the user until the app's exact
  functionality is fully understood. Then `docs/project/REQUESTED-STATE.md` for the
  change. Both pass the mandatory approval (two documents).

## Output layout (pick one with user)

| mode | path | when |
|---|---|---|
| **multi-file** (default) | `docs/project/README.md` + `00-`…`05-` | teams want section owners |
| **single-file** | `docs/project/BLUEPRINT.md` | small projects, one doc |

Record in `.foundry/config.json`:
```json
"blueprint": { "root": "docs/project", "mode": "multi-file", "gate_required": true }
```

Copy templates from `../../templates/blueprint/`.
Copy `../../templates/config/blueprint-agreement.json` → `.foundry/blueprint-agreement.json`.
Copy `../../templates/config/intake.json` → `.foundry/intake.json` (enforced by the gate).

## Import from seed folder (optional)

User may point at an **existing project or blueprint folder** (starter template,
previous repo, `project_overview/`, etc.). **Agent runs:**

`python scripts/foundry_blueprint_import.py <repo> --from <seed_folder> --write`

This:
1. **Copies** missing `docs/project/*.md` from seed (does not overwrite user edits).
2. **Extracts tech stack** from seed + target repo (lockfiles, compose, package.json).
3. Writes `.foundry/tech-stack-extract.json` and drafts `01-tech-stack.md`.

Then **interview user overrides** — seed stack vs what they actually want:

| seed has | user wants | action |
|---|---|---|
| React + Vite | keep | mark `final` agreed |
| Django | swap to FastAPI | conflict row → user `final` |
| (missing) | add ClickHouse | user overrides table |

Never silently adopt seed tech; **user confirms** every `final` row before gate.

## Consolidate existing docs (when `existing_docs_action=consolidate`)

The repo may already hold scattered docs (specs, notes, `documentation/`). Pull
them into the canonical tree instead of leaving duplicates. **Agent runs:**

`python scripts/foundry_blueprint_import.py <repo> --archive-legacy --write`

This MOVES stray `*.md` (outside `docs/project|stack|integration`, agent/skills,
tool folders, and root README/AGENTS/CLAUDE) under `docs/_legacy/` and writes
`.foundry/legacy-docs.json`. It never deletes — the move is reversible.

Then **consolidate each manifest entry** (judgment, not script):
1. Read the archived doc; map its content onto question-bank slots / canonical
   sections (vision, scope, domains, constraints, or a `docs/<component>` page).
2. Merge — fold facts in; dedupe against what normalization already captured.
3. Set the entry `status`: `consolidated` (+ `consolidated_into` path) | `kept`
   (genuinely separate, leave in `docs/_legacy/`) | `dropped` (obsolete).
4. Once no entry is `pending`, delete the now-empty `docs/_legacy/` subtrees for
   `consolidated`/`dropped` items. Keep `kept` items in place.

If `existing_docs_action=keep-separate`, skip archiving; only index them.

## Intake & normalization (run FIRST — all scenarios)

The question bank `../../templates/intake/question-bank.md` is the pre-defined
coverage map (~90% of any project). It defines **every slot Foundry can ask
about** — so the only questions are the gaps. Run it before scaffolding:

1. **SITUATION** — Area 0 checklist: greenfield-idea / seed-folder /
   existing-repo / docs-only; consuming tools (adapter); seed paths;
   existing-docs action. **Name the state** (Empty / Blueprint / Running) and
   record it in `blueprint-agreement.json` `state`.
2. **NORMALIZE** — map the user's input (one sentence *or* a folder of docs)
   onto question-bank slots; record each value's `source`
   (`user`/`seed`/`repo`). A single sentence and a full spec land in the **same**
   slots — that is the "one main structure".
3. **PRE-DRAFT** — Foundry drafts a proposed answer for **every** question in the
   bank: from the input first, then best practice for the rest. Tag each draft
   `source: foundry-decided`. This is the answer set the mode choice operates on.
4. **GAP SCAN** — split blocking slots into **answered** (from user/seed/repo) vs
   **gaps** (only Foundry-drafted so far).
5. **MODE CHOICE — ask the user up front, then proceed by the pick:**
   - **Full autonomy** → Foundry keeps all its drafted answers, deciding tech,
     design, and everything unanswered by best practice. **No further questions.**
     Set `delegated: true` (+ `delegated_by`).
   - **Hybrid** → present BOTH the **already-answered** slots (Foundry's draft, for
     the user to revise) AND the **unanswered** gaps; the user confirms/edits each.
     Prepare final answers from their input. `delegated: false`.
   - Either mode: Foundry decides the `decide=foundry` design/creativity slots
     (visual feel, focal area, nav); user direction overrides. Hand design to
     `../../skills-gen/project-talent/SKILL.md`.
6. **FALLBACKS** — counts (personas/flows/pages/models) → **3**; phases →
   **MVP + v1** (no v2 unless `want_v2=yes`). In Hybrid these are suggestions shown
   for revision; in Full autonomy they are applied.
7. **RECORD (enforced)** — write `.foundry/intake.json` (seed from
   `../../templates/config/intake.json`): every blocking slot gets a `value` +
   `source`. `default`/`foundry-decided` are valid **only** when `delegated: true`
   (Full autonomy). The gate (`foundry_blueprint_check.py`) **fails** on an
   unanswered or guessed-without-delegation slot.
8. **PROCEED** — once every blocking slot is resolved (Hybrid: user
   confirmed/edited; Full autonomy: Foundry filled), scaffold + fill, then run the
   **Approval** step below. Never skip an unresolved blocking slot.

Non-blocking gaps become `06-open-questions.md` rows, not blockers.

## Method — greenfield (new project)

*Empty state uses this. **Blueprint state** uses this too, plus the prune +
dynamic-UI-redesign addenda in Project states above.*

0. **IMPORT** (optional) — if user gave seed folder, run import `--write`.
1. **INTAKE** — run Intake & normalization above (situation, normalize, gaps).
2. **SCAFFOLD** — write all template files; fill normalized slots; remaining
   blocking gaps = `FOUNDRY:TBD`; ask the batched gap questions, then replace.
3. **DECOMPOSE (sizing engine)** — Foundry decides the concrete shape from
   `archetype` + flows. Default **3** each unless the user gave a number:
   - **business flows** → `04-domains.md` cross-domain flows (trigger→steps→outcome)
   - **domains** → group flows into capability areas (each becomes a future leaf)
   - **backend models** → core entities + relationships → `03-architecture.md`
   - **pages/screens** → per domain, with the focal area from design identity
   Record every Foundry-decided count with `source: foundry-decided`; the user
   can bump a count, but absent input the engine proposes a coherent set.
   Then draft architecture + domains tables. Design language comes from
   `../stack-identity/SKILL.md` **greenfield (generative)** method.
4. **PHASE WORKSHOP** — `02-scope-phases.md`: agree **MVP** and **v1** only
   (Foundry proposes the split from flows). **No v2+** unless `want_v2=yes` —
   then add v2 (and v3…) rows, `optional` until promoted.
5. **CLOSE QUESTIONS** — `06-open-questions.md`: every row `answered` or `waived`.
6. **AGREEMENT** — user confirms; set `blueprint-agreement.json`:
   - `phases.mvp.status` / `v1.status` = `"agreed"`
   - `agreed_at`, `agreed_by`, one-line `summary` per phase
7. **COMPLETE** — README `Blueprint status: complete`; run blueprint check.

## Method — brownfield (existing project)

*Running state uses this (or re-run below), plus the current-state +
requested-state dual-doc addenda in Project states above.*

0. **IMPORT** — run import on repo root (`--write`); merge seed folder if given.
1. **SCAFFOLD** same tree (skip files copied from seed).
2. **MINE** — explore subagents inventory code, routes, apps, compose; **draft**
   architecture + domains from reality; mark confidence gaps as TBD for user.
3. **RECONCILE** — user corrects wrong inferences; phases: what is **shipped** vs
   **planned** (MVP/v1 may already be partially shipped — document as-is).
4. **INTAKE GAP SCAN** — run the question bank against mined facts; interview
   only the remaining blocking gaps + phase agreement for **what's next**.
5. Steps 5–7 same as greenfield.

## Method — re-run (Foundry already initialized)

Detected at L1 Step −1 (`.foundry/config.json` + `agent/skills/` exist). **Do
not re-scaffold or re-interview.** The blueprint already exists — treat the
request as a **living update**: amend only the affected sections (see *Living
updates* below), keep the existing identity/fingerprint, re-agree phases only if
the job promotes a phase or changes intent. Then let the changed leaf evolve via
its **Evolution self-check** and sync to all targets.

## Phase agreement ceremony (required)

Present a table; user must explicitly approve:

| phase | in scope (bullets) | out of scope | status |
|---|---|---|---|
| MVP | … | … | agree? |
| v1 | … | … | agree? |
| v2 | *only if `want_v2=yes`* | … | agree? |

On approval → update agreement JSON + phase log in `01-scope-phases.md`.

## Living updates (mid-project)

| change | update |
|---|---|
| scope creep / new v2 item | `02-scope-phases.md` + agreement amend |
| stack change | `01-tech-stack.md` conflicts table + `docs/stack/versions.md` audit |
| new open question | `06-open-questions.md` — **blocks next bootstrap** until closed |
| intent change | blueprint first, then domain docs via docs-gen |
| phase shipped | `status: shipped` in phases + matching domain doc Status |

Append `blueprint_change` event to queue when phases change materially.

## Approval (mandatory — single consolidated document)

The multi-file tree stays the source; for sign-off Foundry assembles **one
document**. Generation does not start without explicit user approval.

1. **ASSEMBLE** — agent runs
   `python ../../scripts/foundry_blueprint_assemble.py <repo>` → writes
   `docs/project/APPROVAL.md` (the whole blueprint in one file).
   **Running state:** also assemble `--current` and `--requested` →
   `docs/project/CURRENT-STATE.md` + `docs/project/REQUESTED-STATE.md`.
2. **PRESENT** — show the consolidated document(s) to the user.
3. **REVISE LOOP** — user requests changes → edit the canonical files →
   re-assemble → present again. **Repeat until the user explicitly approves.**
4. **RECORD** — set `blueprint-agreement.json` `approval.project`
   (Running: `running_approval.current_state` + `requested_state`):
   `approved: true`, `approved_by`, `approved_at`. The gate requires this.

## Verify

Agent runs `python ../../scripts/foundry_blueprint_check.py <repo>` → exit 0.

## Hand-offs (only after gate passes)

| next | read |
|---|---|
| Full docs tree | `../full-tree/SKILL.md` (uses domains + phases) |
| Stack identity | `../stack-identity/SKILL.md` (UX direction from § constraints) |
| Skills/rules bootstrap | `../../SKILL.md` BIG PATH |

## Laws

- Blueprint = intent; domain docs = as-built. Never skip blueprint on brownfield.
- Empty sections are OK **during** interview; not OK at gate.
- User agreement on MVP+v1 is mandatory; v2+ may be draft until user promotes.
