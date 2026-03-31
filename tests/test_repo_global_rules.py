#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import workflow_book_template as wbt  # noqa: E402
import workflow_policy as wp  # noqa: E402
import workflow_rules as wr  # noqa: E402


TERMBASE_HEADER = "en\tlt\tnote\tstatus\tbanned_lt\tfirst_use_policy\tsection_scope\texample_lt\tlocal_override_tag\n"
ACRONYM_HEADER = "acronym\tlt\ten\tpolicy\tnotes\tmust_expand_first\tallowed_in_headings\tambiguous_context\tpreferred_lt_context\n"
GOLD_PHRASE_HEADER = "category\tbad_en_shaped_lt\tpreferred_lt\tnotes\tsource_chapter\n"
CALQUE_HEADER = "match_type\tbanned\tpreferred\treason\tcategory\tseverity\tpromoted_from\tnotes\n"
DISALLOWED_PHRASE_HEADER = "match_type\tbanned\tpreferred\treason\n"
LOCALIZATION_OVERRIDE_HEADER = "source_term\tjurisdiction\treplacement_mode\tlocal_lt\teu_fallback\tscope\treason\tsource_ref\tnotes\n"
LOCALIZATION_SIGNAL_HEADER = "source_term\tjurisdiction\tsignal_type\tmatch_mode\tpattern\tnotes\n"
GOLD_SECTION_INDEX_HEADER = "example_id\tsource_chapter\tblock_id\tblock_type\ttags\tpath\tnotes\n"


