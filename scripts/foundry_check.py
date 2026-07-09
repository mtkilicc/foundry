#!/usr/bin/env python3
"""foundry_check.py — deterministic verification, no LLM judgment.

Modes:
  structure <skills_root>          verify canonical skill tree (usually agent/skills)
  queue <repo_root>                process .foundry/queue.json
  sync <repo_root>                 verify renders match canonical (foundry_sync --check)
  drift <repo_root>                run skill drift scan (--git); fail if proposals need review
  identity <repo_root>             verify project-unique identity docs + fingerprint
  blueprint <repo_root>            verify project blueprint complete + phase agreement
  completeness <repo_root>         once skills exist, require design-identity + domain docs + task-plan
  all <skills_root> <repo_root>    structure + completeness + queue + sync + drift + identity + blueprint

Exit 0 = green. Exit 1 = failures or items needing review (listed on stdout).
Stdlib only. LLMs run this instead of self-grading; humans read the table.
"""
import json, os, re, sys, datetime

OK, BAD = "OK", "FAIL"

# ---------- structure checks ----------
def check_structure(root):
    results = []
    skill_files = []
    for r, _, files in os.walk(root):
        for fn in files:
            if fn == "SKILL.md":
                skill_files.append(os.path.join(r, fn))
    if not skill_files:
        return [(BAD, "no SKILL.md found under " + root)]

    names = {}
    for p in skill_files:
        folder = os.path.basename(os.path.dirname(p))
        txt = open(p, encoding="utf-8").read()
        m = re.search(r"^name:\s*(\S+)", txt, re.M)
        name = m.group(1) if m else None
        names[p] = (folder, name, txt)
        results.append((OK if name == folder else BAD,
                        f"name==folder: {folder!r} vs {name!r} ({p})"))
        if not re.search(r"^description:", txt, re.M):
            results.append((BAD, f"missing description: {p}"))

    # parent decision tables must reference every child skill folder
    for p, (folder, _, txt) in names.items():
        d = os.path.dirname(p)
        children = [c for c in os.listdir(d)
                    if os.path.isdir(os.path.join(d, c))
                    and os.path.exists(os.path.join(d, c, "SKILL.md"))]
        for c in children:
            hit = (c + "/SKILL.md") in txt or f"`{c}`" in txt
            results.append((OK if hit else BAD,
                            f"routing: {folder} references child {c!r}"))

    # leaf size budget + dead relative links
    for p, (folder, _, txt) in names.items():
        depth = os.path.relpath(p, root).count(os.sep)
        if depth >= 2:  # leaves
            n = len(txt.splitlines())
            results.append((OK if n <= 90 else BAD,
                            f"size budget (<=90): {folder} = {n} lines"))
        for link in re.findall(r"`((?:\.\./)+[^`<>]+\.(?:md|py))`", txt):
            t = os.path.normpath(os.path.join(os.path.dirname(p), link))
            results.append((OK if os.path.exists(t) else BAD,
                            f"link: {folder} -> {link}"))

    # vendor-folder leaks outside adapter profiles / examples / README
    for p, (folder, _, txt) in names.items():
        rel = os.path.relpath(p, root)
        if rel.startswith(("adapter", "examples")):
            continue
        leak = re.search(r"\.claude\b|\.cursor\b|\.windsurf\b", txt)
        results.append((OK if not leak else BAD, f"vendor-leak: {rel}"))
    return results

# ---------- queue checks ----------
EVENT_TYPES = {"mcp_proposal", "new_profile", "layer_change",
               "finding", "new_artifact", "new_template", "skill_drift",
               "blueprint_change"}
REQUIRED = {"id", "ts", "type", "by_skill", "summary", "status"}

def load_catalog_mcps(repo_root):
    """MCP names registered in docs stack mcp-setup.md (first table column)."""
    out = set()
    for cand in ("docs/stack/mcp-setup.md",):
        p = os.path.join(repo_root, cand)
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                m = re.match(r"\|\s*([^|]+?)\s*\|", line)
                if m and m.group(1).lower() not in ("name", "---", ":---"):
                    out.add(m.group(1).strip().lower())
    return out

