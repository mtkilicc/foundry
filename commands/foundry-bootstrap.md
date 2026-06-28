---
description: Bootstrap a repo with Foundry — detect run mode, gate the blueprint, run the BIG PATH
argument-hint: "[optional: one-line idea or notes]"
---

Invoke the **foundry** skill to bootstrap this repository.

1. Detect the **project state**: Empty / Blueprint / Running (L1 Step −1).
2. Intake + normalization on `templates/intake/question-bank.md`; pre-draft all
   answers, then ask the user the **mode choice**: **Full autonomy** (Foundry
   answers everything) or **Hybrid** (user revises answered + fills gaps). Design
   slots Foundry decides either way.
3. **Mandatory approval**: assemble the consolidated doc
   (`foundry_blueprint_assemble.py`), present, revise until the user approves
   (Running: current-state + requested-state). Then run the **blueprint gate**.
4. Proceed on the BIG PATH: blueprint → rules → docs → skills → project-talent
   → task-plan → sync + `foundry_check.py all`.

Extra context from the user: $ARGUMENTS

(You can also just ask Foundry in plain language — this command is a shortcut.)
