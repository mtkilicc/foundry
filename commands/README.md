# Foundry commands

Optional slash-command shortcuts for specific Foundry tasks. **They are
shortcuts, not requirements** — Foundry still triggers on natural language
(e.g. "bootstrap this repo", "add a skill for dashboards"). Each command simply
routes into the **foundry** skill with a clear, specific task.

## Install (Claude Code)

A `commands/` folder inside a skill is **not** auto-registered. Copy these into
your commands directory:

```sh
# personal (all projects)
cp commands/foundry-*.md ~/.claude/commands/
# or project-local
cp commands/foundry-*.md .claude/commands/
```

Then type `/foundry-` to see them. (OpenHarness: place under a plugin's
`commands/` dir per its plugin layout.)

## Command list

| command | task |
|---|---|
| `/foundry-bootstrap` | detect run mode, gate blueprint, run BIG PATH |
| `/foundry-blueprint` | create/complete blueprint (intake + question bank + MVP/v1) |
| `/foundry-import <path>` | import a seed folder + consolidate stray docs |
| `/foundry-add-skill <purpose>` | add/extend ONE master-expert skill |
| `/foundry-add-doc <subject>` | document one page/flow/registry (LLM-legible) |
| `/foundry-add-rule <rule>` | one incident/convention → one rule |
| `/foundry-talent [direction]` | unique UI/UX identity + per-project enrichment |
| `/foundry-sync` | render canonical skills to all targets + verify |
| `/foundry-evolve` | post-feature drift scan → update skills |
| `/foundry-tasks` | generate task plan (task → owning skill) |
| `/foundry-check [scope]` | run deterministic checks (all/structure/sync/…) |
| `/foundry-review-queue` | handle needs_review items (evaluator) |

Source of truth lives here; re-copy after edits (or symlink the dir).
