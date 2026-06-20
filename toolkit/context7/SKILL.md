---
name: context7
description: >-
  Version-pinned library documentation protocol via the Context7 MCP. Use
  whenever a doc page, rule example, or skill invariant asserts library
  behavior (ORM, hooks, middleware, build tools) — and on every dependency
  upgrade.
---

# context7 (leaf — read only when routed here)

## Protocol
1. PIN ONCE — read lockfiles (requirements*/poetry.lock,
   package-lock.json); `resolve-library-id` per major library; record
   IDs + versions in `<docs_root>/stack/versions.md`. Every later call
   uses these pins.
2. CALL AT ASSERTION POINTS, not constantly — only when an artifact
   asserts library behavior: a doc page on middleware order or hook
   semantics; a rule prescribing a framework idiom; a skill invariant
   depending on library behavior.
3. SCOPE THE TOPIC — `get-library-docs` with a narrow topic ("model
   Meta options", "useEffect cleanup"). Full dumps poison context.
4. DIVISION OF LABOR — docs CITE (summary + version); skills POINT
   (link the stack doc, never re-query); rules EMBED (one verified
   idiom line inside the do/don't example).
5. ON UPGRADE — a version bump in versions.md triggers an audit pass
   over stack/ docs and every rule example citing that library.

## Verify
No library assertion without a pin; versions.md matches lockfiles.

## Hand-offs
Findings → docs via `../../docs-gen/single-doc/SKILL.md`; rule
examples via `../../rules-gen/single-rule/SKILL.md`.
