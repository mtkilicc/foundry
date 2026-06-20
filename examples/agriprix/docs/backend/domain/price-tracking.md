# Price tracking

Status: shipped

## Overview
Daily wholesale prices per product per market. Sources: manual entry
(admin) and the market-feed importer (Celery, 06:00 Europe/Istanbul).
Consumers: public price API, mobile app charts, weekly digest email.

## Endpoints (exhaustive)
| method | path | auth | request | response | errors |
|---|---|---|---|---|---|
| GET | /api/v1/prices/ | none | ?product, ?market, ?date_from, ?date_to, page | paginated PriceOut | 400 INVALID_RANGE |
| GET | /api/v1/prices/latest/ | none | ?product (req) | PriceOut | 404 PRODUCT_NOT_FOUND |
| POST | /api/v1/prices/ | admin token | PriceIn | PriceOut 201 | 401, 409 DUPLICATE_DAY |
| GET | /api/v1/prices/stats/ | none | ?product, ?window=7d\|30d | {avg, min, max, trend} | 400 BAD_WINDOW |

## Data model (exhaustive)
| field | type | notes |
|---|---|---|
| product | FK Product | indexed with market+date (unique_together) |
| market | FK Market | |
| date | date | one row per product/market/day |
| price_min / price_max / price_avg | Decimal(10,2) | TRY, kuruş precision |
| source | enum: manual, feed | feed rows immutable via admin |
| created_at | datetime | auto |

## Flows
Importer: fetch feed → validate row → upsert by (product, market, date)
→ on conflict with `manual` source, keep manual and log SKIPPED_MANUAL.

## Env vars / settings touched
| var | purpose |
|---|---|
| MARKET_FEED_URL | importer source |
| MARKET_FEED_TOKEN | importer auth (secret) |

## Links
- depends on: ../../stack/versions.md (Django/DRF pins)
- linked from: ../README.md, ../api-public.md
