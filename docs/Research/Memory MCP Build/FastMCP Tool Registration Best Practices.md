<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# FastMCP Tool Registration Best Practices

Based on the FastMCP documentation and community insights, here are the essential best practices for creating and registering tools effectively:

## Core Tool Registration Principles

### 1. **Use Descriptive Function Names and Metadata**

Your function name becomes the tool name by default, so make it clear and descriptive:[^1][^2]

```python
@mcp.tool(name="calculator_add", description="Adds two numbers together")
def add_numbers(num1: int, num2: int) -> int:
    """This function adds two numbers and returns the result"""
    return num1 + num2
```

**Best practices:**

- Use descriptive names that clearly indicate the tool's purpose
- Avoid generic names like `process()` or `handle()`
- Consider using namespaced naming for related tools (e.g., `user_get_profile`, `user_update_email`)


### 2. **Type Hints Are Essential and Required**

Type hints are **crucial** for FastMCP tool registration - they're not optional:[^2][^3][^4]

```python
@mcp.tool()
def process_data(name: str, age: int, active: bool = True) -> dict:
    """Process user data with proper type validation"""
    return {
        "message": f"Hello {name}",
        "status": "active" if active else "inactive",
        "category": "adult" if age >= 18 else "minor"
    }
```

**Why type hints matter:**

- FastMCP uses them to auto-generate schemas for client validation
- Enable automatic argument validation
- Generate proper documentation for LLMs
- Define expected return types for response handling[^4]


### 3. **Write Comprehensive Docstrings**

Docstrings serve as descriptions for LLMs to understand your tools:[^3][^2]

```python
@mcp.tool()
def search_documents(query: str, limit: int = 10) -> list:
    """
    Search through document database using full-text search.
    
    Args:
        query: The search terms to look for
        limit: Maximum number of results to return (default: 10)
        
    Returns:
        List of matching documents with titles and excerpts
    """
    # Implementation here
    return []
```

**Docstring best practices:**

- Explain what the tool does in clear, simple language
- Describe each parameter and what it expects
- Explain the return value format
- Include usage examples if the tool is complex


### 4. **Handle Duplicate Tools Appropriately**

Configure how FastMCP handles duplicate tool names using server settings:[^2]

```python
from fastmcp import FastMCP

mcp = FastMCP(
    name="MyServer",
    on_duplicate_tools="warn"  # Options: 'error', 'warn', 'ignore'
)
```

**Strategies for avoiding duplicates:**

- Use unique, descriptive names
- Implement namespacing for related functionality
- Monitor logs for duplicate warnings during development


### 5. **Use Async Functions for I/O Operations**

Make functions async when they involve waiting operations to avoid blocking the server:[^5][^3]

```python
@mcp.tool()
async def fetch_user_data(user_id: int) -> dict:
    """Fetch user data from external API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/api/users/{user_id}") as response:
            return await response.json()

@mcp.tool()
async def update_file(filename: str, content: str) -> None:
    """Asynchronously write content to file"""
    async with aiofiles.open(filename, 'w') as f:
        await f.write(content)
```


### 6. **Implement Proper Error Handling**

Include comprehensive error handling within your tools:[^3]

```python
@mcp.tool()
async def database_query(sql: str) -> list:
    """Execute database query with error handling"""
    try:
        # Database connection and query logic
        results = await execute_query(sql)
        return results
    except DatabaseError as e:
        raise ValueError(f"Database query failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")
```


### 7. **Keep Tools Focused and Single-Purpose**

Each tool should have one clear, well-defined responsibility:[^1]

```python
# Good: Focused, single-purpose tools
@mcp.tool()
def get_user_profile(user_id: int) -> dict:
    """Get user profile information"""
    pass

@mcp.tool()
def update_user_email(user_id: int, new_email: str) -> bool:
    """Update user's email address"""
    pass

# Avoid: Multi-purpose tools that are hard to understand
@mcp.tool()
def manage_user(action: str, user_id: int, **kwargs) -> dict:
    """Generic user management - too broad"""
    pass
```


### 8. **Leverage Context for Enhanced Functionality**

