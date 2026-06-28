# Foundry scripts — agent execution only

**Users never run these directly.** Users talk to the **foundry** skill (or a
routed child). The agent invokes scripts via the Shell tool.

| script | agent runs when |
|---|---|
| `foundry_blueprint_check.py` | Blueprint gate before bootstrap |
| `foundry_blueprint_import.py` | User provided a seed folder; or `--archive-legacy` to consolidate stray docs |
| `foundry_blueprint_assemble.py` | Assemble multi-file blueprint → one consolidated doc for mandatory user approval (`--current`/`--requested` for Running state) |
| `foundry_sync.py` | After canonical skill edits |
| `foundry_skill_drift.py` | End of feature work |
| `foundry_identity_check.py` | After stack-identity / project-talent |
| `foundry_check.py` | Close-out (`structure` / `completeness` / `sync` / `drift` / `identity` / `blueprint` / `all`) |

Schema docs: `config-schema.md`, `queue-schema.md`, `blueprint-schema.md`.
