# Guide to Authentivault:
  address: "http://apexsigma_vault:8200"
  token: "apexsigma-root-token-2025"  # Development root token (change for production)
  auth_method: "token"     # or "kubernetes", "aws", etc.
  namespace: "apexsigma"   # Optional: Vault namespaceand Retrieve Secrets from HashiCorp Vault for LLxprt

## Overview

This guide will walk you through the process of configuring LLxprt to authenticate with HashiCorp Vault and retrieve secrets securely. This setup ensures that API keys are not stored locally but are instead fetched from Vault when needed.

## Prerequisites

1. Access to HashiCorp Vault
2. Proper permissions to read secrets from Vault
3. Vault token or appropriate authentication method configured

## Step-by-Step Guide

### 1. Configure Vault Connection Settings

Update the `LLxprt Configuration for HashiCorp Vault API Key Management` note with your Vault connection details:

```yaml
vault:
  address: "http://apexsigma_vault:8200"
  token: "${VAULT_TOKEN}"  # Set in environment or retrieve from external source
  auth_method: "token"     # or "kubernetes", "aws", etc.
  namespace: "apexsigma"   # Optional: Vaul/t namespace
```

### 2. Map API Key Secrets

Configure the paths to your API key secrets in Vault:

```yaml
api_keys:
  # Map Vault secret paths to environment variable names
  openai:
    path: "secret/apexsigma/llxprt/openai"
    key: "api_key"
    env_var: "OPENAI_API_KEY"

  openrouter:
    path: "secret/apexsigma/llxprt/openrouter"
    key: "api_key"
    env_var: "OPENROUTER_API_KEY"

  anthropic:
    path: "secret/apexsigma/llxprt/anthropic"
    key: "api_key"
    env_var: "ANTHROPIC_API_KEY"

  gemini:
    path: "secret/apexsigma/llxprt/gemini"
    key: "api_key"
    env_var: "GEMINI_API_KEY"

  github:
    path: "secret/apexsigma/llxprt/github"
    key: "token"
    env_var: "GITHUB_TOKEN"

  langfuse:
    path: "secret/apexsigma/llxprt/langfuse"
    key: "secret_key"
    env_var: "LANGFUSE_SECRET_KEY"

  obsidian:
    path: "secret/apexsigma/llxprt/obsidian"
    key: "api_key"
    env_var: "OBSIDIAN_REST_API_KEY"
```

### 3. Store API Keys in Vault

Use the Vault CLI or UI to store your API keys:

```bash
# Login to Vault
vault login hvs.YOUR_ROOT_TOKEN

# Store OpenAI API key
vault kv put secret/apexsigma/llxprt/openai api_key="sk-your-openai-key-here"

# Store OpenRouter API key
vault kv put secret/apexsigma/llxprt/openrouter api_key="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"

# Store Anthropic API key
vault kv put secret/apexsigma/llxprt/anthropic api_key="sk-ant-your-anthropic-key-here"

# Store Gemini API key
vault kv put secret/apexsigma/llxprt/gemini api_key="your-gemini-key-here"

# Store GitHub token
vault kv put secret/apexsigma/llxprt/github token="ghp_your-github-token-here"

# Store Langfuse secret key
vault kv put secret/apexsigma/llxprt/langfuse secret_key="lf-your-langfuse-secret-here"

# Store Obsidian RestAPI key
vault kv put secret/apexsigma/llxprt/obsidian api_key="f2f148afde389e70639c11f24b53d3d01dfa7089865c53400123890faadbecef"
```

### 4. Set Vault Token

Set your Vault token in your environment:

```bash
export VAULT_TOKEN="apexsigma-root-token-2025"  # Development token
# For production, use proper authentication methods
```

### 5. Configure LLxprt

Update the `LLxprt_Config_Provider_Configuration` note with the Vault configuration as shown above.

### 6. Environment Variables

LLxprt will automatically retrieve and set these environment variables:

- `OPENAI_API_KEY`
- `OPENROUTER_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `GITHUB_TOKEN`
- `LANGFUSE_SECRET_KEY`
- `OBSIDIAN_REST_API_KEY`

## Security Benefits

1. **No Local Key Storage**: API keys are never stored in local files
2. **Centralized Management**: All keys managed in one secure location
3. **Access Control**: Vault provides fine-grained access control
4. **Audit Logging**: All key access is logged and auditable
5. **Key Rotation**: Easy key rotation without code changes

## Troubleshooting

### Common Issues

1. **Vault Connection Failed**
   - Check Vault address and token
   - Verify Vault service is running: `docker ps | grep vault`
   - Check network connectivity: `curl http://apexsigma_vault:8200/v1/sys/health`

2. **Permission Denied**
   - Verify Vault token has read access to secret paths
   - Check Vault policies allow access to `secret/apexsigma/llxprt/*`

3. **Keys Not Found**
   - Verify secret paths exist: `vault kv list secret/apexsigma/llxprt/`
   - Check key names match configuration

### Debug Mode

Enable debug logging to troubleshoot issues:

```yaml
debug: true
log_level: 'DEBUG'
```

## Integration with ApexSigma Infrastructure

This configuration integrates with the existing ApexSigma Vault service:

- **Service Name**: `apexsigma_vault`
- **Internal IP**: `172.26.0.X` (check VERIFIED_DOCKER_NETWORK_MAP_V3.md)
- **Port**: `8200`
- **Development Token**: `myroot` (as configured in security-hardening.yml)

For production deployments, use proper authentication methods instead of token-based auth.

## Conclusion

By following this guide, you have configured LLxprt to securely retrieve API keys from HashiCorp Vault, ensuring that your secrets are managed centrally and securely. This setup enhances security and simplifies key management across your applications.