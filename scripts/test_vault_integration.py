#!/usr/bin/env python3
"""
Test script to verify Vault integration works correctly.
Tests that services can retrieve secrets from Vault.
"""

import sys
from pathlib import Path

# Add the libs directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "libs" / "apexsigma-core"))

from apexsigma_core.vault import get_secret


def test_vault_secrets():
    """Test retrieving secrets from Vault."""
    print("🧪 Testing Vault secret retrieval...")

    test_cases = [
        ("services/memos/database", "postgres_password"),
        ("services/memos/observability", "langfuse_public_key"),
        ("services/memos/observability", "langfuse_secret_key"),
        ("services/devenviro/database", "postgres_password"),
        ("services/devenviro/messaging", "rabbitmq_password"),
        ("services/devenviro/agents", "gemini_cli_token"),
        ("services/tools/observability", "langfuse_public_key"),
        ("services/tools/observability", "langfuse_secret_key"),
        ("services/ingest/observability", "langfuse_public_key"),
        ("services/ingest/observability", "langfuse_secret_key"),
    ]

    success_count = 0
    total_count = len(test_cases)

    for path, key in test_cases:
        secret = get_secret(path, key)
        if secret:
            print(f"  ✅ {path}/{key}: {'*' * len(secret)}")
            success_count += 1
        else:
            print(f"  ❌ {path}/{key}: NOT FOUND")

    print(f"\n📊 Results: {success_count}/{total_count} secrets retrieved successfully")

    if success_count == total_count:
        print("🎉 All Vault secrets are accessible!")
        return True
    else:
        print("⚠️  Some secrets are missing from Vault")
        return False


if __name__ == "__main__":
    success = test_vault_secrets()
    sys.exit(0 if success else 1)