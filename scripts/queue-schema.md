# .foundry/queue.json — the event queue

Skills NEVER self-review. When a skill introduces or discovers something,
it appends ONE event here and moves on. `foundry_check.py queue` then
auto-resolves what logic can resolve and marks the rest `needs_review` —
only those reach the evaluator skill (or the human).

```json
{
  "version": 1,
  "events": [
    {
      "id": "evt-001",
      "ts": "2026-06-11T10:00:00Z",
      "type": "mcp_proposal | new_profile | layer_change | finding | new_artifact | new_template | skill_drift | blueprint_change",
      "by_skill": "skills-gen/single-skill",
      "summary": "one line, human-readable",
      "payload": { "mcp": "...", "path": "...", "kind": "policy|fact|domain|code_map_gap|...", "...": "type-specific" },
      "status": "pending",
      "routed_to": null
    }
  ]
}
```

Auto-resolution rules (in the script, not in any skill):
- mcp_proposal whose MCP is already registered → auto_rejected_duplicate
- new_artifact whose path exists → auto_ok; missing → needs_review
- skill_drift with disposition auto_rejected → auto_rejected_duplicate
- skill_drift otherwise → needs_review → `skills-gen/post-job-update`
- blueprint_change → needs_review → `docs-gen/project-blueprint`
- everything else → needs_review

Statuses: pending → (auto_ok | auto_rejected_duplicate | needs_review)
→ approved | rejected (set by evaluator/human/post-job-update, with routed_to filled).

See also: `.foundry/config.json` (render targets), `.foundry/skill-drift-report.json`.