class RepoGlobalRulesTests(unittest.TestCase):
    maxDiff = None

    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_book_root(self, base_dir: Path, name: str = "book") -> Path:
        book_root = base_dir / name
        for rel_dir in (
            "source/chapters-en",
            "source/pdf",
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
        self.write(book_root / "README.md", "# Test Book\n")
        wbt.write_book_metadata(book_root, wbt.CanonicalSource(kind="pdf", name="SOURCE.pdf"))
        return book_root

    def run_script(self, script_name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / script_name), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_termbase_local_override_wins_by_en(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir), "override-book")
            self.write(
                book_root / "termbase.local.tsv",
                TERMBASE_HEADER
                + "Advanced life support\tvietinis specializuotas gaivinimas\tLocal override\tpreferred\tpažangus gaivinimas\tmust_expand_first\tall\tvietinis specializuotas gaivinimas (ALS)\tunit-test\n",
            )

            rows = wp.load_termbase_rows(book_root)
            als_row = next(row for row in rows if row["en"] == "Advanced life support")

            self.assertEqual(als_row["lt"], "vietinis specializuotas gaivinimas")
            self.assertEqual(als_row["local_override_tag"], "unit-test")

    def test_acronym_local_override_wins_by_acronym(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir), "override-book")
            self.write(
                book_root / "acronyms.local.tsv",
                ACRONYM_HEADER
                + "ALS\tvietinis ALS terminas\tAdvanced life support\tlt-first\tLocal override\tyes\tno\t\tvietinis ALS terminas\n",
            )

            rows = wp.load_acronym_rows(book_root)
            als_row = next(row for row in rows if row["acronym"] == "ALS")

            self.assertEqual(als_row["lt"], "vietinis ALS terminas")
            self.assertEqual(als_row["notes"], "Local override")

    def test_merge_appended_rows_dedupes_and_appends(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            shared_rows = tmp_path / "shared.tsv"
            local_rows = tmp_path / "local.tsv"
            self.write(
                shared_rows,
                CALQUE_HEADER
                + "phrase\teskaluoti pagalbą\tkviesti papildomą pagalbą\tShared rule\tphrase\thigh\tshared\t\n",
            )
            self.write(
                local_rows,
                CALQUE_HEADER
                + "phrase\teskaluoti pagalbą\tkviesti papildomą pagalbą\tShared rule\tphrase\thigh\tshared\t\n"
                + "phrase\tvykdyti stebėjimą\tstebėti\tLocal rule\tphrase\tmedium\tlocal\t\n",
            )

            rows = wr.merge_appended_rows([shared_rows, local_rows])

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["banned"], "eskaluoti pagalbą")
            self.assertEqual(rows[1]["banned"], "vykdyti stebėjimą")

    def test_gold_sections_local_example_replaces_shared_example_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            shared_dir = tmp_path / "shared-gold"
            local_book_root = self.make_book_root(tmp_path, "gold-book")
            shared_dir.mkdir(parents=True, exist_ok=True)

            self.write(
                shared_dir / "index.tsv",
                GOLD_SECTION_INDEX_HEADER + "example-1\t001\tblock-1\tnarrative\tshock\tshared-example.md\tshared\n",
            )
            self.write(shared_dir / "shared-example.md", "Shared example text\n")
            self.write(
                local_book_root / "gold_sections" / "index.tsv",
                GOLD_SECTION_INDEX_HEADER + "example-1\t001\tblock-1\tnarrative\tshock\tlocal-example.md\tlocal\n",
            )
            self.write(local_book_root / "gold_sections" / "local-example.md", "Local example text\n")

            with patch.object(
                wp,
                "gold_section_index_sources",
                return_value=[
                    (shared_dir / "index.tsv", shared_dir),
                    (local_book_root / "gold_sections" / "index.tsv", local_book_root / "gold_sections"),
                ],
            ):
                rows = wp.load_gold_section_examples(local_book_root)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["example_id"], "example-1")
            self.assertEqual(rows[0]["text"], "Local example text")

    def test_shared_only_sources_ignore_book_legacy_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir), "shared-only-book")
            self.write(
                book_root / "clinical_policy_markers.tsv",
                "topic\tmatch_mode\tpattern\tnotes\ncustom\tliteral\tcustom\tlegacy book file\n",
            )
            self.write(
                book_root / "lt_source_map.tsv",
                "domain\tprimary_lt_sources\tsecondary_lt_sources\teu_fallback\tuse_for\tnotes\ncustom\tX\tY\tZ\tQ\tlegacy book file\n",
            )

            marker_topics = {row["topic"] for row in wp.load_clinical_policy_markers(book_root)}
            source_domains = {row["domain"] for row in wp.load_lt_source_map(book_root)}

            self.assertNotIn("custom", marker_topics)
            self.assertNotIn("custom", source_domains)

    def test_two_books_without_local_overrides_share_same_als_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            book_a = self.make_book_root(base, "book-a")
            book_b = self.make_book_root(base, "book-b")

            term_a = next(row for row in wp.load_termbase_rows(book_a) if row["en"] == "Advanced life support")
            term_b = next(row for row in wp.load_termbase_rows(book_b) if row["en"] == "Advanced life support")
            acronym_a = next(row for row in wp.load_acronym_rows(book_a) if row["acronym"] == "ALS")
            acronym_b = next(row for row in wp.load_acronym_rows(book_b) if row["acronym"] == "ALS")

            self.assertEqual(term_a["lt"], "specializuotas gaivinimas")
            self.assertEqual(term_a, term_b)
            self.assertEqual(acronym_a["lt"], "specializuotas gaivinimas")
            self.assertEqual(acronym_a, acronym_b)

    def test_terminology_guard_enforces_shared_als_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir), "terminology-book")
            chapter_path = book_root / "lt" / "chapters" / "001-test.md"
            self.write(
                chapter_path,
                "# ALS\n\nPažangus gaivinimas turi būti pradėtas nedelsiant.\n",
            )

            result = self.run_script("terminology_guard.py", "--book-root", str(book_root), str(chapter_path))

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("pažangus gaivinimas", result.stdout)
            self.assertIn("specializuotas gaivinimas", result.stdout)

    def test_prose_guard_uses_shared_and_local_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir), "prose-book")
            chapter_path = book_root / "lt" / "chapters" / "001-test.md"
            self.write(
                book_root / "disallowed_phrases.local.tsv",
                DISALLOWED_PHRASE_HEADER + "phrase\tvykdyti lokalų bandymą\tatlikti lokalų bandymą\tLocal phrase test\n",
            )
            self.write(
                chapter_path,
                "Reikia eskaluoti pagalbą ir vykdyti lokalų bandymą.\n",
            )

            result = self.run_script("prose_guard.py", "--book-root", str(book_root), str(chapter_path))

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("eskaluoti pagalbą", result.stdout)
            self.assertIn("vykdyti lokalų bandymą", result.stdout)

    def test_validate_localization_readiness_uses_local_signal_and_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir), "localization-book")
            slug = "001-test"
            self.write(
                book_root / "source" / "chapters-en" / f"{slug}.md",
                "# Test Chapter\n\nThis section references Custom UK Tool for orientation only.\n",
            )
            self.write(
                book_root / "localization_signals.local.tsv",
                LOCALIZATION_SIGNAL_HEADER + "Custom UK Tool\tuk\treference tool\tliteral\tCustom UK Tool\tLocal signal\n",
            )
            self.write(
                book_root / "localization_overrides.local.tsv",
                LOCALIZATION_OVERRIDE_HEADER
                + "Custom UK Tool\tuk\treplace_lt\tvietinis LT terminas\t\tall\tLocal override\tlocal-source\tTest note\n",
            )
            research_text = textwrap.dedent(
                """
                # Test Chapter

                - Puslapiai: 1-2
                - PDF: test.pdf
                - Angliškas pagalbinis failas: source/chapters-en/001-test.md
                - Lietuviškas failas: lt/chapters/001-test.md

                ## LT-source branduolio taikymas

                | Sritis | Pagrindinis LT-source kelias | Konkretus LT šaltinis | ES fallback | Pastaba |
                | --- | --- | --- | --- | --- |
                | terminija | terminija_ir_kalbos_forma | VLKK |  | Test note |

                ## Jurisdikcijos ir rinkos signalai

                | Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |
                | --- | --- | --- | --- | --- |
                | Custom UK Tool | uk | reference tool | source intro | Local signal |

                ## LT/EU pakeitimo sprendimai

                | Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |
                | --- | --- | --- | --- | --- | --- |
                | Custom UK Tool | replace_lt | LT | vietinis LT terminas | local-source | Local override |

                ## Vaistų ir dozių LT/EU šaltinių bazė

                | Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |
                | --- | --- | --- | --- | --- |

                ## Norminių teiginių matrica

                | claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
                | --- | --- | --- | --- | --- | --- | --- | --- | --- |

                ## Struktūrinių blokų lokalizacijos sprendimai

                | block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |
                | --- | --- | --- | --- | --- | --- |

                ## Neperkeliamas originalo turinys

                - Nėra.
                """
            ).strip() + "\n"
            self.write(book_root / "research" / f"{slug}.md", research_text)

            result = self.run_script("validate_localization_readiness.py", "--book-root", str(book_root), slug)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("Localization readiness passed", result.stdout)

    def test_promote_rules_emits_shared_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir), "promotion-book")
            slug = "001-test"
            self.write(
                book_root / "review_deltas" / f"{slug}.tsv",
                "block_id\tdefect_class\tbad_form\tfixed_form\tnotes\tpromote_target\n"
                + "block-1\tterm\tpažangus gaivinimas\tspecializuotas gaivinimas\tALS fix\t\n"
                + "block-2\tsemantic_drift\tbad\tgood\tSemantic fix\t\n",
            )

            result = self.run_script("promote_rules.py", "--book-root", str(book_root), slug)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("shared/lexicon/termbase.tsv", result.stdout)
            self.assertIn("regression_examples", result.stdout)

    def test_refresh_template_preserves_non_empty_local_overrides_and_avoids_shared_files(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = self.make_book_root(Path(tmp_dir), "refresh-book")
            self.write(
                book_root / "termbase.local.tsv",
                TERMBASE_HEADER
                + "Advanced life support\tvietinis specializuotas gaivinimas\tLocal override\tpreferred\t\tmust_expand_first\tall\t\t\n",
            )
            self.write(
                book_root / "gold_sections" / "index.tsv",
                GOLD_SECTION_INDEX_HEADER + "example-1\t001\tblock-1\tnarrative\tshock\tlocal-example.md\tlocal\n",
            )
            self.write(book_root / "gold_sections" / "local-example.md", "Local example text\n")

            result = self.run_script("refresh_book_template.py", "--book-root", str(book_root))

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("vietinis specializuotas gaivinimas", (book_root / "termbase.local.tsv").read_text(encoding="utf-8"))
            self.assertEqual((book_root / "gold_sections" / "local-example.md").read_text(encoding="utf-8"), "Local example text\n")
            self.assertFalse((book_root / "termbase.tsv").exists())
            self.assertFalse((book_root / "lt_source_map.tsv").exists())
            self.assertTrue((book_root / "localization_overrides.local.tsv").exists())


if __name__ == "__main__":
    unittest.main()
