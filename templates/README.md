# Foundry templates — index

**Users do not copy these by hand.** The Foundry agent reads paths here and
materializes files into the target repo. Users invoke **foundry** (or a
child skill); the agent runs `scripts/*.py` via Shell.

## Layout

| folder | purpose |
|---|---|
| [`intake/`](intake/) | Question bank (pre-defined coverage map) + work order + standalone intake |
| [`config/`](config/) | `.foundry/*.json` seeds (foundry, blueprint agreement, intake, fingerprint) |
| [`blueprint/`](blueprint/) | `docs/project/` start-point tree |
| [`skills/`](skills/) | Canonical `agent/skills` leaf shape |
| [`docs/`](docs/) | Domain pages, stack identity, agent-tooling, task-plan |
| [`rules/`](rules/) | Policy templates + `.mdc` structure rules |
| [`wiring/`](wiring/) | Tool entry files (e.g. `CLAUDE.md`) |

## Quick map (old → new)

| old path | new path |
|---|---|
| `project-blueprint/*` | `blueprint/*` |
| `foundry-config.json` | `config/foundry.json` |
| `canonical-skill-template.md` | `skills/canonical-leaf.md` |
| `doc-page-template.md` | `docs/domain-page.md` |
| `agent-tooling-template.md` | `docs/agent-tooling.md` |
| `rule-template.md` | `rules/policy.md` |
| `standalone-intake.md` | `intake/standalone.md` |
| `CLAUDE.md.stub` | `wiring/CLAUDE.md.stub` |
