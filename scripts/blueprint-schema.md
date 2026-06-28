# Project blueprint requirements (Foundry contract)

This document defines what the **project blueprint** must contain so Foundry
can generate talented skills, rules, and domain docs. Implementations:
`templates/blueprint/`, `docs-gen/project-blueprint/SKILL.md`,
`scripts/foundry_blueprint_check.py`.

## Purpose

Give the LLM **end-to-end understanding** of the project before any artifact
generation. Works for **greenfield** (empty TBDs → user fills) and
**brownfield** (agent drafts from code → user corrects).

## Location

| mode | path |
|---|---|
| Multi-file (default) | `docs/project/README.md` + `00-vision.md` … `06-open-questions.md` |
| Single-file | `docs/project/BLUEPRINT.md` |

Configured in `.foundry/config.json` → `blueprint.root`, `blueprint.mode`.

## Required sections

| file | title | filled by | gate |
|---|---|---|---|
| README | index + completion checklist | agent | status = complete |
| 00-vision | problem, users, metrics, non-goals | **user** | no required TBD |
| 01-tech-stack | extracted + user overrides | **user** confirms | conflicts resolved |
| 02-scope-phases | MVP, v1, v2, v3+ optional | **user** agrees | phases agreed in JSON |
| 03-architecture | components, data, deployment | agent draft + user | no required TBD |
| 04-domains | capability map → future domain docs | agent draft + user | no required TBD |
| 05-constraints | compliance, integrations, UX direction | **user** | no required TBD |
| 06-open-questions | blocking Q&A | **user** | no `open` rows |

## TBD markers

```html
<!-- FOUNDRY:TBD required="user" prompt="Question for the user?" -->
<!-- FOUNDRY:TBD required="agent" prompt="Agent fills from code." -->
<!-- FOUNDRY:TBD optional="true" prompt="May stay empty." -->
```

`foundry_blueprint_check.py` fails on required TBDs and `Status: empty`.

## Phase agreement

File: `.foundry/blueprint-agreement.json`

| field | rule |
|---|---|
| `required_phases_for_foundry` | default `["mvp", "v1"]` — must be `agreed` |
| `optional_phases` | `v2`, `v3`, `v4`… user may add keys |
| `phases.<name>.status` | `agreed` required for bootstrap |
| `agreed_at`, `agreed_by` | set at ceremony |

User and LLM explicitly align on what MVP vs v1 vs v2 means **before** Foundry runs.

## Foundry integration

| stage | behavior |
|---|---|
| Bootstrap BIG PATH | `foundry_blueprint_check` **blocks** until pass |
| Fast path | allowed; phase promotion requires blueprint update |
| full-tree | reads blueprint domains + active phase for `Status: planned` |
| project-talent | reads UX direction from blueprint constraints |
| Living project | `blueprint_change` queue → project-blueprint skill |

## Import from seed folder

Agent runs: `python scripts/foundry_blueprint_import.py <repo> --from <seed> --write`

Extracts tech stack from seed + repo; copies missing blueprint markdown.
User must still override in `01-tech-stack.md` when intent differs.

## Full pipeline order

```
0. optional: blueprint_import (--from seed)
1. project-blueprint (user interview + stack confirm + agreement)
2. foundry_blueprint_check → green
3. adapter + work-order
4. rules → docs/stack → docs/domain (from blueprint)
5. skills → project-talent → sync → checks
```
