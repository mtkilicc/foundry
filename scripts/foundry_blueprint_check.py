#!/usr/bin/env python3
"""foundry_blueprint_check.py — gate before Foundry bootstrap generation.

Verifies project blueprint is complete, open questions closed, MVP/v1+ phases are
agreed in blueprint-agreement.json, the intake record (.foundry/intake.json) has
every blocking slot answered with a valid source, AND the user has approved the
consolidated document(s) (Running state requires current-state + requested-state).

Enforcement: a blocking slot sourced `default`/`foundry-decided` (i.e. Foundry
guessed) is rejected UNLESS the user delegated (`delegated: true`). Sources
`user`/`seed`/`repo`/`derive` are always allowed.

Usage:
  python scripts/foundry_blueprint_check.py <repo_root>
  python scripts/foundry_blueprint_check.py <repo_root> --skip-intake     # legacy/escape
  python scripts/foundry_blueprint_check.py <repo_root> --skip-approval   # legacy/escape

Exit 0 = ready for Foundry bootstrap. Exit 1 = blockers listed.

Stdlib only.
"""
from __future__ import annotations

import json
import os
import re
import sys

TBD_RE = re.compile(
    r"<!--\s*FOUNDRY:TBD\b([^>]*)-->|"
    r"Status:\s*empty\b",
    re.I,
)
OPEN_Q = re.compile(r"^\|\s*Q\d+\s*\|[^|]*\|[^|]*\|\s*open\s*\|", re.M | re.I)

MULTI_FILES = [
    "README.md",
    "00-vision.md",
    "01-tech-stack.md",
    "02-scope-phases.md",
    "03-architecture.md",
    "04-domains.md",
    "05-constraints.md",
    "06-open-questions.md",
]
AGREEMENT = ".foundry/blueprint-agreement.json"
CONFIG = ".foundry/config.json"
INTAKE = ".foundry/intake.json"

# Blocking slots — must match the Blocking set in templates/intake/question-bank.md.
BLOCKING_SLOTS = [
    "situation", "consuming_tools", "project_name", "pitch", "archetype",
    "personas", "auth_model", "core_flows", "domains", "mvp_scope", "v1_scope",
]
# Sources the user/repo actually provided — allowed without delegation.
PROVIDED_SOURCES = {"user", "seed", "repo", "derive"}
# Foundry guessed these — allowed ONLY when the user delegated.
GUESS_SOURCES = {"default", "foundry-decided"}


