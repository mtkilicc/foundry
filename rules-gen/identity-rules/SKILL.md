---
name: identity-rules
description: >-
  Generates project-unique frontend structure + design identity rules and
  backend structure rule from docs/stack/*-identity.md. Use at bootstrap or
  when identity docs change. Replaces generic design-system rules that assume
  every project looks the same.
---

# identity-rules (leaf — read only when routed here)

## Two-tier frontend (required)

| rule | scope | owns |
|---|---|---|
| **frontend-structure** | `globs: frontend/**` | HOW to build — compose, no ad-hoc, read identity doc first |
| **frontend-design-identity** | `globs: frontend/**` | WHAT to use — this project's shell, kits, component table |

Render from:
- `../../templates/rules/frontend-structure.mdc` (stable across projects)
- `../../templates/rules/frontend-design-identity.mdc` (fill from
  `docs/stack/design-identity.md` — **unique per repo**)

Never ship a single rule that hardcodes `AppShell`, `PriceCard`, or tutorial
layouts unless those paths exist in **this** repo's fingerprint.

## Backend structure rule

Render `../../templates/rules/backend-structure.mdc` from
`docs/stack/backend-identity.md`. Scoped `backend/**`.

## Method
1. READ both identity docs + fingerprint. If missing →
   `../../docs-gen/stack-identity/SKILL.md` first.
2. FILL design-identity rule table from **Signature** + **Feature UI kits**
   sections only — not from model memory.
3. WRITE rules in the adapter profile's format (`.mdc`, AGENTS.md section, …).
4. GREP skills — delete any design-system policy restatements; replace with
   link to identity doc + kit row pointer.
5. Append `new_artifact` events; `foundry_check.py queue`.

## Verify
- frontend-structure does not name project-specific components (only points to doc).
- frontend-design-identity does not duplicate AGENTS.md policy paragraphs.
- `foundry_identity_check.py` passes.
