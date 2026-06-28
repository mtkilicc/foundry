# Business flows

Status: planned

> The end-to-end journeys the product exists to serve — the contract a milestone
> is verified against (the build must actually PERFORM each flow) and the bridge
> from intent to implementation: every flow maps to the domains/skills that build
> it and the tasks that fulfill it. Derived from the intake `core_flows` /
> `flow_detail` slots; kept in step with `docs/project/04-domains.md` cross-domain
> flows. One fact, one layer — this page OWNS flow detail; `04-domains.md` only
> indexes which domains a flow touches.

## How to use this page

- **Blueprint:** decompose the idea into its core flows here before generating
  skills — the flows ARE the MVP definition.
- **Task plan:** every flow maps to ≥1 build task; the task plan must cover every
  MVP flow (a flow with no task is a gap).
- **Milestone verify:** the build must demonstrably perform each MVP flow
  end-to-end; the milestone report lists flow coverage.
- **Modify:** a new feature adds/edits a flow here first, then its tasks.

## Flow index

| id | flow | actor | phase (MVP/v1) | touches domains | status |
|---|---|---|---|---|---|
| F1 | | | MVP | | planned |

<!-- FOUNDRY:TBD required="user+agent" prompt="List every core end-to-end flow (default 3 for the MVP, proposed from the archetype). Each row gets a detail block below." -->

## Flow detail

### F1 — <flow name>

| field | value |
|---|---|
| actor | <who initiates it> |
| trigger | <what starts the flow> |
| steps | 1. … → 2. … → 3. … (the user/system exchange) |
| outcome | <the observable success state> |
| touches | `<domain-a>`, `<domain-b>` (owning skills) |
| acceptance | <how a milestone proves this flow works end-to-end — the QA/behavior check> |
| tasks | <task ids that fulfill it, once the task plan exists> |

<!-- Repeat one block per flow. Acceptance feeds milestone verify (behavior-vs-docs);
     `tasks` closes the loop so flow coverage is checkable. No "see code". -->
