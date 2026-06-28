#!/usr/bin/env python3
"""foundry_skill_drift.py — detect doc/skill drift after feature work.

Compares changed domain docs against anchoring canonical skills. Proposes
skill updates when the contract grew but the map did not.

Usage:
  python scripts/foundry_skill_drift.py <repo> --git
  python scripts/foundry_skill_drift.py <repo> --files path1 path2
  python scripts/foundry_skill_drift.py <repo> --git --enqueue

Output: .foundry/skill-drift-report.json
Optional: skill_drift events in .foundry/queue.json

Stdlib only.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))
from foundry_lib import CANONICAL_ROOT, load_config  # noqa: E402

REPORT_PATH = ".foundry/skill-drift-report.json"
QUEUE_PATH = ".foundry/queue.json"

# Artifacts to compare between docs and skills
PATH_PAT = re.compile(
    r"(?:`|\b)((?:frontend|backend|compose)/[^\s`\"']+?)(?:`|\b)"
)
ROUTE_PAT = re.compile(
    r"`((?:_secured|_auth)/[^`]+?\.tsx)`|"
    r"`([^`]*routes/[^`]+?\.tsx)`|"
    r"\|\s*`([^`]+?\.tsx)`\s*\|"
)
API_PAT = re.compile(r"`(/api/[^`]+)`")
HEADING_PAT = re.compile(r"^#{1,3}\s+(.+)$", re.M)
STATUS_ONLY = re.compile(r"^Status:\s*\w+\s*$", re.M)


def git_changed_files(repo: str) -> list[str]:
    files: set[str] = set()
    for cmd in (
        ["git", "-C", repo, "diff", "--name-only", "HEAD"],
        ["git", "-C", repo, "diff", "--cached", "--name-only"],
        ["git", "-C", repo, "diff", "--name-only"],
    ):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, check=False)
            for line in (out.stdout or "").splitlines():
                line = line.strip()
                if line:
                    files.add(line)
        except OSError:
            pass
    return sorted(files)


def find_skills(repo: str, root: str) -> list[str]:
    base = os.path.join(repo, root)
    out = []
    if not os.path.isdir(base):
        return out
    for r, _, files in os.walk(base):
        if "SKILL.md" in files:
            out.append(os.path.join(r, "SKILL.md"))
    return sorted(out)


def skills_for_doc(repo: str, skills: list[str], doc_rel: str) -> list[str]:
    hits = []
    doc_name = os.path.basename(doc_rel)
    for sp in skills:
        txt = open(sp, encoding="utf-8").read()
        if doc_rel in txt or doc_name in txt:
            hits.append(sp)
    return hits


def extract_doc_artifacts(text: str) -> dict[str, set[str]]:
    paths = set(PATH_PAT.findall(text))
    routes = set()
    for m in ROUTE_PAT.finditer(text):
        routes |= {g for g in m.groups() if g}
    apis = set(API_PAT.findall(text))
    headings = set()
    for h in HEADING_PAT.findall(text):
        h = h.strip()
        if h and not h.startswith(("Status", "When you")):
            headings.add(h)
    return {"paths": paths, "routes": routes, "apis": apis, "headings": headings}


def extract_skill_artifacts(text: str) -> dict[str, set[str]]:
    paths = set(PATH_PAT.findall(text))
    routes = set()
    for m in ROUTE_PAT.finditer(text):
        routes |= {g for g in m.groups() if g}
    apis = set(API_PAT.findall(text))
    desc_m = re.search(r"^description:\s*>?-?\s*(.+)$", text, re.M | re.S)
    desc = desc_m.group(1) if desc_m else ""
    desc = re.sub(r"\s+", " ", desc[:500])
    return {"paths": paths, "routes": routes, "apis": apis, "description": {desc}}


def doc_change_is_status_only(old: str, new: str) -> bool:
    def strip_status(t: str) -> str:
        return STATUS_ONLY.sub("", t).strip()
    return strip_status(old) == strip_status(new)


def feature_tokens(heading: str) -> list[str]:
    stop = {"the", "and", "for", "with", "page", "route", "api", "new", "add"}
    words = re.findall(r"[a-z][a-z0-9_-]{2,}", heading.lower())
    return [w for w in words if w not in stop]


def rel_skill_path(repo: str, skill_path: str) -> str:
    return os.path.relpath(skill_path, repo)


def propose_gaps(
    repo: str,
    doc_rel: str,
    skill_path: str,
    doc_art: dict,
    skill_art: dict,
    old_doc: str | None,
    new_doc: str,
) -> list[dict]:
    proposals = []
    skill_txt = open(skill_path, encoding="utf-8").read()
    skill_rel = rel_skill_path(repo, skill_path)

    if old_doc and doc_change_is_status_only(old_doc, new_doc):
        return [
            {
                "kind": "doc_status_only",
                "skill": skill_rel,
                "doc": doc_rel,
                "summary": f"only Status changed in {doc_rel}",
                "auto_reject": True,
            }
        ]

    for path in sorted(doc_art["paths"] | doc_art["routes"]):
        if path in skill_art["paths"] | skill_art["routes"]:
            continue
        if path in skill_txt:
            continue
        proposals.append(
            {
                "kind": "code_map_gap",
                "skill": skill_rel,
                "doc": doc_rel,
                "artifact": path,
                "summary": f"doc {doc_rel} references {path!r} missing from {skill_rel}",
                "suggested_action": f"Add {path!r} to Code map or Owns in {skill_rel}",
                "auto_reject": False,
            }
        )

    for api in sorted(doc_art["apis"]):
        if api in skill_art["apis"] or api in skill_txt:
            continue
        proposals.append(
            {
                "kind": "code_map_gap",
                "skill": skill_rel,
                "doc": doc_rel,
                "artifact": api,
                "summary": f"endpoint {api} in {doc_rel} not in {skill_rel}",
                "suggested_action": f"Add endpoint {api} to Code map",
                "auto_reject": False,
            }
        )

    desc = next(iter(skill_art.get("description", {""})), "")
    for heading in doc_art["headings"]:
        tokens = feature_tokens(heading)
        if not tokens:
            continue
        missing = [t for t in tokens if t not in desc.lower() and t not in skill_txt.lower()]
        if len(missing) >= 2:
            proposals.append(
                {
                    "kind": "trigger_gap",
                    "skill": skill_rel,
                    "doc": doc_rel,
                    "artifact": heading,
                    "missing_terms": missing,
                    "summary": f"feature {heading!r} may need description triggers in {skill_rel}",
                    "suggested_action": "Extend description with pushy WHEN triggers",
                    "auto_reject": False,
                }
            )
    return proposals


def analyze_repo(repo: str, changed_files: list[str], cfg: dict) -> dict:
    skills_root = cfg.get("canonical_skills_root", CANONICAL_ROOT)
    skills = find_skills(repo, skills_root)
    proposals: list[dict] = []
    scanned_docs: list[str] = []

    domain_docs = [
        f
        for f in changed_files
        if f.startswith("docs/") and "/domain/" in f and f.endswith(".md")
    ]

    for doc_rel in domain_docs:
        doc_path = os.path.join(repo, doc_rel)
        if not os.path.exists(doc_path):
            continue
        scanned_docs.append(doc_rel)
        new_doc = open(doc_path, encoding="utf-8").read()
        old_doc = None
        try:
            r = subprocess.run(
                ["git", "-C", repo, "show", f"HEAD:{doc_rel}"],
                capture_output=True,
                text=True,
                check=False,
            )
            if r.returncode == 0:
                old_doc = r.stdout
        except OSError:
            pass

        doc_art = extract_doc_artifacts(new_doc)
        anchored = skills_for_doc(repo, skills, doc_rel)
        if not anchored:
            proposals.append(
                {
                    "kind": "new_leaf_candidate",
                    "skill": None,
                    "doc": doc_rel,
                    "summary": f"changed doc {doc_rel} has no anchoring skill",
                    "suggested_action": "Run skills-gen/single-skill to create a leaf",
                    "auto_reject": False,
                }
            )
            continue

        for sp in anchored:
            skill_art = extract_skill_artifacts(open(sp, encoding="utf-8").read())
            proposals.extend(
                propose_gaps(repo, doc_rel, sp, doc_art, skill_art, old_doc, new_doc)
            )

    auto_reject = set(cfg.get("drift", {}).get("auto_reject_kinds", []))
    for p in proposals:
        if p.get("kind") in auto_reject or p.get("auto_reject"):
            p["disposition"] = "auto_rejected"
        else:
            p["disposition"] = "needs_review"

    return {
        "version": 1,
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "changed_files": changed_files,
        "scanned_docs": scanned_docs,
        "render_targets": [
            k
            for k, v in cfg.get("render_targets", {}).items()
            if v.get("enabled")
        ],
        "proposals": proposals,
    }


def enqueue_proposals(repo: str, report: dict) -> int:
    qpath = os.path.join(repo, QUEUE_PATH)
    q = {"version": 1, "events": []}
    if os.path.exists(qpath):
        try:
            q = json.load(open(qpath, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    added = 0
    for p in report.get("proposals", []):
        if p.get("disposition") == "auto_rejected":
            continue
        ev_id = "evt-" + uuid.uuid4().hex[:8]
        q.setdefault("events", []).append(
            {
                "id": ev_id,
                "ts": report["ts"],
                "type": "skill_drift",
                "by_skill": "skills-gen/post-job-update",
                "summary": p.get("summary", "skill drift"),
                "payload": p,
                "status": "pending",
                "routed_to": "skills-gen/post-job-update",
            }
        )
        added += 1
    os.makedirs(os.path.dirname(qpath), exist_ok=True)
    json.dump(q, open(qpath, "w", encoding="utf-8"), indent=2)
    return added


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    repo = os.path.abspath(sys.argv[1])
    cfg = load_config(repo)
    if not cfg.get("post_job", {}).get("enabled", True):
        print("[OK] post_job disabled in config")
        return 0

    if "--git" in sys.argv:
        changed = git_changed_files(repo)
    elif "--files" in sys.argv:
        i = sys.argv.index("--files")
        changed = sys.argv[i + 1 :]
    else:
        changed = git_changed_files(repo)

    report = analyze_repo(repo, changed, cfg)
    rpath = os.path.join(repo, REPORT_PATH)
    os.makedirs(os.path.dirname(rpath), exist_ok=True)
    json.dump(report, open(rpath, "w", encoding="utf-8"), indent=2)

    n_prop = len(report["proposals"])
    n_reject = sum(1 for p in report["proposals"] if p.get("disposition") == "auto_rejected")
    n_review = n_prop - n_reject
    print(f"[OK] report: {REPORT_PATH}")
    print(f"[OK] scanned {len(report['scanned_docs'])} domain docs, {n_prop} proposals ({n_review} need review)")

    for p in report["proposals"]:
        tag = p.get("disposition", "?")
        print(f"  [{tag}] {p.get('kind')}: {p.get('summary')}")

    if "--enqueue" in sys.argv and cfg.get("post_job", {}).get("enqueue_proposals", True):
        added = enqueue_proposals(repo, report)
        print(f"[OK] enqueued {added} skill_drift events")

    if n_review > 0:
        print(
            "\nNext: read skills-gen/post-job-update/SKILL.md and apply proposals, "
            "then foundry_sync + foundry_check"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
