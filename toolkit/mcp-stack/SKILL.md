---
name: mcp-stack
description: >-
  MCP catalog, selection protocol, and adoption protocol. Use when any skill
  or generator needs external capability (browser/e2e testing, library docs,
  DB introspection, design files, error tracking, issue trackers...), when
  setting up a repo, or when a needed MCP is not yet in the project stack.
---

# mcp-stack (leaf — read only when routed here)

## Catalog (task → MCP)

| Task | MCP | Typical consumers |
|---|---|---|
| Library/framework truth, version-pinned | Context7 | all generators (`../context7/SKILL.md`) |
| Frontend e2e, browser automation, screenshots, design-consistency checks | Playwright MCP | testing rule; frontend skills; verifying the design-system rule on rendered pages |
| Browser debugging: console, network, live DOM | Chrome DevTools MCP | frontend debugging skills |
| Repo research, PR/history mining, peer-repo scans | GitHub / GitLab MCP | transplant-contract; rules-gen mining |
| DB introspection (schemas, FKs, enums) | Postgres / MySQL / SQLite MCP (READ-ONLY creds) | docs data-model registries |
| Container/runtime state | Docker MCP | ops docs; deployment skills |
| Design source of truth (tokens, components) | Figma MCP | design-system doc + rule; frontend skills |
| Production errors / incident mining | Sentry MCP | rules-gen anti-pattern mining; ops skills |
| Issues/tickets as intent source | Linear / Jira MCP | docs intent pages; planning skills |
| API contract source | OpenAPI/Swagger MCP (or spec fetch) | api-*.md registries; transplant scans |
| Cache/queue introspection | Redis MCP | ops/debugging skills |
| Team comms context | Slack MCP | optional; incident → rule capture |

## Selection protocol (every skill that needs capability)
1. Derive needed CAPABILITIES from the task (not tool names).
2. Map against this catalog ∩ the project's enabled list in
   `<docs_root>/stack/mcp-setup.md`. Pick the MINIMUM set — one, two,
   or all, as the task genuinely demands; never enable speculatively.
3. Reference by capability in skills ("verify via the browser-
   automation MCP"), never by connection details — setup lives in
   mcp-setup.md.

## Adoption protocol (needed MCP not in the stack)
1. The requesting skill appends ONE `mcp_proposal` event to
   `.foundry/queue.json` (payload: mcp, capability, one-line why the
   existing stack can't cover it) — then CONTINUES its job using what
   the current stack allows. No inline review, no waiting.
2. `scripts/foundry_check.py queue` auto-rejects duplicates already in
   mcp-setup.md; the rest become needs_review.
3. `../../evaluator/SKILL.md` decides needs_review items; approved →
   catalog row HERE + registration in mcp-setup.md (name, purpose,
   auth, allowed scope; DB creds read-only) + adoption-log entry.
Never adopt silently; never let a skill use an unregistered MCP.

## Verify
mcp-setup.md exists and matches reality; no skill references an
unregistered MCP; no unused registrations.
