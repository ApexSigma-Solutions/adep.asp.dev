#!/usr/bin/env python3
"""
MCP Startup Script with Vault Integration

This script starts MCP servers with secrets retrieved from HashiCorp Vault.
It handles the complete workflow of pulling secrets and launching MCP services.

Usage:
    python scripts/start_mcp_with_vault.py [--mcp-client claude|cursor|custom] [--config-file .mcp.json]

Requirements:
    - Vault service running in Docker
    - MCP client installed
    - apexsigma-core library installed
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

# Add the libs directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "libs" / "apexsigma-core"))

from apexsigma_core.vault import VaultClient


def get_mcp_secrets_from_vault(vault: VaultClient) -> Dict[str, str]:
    """
    Retrieve all MCP secrets from Vault and return as environment variables.
    
    Args:
        vault: VaultClient instance
        
    Returns:
        Dictionary of environment variables with MCP secrets
    """
    env_vars = {}
    
    # Task Master AI secrets
    task_master_secrets = [
        ("ANTHROPIC_API_KEY", "anthropic"),
        ("PERPLEXITY_API_KEY", "perplexity"), 
        ("OPENAI_API_KEY", "openai"),
        ("GOOGLE_API_KEY", "google"),
        ("XAI_API_KEY", "xai"),
        ("OPENROUTER_API_KEY", "openrouter"),
        ("MISTRAL_API_KEY", "mistral"),
        ("AZURE_OPENAI_API_KEY", "azure_openai"),
        ("OLLAMA_API_KEY", "ollama")
    ]
    
    for env_key, vault_key in task_master_secrets:
        # Try to get from MCP path first, then fallback to common API keys
        value = vault.get_secret("mcp/task-master-ai", vault_key)
        if not value:
            value = vault.get_secret("monorepo/api_keys", vault_key)
        if value:
            env_vars[env_key] = value
    
    # Obsidian secrets
    obsidian_api_key = vault.get_secret("mcp/obsidian", "obsidian_api_key")
    if obsidian_api_key:
        env_vars["OBSIDIAN_API_KEY"] = obsidian_api_key
    
    return env_vars


def create_temp_mcp_config(mcp_secrets: Dict[str, str], base_config_path: Path) -> Optional[Path]:
    """
    Create a temporary MCP configuration file with real secrets.
    
    Args:
        mcp_secrets: Dictionary of MCP secrets as environment variables
        base_config_path: Path to base .mcp.json file
        
    Returns:
        Path to temporary configuration file, or None if failed
    """
    try:
        # Read base configuration
        with open(base_config_path, 'r') as f:
            config = json.load(f)
        
        # Substitute environment variables
        config_str = json.dumps(config)
        for env_key, env_value in mcp_secrets.items():
            config_str = config_str.replace(f"${{{env_key}}}", env_value)
        
        # Parse back to JSON to validate
        final_config = json.loads(config_str)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.mcp.json', 
            delete=False,
            prefix='mcp_vault_'
        )
        
        json.dump(final_config, temp_file, indent=2)
        temp_file.close()
        
        return Path(temp_file.name)
        
    except Exception as e:
        print(f"❌ Failed to create temporary MCP config: {e}")
        return None


def start_mcp_client(client_type: str, config_path: Path) -> bool:
    """
    Start the specified MCP client with the given configuration.
    
    Args:
        client_type: Type of MCP client (claude, cursor, custom)
        config_path: Path to MCP configuration file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if client_type == "claude":
            # Claude Desktop - typically uses config file location
            claude_config_dir = Path.home() / "Library" / "Application Support" / "Claude"
            if claude_config_dir.exists():
                import shutil
                shutil.copy2(config_path, claude_config_dir / "claude_desktop_config.json")
                print("✅ Claude Desktop configuration updated")
                print("🔄 Restart Claude Desktop to apply changes")
                return True
            else:
                print("❌ Claude Desktop not found")
                return False
                
        elif client_type == "cursor":
            # Cursor - typically uses config file location
            cursor_config_dir = Path.home() / ".cursor"
            if cursor_config_dir.exists():
                import shutil
                shutil.copy2(config_path, cursor_config_dir / "mcp.json")
                print("✅ Cursor configuration updated")
                print("🔄 Restart Cursor to apply changes")
                return True
            else:
                print("❌ Cursor not found")
                return False
                
        elif client_type == "custom":
            # Custom - just display the config path for manual use
            print(f"✅ MCP configuration ready: {config_path}")
            print("📋 Use this configuration file with your MCP client")
            return True
            
        else:
            print(f"❌ Unsupported client type: {client_type}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start MCP client: {e}")
        return False


def main():
    """Main function to start MCP with Vault secrets."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start MCP with Vault secrets")
    parser.add_argument(
        "--mcp-client",
        choices=["claude", "cursor", "custom"],
        default="custom",
        help="MCP client type (default: custom)"
    )
    parser.add_argument(
        "--config-file",
        default=".mcp.json",
        help="MCP configuration file path (default: .mcp.json)"
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary configuration file for debugging"
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path
    base_config_path = Path(args.config_file).resolve()
    
    if not base_config_path.exists():
        print(f"❌ MCP configuration file not found: {base_config_path}")
        return 1
    
    print("🚀 Starting MCP with Vault secrets...")
    
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
    print("🔐 Retrieving MCP secrets from Vault...")
    mcp_secrets = get_mcp_secrets_from_vault(vault)
    
    if not mcp_secrets:
        print("⚠️  No MCP secrets found in Vault")
        print("To add secrets, run: python scripts/populate_vault.py")
        return 1
    
    print(f"✅ Retrieved {len(mcp_secrets)} secrets from Vault")
    
    # Create temporary configuration with real secrets
    print("🔧 Creating MCP configuration with real secrets...")
    temp_config_path = create_temp_mcp_config(mcp_secrets, base_config_path)
    
    if not temp_config_path:
        return 1
    
    try:
        # Start MCP client
        print(f"🚀 Starting {args.mcp_client} MCP client...")
        success = start_mcp_client(args.mcp_client, temp_config_path)
        
        if success:
            print("\n🎉 MCP started successfully with Vault secrets!")
            
            if args.mcp_client == "custom":
                print(f"\n📋 Configuration file: {temp_config_path}")
                print("🔧 Use this file with your MCP client")
                print("🗑️  File will be automatically cleaned up on exit")
            
            if not args.keep_temp:
                # Schedule cleanup on exit
                import atexit
                atexit.register(lambda: temp_config_path.unlink(missing_ok=True))
            else:
                print(f"📁 Temporary config kept at: {temp_config_path}")
            
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"❌ Failed to start MCP: {e}")
        # Cleanup on error
        temp_config_path.unlink(missing_ok=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())