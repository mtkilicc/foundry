# Backend identity — {{PROJECT_NAME}}

Status: {{shipped|building|planned}}

> Unique to this repository. Mined from `backend/` layout and conventions —
> not copied from other projects. Skills reference this for *how* to structure
> code; the `backend-structure` rule enforces it during generation.

## Architectural shape

| concern | this project | path anchor |
|---|---|---|
| app layout | `apps/<feature>/{models,serializers,views,services,urls,tasks}.py` | `apps/registry/`, `apps/alerting/` |
| business logic | services layer, thin views | `*/services.py` |
| auth | {{e.g. allauth headless + RBAC}} | `apps/core/permissions.py` |
| live updates | {{e.g. SSE event bus}} | `apps/core/sse_events.py` |
| background work | Celery tasks in app `tasks.py` | `*/tasks.py` |
| API style | {{e.g. DRF ViewSets, one error envelope}} | `docs/backend/api-*.md` |

## Do not introduce (this project)

| forbidden | use instead |
|---|---|
| thick views with business logic | `services.py` |
| parallel auth / permissions | `apps/core/permissions.py` classes |
| ad-hoc SSE / websocket | existing SSE bus |
| second pagination/error shape | see `docs/backend/domain/platform.md` |

## Per-app map (from code)

| app | owns | skill leaf |
|---|---|---|
| `core` | permissions, SSE, settings mounts | `agent/skills/backend/platform/` |
| `user` | RBAC, allauth adapters | `agent/skills/backend/user/` |
| {{...}} | ... | ... |

## Extension workflow

New app → match an existing app's file shape → add row here → add/extend leaf skill.

## Cross-project law

Regenerate from **this** repo's `backend/apps/` — never paste Django patterns
from a different Foundry run.
