#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = REPO_ROOT / "tests"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import update_engineering_ledger  # noqa: E402
from workflow_test_utils import silence_stdio  # noqa: E402


class UpdateEngineeringLedgerTests(unittest.TestCase):
    def test_main_creates_new_ledger(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            output_path = Path(tmp_dir) / "ENGINEERING_LEDGER.md"
            with silence_stdio():
                exit_code = update_engineering_ledger.main(
                    [
                        "--output",
                        str(output_path),
                        "--theme",
                        "Repo engineering memory",
                        "--summary",
                        "Perkelti repo engineering atmintį į tracked ledger.",
                        "--state",
                        "Sukurtas ledger artefaktas.",
                        "--decision",
                        "Repo engineering atmintis laikoma tracked faile.",
                        "--next-step",
                        "Perrašyti dokumentaciją.",
                        "--risk",
                        "Reikia aiškiai atskirti nuo book translation workflow.",
                        "--generated-at",
                        "2026-03-30T16:00:00+03:00",
                        "--branch",
                        "codex/engineering-ledger",
                    ]
                )

            self.assertEqual(exit_code, 0)
            text = output_path.read_text(encoding="utf-8")
            self.assertIn("Theme: Repo engineering memory", text)
            self.assertIn("Branch: codex/engineering-ledger", text)
            self.assertIn("Perkelti repo engineering atmintį į tracked ledger.", text)
            self.assertIn("Sukurtas ledger artefaktas.", text)
            self.assertIn("Repo engineering atmintis laikoma tracked faile.", text)

    def test_completed_notes_are_appended_to_existing_ledger(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            output_path = Path(tmp_dir) / "ENGINEERING_LEDGER.md"
            output_path.write_text(update_engineering_ledger.template_text(), encoding="utf-8")

            with silence_stdio():
                update_engineering_ledger.main(
                    [
                        "--output",
                        str(output_path),
                        "--theme",
                        "Acceptance fixtures",
                        "--completed",
                        "Uždaryta focused fixture banga.",
                        "--generated-at",
                        "2026-03-30T16:10:00+03:00",
                        "--branch",
                        "codex/fixtures",
                    ]
                )
                update_engineering_ledger.main(
                    [
                        "--output",
                        str(output_path),
                        "--theme",
                        "Codex workflow",
                        "--completed",
                        "Atskirtas translation ir repo engineering workflow.",
                        "--generated-at",
                        "2026-03-30T16:20:00+03:00",
                        "--branch",
                        "codex/codex-workflow",
                    ]
                )

            text = output_path.read_text(encoding="utf-8")
            self.assertIn("### 2026-03-30 16:20 | Codex workflow", text)
            self.assertIn("### 2026-03-30 16:10 | Acceptance fixtures", text)
            self.assertIn("Atskirtas translation ir repo engineering workflow.", text)
            self.assertIn("Uždaryta focused fixture banga.", text)


if __name__ == "__main__":
    unittest.main()
