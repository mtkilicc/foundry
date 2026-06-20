---
name: project-talent
description: >-
  Makes skills and rules project-talented: mine UI/backend identity from this
  repo, generate per-project structure rules, enrich leaf skills with
  composition kits and backend patterns. Use at bootstrap after full-hierarchy,
  when skills feel generic, or when starting Foundry on a new repo that must
  NOT look like your other projects.
---

# project-talent — enrich skills from this project

Generic skills route; **talented** skills know this repo's shell, chart kit,
app layout, and forbidden copy-paste from other Foundry runs.

## Pipeline (run in order)

| step | read |
|---|---|
| 1. Mine identity docs | `../../docs-gen/stack-identity/SKILL.md` |
| 2. Structure rules | `../../rules-gen/identity-rules/SKILL.md` |
| 3. Enrich leaves | this file § Enrich method |
| 4. Verify | `foundry_identity_check.py` + `foundry_sync.py` |

## Identity source (no blocking interview)
1. Read `docs/project/05-constraints.md` **Visual / UX direction** (if the user
   gave one) and any question-bank design slots.
2. Greenfield, no direction given → **Foundry decides** via
   `../../docs-gen/stack-identity` *greenfield (generative)* method: it invents a
   focal area + palette fresh each run (design slots are `decide=foundry`), and
   writes `forbidden_cross_project` from the generic patterns it refuses. Do not
   ask the user; do not compare to other repos.
3. Brownfield: skip interview; mine code only.

## Enrich method — every frontend leaf

Add or refresh (≤15 lines total; link, don't restate rules):

```markdown
## UI composition (this project)
- Identity: `docs/stack/design-identity.md` — read the **Feature UI kits** row for this domain.
- Shell: `{{RootLayout path}}`
- Kits: {{comma-separated chart/table components from inventory}}
- Never: {{one anti-pattern from signature table}}
```

Delete generic lines ("use shadcn", "use AppShell") unless that exact
component exists in this repo.

## Enrich method — every backend leaf

```markdown
## Backend patterns (this project)
- Identity: `docs/stack/backend-identity.md`
- App shape: mirror `apps/{{peer}}/`
- Cross-cutting: permissions `{{path}}`, SSE `{{path}}`
```

Domain invariants stay; **shape** points to identity doc.

## Cross-project uniqueness law

| do | don't |
|---|---|
| scan this repo's `components/ui/` | copy design-identity from another repo |
| record fingerprint per project | reuse same `forbidden_cross_project` list |
| regenerate rules when identity changes | hand-edit only `.cursor/rules` without canonical |

## Verify
- Each frontend leaf has **UI composition** with real paths from fingerprint.
- Each backend leaf has **Backend patterns** with real app peer.
- `python ../../scripts/foundry_identity_check.py <repo>` → exit 0.
- Boundary grep: skills contain no `alwaysApply`, no full policy tables.

## Hand-offs
- New domain without leaf → `../single-skill/SKILL.md`
- Identity doc drift after feature → `../post-job-update/SKILL.md`
