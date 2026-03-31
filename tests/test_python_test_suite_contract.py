#!/usr/bin/env python3
from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SUITE_MANIFEST_PATH = REPO_ROOT / "tests" / "python_test_suite.toml"
TESTS_DIR = REPO_ROOT / "tests"


class PythonTestSuiteContractTests(unittest.TestCase):
    maxDiff = None

    def load_suite_manifest(self) -> dict[str, list[str]]:
        with SUITE_MANIFEST_PATH.open("rb") as handle:
            data = tomllib.load(handle)
        return {
            "required": list(data.get("required", [])),
            "non_required_tracked": list(data.get("non_required_tracked", [])),
        }

    def test_tracked_test_modules_are_fully_classified_once(self) -> None:
        suite = self.load_suite_manifest()
        required = suite["required"]
        non_required = suite["non_required_tracked"]

        self.assertEqual(len(required), len(set(required)), msg="`required` contains duplicate modules.")
        self.assertEqual(
            len(non_required),
            len(set(non_required)),
            msg="`non_required_tracked` contains duplicate modules.",
        )

        required_set = set(required)
        non_required_set = set(non_required)
        overlap = sorted(required_set & non_required_set)
        self.assertEqual(overlap, [], msg=f"Modules classified twice: {overlap}")

        tracked = {
            f"tests.{path.stem}"
            for path in TESTS_DIR.glob("test_*.py")
        }
        classified = required_set | non_required_set
        self.assertEqual(
            sorted(tracked - classified),
            [],
            msg=f"Tracked tests missing classification: {sorted(tracked - classified)}",
        )
        self.assertEqual(
            sorted(classified - tracked),
            [],
            msg=f"Suite manifest references missing test modules: {sorted(classified - tracked)}",
        )


if __name__ == "__main__":
    unittest.main()
