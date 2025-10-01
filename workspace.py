# Dagster workspace configuration
# This file defines the repositories that Dagster will load

import importlib.util
import os
import sys

# Add the services directory to the Python path so we can import from memos.as
services_path = os.path.join(os.path.dirname(__file__), "services")
if services_path not in sys.path:
    sys.path.insert(0, services_path)

from dagster import Definitions

# Import the repository from memos.as service
# Note: Using importlib to handle 'as' keyword in module path
memos_as_path = os.path.join(
    services_path, "memos.as", "app", "dagster", "repository.py"
)

if os.path.exists(memos_as_path):
    spec = importlib.util.spec_from_file_location("memos_as_repository", memos_as_path)
    memos_as_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(memos_as_module)
    memos_as_repository = memos_as_module.memos_as_repository
else:
    # Fallback if module doesn't exist
    memos_as_repository = None

# Create Definitions with the repository
defs = Definitions(
    assets=[],
    schedules=[],
    sensors=[],
    resources={},
)
