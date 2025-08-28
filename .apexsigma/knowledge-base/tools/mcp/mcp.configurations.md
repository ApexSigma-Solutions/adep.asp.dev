# Claude Code MCP Service Commands

This document outlines the custom commands available for the Claude Code MCP service. 

These commands are designed to facilitate the interaction between the Claude agent and external tools, ensuring efficient task management and communication within the DevEnviro platform.

## MCP Servers

### Serena

**Remote server**

```uvx
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)
```

### Context 7

 **Remote server**

```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp
```

or 

```bash
claude mcp add --transport sse context7 https://mcp.context7.com/sse
```

Local server    

```bash
claude mcp add --transport http context7 http://localhost:8080/mcp
```

or

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

### Puppeteer

Local server

```bash
npx -y @modelcontextprotocol/server-puppeteer
```

### CC Usage

```bash
npx ccusage@latest  # or: bunx ccusage  # or: pnpm dlx ccusage
```

### Linear

Remote Server

```bash
claude mcp add --transport sse linear-server https://mcp.linear.app/sse
```

```JSON
{
  "linear-server": {
    "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.linear.app/sse"]
  }
},
{
"conport": {
  "command": "uvx",
  "args": [
      "--from",
      "context-portal-mcp",
      "conport-mcp",
      "--mode",
      "stdio",
      "--workspace_id",
      "${workspaceFolder}",
      "--log-file",
      "./logs/conport.log",
      "--log-level",
      "INFO"
     ]
   }
```