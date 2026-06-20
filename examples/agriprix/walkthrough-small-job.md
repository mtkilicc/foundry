# Walkthrough — the fast path (THE main flow)

User: "add a `?currency=` param to the price stats endpoint and document it"

1. TRIAGE (router, ~5 lines of thought): single-artifact, brownfield,
   docs+code touch. No work order — one inline line:
   "Small job: update stats endpoint + its doc page. Proceeding."
2. ROUTE: backend L2 → price-tracking leaf. Read the leaf (≤80 lines)
   and ONLY the doc it anchors. Nothing else loads.
3. DO: code change; update the Endpoints row in
   docs/backend/domain/price-tracking.md (single-doc mission, steps
   3–4 only: write + re-index — ripple grep skipped, one row changed).
4. DRIFT — agent runs `foundry_skill_drift.py . --git --enqueue`
   — if endpoint already in skill Code map → clean; else one
   `skill_drift` event → post-job-update adds the row to Code map.
5. SYNC — agent runs `foundry_sync.py .` (refreshes Claude/Cursor
   renders per `.foundry/config.json`).
6. GATE — agent runs `foundry_check.py all agent/skills .` → green.

Counter-example: "bootstrap docs for the repo" → full-tree + work
order + close-out. Ceremony scales with job size, never the reverse.
