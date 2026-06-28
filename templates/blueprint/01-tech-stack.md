# Tech stack

Status: empty

> **Sources (merge, don't pick one):**
> 1. **Extracted** — lockfiles / compose / seed folder (Foundry agent runs import)
> 2. **User intent** — what you want even if the seed differs
> 3. **Final** — agreed row used by Foundry for `docs/stack/versions.md` + skills

Ask Foundry: *"import tech stack from `<seed path>`"* — agent runs
`scripts/foundry_blueprint_import.py` and fills tables below.

## Final stack (authoritative for Foundry)

| layer | choice | version pin | source | notes |
|---|---|---|---|---|
| backend runtime | | | extracted / user | |
| backend framework | | | extracted / user | |
| frontend runtime | | | extracted / user | |
| frontend framework | | | extracted / user | |
| database | | | extracted / user | |
| cache / queue | | | extracted / user | |
| observability | | | extracted / user | |
| deploy | | | extracted / user | |

<!-- FOUNDRY:TBD required="user" prompt="Confirm or override each row marked extracted. Add rows user wants that seed lacked." -->

## Extracted from seed (read-only snapshot)

Populated by Foundry import from seed folder and/or target repo.
Re-run import after seed changes (ask Foundry).

| artifact | path | detected |
|---|---|---|
| | | |

## User overrides & additions

<!-- FOUNDRY:TBD required="user" prompt="List tech you want changed or added vs the imported folder." -->

| want | instead of (seed) | reason |
|---|---|---|
| | | |

## Conflicts resolved

| topic | seed said | user wants | **final** | agreed |
|---|---|---|---|---|
| | | | | |

Gate: every conflict row must have **final** + `agreed` before bootstrap.
