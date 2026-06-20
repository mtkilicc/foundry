---
description: Import a seed folder and consolidate existing/stray docs into the canonical tree
argument-hint: "[seed folder path]"
---

Invoke the **foundry** skill to import + consolidate.

1. If a seed path is given, run `foundry_blueprint_import.py <repo> --from $1 --write`
   (copies missing blueprint files, extracts tech stack). Confirm `final` stack
   rows with the user — never silently adopt seed tech.
2. Consolidate stray docs: `foundry_blueprint_import.py <repo> --archive-legacy --write`,
   then merge each manifest entry into the canonical tree and prune.

Seed path / notes: $ARGUMENTS
