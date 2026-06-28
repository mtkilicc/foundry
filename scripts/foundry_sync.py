#!/usr/bin/env python3
"""foundry_sync.py — render canonical agent/skills/ to tool-specific layouts.

Canonical tree (SSOT): agent/skills/**/SKILL.md
  tier: root | orchestrator | leaf
  scope: optional glob

Targets (from docs/stack/agent-tooling.md):
  claude-code → .claude/skills/
  cursor      → .cursor/skills/ + .cursor/rules/00-routing.mdc
  openharness → .openharness/skills/ (Claude-compatible SKILL.md format)

Usage:
  python scripts/foundry_sync.py <repo_root>       # write renders
  python scripts/foundry_sync.py <repo_root> --check  # exit 1 if stale

Stdlib only.
"""
from __future__ import annotations

import hashlib
import os
import re
import sys

GENERATED = "<!-- foundry:generated from agent/skills/{rel} — do not edit -->"

CANONICAL_ROOT = "agent/skills"
TOOLING_PATH = "docs/stack/agent-tooling.md"
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLAUDE_STUB = os.path.join(_SCRIPT_DIR, "..", "templates", "wiring", "CLAUDE.md.stub")

TARGET_SKILLS = {
    "claude-code": ".claude/skills",
    "cursor": ".cursor/skills",
    "openharness": ".openharness/skills",
}

ROUTING_RULE = ".cursor/rules/00-routing.mdc"


# ---------- parsing ----------
def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    block = text[3:end]
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    key: str | None = None
    buf: list[str] = []
    for line in block.splitlines():
        if re.match(r"^[a-z_]+:\s*", line) and not line.startswith(" "):
            if key is not None:
                meta[key] = "\n".join(buf).strip()
            m = re.match(r"^([a-z_]+):\s*(.*)$", line)
            key = m.group(1)
            rest = m.group(2).strip()
            if rest in (">-", "|"):
                buf = []
            elif rest:
                buf = [rest]
            else:
                buf = []
        elif key is not None and (line.startswith("  ") or line.startswith("\t")):
            buf.append(line.strip())
        elif key is not None and line.strip():
            buf.append(line.strip())
    if key is not None:
        meta[key] = "\n".join(buf).strip()
    # fold YAML folded scalars to one line
    for k, v in list(meta.items()):
        meta[k] = re.sub(r"\s+", " ", v).strip()
    return meta, body


def parse_tooling(repo: str) -> dict[str, bool]:
    """Return {target: enabled} from agent-tooling.md table."""
    path = os.path.join(repo, TOOLING_PATH)
    defaults = {"claude-code": False, "cursor": False, "openharness": False, "generic": True}
    if not os.path.exists(path):
        return defaults
    text = open(path, encoding="utf-8").read()
    in_targets = False
    for line in text.splitlines():
        if "## Render targets" in line:
            in_targets = True
            continue
        if in_targets and line.startswith("## "):
            break
        if not in_targets:
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("target", "---", ":---"):
            continue
        target = cells[0].lower().replace(" ", "-")
        enabled = cells[1].lower() in ("yes", "true", "1")
        if target in defaults or target.replace("_", "-") in defaults:
            key = target.replace("_", "-")
            if key.startswith("claude"):
                key = "claude-code"
            defaults[key] = enabled
    # single-tool legacy: profile row
    m = re.search(r"\|\s*profile\s*\|\s*([^|]+)\|", text)
    if m:
        prof = m.group(1).strip().lower()
        if prof == "claude-code":
            defaults["claude-code"] = True
        elif prof == "cursor":
            defaults["cursor"] = True
        elif prof == "openharness":
            defaults["openharness"] = True
        elif prof == "multi-tool":
            defaults["claude-code"] = True
            defaults["cursor"] = True
    return defaults


def find_skills(canonical: str) -> list[str]:
    out = []
    for r, _, files in os.walk(canonical):
        if "SKILL.md" in files:
            out.append(os.path.join(r, "SKILL.md"))
    return sorted(out)


# ---------- rendering ----------
def infer_tier(rel: str, body: str, meta: dict[str, str]) -> str:
    if meta.get("tier"):
        return meta["tier"]
    if rel in ("SKILL.md",):
        return "root"
    if re.search(r"\(leaf\s*[—-]\s*read only when routed", body, re.I):
        return "leaf"
    if re.search(r"^#\s+\S+\s+\(leaf\s*[—-]", body, re.M | re.I):
        return "leaf"
    return "orchestrator"


ORCH_SCOPES = {
    "backend": "backend/**",
    "frontend": "frontend/**",
    "orchestration": "compose/**,docker-compose*.yml",
    "observability": "backend/apps/observability/**,backend/apps/alerting/**,frontend/src/modules/observability/**",
}


def infer_scope(body: str, meta: dict[str, str], tier: str, name: str = "") -> str:
    if meta.get("scope"):
        return meta["scope"].strip()
    m = re.search(r"Applies to:\s*`([^`]+)`", body)
    if m:
        return m.group(1).strip()
    m = re.search(r"Applies to:\s*([^\n]+)", body)
    if m:
        return m.group(1).strip().strip("`")
    if tier == "orchestrator" and name in ORCH_SCOPES:
        return ORCH_SCOPES[name]
    return ""


