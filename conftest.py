"""
conftest.py (workspace root)

Ensure the real `services/memos.as` package path is preferred on sys.path during pytest runs.
This avoids accidentally importing files from `services/memos.as.bak` which contain unpatched
raw SQL strings and cause SQLAlchemy textual-SQL warnings in tests.

This is a minimal, low-risk change that only affects test discovery/runtime ordering.
"""

import os
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))
MEMOS_PATH = os.path.join(ROOT, "services", "memos.as")

if os.path.isdir(MEMOS_PATH):
    # Prepend to sys.path so pytest imports the intended package implementation first
    if MEMOS_PATH not in sys.path:
        sys.path.insert(0, MEMOS_PATH)
