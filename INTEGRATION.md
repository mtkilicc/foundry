# Foundry integration guide (for host apps)

How an external application (e.g. HarnessCICD) drives Foundry and bridges its
user-interaction points. **Foundry is instruction-driven**: a worker LLM (Claude
CLI by default, or a local LLM) executes the skill in a target repo. Foundry
communicates state through **files under `.foundry/`** plus a few **pause points**
where it needs the user. The host app relays those pauses to its platform
(web/Telegram/…) and writes answers back.

> Keep this doc updated whenever the intake/approval flow or its files change —
> host apps follow this contract.

## Project states

| State | User brings | Method |
|---|---|---|
| **Empty** | only an idea / text / md (no app) | greenfield |
| **Blueprint** | a blueprint or docs (a seed), no running app | greenfield + **prune** + **dynamic UI redesign** |
| **Running** | an existing, running app | brownfield/re-run + **two approved docs** (current-state + requested-state) |

State is detected at L1 `SKILL.md` Step −1 and recorded in
`.foundry/blueprint-agreement.json` → `state` (`empty` | `blueprint` | `running`).
This guide focuses on **Empty** and **Blueprint** (they differ only at step 8).
For Running, see the note at the end.

## Interaction sequence (Empty & Blueprint)

Steps marked ⏸ need the user — these are the only things the host must bridge.
Everything else is autonomous.

1. **SITUATION** — establish inputs: project name, the idea/content, consuming
   tools (adapter target), and (Blueprint) the seed path. Writes `state`.
   - *Blueprint:* `foundry_blueprint_import.py <repo> --from <seed> --write`
     (copies docs, extracts stack); if stray docs exist,
     `foundry_blueprint_import.py <repo> --archive-legacy --write`.
2. **NORMALIZE** — map the input onto the question bank
   (`templates/intake/question-bank.md`); tag each value's `source`
   (`user` | `seed` | `repo`).
3. **PRE-DRAFT** — draft a proposed answer for every remaining slot (best
   practice), tagged `source: foundry-decided`.
4. **GAP SCAN** — split the **blocking slots** into *answered* (user/seed) vs
   *gaps* (only drafted). Blocking set: `situation, consuming_tools,
   project_name, pitch, archetype, personas, auth_model, core_flows, domains,
   mvp_scope, v1_scope`.
5. ⏸ **MODE CHOICE** — ask the user once:
   - **Full autonomy** → keep all drafts (tech + design + everything); **no
     questions**. Sets `delegated: true`.
   - **Hybrid** → present **both** the already-answered slots (for revision)
     **and** the gaps; user confirms/edits each. `delegated: false`.
   - Either mode: Foundry decides the **design/creativity** slots itself
     (visual feel, focal area) unless the user gives direction.
6. ⏸ **(Hybrid only) Q&A** — user revises drafts / fills gaps. Full autonomy
   skips this.
7. **RECORD** — write `.foundry/intake.json`: every blocking slot gets
   `{value, source}`; `delegated` per mode. (`default`/`foundry-decided` are
   valid only when `delegated: true`.)
