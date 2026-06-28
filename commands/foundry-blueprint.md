---
description: Create or complete the project blueprint (intake, ~90% question bank, MVP/v1 agreement)
argument-hint: "[optional: idea, scope notes, or 'agree phases']"
---

Invoke the **foundry** skill, routing to `docs-gen/project-blueprint`.

- Run **Intake & normalization** first: name the state (Empty/Blueprint/Running),
  normalize any input (one sentence or a doc folder) onto
  `templates/intake/question-bank.md`, and **pre-draft every answer**.
- Ask the user the **mode choice**: **Full autonomy** (Foundry answers all) or
  **Hybrid** (show answered drafts to revise + gaps to fill). Design/creativity
  slots Foundry decides either way; agree **MVP + v1 only** (no v2 unless asked).
- Write `.foundry/intake.json`; **assemble + get mandatory approval** of the
  consolidated doc; record agreement + approval; run the blueprint gate.

User input: $ARGUMENTS