def load_json(repo: str, rel: str) -> dict:
    p = os.path.join(repo, rel)
    if not os.path.exists(p):
        return {}
    try:
        return json.load(open(p, encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def blueprint_root(repo: str) -> tuple[str, str]:
    cfg = load_json(repo, CONFIG)
    bp = cfg.get("blueprint", {})
    root = bp.get("root", "docs/project")
    mode = bp.get("mode", "multi-file")
    if mode == "single-file":
        return root, "single-file"
    return root, "multi-file"


def check_files(repo: str, root: str, mode: str) -> list[tuple[str, str]]:
    results = []
    if mode == "single-file":
        path = os.path.join(repo, root, "BLUEPRINT.md")
        if not os.path.exists(path):
            path = os.path.join(repo, root + ".md")  # docs/project-blueprint.md alt
        if not os.path.exists(path):
            results.append(("FAIL", f"missing single-file blueprint under {root}/"))
            return results
        results.append(("OK", f"found {os.path.relpath(path, repo)}"))
        return results
    base = os.path.join(repo, root)
    if not os.path.isdir(base):
        results.append(("FAIL", f"missing blueprint dir: {root}/"))
        return results
    for fn in MULTI_FILES:
        p = os.path.join(base, fn)
        if os.path.exists(p):
            results.append(("OK", f"found {root}/{fn}"))
        else:
            results.append(("FAIL", f"missing {root}/{fn}"))
    return results


def scan_tbds(repo: str, root: str, mode: str) -> list[tuple[str, str]]:
    results = []
    paths = []
    if mode == "single-file":
        for cand in (os.path.join(root, "BLUEPRINT.md"), root + ".md"):
            if os.path.exists(os.path.join(repo, cand)):
                paths.append(os.path.join(repo, cand))
                break
    else:
        for fn in MULTI_FILES:
            p = os.path.join(repo, root, fn)
            if os.path.exists(p):
                paths.append(p)
    required_tbds = 0
    for p in paths:
        text = open(p, encoding="utf-8").read()
        rel = os.path.relpath(p, repo)
        for m in TBD_RE.finditer(text):
            attrs = m.group(1) or ""
            if 'optional="true"' in attrs.replace(" ", ""):
                continue
            if "required=" in attrs or "Status: empty" in m.group(0):
                required_tbds += 1
                results.append(("FAIL", f"TBD/empty in {rel}: {m.group(0)[:60]}..."))
        oq = "open-questions" in os.path.basename(p) or "06-open" in p
        if oq and OPEN_Q.search(text):
            results.append(("FAIL", f"open questions remain in {rel}"))
    if not required_tbds and paths:
        results.append(("OK", "no blocking TBD markers"))
    return results


def check_agreement(repo: str) -> list[tuple[str, str]]:
    results = []
    data = load_json(repo, AGREEMENT)
    if not data:
        results.append(("FAIL", f"missing {AGREEMENT}"))
        return results
    results.append(("OK", f"found {AGREEMENT}"))
    required = data.get("required_phases_for_foundry", ["mvp", "v1"])
    phases = data.get("phases", {})
    for ph in required:
        st = phases.get(ph, {}).get("status", "empty")
        if st == "agreed":
            results.append(("OK", f"phase {ph!r} agreed"))
        else:
            results.append(("FAIL", f"phase {ph!r} status is {st!r} — need 'agreed'"))
    if not data.get("agreed_at"):
        results.append(("FAIL", "blueprint-agreement.json: agreed_at not set"))
    else:
        results.append(("OK", f"agreed_at={data['agreed_at']}"))
    return results


def check_readme_status(repo: str, root: str, mode: str) -> list[tuple[str, str]]:
    if mode != "multi-file":
        return []
    readme = os.path.join(repo, root, "README.md")
    if not os.path.exists(readme):
        return []
    text = open(readme, encoding="utf-8").read()
    if re.search(r"Blueprint status\s*\|\s*`complete`", text, re.I):
        return [("OK", "README marks blueprint complete")]
    if "complete" in text.lower() and "| complete |" in text.lower():
        return [("OK", "README checklist shows complete")]
    return [("FAIL", f"{root}/README.md: Blueprint status not 'complete'")]


def check_intake(repo: str) -> list[tuple[str, str]]:
    """Hard-enforce that every blocking slot is answered with a valid source,
    and that Foundry-guessed values appear only when the user delegated."""
    results: list[tuple[str, str]] = []
    p = os.path.join(repo, INTAKE)
    if not os.path.exists(p):
        results.append(("FAIL", f"missing {INTAKE} — run intake; ask the user for every gap"))
        return results
    data = load_json(repo, INTAKE)
    if not data:
        results.append(("FAIL", f"{INTAKE} is empty or invalid JSON"))
        return results
    results.append(("OK", f"found {INTAKE}"))

    delegated = data.get("delegated") is True
    if delegated and not data.get("delegated_by"):
        results.append(("FAIL", "intake delegated=true but delegated_by is empty"))
    slots = data.get("slots", {}) or {}

    for key in BLOCKING_SLOTS:
        slot = slots.get(key)
        if not isinstance(slot, dict):
            results.append(("FAIL", f"intake slot {key!r} missing"))
            continue
        value = str(slot.get("value", "")).strip()
        source = str(slot.get("source", "")).strip().lower()
        if not value:
            results.append(("FAIL", f"intake slot {key!r} unanswered — ask the user"))
            continue
        if not source:
            results.append(("FAIL", f"intake slot {key!r} has no source"))
            continue
        if source not in PROVIDED_SOURCES | GUESS_SOURCES:
            results.append(("FAIL", f"intake slot {key!r} invalid source {source!r}"))
            continue
        if source in GUESS_SOURCES and not delegated:
            results.append(("FAIL",
                f"intake slot {key!r} is Foundry-guessed ({source}) but the user "
                f"did not delegate — ask the user or set delegated=true"))
            continue
        results.append(("OK", f"intake {key} ({source})"))
    return results


def _approved(rec: dict) -> bool:
    return bool(rec) and rec.get("approved") is True and bool(rec.get("approved_by"))


def check_approval(repo: str) -> list[tuple[str, str]]:
    """Mandatory user approval of the consolidated document(s).
    Empty/Blueprint: approval.project. Running: both running_approval docs."""
    results: list[tuple[str, str]] = []
    data = load_json(repo, AGREEMENT)
    if not data:
        results.append(("FAIL", "no agreement — cannot verify approval"))
        return results
    state = (data.get("state") or "empty").lower()
    if state == "running":
        ra = data.get("running_approval", {})
        for which in ("current_state", "requested_state"):
            rec = ra.get(which, {})
            if _approved(rec):
                results.append(("OK", f"approval: {which} approved by {rec['approved_by']}"))
            else:
                results.append(("FAIL",
                    f"Running state: {which} document not approved — assemble it, "
                    f"present to the user, record approval (approved + approved_by)"))
    else:
        rec = data.get("approval", {}).get("project", {})
        if _approved(rec):
            results.append(("OK", f"approval: project approved by {rec['approved_by']}"))
        else:
            results.append(("FAIL",
                "blueprint not approved — assemble docs/project/APPROVAL.md, present "
                "to the user, then set approval.project.approved + approved_by"))
    return results


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    repo = os.path.abspath(sys.argv[1])
    skip_intake = "--skip-intake" in sys.argv
    skip_approval = "--skip-approval" in sys.argv
    root, mode = blueprint_root(repo)
    results = []
    results.extend(check_files(repo, root, mode))
    results.extend(scan_tbds(repo, root, mode))
    results.extend(check_readme_status(repo, root, mode))
    results.extend(check_agreement(repo))
    if skip_intake:
        results.append(("OK", "intake check skipped (--skip-intake)"))
    else:
        results.extend(check_intake(repo))
    if skip_approval:
        results.append(("OK", "approval check skipped (--skip-approval)"))
    else:
        results.extend(check_approval(repo))
    fails = [r for r in results if r[0] == "FAIL"]
    for s, msg in results:
        print(f"[{s}] {msg}")
    print(f"\n{len(results) - len(fails)} passed, {len(fails)} failed")
    if fails:
        print("\nBlocked: complete blueprint + intake record + user approval, then re-run.")
        print("Intake: fill .foundry/intake.json — every blocking slot needs a value")
        print("        and a source; guesses (default/foundry-decided) require delegated=true.")
        print("Approval: assemble docs/project/APPROVAL.md (foundry_blueprint_assemble.py),")
        print("          get user sign-off, set approval in blueprint-agreement.json.")
        print("Route: docs-gen/project-blueprint/SKILL.md")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
