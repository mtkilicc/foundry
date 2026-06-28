# Intake question bank — the pre-defined coverage map

**This is the source of truth for *what Foundry can ask*.** Every project — a
one-sentence idea or a folder of docs — is normalized onto these slots. Whatever
the input does **not** answer is a *gap*.

**The user picks the mode up front: Full autonomy or Hybrid.**
- **Full autonomy** — Foundry answers everything itself (tech, design, anything
  the input left open) by best practice. No questions. (`delegated: true`)
- **Hybrid** — Foundry shows the user **both** the slots it already answered (its
  draft, for revision) **and** the open gaps; the user confirms/edits each.
  (`delegated: false`)
In **both** modes Foundry decides the design / creativity slots (`decide=foundry`)
— its creativity mandate — unless the user gives direction.

Goal: these areas cover **~90% of any project**. The remaining ~10% surfaces as
rows in `06-open-questions.md`.

## How the agent uses this file

1. **NORMALIZE** — read the user's input (sentence, paragraph, seed folder,
   existing repo) and map every fact onto a slot below. Record value + `source`
   (`user` | `seed` | `repo`).
2. **PRE-DRAFT** — draft a proposed answer for **every** remaining slot: input
   first, then best practice. Tag drafts `source: foundry-decided`.
3. **GAP SCAN** — split blocking slots into **answered** (user/seed/repo) vs
   **gaps** (only Foundry-drafted).
4. **MODE CHOICE — ask the user, then proceed:**
   - **Full autonomy** → keep all drafts; no questions. Set `delegated: true` (+ `delegated_by`).
   - **Hybrid** → present answered slots (for revision) + gaps (to fill); user
     resolves each (answer or explicit waive). `delegated: false`.
5. **FALLBACKS** — the `default` column (counts → **3**; phases → **MVP + v1**;
   v2+ only if asked) is applied in Full autonomy, and shown as a suggestion in Hybrid.
6. **RECORD (enforced)** — write each blocking slot's value + `source` into
   `.foundry/intake.json` (seed `../config/intake.json`). `default` /
   `foundry-decided` are accepted **only** when `delegated: true` (+ `delegated_by`).
   `foundry_blueprint_check.py` rejects unanswered or guessed-without-delegation slots.
7. **PROCEED** — continue once every blocking slot is *resolved* (Hybrid: user
   confirmed/edited; Full autonomy: Foundry filled), then the **mandatory approval**
   (see `../../docs-gen/project-blueprint/SKILL.md` § Approval).

`Decide` column: `ask` = a Hybrid question · `foundry` = Foundry decides
(design/creativity) · `derive` = compute from input/seed/repo if possible,
otherwise a Hybrid question (never default-and-skip outside Full autonomy).

---

## Area 0 — Situation & sources (the clarifying checklist, always first)

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| situation | What do you have today? | greenfield-idea \| seed-folder \| existing-repo \| docs-only \| re-run (foundry already ran) | auto-detect (see L1 Step −1) | yes | derive | run mode / routing |
| seed_paths | Path(s) to any starter / previous repo / docs to learn from | path list | none | no | ask | import |
| consuming_tools | Which LLM tools consume the output? | claude \| cursor \| openharness \| generic (multi) | claude | yes | ask | adapter / `.foundry/config.json` |
| placement_constraints | Constraints on where docs/code may live? | text | none | no | ask | adapter |
| existing_docs_action | Existing docs found — move, merge, or keep? | consolidate \| keep-separate | consolidate | no | ask | legacy-doc consolidation |

## Area 1 — Project identity

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| project_name | Project name? | text | repo/folder name | yes | derive | all |
| pitch | One sentence: what is it and for whom? | text | — | yes | ask | `00-vision.md` |
| archetype | Project archetype? | saas-b2b \| saas-b2c \| ecommerce \| marketplace \| internal-tool \| on-prem \| dashboard-analytics \| content-cms \| api-service \| dev-tool \| mobile-app \| other | — | yes | ask | identity + sizing |
| deployment | How is it deployed? | cloud-saas \| on-prem \| hybrid \| desktop \| mobile | derive from archetype | no | derive | `03-architecture.md` |
| monetization | Revenue model (if any)? | subscription \| one-time \| freemium \| usage-based \| none-internal | none-internal | no | ask | `00-vision.md` |

## Area 2 — Users & access

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| personas | Who uses it? List roles. | role list | **3** roles (foundry proposes from archetype) | yes | derive | `00-vision.md` |
| primary_persona | Primary persona? | one of personas | first persona | no | derive | `00-vision.md` |
| auth_model | Authentication model? | none \| email-password \| sso-oauth \| magic-link \| rbac-roles | derive from archetype | yes | derive | domains/constraints |
| tenancy | Single- or multi-tenant? | single \| multi | single (multi if saas-b2b) | no | derive | `03-architecture.md` |

