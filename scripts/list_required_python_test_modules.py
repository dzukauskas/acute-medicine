#!/usr/bin/env python3
from __future__ import annotations

import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SUITE_MANIFEST_PATH = REPO_ROOT / "tests" / "python_test_suite.toml"


def load_required_modules(path: Path = SUITE_MANIFEST_PATH) -> list[str]:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    raw_required = data.get("required")
    if not isinstance(raw_required, list) or not all(isinstance(item, str) and item.strip() for item in raw_required):
        raise SystemExit(f"{path}: `required` turi būti netuščias Python unittest modulių sąrašas.")
    return [item.strip() for item in raw_required]


def main() -> int:
    print("\n".join(load_required_modules()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