8. **SCAFFOLD + fill** `docs/project/*`; no `FOUNDRY:TBD` left.
   - *Blueprint:* **prune** parts of the imported blueprint not in the agreed
     idea, and **redesign the UI generatively** (do not inherit the seed's UI).
9. ⏸ **PHASE WORKSHOP** — agree **MVP + v1** (no v2 unless asked) →
   `blueprint-agreement.json.phases`.
10. **ASSEMBLE** — `foundry_blueprint_assemble.py <repo>` →
    `docs/project/APPROVAL.md` (the whole blueprint in one file).
11. ⏸ **APPROVAL LOOP (mandatory)** — present `APPROVAL.md`; user replies
    **yes / no / "add X"**. On no/add → edit canonical files → re-assemble →
    present again. **Repeat until "yes."** Record
    `approval.project.{approved, approved_by, approved_at}`.
12. **GATE** — `foundry_blueprint_check.py <repo>` must exit 0, then generation
    proceeds (docs → rules → skills → task-plan). The gate enforces: files
    present, no TBDs, open questions closed, phases agreed, **intake.json
    complete** (guesses need `delegated:true`), and **approval recorded**.

## File contract (read/write boundary)

| File | Written by | Host app role |
|---|---|---|
| `.foundry/intake.json` | Foundry worker | Read `delegated` + slot drafts; in Hybrid surface gaps as questions; write user answers back here before resuming |
| `.foundry/blueprint-agreement.json` | Foundry worker | Read `state`/`phases`/`approval`; write `approved`/`approved_by` on user approval |
| `docs/project/APPROVAL.md` | `foundry_blueprint_assemble.py` | The single document to render for the yes/no/add loop |
| `docs/project/*` | Foundry worker | Source of truth; re-assembled into APPROVAL.md after each revision |
| `foundry_blueprint_check.py` exit code | gate | 0 = ready to generate; non-zero = still blocked (stdout says why) |

### `.foundry/intake.json` shape
```jsonc
{
  "version": 1,
  "delegated": false,            // true = Full autonomy
  "delegated_by": null,          // required when delegated=true
  "delegated_at": null,
  "slots": {
    "project_name": { "value": "Acme", "source": "user" },
    "auth_model":   { "value": "sso-oauth", "source": "user" }
    // ...one entry per blocking slot; source: user|seed|repo|default|foundry-decided
  }
}
```

### `.foundry/blueprint-agreement.json` (approval-relevant fields)
```jsonc
{
  "state": "empty",             // empty | blueprint | running
  "approval": {
    "project": { "approved": false, "approved_by": null, "approved_at": null,
                 "document": "docs/project/APPROVAL.md" }
  },
  "running_approval": {          // used only when state=running
    "current_state":   { "approved": false, "document": "docs/project/CURRENT-STATE.md" },
    "requested_state": { "approved": false, "document": "docs/project/REQUESTED-STATE.md" }
  },
  "phases": { "mvp": { "status": "agreed" }, "v1": { "status": "agreed" } }
}
```

## The four bridge points

1. **Creation inputs** (step 1) — name, idea, platforms, blueprint y/n, consuming tools.
2. **Mode choice** (step 5) — one question → sets `delegated`.
3. **Hybrid Q&A** (step 6) — only if Hybrid; relay gaps + drafts, collect edits.
4. **Approval loop** (step 11) — render `APPROVAL.md`, collect yes/no/add, loop.

In **Full autonomy** the only mandatory pause is #4 (so Empty can be just
*create → mode=full → approve*). In **Hybrid**, #3 may be several rounds.

## Driving Foundry headlessly

```
invoke worker (e.g. claude -p) to run the foundry skill on <repo>
loop:
  worker runs until it needs the user, then stops having written its
  question(s) into .foundry/intake.json (gaps) or signalled approval-needed
  host: detect the pause -> raise a question|approval signal -> relay to
        web/Telegram -> collect answer -> write into intake.json / set approval
        in blueprint-agreement.json -> re-invoke the worker to resume
until: foundry_blueprint_check.py exits 0
then: proceed to generation (docs/rules/skills/task-plan)
```

## JSON message shapes for the bridge

You may force these with a system prompt ("answer in JSON …"):
```jsonc
// Foundry -> platform: Hybrid question batch (from intake.json gaps)
{ "type": "intake_questions", "delegated": false,
  "questions": [ { "key": "auth_model", "draft": "email-password",
                   "ask": "How do users sign in?",
                   "options": ["none","email-password","sso-oauth","rbac-roles"] } ] }

// platform -> Foundry: answers (merged into intake.json slots)
{ "type": "intake_answers",
  "answers": { "auth_model": { "value": "sso-oauth", "source": "user" } } }

// Foundry -> platform: approval request
{ "type": "approval_request", "document": "docs/project/APPROVAL.md", "state": "empty" }

// platform -> Foundry: approval decision
{ "type": "approval_decision", "decision": "add", "changes": "add billing to MVP" }
// decision: yes | no | add
```

## Integration notes that affect correctness

- **Do not force autonomous "don't ask"** if you want Hybrid. Invoke Foundry
  normally and read `intake.json.delegated` to know whether questions will come.
- **Approval is mandatory and is a hard gate.** Wire your gate UI to (a) render
  `APPROVAL.md`, (b) support a **third action `add`** (not just approve/reject),
  and (c) write the approval record before re-running `foundry_blueprint_check.py`.
- **Escapes** exist for automation/legacy: `foundry_blueprint_check.py <repo>
  --skip-intake` and `--skip-approval`. Use only for explicit overrides.
- **Default executor** in Foundry's own docs is Claude CLI; the host may select a
  local LLM per project/task. Foundry itself is executor-agnostic — it just needs
  a worker that can run shell + read/write files in the repo.

## Running state (brief, for completeness)

Same intake + mode choice, but the host approves **two** assembled documents:
`foundry_blueprint_assemble.py <repo> --current` → `CURRENT-STATE.md` (as-built,
co-created with the user) and `--requested` → `REQUESTED-STATE.md` (the change).
The gate requires **both** `running_approval.current_state` and
`requested_state` approved.

---
*Source of truth for the flow: `docs-gen/project-blueprint/SKILL.md`,
`templates/intake/question-bank.md`, `scripts/foundry_blueprint_{check,assemble,import}.py`,
`templates/config/{intake,blueprint-agreement}.json`. Update this doc when those change.*
