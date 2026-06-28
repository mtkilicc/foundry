"""Shared config for foundry scripts. Stdlib only."""
from __future__ import annotations

import json
import os
import re

CANONICAL_ROOT = "agent/skills"
CONFIG_PATH = ".foundry/config.json"
TOOLING_PATH = "docs/stack/agent-tooling.md"

DEFAULT_CONFIG = {
    "version": 1,
    "canonical_skills_root": CANONICAL_ROOT,
    "post_job": {
        "enabled": True,
        "run_drift_check": True,
        "enqueue_proposals": True,
    },
    "render_targets": {
        "claude-code": {"enabled": False, "skills_root": ".claude/skills"},
        "cursor": {
            "enabled": False,
            "skills_root": ".cursor/skills",
            "routing_rule": ".cursor/rules/00-routing.mdc",
        },
        "generic": {"enabled": True},
    },
    "drift": {
        "auto_reject_kinds": ["doc_status_only", "already_covered"],
        "needs_review_kinds": [
            "code_map_gap",
            "trigger_gap",
            "orchestrator_row",
            "new_leaf_candidate",
        ],
    },
}


def load_config(repo: str) -> dict:
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    path = os.path.join(repo, CONFIG_PATH)
    if os.path.exists(path):
        try:
            user = json.load(open(path, encoding="utf-8"))
            _deep_merge(cfg, user)
        except (json.JSONDecodeError, OSError):
            pass
    _merge_tooling_md(repo, cfg)
    return cfg


def _deep_merge(base: dict, override: dict) -> None:
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def _merge_tooling_md(repo: str, cfg: dict) -> None:
    path = os.path.join(repo, TOOLING_PATH)
    if not os.path.exists(path):
        return
    text = open(path, encoding="utf-8").read()
    in_targets = False
    for line in text.splitlines():
        if "## Render targets" in line:
            in_targets = True
            continue
        if in_targets and line.startswith("## "):
            break
        if not in_targets or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("target", "---", ":---"):
            continue
        key = cells[0].lower().replace(" ", "-")
        if key.startswith("claude"):
            key = "claude-code"
        enabled = cells[1].lower() in ("yes", "true", "1")
        if key in cfg.get("render_targets", {}):
            cfg["render_targets"][key]["enabled"] = enabled
    m = re.search(r"\|\s*profile\s*\|\s*([^|]+)\|", text)
    if m:
        prof = m.group(1).strip().lower()
        if prof in ("multi-tool", "claude-code"):
            cfg["render_targets"]["claude-code"]["enabled"] = True
        if prof in ("multi-tool", "cursor"):
            cfg["render_targets"]["cursor"]["enabled"] = True


def enabled_render_targets(cfg: dict) -> list[str]:
    return [
        k
        for k, v in cfg.get("render_targets", {}).items()
        if v.get("enabled")
    ]