def check_queue(repo_root):
    qpath = os.path.join(repo_root, ".foundry", "queue.json")
    results, review = [], []
    if not os.path.exists(qpath):
        return [(OK, "no queue file — nothing pending")], []
    try:
        q = json.load(open(qpath, encoding="utf-8"))
    except Exception as e:
        return [(BAD, f"queue.json unreadable: {e}")], []
    events = q.get("events", [])
    registered = load_catalog_mcps(repo_root)
    changed = False
    for ev in events:
        missing = REQUIRED - set(ev)
        if missing:
            results.append((BAD, f"event {ev.get('id','?')}: missing {sorted(missing)}"))
            continue
        if ev["type"] not in EVENT_TYPES:
            results.append((BAD, f"event {ev['id']}: unknown type {ev['type']}"))
            continue
        if ev["status"] != "pending":
            continue
        # auto-resolution rules (pure logic, no judgment)
        if ev["type"] == "mcp_proposal":
            name = ev.get("payload", {}).get("mcp", "").lower()
            if name and name in registered:
                ev["status"] = "auto_rejected_duplicate"
                results.append((OK, f"{ev['id']}: MCP {name!r} already registered — auto-rejected"))
            else:
                ev["status"] = "needs_review"
        elif ev["type"] == "new_artifact":
            path = ev.get("payload", {}).get("path", "")
            exists = os.path.exists(os.path.join(repo_root, path))
            ev["status"] = "auto_ok" if exists else "needs_review"
            results.append((OK if exists else BAD,
                            f"{ev['id']}: artifact exists: {path}"))
        elif ev["type"] == "skill_drift":
            if ev.get("payload", {}).get("disposition") == "auto_rejected":
                ev["status"] = "auto_rejected_duplicate"
                results.append((OK, f"{ev['id']}: skill_drift auto-rejected"))
            else:
                ev["status"] = "needs_review"
        else:
            ev["status"] = "needs_review"
        changed = True
        if ev["status"] == "needs_review":
            review.append(ev)
    if changed:
        q["last_check"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        json.dump(q, open(qpath, "w", encoding="utf-8"), indent=2)
    for ev in review:
        results.append((BAD, f"NEEDS_REVIEW {ev['id']} [{ev['type']}] {ev['summary']} (by {ev['by_skill']})"))
    return results, review

# ---------- sync check ----------
def check_sync(repo_root):
    sync_py = os.path.join(os.path.dirname(__file__), "foundry_sync.py")
    if not os.path.exists(sync_py):
        return [(BAD, "foundry_sync.py missing")]
    import subprocess
    r = subprocess.run(
        [sys.executable, sync_py, repo_root, "--check"],
        capture_output=True, text=True,
    )
    lines = (r.stdout or "").strip().splitlines()
    results = []
    for line in lines:
        if line.startswith("[OK]") or line.startswith("[FAIL]"):
            # Parse by the first "]" — a fixed-width slice mis-reads the
            # 6-char "[FAIL]" tag as "FA", so failures never matched BAD
            # and identity/blueprint (and their "all" sub-blocks) always
            # exited 0 even on a fully failing repo.
            close = line.index("]")
            results.append((line[1:close], line[close + 2:]))
    if r.returncode != 0 and not any(x[0] == BAD for x in results):
        results.append((BAD, "sync check failed"))
    if not results:
        results.append((OK if r.returncode == 0 else BAD, "sync check complete"))
    return results

# ---------- drift check ----------
def check_drift(repo_root):
    drift_py = os.path.join(os.path.dirname(__file__), "foundry_skill_drift.py")
    if not os.path.exists(drift_py):
        return [(BAD, "foundry_skill_drift.py missing")]
    import subprocess
    r = subprocess.run(
        [sys.executable, drift_py, repo_root, "--git"],
        capture_output=True, text=True,
    )
    results = []
    for line in (r.stdout or "").strip().splitlines():
        if line.startswith("[OK]") or line.startswith("[FAIL]"):
            # Parse by the first "]" — a fixed-width slice mis-reads the
            # 6-char "[FAIL]" tag as "FA", so failures never matched BAD
            # and identity/blueprint (and their "all" sub-blocks) always
            # exited 0 even on a fully failing repo.
            close = line.index("]")
            results.append((line[1:close], line[close + 2:]))
    report_path = os.path.join(repo_root, ".foundry", "skill-drift-report.json")
    if os.path.exists(report_path):
        try:
            report = json.load(open(report_path, encoding="utf-8"))
            n = sum(
                1 for p in report.get("proposals", [])
                if p.get("disposition") != "auto_rejected"
            )
            if n:
                results.append((BAD, f"{n} skill drift proposal(s) need post-job-update"))
            else:
                results.append((OK, "no skill drift proposals"))
        except (json.JSONDecodeError, OSError):
            results.append((BAD, "skill-drift-report.json unreadable"))
    if r.returncode != 0 and not any(x[0] == BAD for x in results):
        results.append((BAD, "drift check reported proposals"))
    if not results:
        results.append((OK if r.returncode == 0 else BAD, "drift check complete"))
    return results

# ---------- identity check ----------
def check_identity(repo_root):
    id_py = os.path.join(os.path.dirname(__file__), "foundry_identity_check.py")
    if not os.path.exists(id_py):
        return [(BAD, "foundry_identity_check.py missing")]
    import subprocess
    r = subprocess.run(
        [sys.executable, id_py, repo_root],
        capture_output=True, text=True,
    )
    results = []
    for line in (r.stdout or "").strip().splitlines():
        if line.startswith("[OK]") or line.startswith("[FAIL]"):
            # Parse by the first "]" — a fixed-width slice mis-reads the
            # 6-char "[FAIL]" tag as "FA", so failures never matched BAD
            # and identity/blueprint (and their "all" sub-blocks) always
            # exited 0 even on a fully failing repo.
            close = line.index("]")
            results.append((line[1:close], line[close + 2:]))
    if not results:
        results.append((OK if r.returncode == 0 else BAD, "identity check complete"))
    return results

# ---------- bootstrap completeness ----------
def _blueprint_root(repo_root):
    try:
        cfg = json.load(open(os.path.join(repo_root, ".foundry", "config.json"), encoding="utf-8"))
        return cfg.get("blueprint", {}).get("root", "docs/project")
    except (OSError, json.JSONDecodeError):
        return "docs/project"

def check_completeness(repo_root):
    """A bootstrap that produced skills must ALSO have produced the general
    UI/UX definition, domain docs, and a task plan. Catches partial bootstraps
    that otherwise pass every other check (skills look fine but no design /
    no tasks)."""
    skills_root = os.path.join(repo_root, "agent", "skills")
    if not os.path.exists(os.path.join(skills_root, "SKILL.md")):
        return [(OK, "completeness: skills not generated yet — skip")]
    results = []
    design = os.path.join(repo_root, "docs", "stack", "design-identity.md")
    results.append((OK if os.path.exists(design) else BAD,
                    "completeness: docs/stack/design-identity.md (general UI/UX definition)"))
    # at least one domain doc anywhere under docs/**/domain/
    domain_docs = []
    for r, _, files in os.walk(os.path.join(repo_root, "docs")):
        if os.path.basename(r) == "domain":
            domain_docs += [f for f in files if f.endswith(".md")]
    results.append((OK if domain_docs else BAD,
                    f"completeness: domain docs present ({len(domain_docs)} found)"))
    task_plan = os.path.join(repo_root, _blueprint_root(repo_root), "task-plan.md")
    results.append((OK if os.path.exists(task_plan) else BAD,
                    "completeness: task-plan.md (tasks generated)"))
    return results

# ---------- blueprint gate ----------
def check_blueprint(repo_root):
    bp_py = os.path.join(os.path.dirname(__file__), "foundry_blueprint_check.py")
    if not os.path.exists(bp_py):
        return [(BAD, "foundry_blueprint_check.py missing")]
    import subprocess
    r = subprocess.run(
        [sys.executable, bp_py, repo_root],
        capture_output=True, text=True,
    )
    results = []
    for line in (r.stdout or "").strip().splitlines():
        if line.startswith("[OK]") or line.startswith("[FAIL]"):
            # Parse by the first "]" — a fixed-width slice mis-reads the
            # 6-char "[FAIL]" tag as "FA", so failures never matched BAD
            # and identity/blueprint (and their "all" sub-blocks) always
            # exited 0 even on a fully failing repo.
            close = line.index("]")
            results.append((line[1:close], line[close + 2:]))
    if not results:
        results.append((OK if r.returncode == 0 else BAD, "blueprint check complete"))
    return results

# ---------- main ----------
def report(results):
    fails = [r for r in results if r[0] == BAD]
    for s, msg in results:
        print(f"[{s}] {msg}")
    print(f"\n{len(results)-len(fails)} passed, {len(fails)} failed/needs-review")
    return 1 if fails else 0

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    rc = 0
    if mode in ("structure", "all"):
        rc |= report(check_structure(sys.argv[2]))
    if mode in ("completeness", "all"):
        repo = sys.argv[2] if mode == "completeness" else sys.argv[3]
        rc |= report(check_completeness(repo))
    if mode in ("queue", "all"):
        root = sys.argv[3] if mode == "all" else sys.argv[2]
        res, _ = check_queue(root)
        rc |= report(res)
    if mode in ("sync", "all"):
        repo = sys.argv[2] if mode == "sync" else sys.argv[3]
        rc |= report(check_sync(repo))
    if mode in ("drift", "all"):
        repo = sys.argv[2] if mode == "drift" else sys.argv[3]
        rc |= report(check_drift(repo))
    if mode in ("identity", "all"):
        repo = sys.argv[2] if mode == "identity" else sys.argv[3]
        rc |= report(check_identity(repo))
    if mode in ("blueprint", "all"):
        repo = sys.argv[2] if mode == "blueprint" else sys.argv[3]
        rc |= report(check_blueprint(repo))
    sys.exit(rc)
