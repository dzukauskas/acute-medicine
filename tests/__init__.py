"""Test-suite only warning filters.

PyMuPDF 1.27.x on Python 3.12 emits SWIG deprecation warnings during import.
These warnings come from the third-party binding layer, not from repo code.
Filter them only in the test package so local test output stays readable.
"""

from __future__ import annotations

import warnings


warnings.filterwarnings(
    "ignore",
    message=r"builtin type .* has no __module__ attribute",
    category=DeprecationWarning,
)
