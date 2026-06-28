# Build task plan — {{PROJECT_NAME}}

Status: empty | draft | agreed

> Foundry generates this **after** the skill hierarchy exists, so every task can
> name its **owning skill**. It is the build backlog for the agreed phases
> (MVP + v1; v2 only if the user asked). On a **re-run**, Foundry appends only
> tasks for the new scope — it does not regenerate completed rows.

## How Foundry fills this

1. Walk `02-scope-phases.md` (MVP, v1), `04-domains.md` (domains), and
   `business-flows.md` (the end-to-end flows). **Every MVP business flow maps to
   ≥1 task** — a flow with no task is a coverage gap, not a choice.
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
6. **Weight every task** — score it 1–10 (see *Task weight* below).

## Task weight (1–10) — set on every task

Weight captures how **hard**, **complicated**, **big**, and **important** a task
is. Use it for sequencing, parallelization, and where to focus review. Score each
factor 1–5 with the rubric, combine, scale to 1–10.

| factor | measures | 1 (low) | 5 (high) |
|---|---|---|---|
| **H** hardness | technical difficulty, novelty, unknowns | well-trodden, copy-paste | novel/research, high uncertainty |
| **C** complexity | moving parts, integrations, edge cases | single unit, no deps | many components/states/edge cases |
| **B** bigness | size / effort / surface area | tiny, one file | large, many files/screens |
| **I** importance | criticality, blast radius, MVP-criticality | nice-to-have | core/blocking, costly if wrong |

**Formula** (factor weights sum to 1, so `raw ∈ [1,5]`):
```
raw    = 0.30·H + 0.25·C + 0.20·B + 0.25·I
weight = round( 1 + (raw − 1) × 2.25 )      # maps [1,5] → [1,10]; clamp to [1,10]
```
All factors = 1 → weight 1; all = 5 → weight 10.

**Record as** `weight (H·C·B·I)` for auditability. Example `7 (H4·C3·B3·I5)`:
`raw = .30·4 + .25·3 + .20·3 + .25·5 = 3.8` → `1 + (2.8 × 2.25) = 7.3` → **7**.

## Tasks

| id | phase | task | domain | owning skill(s) | weight (1-10) | depends_on | status |
|---|---|---|---|---|---|---|---|
| T001 | MVP | | | `agent/skills/<…>` | 7 (H4·C3·B3·I5) | — | todo |
| T002 | MVP | | | | 4 (H2·C2·B2·I3) | T001 | todo |
| T003 | v1 | | | | | — | todo |

`status`: `todo` \| `in-progress` \| `done`
`weight`: 1–10 from the formula below, shown with its `(H·C·B·I)` breakdown.
`owning skill(s)`: canonical leaf path(s); `new_leaf:<domain>` if no leaf exists yet.

## Re-run / modify — task immutability (NEVER rewrite work)

On a re-run or a modify request, the existing plan is a **ledger, not a draft**.
Foundry **appends**; it does not rewrite history.

- **`done` task → immutable.** Never edit, renumber, reword, reorder, or delete a
  `done` task. If a change touches that capability, write a **NEW** task that
  supersedes it (reference the prior id in the task text). The original work/commit
  stays recoverable.
- **`in-progress` task → ASK first.** If a change genuinely needs an in-progress
  task altered, Foundry does **not** decide silently — it asks the user (or, when
  fully delegated, queues the question and writes a new task instead of mutating).
- **`todo` task (never started) → editable** in place (not yet work).
- **Removing a feature ≠ deleting tasks.** Add a `Remove X` decommission task and
  mark the capability obsolete in the docs; keep the historical rows.
- **Subtasks (optional).** A large task may split into sub-tasks with `T0NN.n` ids
  (e.g. `T012.1`) whose `depends_on` names the parent `T012` — a main-task →
  sub-task tree the dev loop / branch tracking can follow. Subtasks inherit the
  parent's immutability state.

## Coverage check (Foundry verifies before declaring the plan agreed)

- Every MVP + v1 capability in `02-scope-phases.md` maps to ≥1 task.
- Every task has an owning skill (or a `new_leaf` marker).
- No task spans two domains without naming both skills + a hand-off.
- **Every UI leaf has ≥1 UI-build task** that targets its UI surface + the
  global UX states, with acceptance referencing `docs/stack/design-identity.md`.
- **Every task has a `weight` (1-10)** computed from the formula, shown with its
  `(H·C·B·I)` breakdown.
