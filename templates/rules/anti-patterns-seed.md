# Anti-pattern registry seed (render in the active profile's rule format, always-on)

This registry only grows. Append one row per incident
(rules-gen/single-rule).

| incident | wrong move | required move |
|---|---|---|
| rewrote a working module to fix one bug | full rewrite | patch minimally; rewrites need an approved plan |
| second component library appeared | new UI dep | compose design-identity kits per frontend-structure rule |
| copied UI from another Foundry project | transplant component/table rows | mine stack-identity from this repo only |
| generic shadcn dashboard from tutorial | default card grid | use fingerprint shell + chart kit |
| invented an endpoint from memory | guessed API shape | read the api registry doc first |
| edited a generated/contract file by hand | hand-edit | regenerate from source (integration docs) |
| adopted an MCP nobody registered | silent adoption | mcp-stack adoption protocol via evaluator |
