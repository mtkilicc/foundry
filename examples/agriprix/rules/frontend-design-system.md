---
description: Every Agriprix page uses the same shell, tokens, and components
globs: frontend/src/**
---

# Frontend design system

## Principle
Every page composes existing components from `frontend/src/ui/`; a new
visual pattern updates docs/stack/design-system.md FIRST, then ships.

## Change-type → action
| When you... | You must... |
|---|---|
| add a page | wrap in `<AppShell>`; use spacing scale tokens only |
| show a price | use `<PriceCard>` / `<PriceTable>` — never ad-hoc markup |
| need a new component | add to ui/ + design-system doc in the same PR |

## Do / Don't
DO:    <AppShell><PriceTable data={prices} /></AppShell>
DON'T: <div style={{margin:'13px'}}><table>...   // off-scale, ad-hoc

## Conflict resolution
Conflicts with a leaf skill's layout note → this rule wins; update the
skill.
