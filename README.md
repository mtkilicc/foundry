# foundry — automation starter for agent-ready repos

**You use Foundry (the skill). Foundry's agent runs the scripts.**

Ask in natural language — e.g. *"bootstrap this repo"*, *"import blueprint from
`../starter`"*, *"agree MVP and v1"*, *"add a skill for dashboards"*. Do not
run `python scripts/...` yourself unless you are hacking Foundry itself.

**Optional shortcuts:** slash commands in [`commands/`](commands/) map to specific
tasks (`/foundry-bootstrap`, `/foundry-add-skill`, `/foundry-sync`, …). They are
shortcuts only — natural language works the same. See `commands/README.md` to install.

**Integrating Foundry into another app?** See [`INTEGRATION.md`](INTEGRATION.md) —
the host-app contract for the Empty/Blueprint/Running flow: pause points (mode
choice, Hybrid Q&A, approval loop), the `.foundry/` file contract, and JSON bridge
shapes. Keep it updated when the intake/approval flow changes.

## What Foundry produces

Blueprint → agreed phases → docs → rules → skills → Claude/Cursor renders —
with drift and identity checks so the kit stays current.

## Repo layout (after bootstrap)

| What | Path |
|---|---|
| Blueprint (start point) | `docs/project/` |
| Canonical skills | `agent/skills/` |
| Claude render | `.claude/skills/` |
| Cursor render | `.cursor/skills/` |
| Machine config | `.foundry/config.json` |

## Foundry package layout

```
foundry/
├── SKILL.md              L1 router (you start here)
├── commands/             optional slash-command shortcuts (NL still works)
├── adapter/              tool profiles
├── docs-gen/             blueprint · full-tree · single-doc · stack-identity
├── skills-gen/           hierarchy · single-skill · project-talent · post-job-update
├── rules-gen/            full-pack · identity-rules · single-rule
├── toolkit/              context7 · mcp-stack
├── evaluator/            needs_review only
├── scripts/              agent execution only (see scripts/README.md)
├── templates/            see templates/README.md
│   ├── intake/
│   ├── config/
│   ├── blueprint/
│   ├── skills/
│   ├── docs/
│   ├── rules/
│   └── wiring/
└── examples/agriprix/
```

## Typical user phrases → Foundry routes

| You say | Foundry does |
|---|---|
| "Complete the project blueprint" | `docs-gen/project-blueprint` |
| "Import from `~/starters/saas`" | `foundry_blueprint_import` + interview |
| "Bootstrap the repo" | BIG PATH after blueprint gate |
| "Add currency param + update docs" | FAST PATH + post-job drift |
| "Make skills talented / unique UI" | `project-talent` + stack-identity |

## Agent close-out (not for users)

The agent runs `foundry_check.py all agent/skills <repo>` on bootstrap and
the fast-path subset after small jobs. See `scripts/README.md`.
