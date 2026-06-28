---
name: backend
description: >-
  Backend domain orchestrator for the sample project (Django/DRF/Celery). Use for any
  backend task: prices, products, markets, importer, public API, admin —
  even if the user only names a model or an endpoint.
paths: backend/**
---

# backend — domain orchestrator

## Step 1 — confirm scope
One capability or cross-capability? Cross → load multiple leaves.

## Step 2 — decision table
| Trigger | Read |
|---|---|
| price, fiyat, market price, importer, feed, price API/stats | `price-tracking/SKILL.md` |
| product/market catalog CRUD | `catalog/SKILL.md` |
| digest email, notifications | `notifications/SKILL.md` |

## Step 3 — dispatch
State which leaf you read next; follow it exactly.

## Cross-cutting
Migration touching two capabilities → load both leaves; API-shape
changes also update docs/backend/api-public.md (single-doc mission).
