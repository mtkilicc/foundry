---
name: adapter
description: >-
  Tool/framework adapter. Use at the start of EVERY foundry job, and whenever
  output paths, frontmatter fields, or rule formats are about to be written:
  it asks which LLM tool or agent framework the user runs and maps all
  generated artifacts to that tool's layout. Also use to add support for a
  new tool.
---

# adapter — L2 (always consulted first)

## Step 1 — Find or establish the active profile
1. Look for `docs/stack/agent-tooling.md` in the target repo — it
   records enabled render targets. If present, load the matching profile
   from `profiles/` and proceed.
2. If absent, detect candidates from the repo (`.claude/`, `.cursor/`,
   `agent/skills/`, `AGENTS.md`, `CLAUDE.md`) but DO NOT assume — ASK:
   - "Which LLM tools will consume these artifacts? **Pick all that apply:**
     Claude Code, Cursor, OpenHarness, generic/other only"
   - "Any constraints on where docs may live?"
3. Map the answer:
   - **One tool** → `profiles/claude-code.md`, `cursor.md`,
     `openharness.md`, or `generic-agents-md.md`
   - **Two or more tools** → `profiles/multi-tool.md` (default when both
     Claude + Cursor are named; also covers OpenHarness)
   - No match → create from `profiles/_template.md`; append `new_profile`
     to `.foundry/queue.json`
4. Write/refresh `docs/stack/agent-tooling.md` from
   `templates/docs/agent-tooling.md` and copy
   `templates/config/foundry.json` → `.foundry/config.json`.

## Step 2 — Canonical vs rendered (multi-tool law)

| Layer | Path | Who edits |
|---|---|---|
| **Canonical skills (SSOT)** | `agent/skills/**/SKILL.md` | Generators + humans |
| **Claude render** | `.claude/skills/**/SKILL.md` | `foundry_sync.py` only |
| **Cursor render** | `.cursor/skills/**/SKILL.md` | `foundry_sync.py` only |
| **OpenHarness render** | `.openharness/skills/**/SKILL.md` | `foundry_sync.py` only |
| **Cursor always-on router** | `.cursor/rules/00-routing.mdc` | `foundry_sync.py` only |
| **Claude entry** | `CLAUDE.md` (`@AGENTS.md` + routing) | `foundry_sync.py` only |
| **Generic / other** | canonical + `AGENTS.md` link | generators |

**Updating Claude-side content updates Cursor-side automatically** (and
vice versa) because both are renders of the same canonical tree. Never
maintain parallel copies by hand.

Canonical frontmatter dialect (`tier`, `scope`) — see
`profiles/multi-tool.md`. Generators render tool syntax via sync, never
by hardcoding vendor fields into canonical files.

## Step 3 — What each profile still controls
- `rules_root`, `docs_root`, rule file format
- per-target discovery quirks (nested folders, index rule, descriptions)
- degradation: if a tool lacks path scoping, sync keeps scope as prose
  in the body

## Step 4 — After every skill write (agent runs)

`foundry_sync.py <repo>` then `foundry_check.py sync <repo>`

## Step 5 — After every feature job (agent runs)

`foundry_skill_drift.py <repo> --git --enqueue`
If proposals → `skills-gen/post-job-update/SKILL.md` → sync again.
If UI kits or app shape changed → also refresh `docs/stack/*-identity.md`
via `docs-gen/stack-identity` and re-run `skills-gen/project-talent`.
Config: `.foundry/config.json` controls render targets and drift behavior.

## Cross-project uniqueness (multi-repo teams)

Each Foundry run produces **project-local** identity:
- `docs/stack/design-identity.md` + `backend-identity.md`
- `.foundry/project-fingerprint.json` with `forbidden_cross_project` phrases
- Never copy identity docs or design-identity rules between repos.

## Always-on routing guarantee (every target, every prompt)

The generated app must consult skills **by default on every prompt**, not only
when asked. Each target realizes this:

| target | always-on mechanism |
|---|---|
| claude-code | `CLAUDE.md` routing mandate (read `agent/skills/SKILL.md` first) |
| cursor | `.cursor/rules/00-routing.mdc` (`alwaysApply: true`) |
| openharness | root `SKILL.md` description (on-demand) + `AGENTS.md` routing section |
| generic | `AGENTS.md` routing section links `agent/skills/SKILL.md` |

Sync writes these; never drop the routing mandate when wiring a target.

## Hard law for all generators
- Write skills to `agent/skills/` with `tier` + `scope` in frontmatter.
- Never hand-edit `.claude/skills/` or `.cursor/skills/`.
- Never write vendor-only frontmatter into canonical artifacts.
- Policy rules still render per target (`AGENTS.md` canonical law;
  `.claude/rules/*.mdc` / `.cursor/rules/*.mdc` for scoped policy).
