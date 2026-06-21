---
name: <folder-name>
description: >-
  <Third person. WHAT + WHEN, pushy triggers: "Use whenever the user
  mentions A, B, or C, even if they don't say X.">
tier: root | orchestrator | leaf
scope: <glob — required for orchestrator/leaf; omit for root>
---

# <Name> (<tier label — e.g. leaf — read only when routed here>)

> A leaf is the **senior specialist** of ONE area — expert on **two axes**:
> (1) the **domain capability** itself (what doing this well requires, regardless
> of stack) and (2) the **implementation** in THIS repo. Generic tech awareness is
> not enough; it must hold the area to a specialist's quality bar and know the
> operations, states, edge cases, and failure modes of the capability.

## Scope
Owns: ...
Does NOT own: ... (read sibling `<x>/SKILL.md` instead)

## Capability mastery (the domain capability — tech-independent)
*What a senior specialist in this area always knows. Keep it specific to THIS
capability, not generic advice.*
- **Sub-capabilities:** the distinct operations this area must do well (the verbs
  — e.g. auth → register · login · session refresh · password reset · MFA · lockout).
- **Quality bar / "done right":** the standard a specialist holds it to
  (correctness, security, UX, performance, accessibility — whichever apply here).
- **States & edge cases (must-handle):** empty / loading / error / partial;
  concurrency, limits, retries, recovery — the ones THIS capability must cover.
- **Decision criteria:** how a specialist chooses between options here (when X vs Y).
- **Capability failure modes:** the ways this area is commonly done wrong.

## Implementation mastery (how it's built in THIS repo)
- **Contract:** the inputs/outputs this component guarantees (props/API shape,
  events, states) — link the doc, state the invariants here.
- **Key decisions already made:** the 2–4 choices a newcomer would otherwise
  re-litigate (e.g. "list is virtualized", "writes go through the X service").
- **Gotchas / anti-patterns:** the specific traps in THIS component (not generic
  advice) — what breaks, what looks right but isn't.
- **Extension points:** where new behavior slots in cleanly (the "extendable"
  seams) so growth reuses the existing shape.

## Specialist docs (LEAF docs only — never category READMEs)
- `docs/<component>/domain/<leaf>.md` — read when ...

## Code map
- `<path/to/module>` — ...

## MCPs used (capability names; setup lives in docs/stack/mcp-setup.md)
- e.g. browser-automation MCP — verify <flow> before claiming done

## Domain invariants (what no rule can know)
- ...

## Cross-domain hand-offs
- For <adjacent concern> → `../<sibling>/SKILL.md`

## Evolution self-check (this skill owns its own upkeep)
After implementing a feature in this component, **before declaring done**, decide:
did this change the Contract / Code map / decisions / triggers above, add a new
**sub-capability / edge case** the Capability mastery should record, or add a
capability the description wouldn't route to?
- **No** → nothing to do.
- **Yes** → this leaf must evolve. Self-trigger Foundry (do not wait to be told):
  `python scripts/foundry_skill_drift.py . --git --enqueue` → if proposals,
  hand to `../post-job-update/SKILL.md` (patch canonical) → `foundry_sync.py`.
- Learned something beyond this component's scope (a policy, a cross-cutting
  fact)? Don't absorb it — emit a `finding` event for the evaluator to route.

## UI surface I deliver (UI leaves only — what this skill builds)
*A UI leaf must know its target UI/UX, anchored to the general definition. Delete
this section for backend-only leaves.*
- **General definition:** `docs/stack/design-identity.md` (UX system + Feature UI
  kit row for this domain) — this skill conforms to it, never reinvents it.
- **Screens / components I render:** <the concrete views this skill owns>.
- **Layout & placement:** <where they sit in the app shell / page scaffold>.
- **Kits & tokens used:** <real components from the inventory — never generic
  AppShell/shadcn defaults>.
- **UX states I must render:** empty · loading · error · success (per the global
  states table) — list the specific copy/treatment for this surface.
- **Visual acceptance:** "looks like …" <the done-bar for this UI, referencing
  the design language>.

## Backend patterns (this project)
- Identity: `docs/stack/backend-identity.md` — mirror the listed app peer shape.
- Cross-cutting: <permissions/SSE paths from fingerprint>
