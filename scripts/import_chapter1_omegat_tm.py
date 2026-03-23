#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CHAPTER = ROOT / "study" / "en" / "001-cardiorespiratory-arrest-in-hospital.md"
TARGET_CHAPTER = ROOT / "study" / "lt" / "001-cardiorespiratory-arrest-in-hospital.md"
OUTPUT_TMX = ROOT / "study" / "omegat" / "tm" / "chapter-001-study-translation.tmx"

CAPTION_PREFIX = "Figure 1.1\u2002 Algorithm for adult advanced life support."


@dataclass(frozen=True)
class Unit:
    kind: str
    raw_text: str
    analysis_text: str


@dataclass(frozen=True)
class Section:
    key: str
    raw_heading: str
    units: tuple[Unit, ...]


@dataclass(frozen=True)
class SectionSpec:
    source_heading: str
    target_heading: str
    add_heading_pair: bool = True
    merge_target_spans: tuple[tuple[int, int], ...] = ()


TITLE_PAIR = (
    "# CHAPTER 1 Cardiorespiratory arrest in hospital",
    "# 1 skyrius. Kardiorespiracinis sustojimas ligoninėje",
)

SECTION_SPECS = (
    SectionSpec(
        source_heading="# CHAPTER 1 Cardiorespiratory arrest in hospital",
        target_heading="Įvadas",
        add_heading_pair=False,
    ),
    SectionSpec("Background", "Pagrindinė informacija"),
    SectionSpec("Initial management", "Pradinis valdymas"),
    SectionSpec("Figure 1.1", "1.1 paveikslas", add_heading_pair=False),
    SectionSpec("Chest compressions", "Krūtinės ląstos paspaudimai"),
    SectionSpec("Airway and ventilation", "Kvėpavimo takai ir ventiliacija"),
    SectionSpec("Management of cardiac arrest rhythms", "Širdies sustojimo ritmų valdymas"),
    SectionSpec(
        "Ventricular fibrillation/pulseless ventricular tachycardia",
        "Skilvelių virpėjimas / bepulsinė skilvelinė tachikardija",
        merge_target_spans=((1, 3),),
    ),
    SectionSpec("Defibrillators and pulse checks", "Defibriliatoriai ir pulso tikrinimas"),
    SectionSpec("Pulseless electrical activity (PEA)/asystole", "Elektrinė veikla be pulso (PEA) / asistolija"),
    SectionSpec("Reversible causes of cardiac arrest", "Grįžtamos širdies sustojimo priežastys"),
    SectionSpec(
        "Following return of spontaneous circulation (ROSC)",
        "Veiksmai atsistačius spontaninei kraujotakai (ROSC)",
    ),
    SectionSpec("Duration of a resuscitation attempt", "Gaivinimo trukmė"),
    SectionSpec(
        "Decisions regarding cardiopulmonary resuscitation",
        "Sprendimai dėl kardiopulmoninio gaivinimo",
    ),
    SectionSpec("Further reading", "Tolimesnis skaitymas"),
)


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    replacements = {
        "e.g.": "e§g§",
        "i.e.": "i§e§",
        "vs.": "vs§",
        "Dr.": "Dr§",
        "Mr.": "Mr§",
        "Mrs.": "Mrs§",
        "Prof.": "Prof§",
        "No.": "No§",
        "approx.": "approx§",
        "Fig.": "Fig§",
        "P.E.": "P§E§",
        "t. y.": "t§y§",
        "t.y.": "t§y§",
        "pvz.": "pvz§",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Preserve Lithuanian year abbreviations such as "2021 m. Jungtinės ..."
    text = re.sub(r"(\d+) m\. (?=[A-ZĄČĘĖĮŠŲŪŽ])", r"\1 m§ ", text)
    text = re.sub(r"(?<=\b[A-Z])\.(?=[A-Z]\b)", "§", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZĄČĘĖĮŠŲŪŽ0-9(\-#])", text)

    out: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        for old, new in replacements.items():
            part = part.replace(new, old)
        out.append(part.replace("m§", "m.").replace("P§E§", "P.E.").replace("§", "."))
    return out


def make_unit(kind: str, raw_text: str, analysis_text: str | None = None) -> Unit:
    return Unit(kind=kind, raw_text=raw_text, analysis_text=analysis_text or raw_text)


def parse_source_sections(path: Path) -> dict[str, Section]:
    lines = path.read_text(encoding="utf-8").splitlines()
    skip_exact = {
        "Acute Medicine",
        "Cardiorespiratory arrest in hospital",
        "Ann Thompson",
        "CHAPTER 1",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
    }

    sections: dict[str, list[Unit]] = {}
    raw_headings: dict[str, str] = {}
    current_heading = ""
    paragraph_lines: list[str] = []
    in_list = False

    def ensure_section(heading: str) -> None:
        if heading not in sections:
            sections[heading] = []
            raw_headings[heading] = heading

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines and current_heading:
            sections[current_heading].append(make_unit("paragraph", " ".join(paragraph_lines)))
            paragraph_lines = []

    for index, line in enumerate(lines):
        stripped = line.strip()
        next_non_empty = ""
        for nxt in lines[index + 1 :]:
            nxt = nxt.strip()
            if nxt:
                next_non_empty = nxt
                break

        if not stripped:
            flush_paragraph()
            in_list = False
            continue

        hard_break = (
            stripped.startswith("<!-- page:")
            or stripped in skip_exact
            or stripped.startswith("Acute Medicine: A Practical Guide")
            or stripped.startswith("Edited by ")
            or stripped.startswith("© 2026 ")
            or stripped.startswith("- Pages:")
            or stripped.startswith("- PDF:")
        )
        if hard_break:
            flush_paragraph()
            in_list = False
            continue

        bullet_like = in_list and len(stripped.split()) <= 8 and not re.search(r"[.!?]$", stripped)
        heading_like = (not in_list) and (
            stripped.startswith("# CHAPTER ")
            or (
                len(stripped.split()) <= 6
                and not re.search(r"[.!?]$", stripped)
                and stripped[0].isupper()
                and next_non_empty
                and next_non_empty[0].isupper()
                and next_non_empty != next_non_empty.upper()
            )
        )

        if heading_like:
            flush_paragraph()
            current_heading = stripped
            ensure_section(current_heading)
            continue

        if not current_heading:
            continue

        if bullet_like:
            flush_paragraph()
            sections[current_heading].append(make_unit("bullet", stripped))
        else:
            paragraph_lines.append(stripped)

        in_list = stripped.endswith(":") or (in_list and bullet_like)
        if in_list and not bullet_like and not stripped.endswith(":"):
            in_list = False

    flush_paragraph()

    # Split the figure caption out as its own synthetic section.
    figure_units: list[Unit] = []
    for heading, units in list(sections.items()):
        kept_units: list[Unit] = []
        for unit in units:
            if unit.kind == "paragraph" and unit.raw_text.startswith(CAPTION_PREFIX):
                figure_units.append(unit)
            else:
                kept_units.append(unit)
        sections[heading] = kept_units
    if figure_units:
        sections["Figure 1.1"] = figure_units
        raw_headings["Figure 1.1"] = "Figure 1.1"

    return {
        key: Section(key=key, raw_heading=raw_headings[key], units=tuple(units))
        for key, units in sections.items()
    }


def parse_target_sections(path: Path) -> dict[str, Section]:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")) if block.strip()]
    sections: dict[str, list[Unit]] = {}
    raw_headings: dict[str, str] = {}
    current_heading = ""

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        if lines[0].startswith("Mokymosi paskirties vertimas") or lines[0].startswith("Autorius:"):
            continue

        if len(lines) == 1 and lines[0].startswith("#"):
            raw_heading = lines[0]
            current_heading = raw_heading.lstrip("#").strip()
            raw_headings[current_heading] = raw_heading
            sections.setdefault(current_heading, [])
            continue

        if not current_heading:
            continue

        if all(line.startswith("- ") for line in lines):
            for line in lines:
                sections[current_heading].append(
                    make_unit("bullet", raw_text=line, analysis_text=line[2:].strip())
                )
            continue

        raw_text = " ".join(lines)
        sections[current_heading].append(make_unit("paragraph", raw_text=raw_text))

    return {
        key: Section(key=key, raw_heading=raw_headings[key], units=tuple(units))
        for key, units in sections.items()
    }


def merge_target_units(units: tuple[Unit, ...], spans: tuple[tuple[int, int], ...]) -> tuple[Unit, ...]:
    if not spans:
        return units

    merged: list[Unit] = []
    index = 0
    span_map = {start: end for start, end in spans}
    while index < len(units):
        if index in span_map:
            end = span_map[index]
            chunk = units[index:end]
            raw_text = "\n".join(unit.raw_text for unit in chunk)
            analysis_text = " ".join(unit.analysis_text for unit in chunk)
            merged.append(make_unit(chunk[0].kind, raw_text=raw_text, analysis_text=analysis_text))
            index = end
            continue
        merged.append(units[index])
        index += 1
    return tuple(merged)


def source_sentences(section: Section) -> list[str]:
    sentences: list[str] = []
    for unit in section.units:
        if unit.kind == "bullet":
            sentences.append(unit.analysis_text)
        else:
            sentences.extend(split_sentences(unit.analysis_text))
    return sentences


def unit_sentence_count(unit: Unit) -> int:
    if unit.kind == "bullet":
        return 1
    return max(1, len(split_sentences(unit.analysis_text)))


def align_groups(sentences: list[str], target_units: tuple[Unit, ...]) -> list[int]:
    n = len(sentences)
    m = len(target_units)
    if n < m:
        raise RuntimeError(f"Cannot align {n} source sentences to {m} target units.")

    inf = float("inf")
    dp = [[inf] * (n + 1) for _ in range(m + 1)]
    back: list[list[tuple[int, int] | None]] = [[None] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = 0.0

    for i in range(m):
        for j in range(n + 1):
            if dp[i][j] == inf:
                continue
            remaining_units = m - (i + 1)
            max_take = min(6, n - j - remaining_units)
            for take in range(1, max_take + 1):
                src_text = " ".join(sentences[j : j + take])
                tgt_text = target_units[i].analysis_text
                ratio_penalty = abs(math.log((len(tgt_text) + 1) / (len(src_text) + 1)))
                count_penalty = abs(take - unit_sentence_count(target_units[i])) * 0.45
                bullet_penalty = 0.35 * max(0, take - 1) if target_units[i].kind == "bullet" else 0.0
                cost = dp[i][j] + ratio_penalty + count_penalty + bullet_penalty
                if cost < dp[i + 1][j + take]:
                    dp[i + 1][j + take] = cost
                    back[i + 1][j + take] = (j, take)

    if dp[m][n] == inf:
        raise RuntimeError("Failed to align section.")

    groups: list[int] = []
    i = m
    j = n
    while i > 0:
        prev = back[i][j]
        if prev is None:
            raise RuntimeError("Incomplete alignment backtrace.")
        prev_j, take = prev
        groups.append(take)
        i -= 1
        j = prev_j
    groups.reverse()
    return groups


def build_pairs(source_sections: dict[str, Section], target_sections: dict[str, Section]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = [TITLE_PAIR]

    for spec in SECTION_SPECS:
        source_section = source_sections[spec.source_heading]
        target_section = target_sections[spec.target_heading]

        if spec.add_heading_pair:
            pairs.append((source_section.raw_heading, target_section.raw_heading))

        if spec.source_heading == "Figure 1.1":
            source_text = " ".join(unit.raw_text for unit in source_section.units)
            target_text = " ".join(unit.raw_text for unit in target_section.units)
            pairs.append((source_text, target_text))
            continue

        src_sentences = source_sentences(source_section)
        target_units = merge_target_units(target_section.units, spec.merge_target_spans)
        groups = align_groups(src_sentences, target_units)

        position = 0
        for unit, take in zip(target_units, groups):
            source_text = " ".join(src_sentences[position : position + take]).strip()
            target_text = unit.raw_text.strip()
            position += take
            if source_text and target_text:
                pairs.append((source_text, target_text))

    return pairs


def write_tmx(pairs: list[tuple[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    tmx = ET.Element("tmx", version="1.4")
    ET.SubElement(
        tmx,
        "header",
        {
            "creationtool": "Codex",
            "creationtoolversion": "1.0",
            "segtype": "sentence",
            "o-tmf": "OmegaT TMX",
            "adminlang": "en-US",
            "srclang": "en",
            "datatype": "plaintext",
        },
    )
    body = ET.SubElement(tmx, "body")

    seen: set[tuple[str, str]] = set()
    tuid = 1
    for source_text, target_text in pairs:
        pair = (source_text.strip(), target_text.strip())
        if not pair[0] or not pair[1] or pair in seen:
            continue
        seen.add(pair)

        tu = ET.SubElement(body, "tu", {"tuid": str(tuid)})
        tuv_en = ET.SubElement(tu, "tuv", {"{http://www.w3.org/XML/1998/namespace}lang": "en"})
        ET.SubElement(tuv_en, "seg").text = pair[0]
        tuv_lt = ET.SubElement(tu, "tuv", {"{http://www.w3.org/XML/1998/namespace}lang": "lt"})
        ET.SubElement(tuv_lt, "seg").text = pair[1]
        tuid += 1

    tree = ET.ElementTree(tmx)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    source_sections = parse_source_sections(SOURCE_CHAPTER)
    target_sections = parse_target_sections(TARGET_CHAPTER)
    pairs = build_pairs(source_sections, target_sections)
    write_tmx(pairs, OUTPUT_TMX)
    print(OUTPUT_TMX)
    print(f"pairs={len(pairs)}")


if __name__ == "__main__":
    main()
