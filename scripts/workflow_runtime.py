#!/usr/bin/env python3
from __future__ import annotations

import importlib
import os
import sys
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_CONFIG_PATH = REPO_ROOT / "repo_config.toml"
REPO_LOCAL_CONFIG_PATH = REPO_ROOT / "repo_config.local.toml"


def load_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    return data or {}


def merge_config(base: dict[str, object], override: dict[str, object]) -> dict[str, object]:
    merged = dict(base)
    for key, value in override.items():
        existing = merged.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = merge_config(existing, value)
            continue
        merged[key] = value
    return merged


def load_repo_config() -> dict[str, object]:
    if not REPO_CONFIG_PATH.exists():
        raise SystemExit(
            f"Nerastas repo config failas: {REPO_CONFIG_PATH}\n"
            "Sukurkite `repo_config.toml` pagal `repo_config.example.toml`."
        )
    config = load_toml(REPO_CONFIG_PATH)
    if REPO_LOCAL_CONFIG_PATH.exists():
        config = merge_config(config, load_toml(REPO_LOCAL_CONFIG_PATH))
    return config


def obsidian_config() -> dict[str, str]:
    config = load_repo_config()
    raw_section = config.get("obsidian")
    if not isinstance(raw_section, dict):
        raise SystemExit(f"{REPO_CONFIG_PATH}: trūksta `[obsidian]` sekcijos.")
    section = {str(key): str(value).strip() for key, value in raw_section.items()}
    missing = [key for key in ("base_dir", "vault_name", "launch_agent_prefix") if not section.get(key, "")]
    if missing:
        raise SystemExit(
            f"{REPO_CONFIG_PATH}: `[obsidian]` sekcijoje trūksta laukų: {', '.join(missing)}."
        )
    return section


def obsidian_vault_root() -> Path:
    config = obsidian_config()
    return Path(config["base_dir"]).expanduser() / config["vault_name"]


def obsidian_dest_for_title(title: str) -> Path:
    return obsidian_vault_root() / title


def parse_bool(value: str, default: bool = False) -> bool:
    cleaned = (value or "").strip().lower()
    if not cleaned:
        return default
    return cleaned in {"1", "true", "yes", "y", "taip"}


def ensure_python_module(module_name: str, package_name: str | None = None) -> None:
    try:
        importlib.import_module(module_name)
        return
    except ModuleNotFoundError:
        venv_python = REPO_ROOT / ".venv" / "bin" / "python"
        current_python = Path(sys.executable)
        if venv_python.exists() and current_python != venv_python:
            os.execv(str(venv_python), [str(venv_python), *sys.argv])
        package_hint = package_name or module_name
        raise SystemExit(
            f"Nerastas Python modulis `{module_name}`. "
            f"Įdiekite `{package_hint}` į aktyvią aplinką arba naudokite repo `.venv`."
        )
