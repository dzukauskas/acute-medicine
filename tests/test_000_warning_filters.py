#!/usr/bin/env python3
from __future__ import annotations

import warnings


# PyMuPDF 1.27.x on Python 3.12 emits SWIG deprecation warnings during import.
# This is third-party noise, so filter it as early as possible in the test suite.
warnings.filterwarnings(
    "ignore",
    message=r"builtin type .* has no __module__ attribute",
    category=DeprecationWarning,
)
