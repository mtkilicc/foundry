# Work order (BIG PATH ONLY — full-system, new major domain, transplant, audit; fast-path jobs use one inline confirmation line instead)

**Prerequisite:** agent runs `foundry_blueprint_check.py` → exit 0.
Blueprint: `docs/project/` (or single `BLUEPRINT.md`) + `.foundry/blueprint-agreement.json`.

| field | value |
|---|---|
| tool profile | from adapter (ask user if unknown) |
| scenario | greenfield / brownfield / transplant / audit |
| scope | full-system / single-domain / single-artifact |
| blueprint phase | MVP / v1 / v2 / v3+ (from agreement JSON) |
| artifacts + order | any subset of {docs, skills, rules}; e.g. "rules only", "single skill" |
| source(s) of truth | **blueprint** → code / repo X contract + repo Y intent |
| skills to read | e.g. docs-gen/single-doc |
| research needed | code map? context7 pins? X-repo scan? MCPs (which)? |

## Blocking questions per scenario (ask only these)
- always: blueprint gate green? which phase (MVP/v1/…) does this job advance?
- greenfield: which planned features in agreed phase?
- brownfield: blueprint reconciled with code? known-drifted areas?
- transplant: paths/access for BOTH repos; CONTRACT vs CONVENTION vs
  IRRELEVANT split of X; NEW features Y adds that X cannot answer.
- single-artifact: one-sentence purpose; where it slots.
- always: which LLM tool/framework consumes the artifacts (adapter).
