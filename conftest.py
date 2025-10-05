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


# Pytest fixtures for test isolation
import pytest
from typing import Any


@pytest.fixture
def isolated_db_session(request: Any) -> Any:
    """Fixture to provide a unique database session for each test."""
    test_id = request.node.nodeid  # Unique ID for the test
    print(f"Setting up isolated DB session for test: {test_id}")

    # Setup code for the database session
    # Example: Create a unique schema or transaction for the test
    db_session = setup_database_session(test_id)

    yield db_session

    # Teardown code for the database session
    print(f"Tearing down isolated DB session for test: {test_id}")
    teardown_database_session(db_session)


def setup_database_session(test_id: str) -> str:
    """Setup logic for database session."""
    # TODO: Implement actual database session setup
    # This should create a unique database session/schema for the test
    return f"DB session for {test_id}"


def teardown_database_session(db_session: str) -> None:
    """Teardown logic for database session."""
    # TODO: Implement actual database session cleanup
    print(f"Closed {db_session}")
