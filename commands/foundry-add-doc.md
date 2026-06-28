---
description: Document one page, flow, or registry (LLM-legible doc in the canonical tree)
argument-hint: "[subject, e.g. 'the checkout flow']"
---

Invoke the **foundry** skill, routing to `docs-gen/single-doc`.

- Write to the correct doc stratum (project / stack / `<component>/domain`).
- Honor the **LLM-legibility standard**: lead with the contract, exhaustive
  registries in tables, define terms, relative links, one fact per doc.
- Note follow-ups (new leaf, repeated drift) as queue events; run `foundry_check.py queue`.

Doc subject: $ARGUMENTS
