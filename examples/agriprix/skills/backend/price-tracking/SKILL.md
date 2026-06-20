---
name: price-tracking
description: >-
  Specialist for Agriprix price tracking: price model, importer, public
  price endpoints and stats. Use whenever the user mentions prices, fiyat,
  the market feed, price charts data, or DUPLICATE_DAY/SKIPPED_MANUAL —
  even without the word "price-tracking".
paths: backend/prices/**
disable-model-invocation: true
---

# price-tracking (leaf — read only when routed here)

## Scope
Owns: Price model, importer task, /api/v1/prices/*.
Does NOT own: Product/Market models (`../catalog/SKILL.md`), digest
email rendering (`../notifications/SKILL.md`).

## Specialist docs (leaf docs only)
- `docs/backend/domain/price-tracking.md` — contract; read FIRST.

## Code map
- `backend/prices/models.py` — unique_together (product, market, date)
- `backend/prices/tasks.py` — importer; upsert + SKIPPED_MANUAL log
- `backend/prices/api.py` — views; stats window calc

## MCPs used
- DB MCP (read-only) — verify schema before migration advice
- Context7 — DRF pagination/idioms at pinned version

## Domain invariants (no rule can know these)
- feed rows are immutable in admin; never "fix" a feed row manually
- stats windows are calendar days in Europe/Istanbul, not UTC
- a manual row always wins over a feed row for the same day

## Cross-domain hand-offs
New price-derived notification → `../notifications/SKILL.md`.
