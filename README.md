# Foundry

**Turn any repository into an agent-ready codebase** — with a shared blueprint, documentation, rules, and a skill hierarchy that AI coding tools can actually follow.

Foundry is an instruction-driven automation kit for LLM agents. You talk to Foundry in natural language; your agent reads the skill tree, runs the Python scripts, and writes the artifacts into your project. You do not run the scripts yourself unless you are hacking on Foundry itself.

```
You  →  "bootstrap this repo" / "document the checkout flow"
Agent  →  reads Foundry skills  →  runs scripts  →  writes docs, rules, skills
Tools  →  Claude Code, Cursor, OpenHarness pick up the generated kit
```

> **Project status.** This skill set is a working draft, not a finished product.
> You may hit gaps, rough edges, or missing pieces. I am publishing it as-is
> because I am moving on to build a dedicated **Foundry Agent** on top of these
> ideas — and I will not be actively improving this repository further. Use it
> as a starting point; expect to fill in holes yourself or fork and adapt.

---

## Why Foundry?

Most AI coding setups fail for the same reasons: no shared project context, generic skills that do not match your stack, rules that drift from reality, and no way to keep everything in sync after each feature ships.

Foundry treats three layers as first-class artifacts:

| Layer | Role | Where it lives |
|---|---|---|
| **Docs** | Contract — what the system is and how it works | `docs/project/`, `docs/stack/`, `docs/backend/` |
| **Rules** | Law — always-on policy the agent must follow | `.cursor/rules/`, project rules |
| **Skills** | Map — routing tree that tells the agent what to read and when | `agent/skills/` (canonical) |

One fact, one layer. Everything else links back.

After bootstrap, Foundry keeps the kit current with drift detection, identity checks, and sync to every tool you use.

---

## Quick start

### 1. Install the skill

Copy Foundry into your agent's skills directory:

```sh
# Claude Code (personal — all projects)
git clone https://github.com/YOUR_ORG/foundry.git ~/.claude/skills/foundry

# Claude Code (project-local)
git clone https://github.com/YOUR_ORG/foundry.git .claude/skills/foundry

# Cursor
git clone https://github.com/YOUR_ORG/foundry.git ~/.cursor/skills/foundry
```

Replace `YOUR_ORG/foundry` with this repo's URL once published.

### 2. Optional: install slash commands

Foundry works with plain language alone. Slash commands are shortcuts for common tasks:

```sh
# Claude Code
cp foundry/commands/foundry-*.md ~/.claude/commands/
# or project-local
cp foundry/commands/foundry-*.md .claude/commands/
```

Type `/foundry-` to see the list. See [`commands/README.md`](commands/README.md) for details.

### 3. Open your target repo and ask

Open the repository you want to foundryize in your agent, then say something like:

```
Bootstrap this repo for Claude Code and Cursor.
```

Foundry detects your project state, walks through blueprint intake if needed, and generates the full kit.

---

## What you can ask

Foundry scales ceremony to job size. Small, focused requests are the main flow — full bootstrap is the exception.

| You say | Foundry does |
|---|---|
| *"Bootstrap this repo"* | Full setup: blueprint → docs → rules → skills → task plan |
| *"Complete the project blueprint"* | Intake, gap-fill, MVP/v1 agreement |
| *"Import blueprint from `~/starters/saas`"* | Seed import + consolidation |
| *"Document the checkout flow"* | One focused doc page |
| *"Add a skill for dashboards"* | One new leaf skill in the hierarchy |
| *"Add a rule: never use inline styles on pages"* | One incident → one rule |
| *"Make skills match our unique UI"* | Stack identity mining + project talent |
| *"Sync skills to Cursor"* | Render canonical skills to all configured targets |
| *"Update skills after this feature shipped"* | Drift scan → skill refresh |

See [`examples/sample-project/walkthrough-small-job.md`](examples/sample-project/walkthrough-small-job.md) for a realistic fast-path example.

---

## Project states

Foundry detects what you bring and routes accordingly:

| State | You have | Foundry approach |
|---|---|---|
| **Empty** | An idea or notes, no code | Greenfield bootstrap — generative design from scratch |
| **Blueprint** | Docs or a seed folder, no running app | Import + prune + fresh UI design |
| **Running** | An existing codebase | Brownfield — mine code, write current-state + requested-state docs |
| **Foundryized** | `.foundry/config.json` + `agent/skills/` already exist | Incremental updates only — no re-bootstrap |

When ambiguous, Foundry asks before proceeding.

---

## What gets generated

After a full bootstrap, your target repo looks like this:

