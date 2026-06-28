# Project blueprint — {{PROJECT_NAME}}

**Start here.** Foundry does not bootstrap skills, rules, or the full docs tree
until this blueprint is **complete** and **phase-agreed** (see gate below).

| field | value |
|---|---|
| Blueprint status | `empty` \| `draft` \| `complete` |
| Last reviewed | {{ISO date}} |
| Mode | `multi-file` (this tree) or `single-file` (`BLUEPRINT.md`) |
| Seed folder | optional — tell Foundry the path; agent runs import |
| Agreement record | [`.foundry/blueprint-agreement.json`](../../.foundry/blueprint-agreement.json) |

## Completion checklist

Every row must be `complete` before Foundry generation starts.

| # | document | status | owner |
|---|---|---|---|
| 1 | [00-vision.md](00-vision.md) | empty | user |
| 2 | [01-tech-stack.md](01-tech-stack.md) | empty | extract + **user** confirms/overrides |
| 3 | [02-scope-phases.md](02-scope-phases.md) | empty | user |
| 4 | [03-architecture.md](03-architecture.md) | empty | user+agent |
| 5 | [04-domains.md](04-domains.md) | empty | user+agent |
| 6 | [05-constraints.md](05-constraints.md) | empty | user |
| 7 | [06-open-questions.md](06-open-questions.md) | empty | user |

**User:** ask Foundry to import a seed folder or complete the blueprint interview.  
**Agent:** run `scripts/foundry_blueprint_import.py` and `scripts/foundry_blueprint_check.py`.

## How this relates to other docs

| stratum | role |
|---|---|
| **`docs/project/`** (this tree) | **WHY, WHAT, WITH WHAT** — intent, tech stack, phases |
| `docs/stack/` | HOW built — Docker, identity, tooling (Foundry-generated) |
| `docs/<component>/domain/` | WHAT IS — shipped capabilities (Foundry-generated) |

## Living document

Scope or stack changes → update `01-tech-stack.md` and/or `02-scope-phases.md` +
re-run phase agreement with Foundry.
