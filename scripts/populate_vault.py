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


def populate_mcp_secrets(vault: VaultClient):
    """Populate Vault with MCP server secrets."""
    print(f"\n🔐 Populating MCP secrets...")

    # MCP Task Master AI secrets
    task_master_secrets = {
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "perplexity": os.getenv("PERPLEXITY_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY"),
        "google": os.getenv("GOOGLE_API_KEY"),
        "xai": os.getenv("XAI_API_KEY"),
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
        "mistral": os.getenv("MISTRAL_API_KEY"),
        "azure_openai": os.getenv("AZURE_OPENAI_API_KEY"),
        "ollama": os.getenv("OLLAMA_API_KEY")
    }

    # Store Task Master AI secrets
    valid_task_master_secrets = {}
    for key, value in task_master_secrets.items():
        if value and value not in ["", "your_api_key_here", "YOUR_API_KEY_HERE"]:
            valid_task_master_secrets[key] = value
        else:
            print(f"  ⚠️  Skipping mcp/task-master-ai/{key} (empty or placeholder value)")

    if valid_task_master_secrets:
        success = vault.set_secret("mcp/task-master-ai", valid_task_master_secrets)
        if success:
            for key in valid_task_master_secrets:
                print(f"  ✅ mcp/task-master-ai/{key}")
        else:
            print(f"  ❌ Failed to set Task Master AI secrets")
    else:
        print(f"  ⚠️  No valid Task Master AI secrets to store")

    # MCP Obsidian secrets
    obsidian_api_key = os.getenv("OBSIDIAN_API_KEY")
    if obsidian_api_key and obsidian_api_key not in ["", "your_obsidian_api_key", "YOUR_OBSIDIAN_API_KEY"]:
        success = vault.set_secret("mcp/obsidian", {"obsidian_api_key": obsidian_api_key})
        if success:
            print(f"  ✅ mcp/obsidian/obsidian_api_key")
        else:
            print(f"  ❌ Failed to set Obsidian secrets")
    else:
        print(f"  ⚠️  No valid Obsidian API key to store")

    # Common API keys (fallback for MCP)
    common_api_keys = {
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "perplexity": os.getenv("PERPLEXITY_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY"),
        "google": os.getenv("GOOGLE_API_KEY"),
        "xai": os.getenv("XAI_API_KEY"),
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
        "mistral": os.getenv("MISTRAL_API_KEY"),
        "azure_openai": os.getenv("AZURE_OPENAI_API_KEY"),
        "ollama": os.getenv("OLLAMA_API_KEY")
    }

    # Store common API keys
    valid_common_secrets = {}
    for key, value in common_api_keys.items():
        if value and value not in ["", "your_api_key_here", "YOUR_API_KEY_HERE"]:
            valid_common_secrets[key] = value

    if valid_common_secrets:
        success = vault.set_secret("monorepo/api_keys", valid_common_secrets)
        if success:
            print(f"  ✅ monorepo/api_keys ({len(valid_common_secrets)} keys)")
        else:
            print(f"  ❌ Failed to set common API keys")
    else:
        print(f"  ⚠️  No valid common API keys to store")


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

    # Populate MCP secrets
    populate_mcp_secrets(vault)

    print("\n🎉 Vault population complete!")
    print("\n📋 Next steps:")
    print("1. Remove secrets from .env files")
    print("2. Restart services to use Vault secrets")
    print("3. Test that services work with Vault secrets")
    print("4. Use MCP with Vault: python scripts/start_mcp_with_vault.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())