## Area 3 — Business flows / capabilities

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| core_flows | Core end-to-end flows users perform? | flow list | **3** flows (foundry proposes from archetype) | yes | derive | `04-domains.md` |
| flow_detail | For each flow: trigger → steps → outcome | per-flow text | foundry drafts | no | derive | `04-domains.md` |
| domains | Capability/domain areas (group flows)? | domain list | derive from flows | yes | derive | `04-domains.md` |

## Area 4 — Pages / screens

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| pages | Pages/screens for MVP? | page list | **3** pages (foundry proposes from flows) | no | derive | `04-domains.md` / design |
| nav_shape | Navigation shape? | sidebar \| topnav \| tabs \| wizard \| single-page | foundry decides | no | foundry | design-identity |

## Area 5 — Data / backend models

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| models | Core data entities? | entity list | **3** models (foundry proposes from flows) | no | derive | `04-domains.md` |
| relationships | Key relationships between entities? | text | foundry drafts | no | derive | `03-architecture.md` |
| storage | Storage type? | relational \| document \| both \| none | relational | no | derive | `01-tech-stack.md` |

## Area 6 — Integrations & external services

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| integrations | Third-party services (payments, email, storage, analytics, LLM)? | service list | none | no | ask | `05-constraints.md` |
| llm_provider | If AI features: which model provider? | anthropic-claude \| other \| none | anthropic-claude | no | ask | `01-tech-stack.md` / toolkit |

## Area 7 — Tech stack

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| frontend | Frontend framework? | text | foundry picks for archetype | no | derive | `01-tech-stack.md` |
| backend | Backend framework? | text | foundry picks for archetype | no | derive | `01-tech-stack.md` |
| database | Database? | text | foundry picks for storage | no | derive | `01-tech-stack.md` |
| hosting | Hosting/runtime target? | text | derive from deployment | no | derive | `01-tech-stack.md` |

> Greenfield + unspecified: Foundry picks a current, coherent stack for the
> archetype (context7-verified versions), records `source: foundry-decided`, and
> lets the user override before the gate.

## Area 8 — Design / UX identity (creativity inputs)

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| visual_feel | 3–8 words for the visual feel? | text | **foundry decides** | no | foundry | design-identity |
| focal_area | What should the UI make *shine* (the signature)? | text | **foundry chooses** | no | foundry | design-identity |
| color_theme | Brand color / theme direction? | text | **foundry decides** | no | foundry | design-identity |
| density | Layout density? | spacious \| balanced \| dense | foundry decides | no | foundry | design-identity |
| mood | Mood? | playful \| professional \| minimal \| bold \| editorial | foundry decides | no | foundry | design-identity |

> **Anti-sameness law:** there is **no cross-project comparison**. Even given the
> same input twice, Foundry must pick a *fresh focal area* and creatively decide
> color/theme/density/mood so each run is distinct and extendable. See
> `../../skills-gen/project-talent/SKILL.md` and `../../docs-gen/stack-identity`.

## Area 9 — Scope & phasing

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| mvp_scope | MVP must-haves? | bullet list | foundry proposes from flows | yes | derive | `02-scope-phases.md` |
| v1_scope | v1 next features? | bullet list | foundry proposes | yes | derive | `02-scope-phases.md` |
| out_of_scope | Explicitly out of scope? | bullet list | foundry proposes | no | derive | `02-scope-phases.md` |
| want_v2 | Need a v2+ phase now? | yes \| no | **no** | no | ask | `02-scope-phases.md` |

## Area 10 — Constraints & non-functional

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| compliance | Compliance needs? | GDPR \| HIPAA \| PCI \| SOC2 \| none | none | no | ask | `05-constraints.md` |
| scale | Scale expectation? | prototype \| small \| growth \| large | small | no | ask | `05-constraints.md` |
| a11y_i18n | Accessibility / i18n required? | a11y \| i18n \| both \| none | none | no | ask | `05-constraints.md` |
| slos | Performance/reliability SLOs? | text | none | no | ask | `05-constraints.md` |

## Area 11 — Operations (optional, non-blocking)

| key | question | type / enum | default | blocking | decide | feeds |
|---|---|---|---|---|---|---|
| environments | Environments? | dev-only \| dev-staging-prod | dev-staging-prod | no | derive | `03-architecture.md` |
| cicd | CI/CD expectation? | text | none | no | ask | `05-constraints.md` |
| observability | Logging/metrics/tracing needs? | text | none | no | ask | `05-constraints.md` |

---

## Blocking set (must be filled or defaulted before the gate)

`situation`, `consuming_tools`, `project_name`, `pitch`, `archetype`,
`personas`, `auth_model`, `core_flows`, `domains`, `mvp_scope`, `v1_scope`.

Everything else is non-blocking: derived from input, Foundry-decided (design), or
parked as an open question. In **Hybrid**, any blocking slot the input didn't fill
is asked of the user (Foundry's draft shown for revision). In **Full autonomy**,
Foundry fills the whole set itself. Either way the gate enforces every blocking
slot is recorded with a valid `source`.
