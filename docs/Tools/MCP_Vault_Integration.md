# MCP + HashiCorp Vault Integration Guide

This guide explains how to use MCP (Model Context Protocol) servers with HashiCorp Vault for secure secret management in the ApexSigma ecosystem.

## Overview

The integration provides:
- **Secure secret storage** in HashiCorp Vault
- **Dynamic secret loading** for MCP servers
- **No plaintext secrets** in configuration files
- **Centralized secret management** across all services

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │───▶│  Vault Scripts   │───▶│  HashiCorp      │
│ (Claude/Cursor) │    │  (Python)        │    │  Vault          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  MCP Servers     │
                       │ (task-master-ai, │
                       │  obsidian)       │
                       └──────────────────┘
```

## Setup Instructions

### 1. Start HashiCorp Vault

```bash
# Start Vault service
docker-compose -f docker-compose.unified.yml up -d apexsigma_vault

# Verify Vault is running
docker logs apexsigma_vault
```

### 2. Populate Vault with Secrets

Set your API keys as environment variables, then run:

```bash
# Set your API keys as environment variables
export ANTHROPIC_API_KEY="your_anthropic_key"
export OPENAI_API_KEY="your_openai_key"
export GOOGLE_API_KEY="your_google_key"
export OBSIDIAN_API_KEY="your_obsidian_key"
# ... add other API keys as needed

# Populate Vault with secrets
python scripts/populate_vault.py
```

### 3. Use MCP with Vault

#### Option A: Generate Static Configuration

```bash
# Generate .mcp.json with real secrets from Vault
python scripts/mcp_vault_secrets.py --output-file .mcp.json --backup

# Use the generated configuration with your MCP client
```

#### Option B: Dynamic Startup (Recommended)

```bash
# Start MCP with Vault integration
python scripts/start_mcp_with_vault.py --mcp-client claude
# or
python scripts/start_mcp_with_vault.py --mcp-client cursor
# or
python scripts/start_mcp_with_vault.py --mcp-client custom
```

## Vault Secret Structure

### MCP Task Master AI Secrets
Path: `mcp/task-master-ai`

```json
{
  "anthropic": "your_anthropic_api_key",
  "perplexity": "your_perplexity_api_key",
  "openai": "your_openai_api_key",
  "google": "your_google_api_key",
  "xai": "your_xai_api_key",
  "openrouter": "your_openrouter_api_key",
  "mistral": "your_mistral_api_key",
  "azure_openai": "your_azure_openai_api_key",
  "ollama": "your_ollama_api_key"
}
```

### MCP Obsidian Secrets
Path: `mcp/obsidian`

```json
{
  "obsidian_api_key": "your_obsidian_api_key"
}
```

### Common API Keys (Fallback)
Path: `monorepo/api_keys`

```json
{
  "anthropic": "your_anthropic_api_key",
  "perplexity": "your_perplexity_api_key",
  "openai": "your_openai_api_key",
  "google": "your_google_api_key",
  "xai": "your_xai_api_key",
  "openrouter": "your_openrouter_api_key",
  "mistral": "your_mistral_api_key",
  "azure_openai": "your_azure_openai_api_key",
  "ollama": "your_ollama_api_key"
}
```

## Configuration Files

### Base .mcp.json (Template)

The base configuration uses environment variable placeholders:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "GOOGLE_API_KEY": "${GOOGLE_API_KEY}",
        "OBSIDIAN_API_KEY": "${OBSIDIAN_API_KEY}"
        // ... other API keys
      }
    },
    "obsidian": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "OBSIDIAN_HOST", "-e", "OBSIDIAN_API_KEY", "mcp/obsidian"],
      "env": {
        "OBSIDIAN_HOST": "host.docker.internal",
        "OBSIDIAN_API_KEY": "${OBSIDIAN_API_KEY}"
      }
    }
  }
}
```

## Scripts Description

### 1. `scripts/mcp_vault_secrets.py`

Retrieves MCP secrets from Vault and generates a static `.mcp.json` file.

**Usage:**
```bash
python scripts/mcp_vault_secrets.py [--output-file path/to/.mcp.json] [--backup]
```

**Features:**
- Retrieves secrets from Vault
- Generates static configuration file
- Creates backup of existing configuration
- Handles missing secrets gracefully

### 2. `scripts/start_mcp_with_vault.py`

Starts MCP servers with dynamic secret loading from Vault.

**Usage:**
```bash
python scripts/start_mcp_with_vault.py [--mcp-client claude|cursor|custom] [--config-file .mcp.json]
```

**Features:**
- Dynamic secret loading from Vault
- Support for multiple MCP clients
- Temporary configuration file creation
- Automatic cleanup

### 3. `scripts/populate_vault.py` (Extended)

Extended to include MCP secrets alongside service secrets.

**Usage:**
```bash
# Set environment variables with your API keys
export ANTHROPIC_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
# ... other keys

# Populate Vault
python scripts/populate_vault.py
```

## Security Benefits

1. **No Plaintext Secrets**: API keys are never stored in configuration files
2. **Centralized Management**: All secrets in one secure location
3. **Audit Trail**: Vault logs all secret access
4. **Easy Rotation**: Update secrets in Vault without file changes
5. **Consistent Security**: Same security model as other ApexSigma services

## Troubleshooting

### Vault Connection Issues

```bash
# Check if Vault is running
docker-compose -f docker-compose.unified.yml ps apexsigma_vault

# Check Vault logs
docker logs apexsigma_vault

# Test Vault connection
python -c "from apexsigma_core.vault import VaultClient; print(VaultClient().is_authenticated())"
```

### Missing Secrets

```bash
# Check what secrets are stored
python scripts/mcp_vault_secrets.py

# Add missing secrets to environment and re-run populate
export MISSING_API_KEY="your_key"
python scripts/populate_vault.py
```

### MCP Client Issues

```bash
# Keep temporary files for debugging
python scripts/start_mcp_with_vault.py --keep-temp

# Check generated configuration
cat /tmp/mcp_vault_*.json
```

## Best Practices

1. **Regular Rotation**: Rotate API keys regularly using Vault
2. **Access Control**: Use Vault policies to restrict secret access
3. **Audit Monitoring**: Monitor Vault logs for secret access
4. **Backup**: Backup Vault data regularly
5. **Environment Separation**: Use different Vault paths for dev/staging/prod

## Integration with Other Tools

The MCP + Vault integration works seamlessly with:

- **iFlow CLI**: Uses same Vault infrastructure
- **ApexSigma Services**: Shared secret management
- **Docker Compose**: Unified infrastructure
- **Monitoring**: Complete observability stack

## Next Steps

1. **Set up Vault**: Start Vault service and verify connectivity
2. **Populate Secrets**: Add your API keys to Vault using the populate script
3. **Test Integration**: Use MCP with Vault integration
4. **Configure Clients**: Set up your preferred MCP client
5. **Monitor Usage**: Check Vault logs for secret access patterns