---
name: transplant-contract
description: >-
  Learn-from-X-build-Y workflow: read-only contract scan of source repo X,
  generating regenerable integration docs for target repo Y. Use whenever two
  repos are involved — external apps consuming a main app's auth/events/APIs,
  or re-syncing after X changed.
---

# transplant-contract (leaf — read only when routed here)

## Method
1. CONTRACT SCAN (X is read-only) — map ONLY the surface Y touches:
   auth handshake, shared models/serializers, event/log formats,
   endpoints Y calls, queue/topic names, shared env vars.
2. CLASSIFY each item: CONTRACT (match exactly) / CONVENTION (follow)
   / IRRELEVANT. Output a contract table with X path + commit as
   evidence per CONTRACT row. Get approval.
3. GENERATE `<docs_root>/integration/<x>/` — one page per surface
   (auth.md, event-format.md, endpoints.md...); each records its X
   source path + commit. Pages are REGENERABLE; hand-editing forbidden
   (a rule enforces this).
4. Y's NEW features are NOT written here — they go to component
   domain docs via `../single-doc/SKILL.md`, linking these pages,
   never restating them.
5. DRIFT PROTOCOL — X changed: rerun scan, diff the table, regenerate
   changed pages, list every Y domain doc linking a changed page.

## Verify
- Every CONTRACT row has evidence; no Y-feature content in
  integration/; immediate diff-rerun produces zero changes.

## Hand-offs
- integration rules → `../../rules-gen/single-rule/SKILL.md`
- `integration-with-<x>` orchestrator skill →
  `../../skills-gen/full-hierarchy/SKILL.md`