Use the Context parameter for logging, progress reporting, and LLM sampling:[^1]

```python
from fastmcp import FastMCP, Context

@mcp.tool()
async def analyze_document(file_path: str, ctx: Context) -> dict:
    """Analyze document with progress reporting"""
    await ctx.info(f"Starting analysis of {file_path}")
    
    # Report progress
    await ctx.report_progress(0, "Loading document...")
    content = await load_file(file_path)
    
    await ctx.report_progress(50, "Processing content...")
    analysis = await process_content(content)
    
    await ctx.report_progress(100, "Analysis complete")
    return analysis
```


### 9. **Test Your Tools Thoroughly**

Implement comprehensive testing for each tool:[^6]

```python
from fastmcp import FastMCP, Client
import pytest

@pytest.mark.asyncio
async def test_add_tool():
    mcp = FastMCP("Test Server")
    
    @mcp.tool()
    def add(a: int, b: int) -> int:
        return a + b
    
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": 5, "b": 3})
        assert result.content[^0].text == "8"
```

**Testing strategies:**

- Test with various input parameters
- Verify error handling with invalid inputs
- Test async operations don't block
- Validate return types match expectations


### 10. **Configuration and Server Settings**

Use appropriate server configuration for production environments:[^2]

```python
mcp = FastMCP(
    name="Production Server",
    instructions="Server for production document management",
    port=8080,
    host="0.0.0.0",
    log_level="INFO",
    on_duplicate_tools="error"  # Strict in production
)
```

Following these best practices ensures your FastMCP tools are robust, maintainable, and provide excellent user experience for LLMs interacting with your server.[^3][^1][^2]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^7][^8][^9]</span>

<div style="text-align: center">⁂</div>

[^1]: https://github.com/jlowin/fastmcp

[^2]: https://apidog.com/blog/fastmcp/

[^3]: https://www.pondhouse-data.com/blog/create-mcp-server-with-fastmcp

[^4]: https://the-pocket.github.io/PocketFlow-Tutorial-Codebase-Knowledge/MCP Python SDK/04_fastmcp_tools___tool____toolmanager__.html

[^5]: https://scrapfly.io/blog/how-to-build-an-mcp-server-in-python-a-complete-guide/

[^6]: https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python

[^7]: https://ebm.bmj.com/lookup/doi/10.1136/bmjebm-2023-112395

[^8]: http://medrxiv.org/lookup/doi/10.1101/2023.04.03.23288059

[^9]: https://jnnp.bmj.com/lookup/doi/10.1136/jnnp-2023-331733

[^10]: https://www.frontiersin.org/articles/10.3389/fpubh.2024.1462756/full

[^11]: https://bmjopen.bmj.com/lookup/doi/10.1136/bmjopen-2023-077036

[^12]: https://implementationsciencecomms.biomedcentral.com/articles/10.1186/s43058-024-00551-6

[^13]: https://onlinelibrary.wiley.com/doi/10.1111/fare.12826

[^14]: https://www.semanticscholar.org/paper/cff54ea560062a28703350b86273fc82a9cd07b7

[^15]: https://journals.lww.com/10.34067/KID.0000000000000277

[^16]: https://www.semanticscholar.org/paper/8dc94d2e697b887070a05af0113b633a35976c98

[^17]: https://www.mdpi.com/1999-5903/16/7/233

[^18]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9832703/

[^19]: https://www.mdpi.com/1424-8220/22/17/6333/pdf?version=1661756623

[^20]: http://arxiv.org/pdf/2209.13643.pdf

[^21]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10126156/

[^22]: https://arxiv.org/pdf/2206.03776.pdf

[^23]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9460924/

[^24]: http://arxiv.org/pdf/2403.18149.pdf

[^25]: https://arxiv.org/abs/2311.04406

[^26]: http://arxiv.org/pdf/1902.06288.pdf

[^27]: https://modelcontextprotocol.io/docs/concepts/tools

[^28]: https://www.reddit.com/r/modelcontextprotocol/comments/1hrq8x9/how_to_build_mcp_servers_with_fastmcp_stepbystep/

