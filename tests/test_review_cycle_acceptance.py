#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = Path(__file__).resolve().parent
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import workflow_rules as wr  # noqa: E402
from workflow_test_utils import copy_fixture, run_script, seed_canonical_artifacts  # noqa: E402


REVIEW_DELTA_FIELDS = [
    "block_id",
    "defect_class",
    "bad_form",
    "fixed_form",
    "severity",
    "promote_target",
    "notes",
]


class ReviewCycleAcceptanceTests(unittest.TestCase):
    maxDiff = None

    def test_review_delta_cycle_routes_candidates_to_expected_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_fixture(Path(tmp_dir), "review_book")
            slug = seed_canonical_artifacts(book_root)
            pack_path = book_root / "chapter_packs" / f"{slug}.yaml"
            before_path = book_root / "review_inputs" / f"{slug}-before.md"
            after_path = book_root / "review_inputs" / f"{slug}-after.md"
            delta_path = book_root / "review_deltas" / f"{slug}.tsv"

            mine_result = run_script(
                "mine_review_deltas.py",
                "--chapter-pack",
                str(pack_path),
                "--before",
                str(before_path),
                "--after",
                str(after_path),
                "--out",
                str(delta_path),
            )

            self.assertEqual(mine_result.returncode, 0, msg=mine_result.stdout + mine_result.stderr)
            rows = wr.read_tsv(delta_path)
            self.assertEqual([row["block_id"] for row in rows], ["narrative-01-flow", "narrative-02-market", "narrative-03-meaning"])

            enriched_rows = [
                {
                    **rows[0],
                    "defect_class": "collocation",
                    "severity": "medium",
                    "notes": "Stabilus LT žodžių junginys, tinkamas gold phrase taisyklei.",
                },
                {
                    **rows[1],
                    "defect_class": "market_drift",
                    "severity": "high",
                    "notes": "Rinkos etiketė turi būti generinama į LT kompensavimo kontekstą.",
                },
                {
                    **rows[2],
                    "defect_class": "semantic_drift",
                    "severity": "high",
                    "notes": "Pavyzdys regression rinkiniui, nes klaida keičia klinikinę prasmę.",
                },
            ]
            wr.write_tsv(delta_path, REVIEW_DELTA_FIELDS, enriched_rows)

            promote_result = run_script(
                "promote_rules.py",
                "--book-root",
                str(book_root),
                "--emit-regression",
                slug,
            )

            output = promote_result.stdout + promote_result.stderr
            self.assertEqual(promote_result.returncode, 0, msg=output)
            self.assertIn("## Candidates for `shared/prose/gold_phrases.tsv`", output)
            self.assertIn("collocation\tBloga kolokacija.\tTiksli kolokacija.", output)
            self.assertIn("## Candidates for `shared/localization/localization_overrides.tsv`", output)
            self.assertIn("Drug Tariff paliekamas kaip vietinis standartas.\tmixed-anglosphere\tgenericize", output)
            self.assertIn("## Candidates for `regression_examples`", output)
            self.assertIn("\"defect_class\": \"semantic_drift\"", output)
            self.assertIn("\"chapter_slug\": \"001-review\"", output)


if __name__ == "__main__":
    unittest.main()
