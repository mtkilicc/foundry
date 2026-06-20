---
name: single-rule
description: >-
  Converts ONE incident or convention into ONE rule and appends it to the
  anti-pattern registry. Use the moment something goes wrong ("every page got
  a different layout again") or a new convention is decided.
---

# single-rule (leaf — read only when routed here)

## Method
1. CAPTURE — what happened, where, what correct behavior was. One
   sentence each.
2. GENERALIZE — write against the PATTERN, not the instance ("every
   page composes layout components from ui/layout/" — not "fix the
   settings page").
3. PLACE — existing rule owns this concern → extend it; new concern →
   new rule from `../../templates/rules/policy.md` in the profile's
   format. EITHER WAY append one registry row:
   incident → wrong move → required move.
4. EXAMPLE — one minimal do/don't pair from the real incident
   (sanitized); framework idioms via `../../toolkit/context7/SKILL.md`.
5. VERIFY — format valid per profile; no overlap; grep skills for
   restatements; final test: would reading this rule alone have
   prevented the incident?

## Hand-offs
- Missing domain knowledge (not policy) → an L3+ skill:
  `../../skills-gen/single-skill/SKILL.md`
- Finding beyond this rule's scope → append a `finding` event to
  .foundry/queue.json (script routes it)
