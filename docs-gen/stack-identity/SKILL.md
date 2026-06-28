---
name: stack-identity
description: >-
  Creates or audits docs/stack/design-identity.md and backend-identity.md by
  mining THIS repository's code — never copying from other Foundry projects.
  Use at bootstrap, after major UI/backend refactors, or when skills need a
  richer component and app inventory.
---

# stack-identity (leaf — read only when routed here)

## Laws
- **Mine, don't memory** (brownfield): scan `frontend/src`, `backend/apps/`,
  tailwind/theme config. Zero rows from another repo or generic tutorials.
- **Generate, don't compare** (greenfield): with no code to mine, *invent* a
  distinct identity from the archetype. Distinctiveness comes from a fresh
  creative pass each run — **never** from comparing against other projects.
- **Interview once:** if the user offers a visual direction, record it; if not,
  Foundry **decides** it (design slots in the question bank are `decide=foundry`).
- Facts live here; rules point here; skills link here (one sentence + table row).

## Method — greenfield (generative, nothing to mine)

Run when `situation=greenfield-idea` (no `frontend/src` to inventory). Foundry
**decides every design piece** — it does not ask, and it does not copy.

**Blueprint state also uses this method** (user brought a blueprint but no app):
**redesign the UI fresh from the project idea — do NOT inherit the blueprint's
UI.** The design is dynamic/regenerable, not a copy of the provided one.

1. **CREATIVE BRIEF** — fill this prompt from `archetype` + `pitch` (+ any user
   `visual_feel`/`mood`), then commit to the answers:
   > *For a {archetype} called {name} that {pitch}: name the ONE focal area /
   > interaction that must shine ({focal_area}); a visual concept in 3–8 words
   > ({visual_feel}); a mood ({mood}); and the generic version we refuse to ship
   > ({divergence}).*
   **Anti-sameness law:** given the *same* input twice, pick a **different**
   focal area and palette. Distinctiveness is generated, not compared — there is
   no cross-project registry and no other repo to diff against.
2. **UX SYSTEM (general definition — required)** — fill the design-identity
   **UX system** section: design language (color/type/density/radius/motion),
   layout system (app shell, navigation, grid, page scaffold), global UX states
   (empty/loading/error/success), and the interaction + accessibility baseline.
   This is the project-wide UI/UX contract every UI leaf builds against.
3. **SIGNATURE COMPONENTS** — name the components the focal area needs (specific,
   not "a card"); fill the signature table with ≥3 "do NOT default to" contrasts
   (e.g. *not* a generic shadcn dashboard).
4. **WRITE** — fill `../../templates/docs/stack-design-identity.md` →
   `docs/stack/design-identity.md`; same for backend identity from the archetype.
5. **FINGERPRINT** — `.foundry/project-fingerprint.json`: `visual_signature` =
   the concept; `forbidden_cross_project` = the generic patterns this project
   refuses; planned (not-yet-existing) frontend/backend paths.
6. **INDEX + EMIT** — add both docs to `docs/stack/README.md`; emit
   `new_artifact` events. Extendable by design: leave a "Growth hooks" note so
   later domains slot into the same language.

## Method — brownfield (mine existing code)
1. FINGERPRINT — write `.foundry/project-fingerprint.json` from
   `../../templates/config/project-fingerprint.json` (paths, shell name, forbidden
   cross-project phrases from any *other* repo the user names).
2. MINE FRONTEND — inventory `components/ui/`, `components/charts/`, layout
   (`routes/`, shell component), theme provider, module hooks pattern.
   Fill `../../templates/docs/stack-design-identity.md` →
   `docs/stack/design-identity.md`.
3. MINE BACKEND — inventory `apps/*/` file shapes, permissions, SSE, Celery.
   Fill `../../templates/docs/stack-backend-identity.md` →
   `docs/stack/backend-identity.md`.
4. INDEX — add both to `docs/stack/README.md` (or create it).
5. EMIT `new_artifact` events for both docs.

## Verify
- Every component row has a path that exists on disk.
- Signature table has at least 3 "do NOT default to" contrasts.
- No `{{placeholders}}` left.
- Run `python ../../scripts/foundry_identity_check.py <repo>`.

## Hand-offs
- Structure rules → `../../rules-gen/identity-rules/SKILL.md`
- Enrich skills → `../../skills-gen/project-talent/SKILL.md`