def render_claude_cursor(meta: dict[str, str], body: str, rel: str) -> str:
    name = meta.get("name", "")
    desc = meta.get("description", "")
    tier = infer_tier(rel, body, meta)
    scope = infer_scope(body, meta, tier, name)

    lines = ["---", f"name: {name}", f"description: >-", f"  {desc}"]
    if tier == "leaf":
        lines.append("disable-model-invocation: true")
        if scope:
            lines.append(f"paths: {scope}")
    elif tier == "orchestrator" and scope:
        lines.append(f"paths: {scope}")
    # root: unscoped, auto-invokable
    lines.append("---")
    lines.append("")
    lines.append(GENERATED.format(rel=rel))
    lines.append("")
    lines.append(body.rstrip())
    lines.append("")
    return "\n".join(lines)


def routing_mdc_body(root_body: str) -> str:
  return (
      "# Skill routing (always on)\n\n"
      "Before any implementation, read `agent/skills/SKILL.md` and follow its "
      "decision table. State which child skill you read next. Leaf skills only "
      "when the parent routes you there.\n\n"
      "Canonical tree: `agent/skills/`. After skill edits run "
      "`python scripts/foundry_sync.py .` (Foundry agent).\n\n"
      "## Root decision table (mirror)\n\n"
      + extract_decision_table(root_body)
  )


def extract_decision_table(body: str) -> str:
    """Pull decision table from root skill body for the Cursor always-on rule."""
    lines = body.splitlines()
    out: list[str] = []
    in_table = False
    for line in lines:
        if re.match(r"^##\s+Step\s+2\s+—\s+decision table", line, re.I):
            in_table = True
            continue
        if in_table and line.startswith("## Step"):
            break
        if in_table:
            out.append(line)
    return "\n".join(out).strip() + "\n" if out else "(see agent/skills/SKILL.md)\n"


def render_routing_mdc(root_meta: dict[str, str], root_body: str) -> str:
    desc = root_meta.get("description", "Project skill router")
    body = routing_mdc_body(root_body)
    return (
        "---\n"
        f"description: {desc[:200]}\n"
        "alwaysApply: true\n"
        "---\n\n"
        f"{GENERATED.format(rel='SKILL.md')}\n\n"
        f"{body}"
    )


def claude_md_content(repo: str) -> str:
    if os.path.exists(CLAUDE_STUB):
        return open(CLAUDE_STUB, encoding="utf-8").read().strip() + "\n"
    return (
        "@AGENTS.md\n\n"
        "## Routing\n\n"
        "Read `agent/skills/SKILL.md` before any implementation.\n"
    )


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sync_repo(repo: str, check_only: bool = False) -> list[tuple[str, str]]:
    """Returns list of (status, message). status OK or FAIL."""
    results: list[tuple[str, str]] = []
    canonical = os.path.join(repo, CANONICAL_ROOT)
    if not os.path.isdir(canonical):
        results.append(("FAIL", f"missing canonical tree: {CANONICAL_ROOT}/"))
        return results

    targets = parse_tooling(repo)
    skills = find_skills(canonical)
    if not skills:
        results.append(("FAIL", f"no SKILL.md under {CANONICAL_ROOT}/"))
        return results

    root_skill = os.path.join(canonical, "SKILL.md")
    root_meta, root_body = {}, ""
    if os.path.exists(root_skill):
        root_meta, root_body = parse_frontmatter(open(root_skill, encoding="utf-8").read())

    planned: dict[str, str] = {}

    for skill_path in skills:
        rel = os.path.relpath(skill_path, canonical)
        rel_dir = os.path.dirname(rel)
        raw = open(skill_path, encoding="utf-8").read()
        meta, body = parse_frontmatter(raw)
        if not meta.get("name"):
            results.append(("FAIL", f"missing name: {skill_path}"))
            continue
        rendered = render_claude_cursor(meta, body, rel)
        for target, out_root in TARGET_SKILLS.items():
            if not targets.get(target):
                continue
            out_path = os.path.join(repo, out_root, rel_dir, "SKILL.md")
            planned[out_path] = rendered

    if targets.get("cursor") and root_body:
        planned[os.path.join(repo, ROUTING_RULE)] = render_routing_mdc(root_meta, root_body)

    if targets.get("claude-code"):
        planned[os.path.join(repo, "CLAUDE.md")] = claude_md_content(repo)

    stale = []
    for path, content in sorted(planned.items()):
        if os.path.exists(path):
            existing = open(path, encoding="utf-8").read()
            if sha(existing) == sha(content):
                results.append(("OK", f"up to date: {os.path.relpath(path, repo)}"))
                continue
            stale.append(os.path.relpath(path, repo))
        else:
            stale.append(os.path.relpath(path, repo))

        if not check_only:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(content)
            results.append(("OK", f"written: {os.path.relpath(path, repo)}"))
        else:
            results.append(("FAIL", f"stale or missing: {os.path.relpath(path, repo)}"))

    if check_only and stale:
        results.append(("FAIL", f"sync required — run: python scripts/foundry_sync.py {repo}"))

    enabled = [t for t, on in targets.items() if on and t in TARGET_SKILLS]
    if enabled:
        results.append(("OK", f"targets: {', '.join(enabled)}"))
    else:
        results.append(("OK", "generic-only — no tool renders enabled"))

    return results


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    repo = os.path.abspath(sys.argv[1])
    check_only = "--check" in sys.argv
    results = sync_repo(repo, check_only=check_only)
    fails = [r for r in results if r[0] == "FAIL"]
    for status, msg in results:
        print(f"[{status}] {msg}")
    print(f"\n{len(results) - len(fails)} passed, {len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
