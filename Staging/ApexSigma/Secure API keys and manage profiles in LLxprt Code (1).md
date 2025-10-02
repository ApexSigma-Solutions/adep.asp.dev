<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Secure API keys and manage profiles in LLxprt Code settings

Based on my knowledge of LLxprt Code and secure API key management practices, here's how to properly secure API keys and manage profiles in LLxprt Code settings:

## Secure API Key Storage

### Environment Variables Method

The most secure approach is using environment variables to store your API keys:

```bash
# Add to your ~/.bashrc or ~/.zshrc
export OPENROUTER_API_KEY="sk-or-your-openrouter-api-key-here"
export OPENAI_API_KEY="sk-your-openai-key-here"
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key-here"
```


### Keyfile Configuration

Create dedicated keyfiles with restricted permissions:

```bash
# Create secure keyfiles
echo "your-api-key-here" > ~/.llxprt/openrouter.key
echo "your-openai-key" > ~/.llxprt/openai.key
chmod 600 ~/.llxprt/*.key
```


### VS Code Settings Integration

Configure LLxprt through VS Code's settings.json for centralized management:

```json
{
  "llxprt.apiKeys": {
    "openrouter": "${env:OPENROUTER_API_KEY}",
    "openai": "${env:OPENAI_API_KEY}",
    "anthropic": "${env:ANTHROPIC_API_KEY}"
  },
  "llxprt.defaultProvider": "openrouter",
  "llxprt.keyfileDirectory": "~/.llxprt/keys"
}
```


## Profile Management System

### Creating Named Profiles

Organize different configurations into reusable profiles:

```bash
# OpenRouter profile for code generation
llxprt
/provider openai
/baseurl https://openrouter.ai/api/v1/
/keyfile ~/.llxprt/openrouter.key
/model qwen/qwen-2.5-coder-32b-instruct
/temperature 0.1
/profile save coding-openrouter

# Anthropic profile for analysis
/provider anthropic
/keyfile ~/.llxprt/anthropic.key
/model claude-3-5-sonnet-20241022
/temperature 0.3
/profile save analysis-claude
```


### Profile Directory Structure

Organize profiles in a dedicated directory:

```
~/.llxprt/
├── keys/
│   ├── openrouter.key
│   ├── openai.key
│   └── anthropic.key
├── profiles/
│   ├── coding-openrouter.json
│   ├── analysis-claude.json
│   └── default.json
└── config.json
```


### Loading and Switching Profiles

Quick profile switching during development:

```bash
# Load specific profile
llxprt --profile-load coding-openrouter

# Switch between profiles in session
/profile load analysis-claude
/profile list
/profile current
```


## Advanced Security Configuration

### Key Rotation Management

Implement regular key rotation practices:

```bash
# Create backup and rotate keys
cp ~/.llxprt/openrouter.key ~/.llxprt/openrouter.key.backup
echo "new-rotated-key" > ~/.llxprt/openrouter.key
/profile reload
```


### Access Control Settings

Configure file-level security for sensitive data:

```bash
# Secure the entire LLxprt directory
chmod 700 ~/.llxprt/
chmod 600 ~/.llxprt/keys/*
chmod 644 ~/.llxprt/profiles/*
```


### Workspace-Specific Configurations

Create project-specific settings without exposing global keys:

```json
// .vscode/settings.json (project-specific)
{
  "llxprt.profile": "coding-openrouter",
  "llxprt.contextLength": 32000,
  "llxprt.autoSave": true,
  "llxprt.logLevel": "info"
}
```


## Profile Template System

### Base Profile Configuration

Create template profiles for common use cases:

```bash
# Template for code review
/provider openai
/baseurl https://openrouter.ai/api/v1/
/model meta-llama/llama-3.1-70b-instruct
/temperature 0.2
/max_tokens 4000
/system_prompt "You are an expert code reviewer focused on security, performance, and best practices."
/profile save template-code-review

# Template for documentation
/model anthropic/claude-3-5-sonnet
/temperature 0.1
/system_prompt "You are a technical writer specializing in clear, comprehensive documentation."
/profile save template-documentation
```


### Profile Inheritance

Set up profile hierarchies for different development contexts:

```bash
# Base development profile
/profile save base-dev

# Inherit and customize
/profile load base-dev
/model qwen/qwen-2.5-coder-32b-instruct
/profile save python-dev

/profile load base-dev
/model deepseek/deepseek-coder
/profile save javascript-dev
```


## Best Practices Summary

**Security Guidelines:**

- Never hardcode API keys in configuration files
- Use environment variables or secure keyfiles exclusively
- Set restrictive file permissions (600 for keys, 700 for directories)
- Implement regular key rotation schedules
- Monitor API usage and set spending limits

**Profile Management:**

- Create specific profiles for different development tasks
- Use descriptive naming conventions for easy identification
- Maintain separate profiles for different projects or teams
- Regular backup of profile configurations
- Version control profile templates (without sensitive data)

This approach ensures your API keys remain secure while providing flexible profile management for different development scenarios in LLxprt Code.

