<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# FastMCP 2.0: A Comprehensive Guide

FastMCP 2.0 is the actively maintained version of the standard framework for working with the Model Context Protocol (MCP). While FastMCP 1.0 was incorporated into the official MCP Python SDK in 2024, version 2.0 provides a complete toolkit for the MCP ecosystem, going far beyond the core protocol specification.[^1][^2]

## What is FastMCP 2.0?

FastMCP 2.0 is a **production-ready framework** that makes building MCP servers and clients simple and intuitive. The Model Context Protocol serves as "the USB-C port for AI," providing a standardized way to connect LLMs to resources and tools.[^3][^2][^1]

## Core Components

FastMCP supports three main MCP components:

- **Resources**: Think of these as GET endpoints used to load information into the LLM's context[^3][^1]
- **Tools**: Similar to POST endpoints used to execute code or produce side effects[^1][^3]
- **Prompts**: Reusable templates for LLM interactions[^3][^1]


## Simple Getting Started Example

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

Run the server with:

```bash
fastmcp run server.py
```


## Advanced Features in FastMCP 2.0

### 1. Proxy Servers

Create intermediary servers for other MCP servers using `FastMCP.as_proxy()`, useful for bridging transports or adding authentication layers.[^2][^4]

### 2. Server Composition

Build modular applications by mounting multiple FastMCP instances using `mcp.mount()` (live link) or `mcp.import_server()` (static copy).[^5][^2]

### 3. OpenAPI \& FastAPI Integration

Automatically generate MCP servers from existing APIs:

- `FastMCP.from_openapi()` - Generate from OpenAPI specifications
- `FastMCP.from_fastapi()` - Generate from FastAPI applications[^4][^2][^5]


### 4. Authentication \& Security

Built-in authentication support for both servers and clients with:

- Server endpoint protection with configurable authentication providers
- Client authentication with automatic credential management
- Production-ready enterprise authentication patterns[^2][^5]


## Key Improvements Over Version 1.0

FastMCP 2.0 represents a major evolution from the minimal demo-friendly 1.0 library to a production-ready framework:[^6]

- **Modular and Composable**: Mount multiple FastMCP apps together for team collaboration
- **Built-in Proxying**: Bridge different transports and add authentication layers
- **OpenAPI Integration**: Convert existing HTTP APIs to MCP tools automatically
- **Context Object**: Available in every tool for logging, streaming, file operations, and metadata tracking
- **Async Support**: Fully async-capable for concurrent operations and cloud deployments[^6]


## Documentation and Resources

FastMCP 2.0 provides comprehensive documentation at **gofastmcp.com**, including:[^2]

- **LLM-Friendly Documentation**: Available in [llms.txt format](https://llmstxt.org/)
- **API References**: Detailed guides and advanced patterns
- **Community Showcase**: High-quality projects and examples from the community[^7]

The documentation is accessible in multiple formats:

- Standard web format at gofastmcp.com
- Markdown format by appending `.md` to any URL
- LLM-consumable formats at `llms.txt` and `llms-full.txt`[^3]


## Installation

FastMCP 2.0 is available on PyPI and can be installed via pip. The documentation includes upgrade instructions for those migrating from the official MCP SDK.[^5][^3]

FastMCP 2.0 aims to be fast, simple, Pythonic, and complete - providing the simplest path from development to production for MCP applications.[^2][^3]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^8][^9]</span>

<div style="text-align: center">⁂</div>

[^1]: https://gofastmcp.com/getting-started/welcome

[^2]: https://github.com/jlowin/fastmcp

[^3]: https://gofastmcp.com

[^4]: https://gofastmcp.com/servers/server

[^5]: https://pypi.org/project/fastmcp/

[^6]: https://gyliu513.github.io/jekyll/update/2025/06/08/fast-mcp-quick-start.html

[^7]: https://gofastmcp.com/community/showcase

[^8]: https://arxiv.org/abs/2408.10205

[^9]: https://academic.oup.com/nar/article/51/W1/W310/7160190

[^10]: http://biorxiv.org/lookup/doi/10.1101/2023.03.08.531791

[^11]: https://gut.bmj.com/lookup/doi/10.1136/gutjnl-2023-330616

[^12]: https://onlinelibrary.wiley.com/doi/10.1111/aor.14503

[^13]: https://ascopubs.org/doi/10.1200/JCO.23.01059

[^14]: https://www.nature.com/articles/s41592-022-01663-4

[^15]: https://academic.oup.com/nar/article/51/D1/D870/6775381

[^16]: https://dl.acm.org/doi/10.1145/3583780.3615285

[^17]: https://academic.oup.com/nar/article/49/W1/W5/6249611

[^18]: https://www.mdpi.com/1424-8220/22/17/6333/pdf?version=1661756623

[^19]: https://www.mdpi.com/1999-5903/16/7/233

[^20]: https://arxiv.org/pdf/2206.03776.pdf

[^21]: https://arxiv.org/pdf/1610.05329.pdf

[^22]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9460924/

[^23]: http://arxiv.org/pdf/2403.18374.pdf

[^24]: https://www.mdpi.com/2673-4001/3/4/33/pdf?version=1666185017

[^25]: https://www.mdpi.com/2079-9292/10/6/711/pdf

[^26]: https://www.mdpi.com/1424-8220/21/18/6289/pdf

[^27]: https://www.mdpi.com/2079-9292/10/17/2175/pdf

[^28]: https://www.jlowin.dev/blog/fastmcp-2

[^29]: https://gofastmcp.com/development/releases

[^30]: https://anish-natekar.github.io/mcp_docs/examples.html

[^31]: https://www.npmjs.com/package/fastmcp

[^32]: https://github.com/jlowin/fastmcp/discussions/1232

[^33]: https://www.vunda.ai/blog/fast-mcp-deep-dive

[^34]: https://github.com/sauliussed/fastmcp-examples

[^35]: https://sur.ly/i/gofastmcp.com/

[^36]: https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python

[^37]: https://mcp.so/server/fastmcp/jlowin

[^38]: https://www.pondhouse-data.com/blog/create-mcp-server-with-fastmcp

[^39]: https://gofastmcp.com/getting-started/installation

[^40]: https://codesandbox.io/examples/package/fastmcp

