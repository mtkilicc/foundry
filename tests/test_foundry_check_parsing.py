"""Regression lock for the [FAIL]-slicing bug in scripts/foundry_check.py.

The status-tag parser used fixed-width slicing sized for the 4-char "[OK]"
tag; the 6-char "[FAIL]" tag was mis-read as "FA", so no failure ever matched
BAD and ``foundry_check.py identity|blueprint`` (and those sub-blocks of
``all``) ALWAYS exited 0 — even on a repo where every underlying check fails.

These tests drive the real script as a subprocess against an empty repo
(where identity/blueprint genuinely fail) and pin the nonzero exit codes.
Run: python3 -m unittest discover -s tests
"""

import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts",
    "foundry_check.py",
)


def _run(mode: str, repo: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, SCRIPT, mode, repo],
        capture_output=True,
        text=True,
    )


class TestFailTagParsing(unittest.TestCase):
    def test_identity_fails_on_empty_repo(self) -> None:
        with tempfile.TemporaryDirectory() as repo:
            r = _run("identity", repo)
            self.assertNotEqual(
                r.returncode, 0,
                "identity must exit nonzero on an empty repo "
                f"(stdout: {r.stdout[-400:]!r})",
            )

    def test_blueprint_fails_on_empty_repo(self) -> None:
        with tempfile.TemporaryDirectory() as repo:
            r = _run("blueprint", repo)
            self.assertNotEqual(
                r.returncode, 0,
                "blueprint must exit nonzero on an empty repo "
                f"(stdout: {r.stdout[-400:]!r})",
            )

    def test_fail_lines_render_with_full_tag(self) -> None:
        # The mis-slice also mangled the report text: "FA" tags and messages
        # with a leading "] ". A correct parse renders "[FAIL] <msg>" intact.
        with tempfile.TemporaryDirectory() as repo:
            r = _run("identity", repo)
            self.assertNotIn("[FA]", r.stdout)
            self.assertNotIn("] ]", r.stdout)


if __name__ == "__main__":
    unittest.main()
