# Design identity — {{PROJECT_NAME}}

Status: {{shipped|building|planned}}

> **This file is unique to this repository.** Foundry mines it from local code
> and your stated visual direction — never copied from another project's
> design-system doc. Skills reference this page for *which* components to use;
> `frontend-structure` rule (law) defines *how* to compose them.

## Visual direction (one paragraph)

{{USER_STATED_DIRECTION — e.g. "Dense ops console: dark-first, monospace
metrics, floating nav, alarm-forward — not a marketing SaaS landing page."}}

## Signature (what makes this project visually distinct)

| element | this project | do NOT default to |
|---|---|---|
| app shell | `{{e.g. RootLayout + floating navbar}}` | generic sidebar + topbar template |
| primary layout | `{{e.g. full-width charts, no card grid}}` | dashboard card grid from tutorials |
| data density | `{{e.g. compact tables, 12px labels}}` | spacious consumer spacing |
| accent / alarm | `{{e.g. red badge on AlertsBell}}` | generic toast-only alerts |
| chart style | `{{e.g. shared charts/ components}}` | inline recharts from memory |

## Component inventory (exhaustive — from code scan)

Mine `{{frontend_root}}/components/ui/` and feature modules. List every
reusable primitive the agent may compose:

| component | path | use when |
|---|---|---|
| {{Button}} | `components/ui/button.tsx` | actions |
| {{...}} | `...` | ... |

## Feature UI kits (domain-specific composition)

| screen type | compose from | never |
|---|---|---|
| dashboard / metrics | `MetricTimeseriesChart`, `TimeRangeControl`, `ExpandableChart` | hand-rolled recharts |
| alarm surface | `AlertsBell` in header | nav link to alerts |
| tables | `components/ui/table` + module hooks | raw `<table>` markup |

## Tokens & styling source of truth

| concern | where defined | notes |
|---|---|---|
| colors / theme | `{{ThemeProvider path}}` | {{e.g. hand-rolled localStorage, not next-themes}} |
| spacing | `{{tailwind config or token file}}` | |
| typography | `{{...}}` | |

## New UI workflow

1. Check this page for an existing component or kit row.
2. If missing → add primitive to `components/ui/` **in the same PR** and add a row here.
3. Leaf skills link here; they do not invent parallel component lists.

## Cross-project law

When you run Foundry on another repo, **regenerate this file from that repo's
code** — do not transplant rows from this project.