```
your-project/
├── docs/
│   ├── project/          # Blueprint — vision, scope, architecture, phases
│   └── stack/            # Design + backend identity (mined from your code)
├── agent/skills/         # Canonical skill tree (single source of truth)
├── .claude/skills/       # Rendered for Claude Code
├── .cursor/skills/       # Rendered for Cursor
├── .cursor/rules/        # Always-on routing + project rules
├── .foundry/
│   ├── config.json       # Render targets, drift settings
│   ├── intake.json       # Blueprint intake answers
│   └── blueprint-agreement.json  # MVP/v1 phases + approval record
└── CLAUDE.md / AGENTS.md # Entry points for agent tools
```

Foundry supports **Claude Code**, **Cursor**, **OpenHarness**, and generic `AGENTS.md` layouts. The adapter picks the right profile and syncs all targets from one canonical tree. See [`adapter/SKILL.md`](adapter/SKILL.md).

---

## How it works

### The three paths

**Fast path** (default) — one focused change: a doc page, one skill, one rule. Minimal ceremony, automatic drift check at the end.

**Big path** — first-time bootstrap or major expansion. Work order → blueprint gate → docs → rules → skills → project talent → task plan.

**Re-run** — repo is already foundryized. Touch only what changed; never wipe existing identity or skills.

### Blueprint gate

Before a big bootstrap, Foundry runs a deterministic gate (`foundry_blueprint_check.py`). If the blueprint is incomplete, it walks through intake:

1. Normalize your input onto a structured question bank
2. Ask for gaps (or accept full autonomy if you delegate)
3. Fill `docs/project/*` — no placeholders left
4. Agree MVP and v1 scope
5. Present `APPROVAL.md` — you approve, reject, or request changes
6. Gate passes → generation begins

### Agent close-out

The agent — not you — runs scripts at the end of every job:

| Script | When |
|---|---|
| `foundry_blueprint_check.py` | Before bootstrap |
| `foundry_sync.py` | After skill edits |
| `foundry_skill_drift.py` | After feature work |
| `foundry_check.py` | Final validation |

See [`scripts/README.md`](scripts/README.md) for the full list.

---

## Foundry package layout

This repository is the Foundry skill itself — not a library you import:

```
foundry/
├── SKILL.md                 # L1 router — start here
├── commands/                # Optional slash-command shortcuts
├── adapter/                 # Tool profiles (Claude, Cursor, OpenHarness, …)
├── docs-gen/                # Blueprint, full-tree, single-doc, stack-identity
├── skills-gen/              # Hierarchy, single-skill, project-talent, post-job-update
├── rules-gen/               # Full pack, identity rules, single-rule
├── toolkit/                 # Context7 library docs, MCP stack
├── evaluator/               # Human review for ambiguous queue items
├── scripts/                 # Deterministic checks and sync (agent-only)
├── templates/               # Blueprint, intake, config, docs, rules, skills seeds
└── examples/sample-project/  # Quality bar + fast-path walkthrough
```

---

## Slash commands

| Command | Task |
|---|---|
| `/foundry-bootstrap` | Detect mode, gate blueprint, run full setup |
| `/foundry-blueprint` | Create or complete the project blueprint |
| `/foundry-import <path>` | Import a seed folder |
| `/foundry-add-skill <purpose>` | Add one skill |
| `/foundry-add-doc <subject>` | Document one page or flow |
| `/foundry-add-rule <rule>` | Add one rule from an incident or convention |
| `/foundry-talent` | Unique UI/UX identity + per-project enrichment |
| `/foundry-sync` | Render canonical skills to all targets |
| `/foundry-evolve` | Post-feature drift scan → update skills |
| `/foundry-tasks` | Generate task plan (task → owning skill) |
| `/foundry-check [scope]` | Run deterministic checks |
| `/foundry-review-queue` | Handle items flagged for human review |

Natural language works identically — commands are just shortcuts.

---

## Examples

The [`examples/sample-project/`](examples/sample-project/) folder shows the quality bar Foundry targets — domain docs, skill hierarchy, rules, and a step-by-step fast-path walkthrough. Generators imitate these files, not just template shape.

---

## Requirements

- **Python 3.10+** — scripts run via your agent's shell, not by you directly
- **An LLM agent with shell + file access** — Claude Code, Cursor, OpenHarness, or similar
- **A target git repository** — greenfield, brownfield, or already foundryized

No pip install. Foundry is a skill tree + scripts, not a Python package.

---

## Contributing

Foundry is instruction-driven — the skills *are* the product. When changing intake flow, file contracts, or generator behavior:

1. Update the relevant `SKILL.md` and templates
2. Regenerate or refresh examples under `examples/` if output quality shifts

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
