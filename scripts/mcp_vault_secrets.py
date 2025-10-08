#!/usr/bin/env python3
"""
MCP Vault Secrets Integration Script

This script retrieves MCP server secrets from HashiCorp Vault and generates
a secure .mcp.json configuration file with real API keys instead of placeholders.

Usage:
    python scripts/mcp_vault_secrets.py [--output-file path/to/.mcp.json]

Requirements:
    - Vault service running in Docker
    - apexsigma-core library installed
    - MCP secrets stored in Vault
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add the libs directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "libs" / "apexsigma-core"))

from apexsigma_core.vault import VaultClient


def get_mcp_secrets(vault: VaultClient) -> Dict[str, Dict[str, str]]:
    """
    Retrieve all MCP secrets from Vault.
    
    Args:
        vault: VaultClient instance
        
    Returns:
        Dictionary containing all MCP secrets organized by server
    """
    mcp_secrets = {
        "task-master-ai": {},
        "obsidian": {}
    }
    
    # Task Master AI secrets
    task_master_secrets = [
        "ANTHROPIC_API_KEY",
        "PERPLEXITY_API_KEY", 
        "OPENAI_API_KEY",
        "GOOGLE_API_KEY",
        "XAI_API_KEY",
        "OPENROUTER_API_KEY",
        "MISTRAL_API_KEY",
        "AZURE_OPENAI_API_KEY",
        "OLLAMA_API_KEY"
    ]
    
    for secret_key in task_master_secrets:
        # Try to get from MCP path first, then fallback to common API keys
        value = vault.get_secret("mcp/task-master-ai", secret_key.lower())
        if not value:
            value = vault.get_secret("monorepo/api_keys", secret_key.lower())
        if value:
            mcp_secrets["task-master-ai"][secret_key] = value
    
    # Obsidian secrets
    obsidian_api_key = vault.get_secret("mcp/obsidian", "obsidian_api_key")
    if obsidian_api_key:
        mcp_secrets["obsidian"]["OBSIDIAN_API_KEY"] = obsidian_api_key
    
    return mcp_secrets


def generate_mcp_config(mcp_secrets: Dict[str, Dict[str, str]], output_file: Path) -> bool:
    """
    Generate .mcp.json configuration file with real secrets from Vault.
    
    Args:
        mcp_secrets: Dictionary containing MCP secrets
        output_file: Path to output .mcp.json file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Base MCP configuration structure
        mcp_config = {
            "mcpServers": {
                "task-master-ai": {
                    "type": "stdio",
                    "command": "npx",
                    "args": [
                        "-y",
                        "--package=task-master-ai",
                        "task-master-ai"
                    ],
                    "env": {}
                },
                "obsidian": {
                    "command": "docker",
                    "args": [
                        "run",
                        "-i",
                        "--rm",
                        "-e",
                        "OBSIDIAN_HOST",
                        "-e",
                        "OBSIDIAN_API_KEY",
                        "mcp/obsidian"
                    ],
                    "env": {
                        "OBSIDIAN_HOST": "host.docker.internal"
                    }
                }
            }
        }
        
        # Add task-master-ai secrets if available
        if mcp_secrets.get("task-master-ai"):
            mcp_config["mcpServers"]["task-master-ai"]["env"] = mcp_secrets["task-master-ai"]
        else:
            print("⚠️  No task-master-ai secrets found in Vault, using placeholders")
            mcp_config["mcpServers"]["task-master-ai"]["env"] = {
                "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
                "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
                "OPENAI_API_KEY": "YOUR_OPENAI_KEY_HERE",
                "GOOGLE_API_KEY": "YOUR_GOOGLE_KEY_HERE",
                "XAI_API_KEY": "YOUR_XAI_KEY_HERE",
                "OPENROUTER_API_KEY": "YOUR_OPENROUTER_KEY_HERE",
                "MISTRAL_API_KEY": "YOUR_MISTRAL_KEY_HERE",
                "AZURE_OPENAI_API_KEY": "YOUR_AZURE_KEY_HERE",
                "OLLAMA_API_KEY": "YOUR_OLLAMA_API_KEY_HERE"
            }
        
        # Add obsidian secrets if available
        if mcp_secrets.get("obsidian", {}).get("OBSIDIAN_API_KEY"):
            mcp_config["mcpServers"]["obsidian"]["env"]["OBSIDIAN_API_KEY"] = \
                mcp_secrets["obsidian"]["OBSIDIAN_API_KEY"]
        else:
            print("⚠️  No Obsidian API key found in Vault, using placeholder")
            mcp_config["mcpServers"]["obsidian"]["env"]["OBSIDIAN_API_KEY"] = "YOUR_OBSIDIAN_API_KEY"
        
        # Write configuration to file
        with open(output_file, 'w') as f:
            json.dump(mcp_config, f, indent=2)
        
        print(f"✅ MCP configuration generated: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate MCP configuration: {e}")
        return False


def main():
    """Main function to generate MCP configuration with Vault secrets."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate MCP configuration with Vault secrets")
    parser.add_argument(
        "--output-file", 
        default=".mcp.json",
        help="Output file path for .mcp.json (default: .mcp.json)"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create backup of existing .mcp.json"
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path
    output_file = Path(args.output_file).resolve()
    
    # Create backup if requested and file exists
    if args.backup and output_file.exists():
        backup_file = output_file.with_suffix(f".json.backup")
        try:
            import shutil
            shutil.copy2(output_file, backup_file)
            print(f"📋 Backup created: {backup_file}")
        except Exception as e:
            print(f"⚠️  Could not create backup: {e}")
    
    print("🔐 Retrieving MCP secrets from Vault...")
    
    # Initialize Vault client
    try:
        vault = VaultClient()
        if not vault.is_authenticated():
            print("❌ Failed to authenticate with Vault")
            print("Make sure Vault is running: docker-compose -f docker-compose.unified.yml up -d apexsigma_vault")
            return 1
        print("✅ Connected to Vault")
    except Exception as e:
        print(f"❌ Failed to connect to Vault: {e}")
        return 1
    
    # Retrieve MCP secrets
    mcp_secrets = get_mcp_secrets(vault)
    
    # Show what secrets we found
    print("\n📊 Found secrets:")
    for server, secrets in mcp_secrets.items():
        if secrets:
            print(f"  📦 {server}: {len(secrets)} secrets")
            for key in secrets:
                print(f"    ✅ {key}")
        else:
            print(f"  ⚠️  {server}: No secrets found")
    
    # Generate MCP configuration
    print(f"\n🔧 Generating MCP configuration...")
    success = generate_mcp_config(mcp_secrets, output_file)
    
    if success:
        print(f"\n🎉 MCP configuration successfully generated!")
        print(f"📍 Output file: {output_file}")
        print("\n📋 Next steps:")
        print("1. Restart your MCP client to use the new configuration")
        print("2. Verify MCP servers are working with the retrieved secrets")
        
        # Show missing secrets if any
        missing_servers = [server for server, secrets in mcp_secrets.items() if not secrets]
        if missing_servers:
            print(f"\n⚠️  Missing secrets for: {', '.join(missing_servers)}")
            print("To add missing secrets, run: python scripts/populate_vault.py")
        
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())