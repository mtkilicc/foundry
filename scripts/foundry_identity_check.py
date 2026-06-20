#!/usr/bin/env python3
"""foundry_identity_check.py — verify project-unique identity docs and rules.

Ensures design/backend identity docs reference real paths in THIS repo and
do not contain forbidden cross-project boilerplate.

Usage:
  python scripts/foundry_identity_check.py <repo_root>

Stdlib only.
"""
from __future__ import annotations

import json
import os
import re
import sys

FP_PATH = ".foundry/project-fingerprint.json"
DESIGN_DOC = "docs/stack/design-identity.md"
BACKEND_DOC = "docs/stack/backend-identity.md"

FORBIDDEN_DEFAULTS = [
    r"\bAppShell\b",
    r"\bPriceCard\b",
    r"\bPriceTable\b",
    r"generic shadcn",
    r"default dashboard template",
    r"copied from agriprix",
    r"copied from another project",
]

PATH_IN_DOC = re.compile(
    r"`((?:frontend|backend)/[^`]+?\.(?:tsx?|py|md))`"
    r"|`((?:frontend|backend)/[^`]+?/)`"
)


def load_fingerprint(repo: str) -> dict:
    p = os.path.join(repo, FP_PATH)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def check_doc(repo: str, rel: str, label: str) -> list[tuple[str, str]]:
    results = []
    path = os.path.join(repo, rel)
    if not os.path.exists(path):
        results.append(("FAIL", f"missing {label}: {rel}"))
        return results
    text = open(path, encoding="utf-8").read()
    if "{{" in text or "PROJECT_NAME" in text:
        results.append(("FAIL", f"{label} still has template placeholders"))
    fp = load_fingerprint(repo)
    for phrase in fp.get("forbidden_cross_project", []):
        if phrase.lower() in text.lower():
            results.append(("FAIL", f"{label} contains forbidden cross-project phrase: {phrase!r}"))
    for pat in FORBIDDEN_DEFAULTS:
        if not re.search(pat, text, re.I):
            continue
        if pat == r"\bAppShell\b":
            shell = fp.get("frontend", {}).get("shell_component", "")
            if shell and "AppShell" not in shell and "AppShell" in text:
                results.append(("FAIL", f"{label} mentions AppShell but project shell is {shell!r}"))
        elif pat in (r"\bPriceCard\b", r"\bPriceTable\b"):
            if re.search(pat, text):
                results.append(("FAIL", f"{label} contains example-project component {pat}"))
        elif pat == r"generic shadcn" and "do NOT default" not in text:
            results.append(("FAIL", f"{label} may be generic shadcn boilerplate"))
    paths_found = 0
    paths_ok = 0
    for m in PATH_IN_DOC.finditer(text):
        p = m.group(1) or m.group(2)
        if not p or "{{" in p:
            continue
        paths_found += 1
        full = os.path.join(repo, p.rstrip("/"))
        if os.path.exists(full):
            paths_ok += 1
        else:
            results.append(("FAIL", f"{label} references missing path: {p}"))
    if paths_found:
        results.append(("OK", f"{label}: {paths_ok}/{paths_found} anchored paths exist"))
    else:
        results.append(("FAIL", f"{label}: no code paths anchored — run project-talent mine"))
    return results


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    repo = os.path.abspath(sys.argv[1])
    results = []
    if not os.path.exists(os.path.join(repo, FP_PATH)):
        results.append(("FAIL", f"missing {FP_PATH} — run skills-gen/project-talent"))
    else:
        results.append(("OK", f"found {FP_PATH}"))
    results.extend(check_doc(repo, DESIGN_DOC, "design-identity"))
    results.extend(check_doc(repo, BACKEND_DOC, "backend-identity"))
    fails = [r for r in results if r[0] == "FAIL"]
    for s, msg in results:
        print(f"[{s}] {msg}")
    print(f"\n{len(results) - len(fails)} passed, {len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
