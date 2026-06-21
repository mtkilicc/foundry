# Build task plan — {{PROJECT_NAME}}

Status: empty | draft | agreed

> Foundry generates this **after** the skill hierarchy exists, so every task can
> name its **owning skill**. It is the build backlog for the agreed phases
> (MVP + v1; v2 only if the user asked). On a **re-run**, Foundry appends only
> tasks for the new scope — it does not regenerate completed rows.

## How Foundry fills this

1. Walk `02-scope-phases.md` (MVP, v1) and `04-domains.md` (domains + flows).
2. Break each phase capability into shippable tasks (one PR-sized slice each).
3. Assign the **owning skill** = the leaf whose `scope`/Owns covers that
   component (FE leaf, BE leaf, or both for full-stack flows).
4. Set `depends_on` for ordering; default unowned tasks get a `new_leaf`
   marker → create the leaf via `skills-gen/single-skill` first.
5. **UI build tasks (required):** for every UI leaf, emit task(s) to build its
   **UI surface** to the target UI/UX — implement the screens/components, the
   layout, and the **empty/loading/error/success** states from that leaf's
   *UI surface I deliver* section. Acceptance **must reference**
   `docs/stack/design-identity.md` (the general definition), not just "renders".
   A UI capability is not done until it reaches the defined UI/UX.

## Tasks

| id | phase | task | domain | owning skill(s) | depends_on | status |
|---|---|---|---|---|---|---|
| T001 | MVP | | | `agent/skills/<…>` | — | todo |
| T002 | MVP | | | | T001 | todo |
| T003 | v1 | | | | — | todo |

`status`: `todo` \| `in-progress` \| `done`
`owning skill(s)`: canonical leaf path(s); `new_leaf:<domain>` if no leaf exists yet.

## Coverage check (Foundry verifies before declaring the plan agreed)

- Every MVP + v1 capability in `02-scope-phases.md` maps to ≥1 task.
- Every task has an owning skill (or a `new_leaf` marker).
- No task spans two domains without naming both skills + a hand-off.
- **Every UI leaf has ≥1 UI-build task** that targets its UI surface + the
  global UX states, with acceptance referencing `docs/stack/design-identity.md`.
