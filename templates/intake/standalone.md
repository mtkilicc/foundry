# Standalone mini-intake (when an L2 is invoked without the router)

1. Adapter — if `docs/stack/agent-tooling.md` exists, use it; else run
   `../adapter/SKILL.md` (ask the user their tool).
2. Triage — FAST PATH unless this is clearly a bootstrap/new-domain/
   transplant/audit job. Fast path: no work order, one inline
   confirmation line, route to the leaf.
3. Quality bar — first artifact of this type this session? Read its
   `../examples/sample-project/` counterpart first.
4. Finish — append any new/discovered things as events to
   `.foundry/queue.json`; agent runs `foundry_check.py queue <repo>`;
   evaluator ONLY for needs_review items.
