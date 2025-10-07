#!/usr/bin/env python3
"""
Vault Population Script for ApexSigma Services

This script populates HashiCorp Vault with secrets from existing .env files
and migrates all services to use Vault for secrets management.

Usage:
    python scripts/populate_vault.py

Requirements:
    - Vault service running in Docker
    - .env files present in service directories
    - apexsigma-core library installed
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any
import dotenv

# Add the libs directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "libs" / "apexsigma-core"))

from apexsigma_core.vault import VaultClient


def load_env_file(env_path: Path) -> Dict[str, str]:
    """Load environment variables from a .env file."""
    if not env_path.exists():
        print(f"Warning: {env_path} not found, skipping")
        return {}

    # Load the .env file
    env_vars = dotenv.dotenv_values(env_path)
    return {k: v for k, v in env_vars.items() if v is not None and v != ""}


def populate_service_secrets(service_name: str, env_vars: Dict[str, str], vault: VaultClient):
    """Populate Vault with secrets for a specific service."""
    print(f"\n🔐 Populating secrets for {service_name}...")

    # Define secret mappings for each service
    secret_mappings = {
        "memos": {
            "database": {
                "postgres_password": env_vars.get("POSTGRES_PASSWORD", "Apexsigma123_")
            },
            "observability": {
                "langfuse_public_key": env_vars.get("LANGFUSE_PUBLIC_KEY"),
                "langfuse_secret_key": env_vars.get("LANGFUSE_SECRET_KEY")
            },
            "security": {
                "jwt_secret_key": env_vars.get("JWT_SECRET_KEY", "apexsigma-mcp-secret-key-2025")
            }
        },
        "devenviro": {
            "database": {
                "postgres_password": env_vars.get("POSTGRES_PASSWORD", "Apexsigma123_")
            },
            "messaging": {
                "rabbitmq_password": env_vars.get("RABBITMQ_PASSWORD", "Apexsigma123_")
            },
            "agents": {
                "gemini_cli_token": env_vars.get("AGENT_GEMINI_CLI_TOKEN", "supersecrettoken_gemini_cli")
            },
            "observability": {
                "langfuse_public_key": env_vars.get("LANGFUSE_PUBLIC_KEY"),
                "langfuse_secret_key": env_vars.get("LANGFUSE_SECRET_KEY")
            }
        },
        "tools": {
            "api": {
                "serper_api_key": env_vars.get("SERPER_API_KEY", "your_serper_api_key_here")
            },
            "observability": {
                "langfuse_public_key": env_vars.get("LANGFUSE_PUBLIC_KEY"),
                "langfuse_secret_key": env_vars.get("LANGFUSE_SECRET_KEY")
            }
        },
        "ingest": {
            "database": {
                "postgres_password": env_vars.get("POSTGRES_PASSWORD", "Apexsigma123_")
            },
            "api": {
                "memos_api_key": env_vars.get("MEMOS_API_KEY")
            },
            "llm": {
                "lm_studio_api_key": env_vars.get("LM_STUDIO_API_KEY")
            },
            "observability": {
                "langfuse_public_key": env_vars.get("LANGFUSE_PUBLIC_KEY"),
                "langfuse_secret_key": env_vars.get("LANGFUSE_SECRET_KEY")
            }
        }
    }

    if service_name not in secret_mappings:
        print(f"Warning: No secret mappings defined for {service_name}")
        return

    # Populate secrets
    for category, secrets in secret_mappings[service_name].items():
        vault_path = f"services/{service_name}/{category}"
        # Collect all valid secrets for this path
        valid_secrets = {}
        for key, value in secrets.items():
            if value and value not in ["", "your_secure_postgres_password_here", "your_serper_api_key_here"]:
                valid_secrets[key] = value
            else:
                print(f"  ⚠️  Skipping {vault_path}/{key} (empty or placeholder value)")

        # Store all secrets for this path at once
        if valid_secrets:
            success = vault.set_secret(vault_path, valid_secrets)
            if success:
                for key in valid_secrets:
                    print(f"  ✅ {vault_path}/{key}")
            else:
                print(f"  ❌ Failed to set secrets at {vault_path}")
        else:
            print(f"  ⚠️  No valid secrets to store at {vault_path}")


def main():
    """Main function to populate Vault with all service secrets."""
    print("🚀 Starting Vault population for ApexSigma services...")

    # Initialize Vault client
    try:
        vault = VaultClient()
        print("✅ Connected to Vault")
    except Exception as e:
        print(f"❌ Failed to connect to Vault: {e}")
        print("Make sure Vault is running: docker-compose -f docker-compose.unified.yml up -d apexsigma_vault")
        return 1

    # Base directory
    base_dir = Path(__file__).parent.parent

    # Service configurations
    services = {
        "memos": base_dir / "services" / "memos.as" / ".env",
        "devenviro": base_dir / "services" / "devenviro.as" / ".env",
        "tools": base_dir / "services" / "tools.as" / ".env",
        "ingest": base_dir / "services" / "InGest-LLM.as" / ".env"
    }

    # Populate secrets for each service
    for service_name, env_path in services.items():
        env_vars = load_env_file(env_path)
        populate_service_secrets(service_name, env_vars, vault)

    print("\n🎉 Vault population complete!")
    print("\n📋 Next steps:")
    print("1. Remove secrets from .env files")
    print("2. Restart services to use Vault secrets")
    print("3. Test that services work with Vault secrets")

    return 0


if __name__ == "__main__":
    sys.exit(main())