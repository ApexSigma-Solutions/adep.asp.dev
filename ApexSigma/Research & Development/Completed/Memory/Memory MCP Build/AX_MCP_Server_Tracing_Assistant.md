---
description: >-
  Add Arize's tracing assistant MCP server to your IDE or LLM for seamless
  support and instrumentation with Arize AX.
---

# AX MCP Server Tracing Assistant

&#x20;:package:  [View on PyPI](https://pypi.org/project/arize-tracing-assistant/)

## Overview

The **Arize Tracing Assistant** is a Model Context Protocol (MCP) server that enhances your development workflow by integrating Arize support, documentation, and curated examples directly into your IDE or LLM.

{% embed url="https://storage.googleapis.com/arize-phoenix-assets/assets/gifs/mcp-intro.gif" %}

## **Key Features**

* Access instrumentation guides for Arize AX
* Use curated tracing examples and best practices
* Direct connection to Arize support through natural language queries

## Installation

The Arize Tracing Assistant is distributed via [uv](https://github.com/astral-sh/uv), a fast Python package manager.

#### Install `uv`

{% tabs %}
{% tab title="macOS" %}
```bash
pip install uv
# or
brew install uv
```
{% endtab %}

{% tab title="Linux" %}
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
{% endtab %}

{% tab title="Windows" %}
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
{% endtab %}
{% endtabs %}

## IDE Integration

#### Cursor IDE

1. Navigate to: `Settings` → `MCP`
2. Click **Add new global MCP server**
3.  Insert the following into your config JSON:

    ```json
    "arize-tracing-assistant": {
      "command": "uvx",
      "args": ["arize-tracing-assistant@latest"]
    }
    ```

#### Claude Desktop

1. Open: `Settings` → `Developer` → `Edit Config`
2.  Add the following config:

    ```json
    "mcpServers": {
      "arize-tracing-assistant": {
        "command": "uvx",
        "args": ["arize-tracing-assistant@latest"]
      }
    }
    ```

#### Manual MCP Config

Add this snippet to your `mcpServers` config section:

```json
"mcpServers": {
  "arize-tracing-assistant": {
    "command": "uvx",
    "args": ["arize-tracing-assistant@latest"]
  }
}
```

## Usage

Once the MCP server is running, you can ask your IDE or LLM natural-language questions like:

* “Instrument this app using Arize.”
* “Can you use manual instrumentation so that I have more control over my traces?”
* “How can I redact sensitive information from my spans?”
* “Can you make sure the context of this trace is propagated across these tool calls?”
* “Where can I find my Arize keys?”

## Troubleshooting

* &#x20;Ensure your JSON configs are properly formatted
* Run `uv cache clean` to reset any cached versions
*   &#x20;Confirm the `uv` path using:

    ```bash
    which uv
    ```
*   Start the server manually by running:

    ```bash
    uvx arize-tracing-assistant@latest
    ```
*   Use Anthropic's MCP inspector:

    ```bash
    npx @modelcontextprotocol/inspector uvx arize-tracing-assistant@latest
    ```

