---
date created: 266,23O September9 2025 05:47 am 
date modified: 266,23O September9 2025 11:06 pm 
---

# Gemini Settings

## Gemini CLI and its Forks

```json
{/

  "accessibility": {

    "screenReader": true

  },

  "autoAccept": false,

  "contextFileName": [

    "GEMINI.md",

    "OMEGA_INGEST_LAWS.md",

    "AGENTS.md"

  ],

  "fileFiltering": {

    "respectGitIgnore": true,

    "enableRecursiveFileSearch": true,

    "disableFuzzySearch": true

  },

  "folderTrustFeature": true,

  "folderTrust": true,

  "hasSeenIdeIntegrationNudge": true,

  "hideBanner": false,

  "hideContextSummary": false,

  "showMemoryUsage": true,

  "showLineNumbers": true,

  "showCitations": true,

  "ideMode": true,

  "mcpServers": {

    "fetch": {

      "command": "uvx",

      "args": [

        "mcp-server-fetch"

      ]

    },

    "task-master-ai": {

      "command": "npx",

      "args": [

        "-y",

        "--package=task-master-ai",

        "task-master-ai"

      ],

      "env": {

        "ANTHROPIC_API_KEY": "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",

        "PERPLEXITY_API_KEY": "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",

        "OPENAI_API_KEY": "YOUR_OPENAI_KEY_HERE",

        "GOOGLE_API_KEY": "YAIzaSyCvK-TF1s9WVpPR0QL2UfYTSzNCYuy2u8M",

        "Gemini_API_KEY": "AIzaSyAILXEdq15qV8ZZ78dWvuClf1Ungb7sU1s",

        "MISTRAL_API_KEY": "29uBw28Wf3ImlLhE121SbkY7dm1GvZsz",

        "GROQ_API_KEY": "YOUR_GROQ_KEY_HERE",

        "OPENROUTER_API_KEY": "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",

        "XAI_API_KEY": "xai-iRSUa7HlRSNdoot6luO5EZsR0v2kYKqZSSsLubXDNLMzmcjq2s8saO0Y27XrJvQUIhYJ66RHXyPPlrPV",

        "AZURE_OPENAI_API_KEY": "YOUR_AZURE_KEY_HERE",

        "OLLAMA_API_KEY": "YOUR_OLLAMA_API_KEY_HERE"

      },

      "type": "stdio"

    },

    "neo4j": {

      "command": "npx",

      "args": [

        "@alanse/mcp-neo4j-server"

      ],

      "env": {

        "NEO4J_URI": "bolt://localhost:7687",

        "NEO4J_USERNAME": "neo4j",

        "NEO4J_PASSWORD": "your-password",

        "NEO4J_DATABASE": "neo4j"

      }

    },

    "sequential-thinking": {

      "command": "npx",

      "args": [

        "-y",

        "@modelcontextprotocol/server-sequential-thinking"

      ]

    },

    "Context7": {

      "command": "npx",

      "args": [

        "-y",

        "@upstash/context7-mcp"

      ]

    },

    "langfuse-docs": {

      "url": "https://langfuse.com/api/mcp"

    },

    "linear": {

      "command": "npx",

      "args": ["-y", "mcp-remote", "https://mcp.linear.app/sse"]

    },

    "time": {

      "command": "uvx",

      "args": [

        "mcp-server-time"

      ]

    },

    "github": {

      "command": "docker",

      "args": [

        "run",

        "-i",

        "--rm",

        "-e",

        "GITHUB_PERSONAL_ACCESS_TOKEN",

        "ghcr.io/github/github-mcp-server"

      ],

      "env": {

        "GITHUB_PERSONAL_ACCESS_TOKEN": "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"

      }

    }

  },

  "preferredEditor": "vscode",

  "selectedAuthType": "oauth-personal",

  "skipNextSpeakerCheck": true,

  "telemetry": {

    "enabled": false,

    "target": "local",

    "otlpEndpoint": "http://localhost:16686",

    "logPrompts": true

  },

  "theme": "Dracula",

  "usageStatisticsEnabled": true,

  "useRipgrep": true

}
```