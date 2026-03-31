#!/usr/bin/env python3
from __future__ import annotations

import multiprocessing
import queue
import tempfile
import textwrap
import traceback
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = Path(__file__).resolve().parent
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import build_chapter_pack  # noqa: E402
import mine_term_candidates  # noqa: E402
import workflow_rules as wr  # noqa: E402
from workflow_test_utils import silence_stdio  # noqa: E402


TERM_CANDIDATE_HEADER = "\t".join(wr.TERM_CANDIDATE_FIELDS) + "\n"
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


def refresh_term_candidates_in_process(
    book_root: str,
    slug: str,
    barrier: multiprocessing.synchronize.Barrier,
    errors: multiprocessing.queues.Queue[str],
) -> None:
    try:
        barrier.wait(timeout=10)
        mine_term_candidates.refresh_term_candidates_for_chapter(slug, book_root=book_root)
    except BaseException:
        errors.put(traceback.format_exc())
        raise


class TermCandidateWorkflowTests(unittest.TestCase):
    maxDiff = None

    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_book_root(self, base_dir: Path, name: str = "candidate-book") -> Path:
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
        self.write(book_root / "README.md", "# Candidate Book\n")
        self.write(book_root / "term_candidates.tsv", TERM_CANDIDATE_HEADER)
        self.write(book_root / "gold_sections" / "index.tsv", "example_id\tsource_chapter\tblock_id\tblock_type\ttags\tpath\tnotes\n")
        return book_root

    def minimal_research(self, slug: str, title: str, risky_terms: list[str]) -> str:
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

    def test_miner_collects_risky_terms_and_unknown_source_acronyms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-test-chapter"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                "# Test chapter\n\nSentinel perfusion window is described here.\n"
                "Zonal Zero Emergency Management System (ZZEMS) is also referenced.\n"
                "BrandX Tool remains original-context only.\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(slug, "Test chapter", ["Sentinel perfusion window", "BrandX Tool"]),
            )
            self.write(
                book_root / "localization_overrides.local.tsv",
                "source_term\tjurisdiction\treplacement_mode\tlocal_lt\teu_fallback\tscope\treason\tsource_ref\tnotes\n"
                "BrandX Tool\tuk\toriginal_context_callout\t\t\tall\tOriginal-context only\tlocal\tTest\n",
            )

            rows = mine_term_candidates.refresh_term_candidates_for_chapter(slug, book_root=book_root)

            self.assertEqual([row["source_term"] for row in rows], ["ZZEMS", "Sentinel perfusion window"])
            acronym_row = next(row for row in rows if row["candidate_kind"] == "acronym")
            term_row = next(row for row in rows if row["candidate_kind"] == "term")
            self.assertEqual(acronym_row["source_expansion"], "Zonal Zero Emergency Management System")
            self.assertIn("source tekste kaip santrumpa", acronym_row["reason"])
            self.assertIn("Rizikingi terminai", term_row["reason"])

    def test_rerun_preserves_manual_candidate_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-test-chapter"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                "# Test chapter\n\nSentinel perfusion window is described here.\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(slug, "Test chapter", ["Sentinel perfusion window"]),
            )

            mine_term_candidates.refresh_term_candidates_for_chapter(slug, book_root=book_root)
            rows = wr.read_tsv(book_root / "term_candidates.tsv")
            rows[0]["proposed_lt"] = "sarginis perfuzijos langas"
            rows[0]["status"] = "approved_local"
            rows[0]["notes"] = "Patvirtinta ranka"
            wr.write_tsv(book_root / "term_candidates.tsv", wr.TERM_CANDIDATE_FIELDS, rows)

            rerun_rows = mine_term_candidates.refresh_term_candidates_for_chapter(slug, book_root=book_root)

            self.assertEqual(len(rerun_rows), 1)
            self.assertEqual(rerun_rows[0]["proposed_lt"], "sarginis perfuzijos langas")
            self.assertEqual(rerun_rows[0]["status"], "approved_local")
            self.assertEqual(rerun_rows[0]["notes"], "Patvirtinta ranka")

    def test_miner_skips_research_note_items_that_are_not_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-test-chapter"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                "# Test chapter\n\nThis section discusses respectful terminology.\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(
                    slug,
                    "Test chapter",
                    ["woman / women / mother vartosena ginekologinių ir nėštumo būklių kontekste"],
                ),
            )

            rows = mine_term_candidates.refresh_term_candidates_for_chapter(slug, book_root=book_root)

            self.assertEqual(rows, [])

    def test_miner_skips_all_caps_person_name_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-test-chapter"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                "# Test chapter\n\nDr ALISON WALKER\n\nCATHRYN JAMES\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(slug, "Test chapter", []),
            )

            rows = mine_term_candidates.refresh_term_candidates_for_chapter(slug, book_root=book_root)

            self.assertEqual(rows, [])

    def test_build_chapter_pack_updates_and_embeds_term_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug = "001-test-chapter"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                "# Test chapter\n\nSentinel perfusion window is described here.\n",
            )
            self.write(
                book_root / "research" / f"{slug}.md",
                self.minimal_research(slug, "Test chapter", ["Sentinel perfusion window"]),
            )
            self.write(book_root / "lt" / "chapters" / f"{slug}.md", "# Test chapter\n")

            with (
                patch.object(build_chapter_pack, "validate_chapter_inventory_or_raise", lambda *_: None),
                patch.object(build_chapter_pack, "validate_localization_readiness_or_raise", lambda *_: None),
                patch.object(build_chapter_pack, "validate_term_readiness_or_raise", lambda *_args, **_kwargs: None),
                patch.object(
                    build_chapter_pack,
                    "parse_args",
                    return_value=Namespace(book_root=str(book_root), chapter=slug, out=None),
                ),
            ):
                with silence_stdio():
                    result = build_chapter_pack.main()

            self.assertEqual(result, 0)
            pack_path = book_root / "chapter_packs" / f"{slug}.yaml"
            pack = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
            self.assertEqual(pack["term_candidates_path"], "term_candidates.tsv")
            self.assertEqual(len(pack["term_candidates"]), 1)
            self.assertEqual(pack["term_candidates"][0]["source_term"], "Sentinel perfusion window")
            candidate_rows = wr.read_tsv(book_root / "term_candidates.tsv")
            self.assertEqual(len(candidate_rows), 1)
            self.assertEqual(candidate_rows[0]["candidate_kind"], "term")

    def test_process_parallel_refresh_preserves_both_chapters_and_avoids_nul_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir))
            slug_a = "001-test-chapter"
            slug_b = "002-second-test-chapter"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug_a}.md",
                "# Test chapter\n\nSentinel perfusion window is described here.\n",
            )
            self.write(
                book_root / "source" / "chapters-en" / f"{slug_b}.md",
                "# Second test chapter\n\nZonal perfusion reserve is described here.\n",
            )
            self.write(
                book_root / "research" / f"{slug_a}.md",
                self.minimal_research(slug_a, "Test chapter", ["Sentinel perfusion window"]),
            )
            self.write(
                book_root / "research" / f"{slug_b}.md",
                self.minimal_research(slug_b, "Second test chapter", ["Zonal perfusion reserve"]),
            )

            ctx = multiprocessing.get_context("spawn")
            barrier = ctx.Barrier(2)
            errors = ctx.Queue()
            processes = [
                ctx.Process(target=refresh_term_candidates_in_process, args=(str(book_root), slug_a, barrier, errors)),
                ctx.Process(target=refresh_term_candidates_in_process, args=(str(book_root), slug_b, barrier, errors)),
            ]
            for process in processes:
                process.start()
            for process in processes:
                process.join(timeout=20)
            for process in processes:
                if process.is_alive():
                    process.terminate()
                    process.join(timeout=5)
                    self.fail(f"Parallel refresh worker did not finish cleanly: pid={process.pid}")

            error_messages: list[str] = []
            while True:
                try:
                    error_messages.append(errors.get_nowait())
                except queue.Empty:
                    break
            if error_messages:
                self.fail("\n\n".join(error_messages))

            for process in processes:
                self.assertEqual(process.exitcode, 0)

            data = (book_root / "term_candidates.tsv").read_bytes()
            self.assertNotIn(b"\x00", data)

            rows = wr.read_tsv(book_root / "term_candidates.tsv")
            self.assertEqual({row["chapter_slug"] for row in rows}, {slug_a, slug_b})
            self.assertEqual(
                {row["source_term"] for row in rows},
                {"Sentinel perfusion window", "Zonal perfusion reserve"},
            )


if __name__ == "__main__":
    unittest.main()
