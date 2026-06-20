---
name: <folder-name>
description: >-
  <Third person. WHAT + WHEN, pushy triggers: "Use whenever the user
  mentions A, B, or C, even if they don't say X.">
tier: root | orchestrator | leaf
scope: <glob — required for orchestrator/leaf; omit for root>
---

# <Name> (<tier label — e.g. leaf — read only when routed here>)

> A leaf is the **master expert** of ONE component (a FE feature or a BE
> service), not a generic router. It knows this component's contract, the
> decisions already made, the traps, and how to extend it — enough that an agent
> can ship a change here correctly without re-reading the whole codebase.

## Scope
Owns: ...
Does NOT own: ... (read sibling `<x>/SKILL.md` instead)

## Mastery (what makes this leaf an expert, not a router)
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
did this change the Contract / Code map / decisions / triggers above, or add a
capability the description wouldn't route to?
- **No** → nothing to do.
- **Yes** → this leaf must evolve. Self-trigger Foundry (do not wait to be told):
  `python scripts/foundry_skill_drift.py . --git --enqueue` → if proposals,
  hand to `../post-job-update/SKILL.md` (patch canonical) → `foundry_sync.py`.
- Learned something beyond this component's scope (a policy, a cross-cutting
  fact)? Don't absorb it — emit a `finding` event for the evaluator to route.

## UI composition (this project)
- Identity: `docs/stack/design-identity.md` — use the **Feature UI kits** row for this domain.
- Shell / kits: <real paths from fingerprint — never generic AppShell/shadcn defaults>

## Backend patterns (this project)
- Identity: `docs/stack/backend-identity.md` — mirror the listed app peer shape.
- Cross-cutting: <permissions/SSE paths from fingerprint>
