#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import book_workflow_support as bws  # noqa: E402
import mine_term_candidates  # noqa: E402
import validate_term_readiness  # noqa: E402


TERM_CANDIDATE_HEADER = "\t".join(bws.TERM_CANDIDATE_FIELDS) + "\n"
TERMBASE_HEADER = "en\tlt\tnote\tstatus\tbanned_lt\tfirst_use_policy\tsection_scope\texample_lt\tlocal_override_tag\n"
AUDIT_ROWS = [
    "| Sritis | Statusas | Pastaba |",
    "| --- | --- | --- |",
    "| terminija | ok |  |",
    "| kolokacijos | ok |  |",
    "| gramatika | ok |  |",
    "| semantika | ok |  |",
    "| norminė logika | ok |  |",
    "| atviros abejonės | ok |  |",
]


class TermReadinessGateTests(unittest.TestCase):
    maxDiff = None

    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_book_root(self, base_dir: Path, name: str = "term-ready-book") -> Path:
        book_root = base_dir / name
        for rel_dir in (
            "source/chapters-en",
            "source/index",
            "lt/chapters",
            "lt/figures",
            "research",
            "chapter_packs",
            "adjudication_packs",
            "review_deltas",
            "regression_examples",
            "archive",
            "gold_sections",
        ):
            (book_root / rel_dir).mkdir(parents=True, exist_ok=True)
        self.write(book_root / "README.md", "# Term readiness book\n")
        self.write(book_root / "term_candidates.tsv", TERM_CANDIDATE_HEADER)
        self.write(book_root / "gold_sections" / "index.tsv", "example_id\tsource_chapter\tblock_id\tblock_type\ttags\tpath\tnotes\n")
        return book_root

    def minimal_research(self, slug: str, title: str, risky_terms: list[str] | None = None) -> str:
        risky_terms = risky_terms or []
        risky_block = "\n".join(f"- {item}" for item in risky_terms) if risky_terms else "- "
        lines = [
            f"# {int(slug.split('-', 1)[0])} skyrius. {title}",
            "",
            "- Puslapiai: 1-2",
            f"- Angliškas pagalbinis failas: source/chapters-en/{slug}.md",
            f"- Lietuviškas failas: lt/chapters/{slug}.md",
            "",
            "## Source inventorius",
            "",
            "### Poskyriai",
            "",
            f"- {title}",
            "",
            "### Lentelės",
            "",
            "- Kol kas neužfiksuota",
            "",
            "### Paveikslai / schemos / algoritmai",
            "",
            "- Kol kas neužfiksuota",
            "",
            "### Rėmeliai / papildomi blokai",
            "",
            "- Kol kas neužfiksuota",
            "",
            "## Rizikingi terminai",
            "",
            risky_block,
            "",
            "## Jurisdikcijos ir rinkos signalai",
            "",
            "| Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |",
            "| --- | --- | --- | --- | --- |",
            "",
            "## LT/EU pakeitimo sprendimai",
            "",
            "| Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |",
            "| --- | --- | --- | --- | --- | --- |",
            "",
            "## Vaistų ir dozių LT/EU šaltinių bazė",
            "",
            "| Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |",
            "| --- | --- | --- | --- | --- |",
            "",
            "## Norminių teiginių matrica",
            "",
            "| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            "",
            "## Struktūrinių blokų lokalizacijos sprendimai",
            "",
            "| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |",
            "| --- | --- | --- | --- | --- | --- |",
            "",
            "## Finalus agento auditas",
            "",
            *AUDIT_ROWS,
            "",
        ]
        return "\n".join(lines)

    def test_miner_collects_high_value_guideline_title_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-sentinel-life-support"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                textwrap.dedent(
                    """
                    | Col 1 | Col 2 | Col 3 |
                    | --- | --- | --- |
                    | Resuscitation |  |  |
                    | Guideline Title | Last Update | Notes |
                    | Sentinel Life Support in Adults | March 2026 | Revised and updated. |
                    """
                ).strip()
                + "\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(slug, "Sentinel update"),
            )

            rows = mine_term_candidates.refresh_term_candidates_for_chapter(slug, book_root=book_root)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["source_term"], "Sentinel Life Support")
            self.assertEqual(rows[0]["candidate_kind"], "term")
            self.assertEqual(rows[0]["candidate_origin"], "source_guideline_title")

    def test_validate_term_readiness_blocks_unresolved_high_risk_term(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-sentinel-life-support"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                textwrap.dedent(
                    """
                    | Col 1 | Col 2 | Col 3 |
                    | --- | --- | --- |
                    | Resuscitation |  |  |
                    | Guideline Title | Last Update | Notes |
                    | Sentinel Life Support in Adults | March 2026 | Revised and updated. |
                    """
                ).strip()
                + "\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(slug, "Sentinel update"),
            )

            errors = validate_term_readiness.validate_term_readiness(slug, book_root=book_root)

            self.assertEqual(len(errors), 1)
            self.assertIn("Sentinel Life Support", errors[0])
            self.assertIn("term_candidates.tsv", errors[0])

    def test_validate_term_readiness_passes_after_local_termbase_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-sentinel-life-support"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                textwrap.dedent(
                    """
                    | Col 1 | Col 2 | Col 3 |
                    | --- | --- | --- |
                    | Resuscitation |  |  |
                    | Guideline Title | Last Update | Notes |
                    | Sentinel Life Support in Adults | March 2026 | Revised and updated. |
                    """
                ).strip()
                + "\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(slug, "Sentinel update"),
            )
            self.write(
                book_root / "termbase.local.tsv",
                TERMBASE_HEADER
                + "Sentinel Life Support\tsarginis gaivinimas\tTest\tpreferred\t\tmust_expand_first\tall\tsarginis gaivinimas\t\n",
            )

            errors = validate_term_readiness.validate_term_readiness(slug, book_root=book_root)

            self.assertEqual(errors, [])

    def test_validate_term_readiness_allows_explicitly_rejected_context_item(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-org-context"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                "AACE remains original context only.\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(slug, "Org context", ["AACE"]),
            )

            mine_term_candidates.refresh_term_candidates_for_chapter(slug, book_root=book_root)
            rows = bws.read_tsv(book_root / "term_candidates.tsv")
            rows[0]["status"] = "rejected"
            rows[0]["notes"] = "Originalo institucinė santrumpa."
            bws.write_tsv(book_root / "term_candidates.tsv", bws.TERM_CANDIDATE_FIELDS, rows)

            errors = validate_term_readiness.validate_term_readiness(slug, book_root=book_root)

            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
