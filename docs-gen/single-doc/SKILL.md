---
name: single-doc
description: >-
  Focused docs mission: create or edit ONE page (feature flow, registry,
  integration page) without restructuring the tree. Use for any small
  documentation request.
---

# single-doc (leaf — read only when routed here)

## Method
1. LOCATE — read `<docs_root>/README.md` + component README. Classify:
   (a) new leaf, (b) edit existing leaf, (c) genuinely new category →
   STOP, recommend `../full-tree/SKILL.md`.
2. RESEARCH THE SLICE ONLY — just the code paths this page covers;
   context7 for asserted library semantics; integration pages scan
   only the mirrored peer surface.
3. WRITE — `../../templates/docs/domain-page.md`: explicit
   registries, tables, status header for domain docs, relative links;
   link dependencies AND add backlinks from touched pages.
4. RE-INDEX — update every README between this file and the root.
   A leaf no index lists does not exist.
5. RIPPLE CHECK (bounded) — grep docs for concepts this page now owns;
   pages restating them get cut to a link.

## Verify
Template followed; links resolve both ways; READMEs updated.

## Hand-offs
- skill should anchor this page → note for
  `../../skills-gen/single-skill/SKILL.md`
- peer-contract content → `../transplant-contract/SKILL.md`
