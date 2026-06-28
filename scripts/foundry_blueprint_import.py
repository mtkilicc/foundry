#!/usr/bin/env python3
"""foundry_blueprint_import.py — import blueprint seed + extract tech stack.

Merges content from an existing blueprint/project folder with the target repo
and writes extract snapshot + drafts 01-tech-stack.md tables.

Usage:
  python scripts/foundry_blueprint_import.py <repo> --from <seed_folder>
  python scripts/foundry_blueprint_import.py <repo>              # repo root only
  python scripts/foundry_blueprint_import.py <repo> --from <seed> --write
  python scripts/foundry_blueprint_import.py <repo> --archive-legacy --write

--write           copies missing blueprint files from seed and updates tech-stack doc.
--archive-legacy  discover stray *.md outside the canonical tree, MOVE them under
                  docs/_legacy/ (with --write; reversible) and write
                  .foundry/legacy-docs.json for the blueprint skill to consolidate.

Stdlib only.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

EXTRACT_OUT = ".foundry/tech-stack-extract.json"
LEGACY_MANIFEST = ".foundry/legacy-docs.json"
LEGACY_DEST = "docs/_legacy"
TECH_DOC = "docs/project/01-tech-stack.md"

# Markdown outside these stays put; everything else is a consolidation candidate.
CANONICAL_DOC_PREFIXES = (
    "docs/project",
    "docs/stack",
    "docs/integration",
    "docs/_legacy",
    "agent/skills",
)
# Directories never scanned for legacy docs.
SKIP_DIRS = {
    ".git", ".foundry", ".claude", ".cursor", ".openharness",
    "node_modules", "dist", "build", "__pycache__", ".venv", "venv",
}
# Root files that are entry points, not legacy content.
KEEP_ROOT_FILES = {"README.md", "AGENTS.md", "CLAUDE.md", "CHANGELOG.md", "LICENSE.md"}
BLUEPRINT_FILES = [
    "README.md",
    "00-vision.md",
    "01-tech-stack.md",
    "02-scope-phases.md",
    "03-architecture.md",
    "04-domains.md",
    "05-constraints.md",
    "06-open-questions.md",
]

# Renumbered: old 01-scope -> 02-scope etc. Import handles both layouts.


def read_json(path: str) -> dict | list | None:
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def detect_in_dir(base: str) -> list[dict]:
    """Return detected stack rows from lockfiles and compose under base."""
    rows: list[dict] = []
    if not base or not os.path.isdir(base):
        return rows

    def add(layer: str, choice: str, version: str, artifact: str) -> None:
        if choice:
            rows.append({
                "layer": layer,
                "choice": choice,
                "version": version,
                "artifact": artifact,
                "source": "extracted",
            })

    pj = os.path.join(base, "package.json")
    if os.path.exists(pj):
        data = read_json(pj) or {}
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        add("frontend runtime", "node", data.get("engines", {}).get("node", ""), "package.json")
        for key, layer in (
            ("react", "frontend framework"),
            ("vue", "frontend framework"),
            ("next", "frontend framework"),
            ("vite", "frontend bundler"),
            ("@tanstack/react-router", "frontend routing"),
            ("typescript", "frontend language"),
        ):
            if key in deps:
                add(layer, key, deps[key], "package.json")

    for req in ("requirements.txt", "pyproject.toml", "Pipfile"):
        p = os.path.join(base, req)
        if os.path.exists(p):
            text = open(p, encoding="utf-8", errors="replace").read()[:8000]
            add("backend manifest", req, "", req)
            for pat, name in [
                (r"Django[=<>~!]*([0-9.]+)?", "Django"),
                (r"djangorestframework", "DRF"),
                (r"celery", "Celery"),
                (r"fastapi", "FastAPI"),
                (r"flask", "Flask"),
            ]:
                m = re.search(pat, text, re.I)
                if m:
                    add("backend framework", name, m.group(0), req)

    for compose in ("docker-compose.yml", "docker-compose.yaml", "compose.yml"):
        p = os.path.join(base, compose)
        if os.path.exists(p):
            text = open(p, encoding="utf-8", errors="replace").read()[:12000]
            add("deploy", "docker compose", "", compose)
            for svc in ("postgres", "redis", "nginx", "traefik", "prometheus", "loki", "grafana"):
                if re.search(rf"\b{svc}\b", text, re.I):
                    add("infrastructure", svc, "", compose)

    go = os.path.join(base, "go.mod")
    if os.path.exists(go):
        add("backend runtime", "go", "", "go.mod")

    return rows


def find_blueprint_root(seed: str) -> str | None:
    for cand in (
        os.path.join(seed, "docs", "project"),
        os.path.join(seed, "project_overview"),
        os.path.join(seed, "blueprint"),
        seed,
    ):
        if os.path.isdir(cand) and (
            os.path.exists(os.path.join(cand, "README.md"))
            or os.path.exists(os.path.join(cand, "00-vision.md"))
            or os.path.exists(os.path.join(cand, "BLUEPRINT.md"))
        ):
            return cand
    return None


def copy_blueprint_seed(seed_bp: str, repo: str, write: bool) -> list[str]:
    copied = []
    if not write:
        return copied
    dest = os.path.join(repo, "docs", "project")
    os.makedirs(dest, exist_ok=True)
    for fn in os.listdir(seed_bp):
        src = os.path.join(seed_bp, fn)
        if not os.path.isfile(src) or not fn.endswith(".md"):
            continue
        dst = os.path.join(dest, fn)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            copied.append(fn)
    return copied


def render_extract_table(rows: list[dict]) -> str:
    lines = ["| artifact | path | detected |", "|---|---|---|"]
    for r in rows:
        det = f"{r.get('choice', '')} {r.get('version', '')}".strip()
        lines.append(f"| {r.get('layer', '')} | `{r.get('artifact', '')}` | {det} |")
    return "\n".join(lines) if len(lines) > 2 else "| | | |"


def render_final_table(rows: list[dict]) -> str:
    lines = [
        "| layer | choice | version pin | source | notes |",
        "|---|---|---|---|---|",
    ]
    seen = set()
    for r in rows:
        key = (r.get("layer"), r.get("choice"))
        if key in seen:
            continue
        seen.add(key)
        lines.append(
            f"| {r.get('layer', '')} | {r.get('choice', '')} | {r.get('version', '')} | "
            f"{r.get('source', 'extracted')} | confirm in interview |"
        )
    return "\n".join(lines)


def update_tech_doc(repo: str, rows: list[dict], write: bool) -> None:
    path = os.path.join(repo, TECH_DOC)
    if not write or not rows:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        text = open(path, encoding="utf-8").read()
    else:
        tpl = os.path.join(
            os.path.dirname(__file__), "..", "templates", "blueprint", "01-tech-stack.md"
        )
        text = open(tpl, encoding="utf-8").read() if os.path.exists(tpl) else "# Tech stack\n"
    extract_block = render_extract_table(rows)
    final_block = render_final_table(rows)
    if "## Extracted from seed" in text:
        text = re.sub(
            r"(## Extracted from seed[^\n]*\n)(?:.*?\n)(?=## User overrides)",
            r"\1\n" + extract_block + "\n\n",
            text,
            flags=re.S,
        )
    if "## Final stack" in text and "| backend runtime |" in text:
        text = re.sub(
            r"(## Final stack[^\n]*\n\n\| layer \|.*?\n\|[-| ]+\|\n)(?:.*?\n)*?(?=\n<!--|\n## )",
            r"\1" + "\n".join(final_block.splitlines()[2:]) + "\n\n",
            text,
            flags=re.S,
        )
    text = re.sub(r"Status:\s*empty", "Status: draft", text, count=1)
    open(path, "w", encoding="utf-8").write(text)


def first_heading(path: str) -> str:
    try:
        for line in open(path, encoding="utf-8", errors="replace"):
            s = line.strip()
            if s.startswith("#"):
                return s.lstrip("# ").strip()[:80]
    except OSError:
        pass
    return ""


def discover_legacy_docs(repo: str) -> list[dict]:
    """Markdown files that look like stray project docs to be consolidated.

    Excludes the canonical tree, tool folders, and root entry files.
    """
    found: list[dict] = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            abs_p = os.path.join(root, fn)
            rel = os.path.relpath(abs_p, repo).replace(os.sep, "/")
            if rel.startswith(CANONICAL_DOC_PREFIXES):
                continue
            if "/" not in rel and rel in KEEP_ROOT_FILES:
                continue
            found.append({
                "path": rel,
                "topic": first_heading(abs_p),
                "bytes": os.path.getsize(abs_p),
                "status": "pending",  # agent sets: consolidated | kept | dropped
                "consolidated_into": None,
            })
    return found


def archive_legacy(repo: str, write: bool) -> dict:
    """Discover stray docs; with --write, MOVE them under docs/_legacy/ (reversible)
    and write a manifest the blueprint skill consolidates from. Never deletes."""
    docs = discover_legacy_docs(repo)
    manifest = {
        "version": 1,
        "ts": datetime.now(timezone.utc).isoformat(),
        "dest": LEGACY_DEST,
        "action": "archived" if (write and docs) else "scanned",
        "note": "Agent consolidates each into docs/project|stack|<component>, "
                "sets status, then may remove docs/_legacy once status!=pending.",
        "docs": docs,
    }
    if write:
        for d in docs:
            src = os.path.join(repo, d["path"])
            dst = os.path.join(repo, LEGACY_DEST, d["path"])
            if os.path.abspath(src) == os.path.abspath(dst):
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.move(src, dst)
                d["archived_to"] = os.path.relpath(dst, repo).replace(os.sep, "/")
    os.makedirs(os.path.join(repo, ".foundry"), exist_ok=True)
    json.dump(manifest, open(os.path.join(repo, LEGACY_MANIFEST), "w", encoding="utf-8"), indent=2)
    return manifest


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    repo = os.path.abspath(sys.argv[1])
    seed = None
    if "--from" in sys.argv:
        i = sys.argv.index("--from")
        if i + 1 < len(sys.argv):
            seed = os.path.abspath(sys.argv[i + 1])
    write = "--write" in sys.argv

    if "--archive-legacy" in sys.argv:
        man = archive_legacy(repo, write)
        n = len(man["docs"])
        print(f"[OK] legacy docs {man['action']}: {n} → {LEGACY_MANIFEST}")
        if write and n:
            print(f"[OK] moved under {LEGACY_DEST}/ — agent now consolidates per manifest")
        elif not write:
            print("[OK] dry-run — pass --write to move them under docs/_legacy/")
        return 0

    rows = detect_in_dir(repo)
    seed_bp = None
    if seed:
        rows_seed = detect_in_dir(seed)
        # seed rows first, repo rows override same layer+choice
        keys = {(r["layer"], r["choice"]) for r in rows}
        for r in rows_seed:
            if (r["layer"], r["choice"]) not in keys:
                rows.append(r)
        seed_bp = find_blueprint_root(seed)

    out = {
        "version": 1,
        "ts": datetime.now(timezone.utc).isoformat(),
        "repo": repo,
        "seed": seed,
        "seed_blueprint_root": seed_bp,
        "rows": rows,
    }
    os.makedirs(os.path.join(repo, ".foundry"), exist_ok=True)
    json.dump(out, open(os.path.join(repo, EXTRACT_OUT), "w", encoding="utf-8"), indent=2)

    copied = []
    if seed_bp:
        copied = copy_blueprint_seed(seed_bp, repo, write)
    if write:
        update_tech_doc(repo, rows, True)

    print(f"[OK] extracted {len(rows)} tech signals → {EXTRACT_OUT}")
    if seed_bp:
        print(f"[OK] seed blueprint root: {seed_bp}")
    if copied:
        print(f"[OK] copied blueprint files: {', '.join(copied)}")
    if not write:
        print("[OK] dry-run — pass --write to merge into docs/project/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
