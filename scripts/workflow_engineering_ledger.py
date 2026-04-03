#!/usr/bin/env python3
from __future__ import annotations

import re


SECTION_KEYS = (
    "active_theme",
    "summary",
    "current_state",
    "decisions",
    "next_steps",
    "risks",
    "completed",
)
CHECKPOINT_SECTION_KEYS = (
    "active_theme",
    "summary",
    "current_state",
    "next_steps",
    "completed",
)


def ensure_sections(text: str, section_keys: tuple[str, ...] = SECTION_KEYS) -> str:
    for key in section_keys:
        if f"<!-- ledger:{key}:start -->" not in text or f"<!-- ledger:{key}:end -->" not in text:
            raise ValueError(f"Ledger faile trūksta sekcijos marker'ių: {key}")
    return text


def replace_section(text: str, key: str, body: str) -> str:
    pattern = re.compile(
        rf"(<!-- ledger:{key}:start -->\n)(.*?)(\n<!-- ledger:{key}:end -->)",
        flags=re.DOTALL,
    )
    updated, count = pattern.subn(rf"\1{body}\3", text, count=1)
    if count != 1:
        raise ValueError(f"Nepavyko atnaujinti ledger sekcijos: {key}")
    return updated


def extract_section(text: str, key: str) -> str:
    pattern = re.compile(
        rf"<!-- ledger:{key}:start -->\n(.*?)\n<!-- ledger:{key}:end -->",
        flags=re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Nepavyko perskaityti ledger sekcijos: {key}")
    return match.group(1).strip()


def extract_theme_label(active_body: str) -> str:
    match = re.search(r"Theme:\s*(.+)", active_body)
    if not match:
        return ""
    return match.group(1).strip()
