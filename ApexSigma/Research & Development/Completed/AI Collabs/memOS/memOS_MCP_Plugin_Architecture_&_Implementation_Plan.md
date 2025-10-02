# memOS MCP Plugin Architecture & Implementation Plan
## High-Impact Foundation for CLI Integration

### Plugin Architecture Design

```
memOS Server
├── Core MCP Server (existing)
├── Plugin Registry
│   ├── Context Plugin ←── NEW
│   ├── Semantic Plugin ←── NEW  
│   └── Handoff Plugin ←── NEW
└── Storage Layer
    ├── Vector Store (enhanced)
    ├── Session Store ←── NEW
    └── Episodic Store ←── NEW
```

### Phase 1: Core Context Plugin (Week 1)

#### New MCP Tools Implementation:

```python
# /plugins/context_plugin.py
@mcp_tool("store_session_context")
async def store_session_context(
    session_id: str,
    tool_name: str,  # "gemini_cli" | "qwen_coder" 
    working_directory: str,
    active_files: List[str],
    recent_commands: List[str],
    context_summary: str,
    project_type: str = "apexsigma"  # "apexsigma" | "vida_caffe"
) -> dict:
    """Store current session context with project-specific granularity"""

@mcp_tool("restore_session_context") 
async def restore_session_context(
    session_id: Optional[str] = None,
    working_directory: Optional[str] = None
) -> dict:
    """Restore last session context for directory or specific session"""

@mcp_tool("query_working_directory_context")
async def query_working_directory_context(
    directory_path: str,
    time_range_hours: int = 24
) -> List[dict]:
    """Get all recent context for a working directory"""
```

### Phase 2: Semantic Enhancement Plugin (Week 2)

#### Vector Store Migration Strategy:

```python
# Current: NumPy + sentence-transformers
# Target: ChromaDB or Qdrant for production scale

@mcp_tool("search_semantic_context")
async def search_semantic_context(
    query: str,
    context_types: List[str] = ["session", "episodic"],
    project_filter: Optional[str] = None,
    similarity_threshold: float = 0.7
) -> List[dict]:
    """Semantic search across all stored contexts"""

@mcp_tool("store_episodic_event")
async def store_episodic_event(
    session_id: str,
    event_type: str,  # "file_change" | "command_exec" | "debug_session"
    file_path: Optional[str] = None,
    change_summary: str = "",
    semantic_tags: List[str] = [],
    granularity_level: str = "standard"  # "minimal" | "standard" | "detailed"
) -> dict:
    """Store episodic memory with adaptive granularity"""
```

### Phase 3: Cross-Tool Handoff Plugin (Week 3)

#### Container-Aware Context Handoff:

```python
@mcp_tool("export_context_snapshot")
async def export_context_snapshot(
    session_id: str,
    target_tool: str,
    include_files: bool = True,
    include_container_state: bool = True
) -> dict:
    """Export context for handoff to another tool"""

@mcp_tool("import_context_snapshot") 
async def import_context_snapshot(
    snapshot_data: dict,
    merge_strategy: str = "overlay"  # "replace" | "overlay" | "selective"
) -> dict:
    """Import context from another tool session"""

@mcp_tool("sync_container_context")
async def sync_container_context(
    container_name: Optional[str] = None,
    working_directory: str = "/workspace"
) -> dict:
    """Sync context with VS Code dev container state"""
```

### Adaptive Granularity Implementation

#### Project-Specific Context Levels:

```python
GRANULARITY_CONFIGS = {
    "apexsigma": {
        "file_tracking": "detailed",  # Track imports, dependencies, AST changes
        "command_history": 50,
        "semantic_indexing": True,
        "episodic_events": ["architecture_decisions", "debugging_sessions", "refactors"]
    },
    "vida_caffe": {
        "file_tracking": "standard",  # Track file changes, not internal structure
        "command_history": 20,
        "semantic_indexing": False,  # Excel analysis doesn't need semantic search
        "episodic_events": ["data_analysis", "report_generation"]
    },
    "minimal": {
        "file_tracking": "basic",     # Just file paths and timestamps
        "command_history": 10,
        "semantic_indexing": False,
        "episodic_events": []
    }
}
```

### Container-Aware Implementation

#### VS Code Dev Container Integration:

```python
async def detect_container_environment():
    """Auto-detect if running in VS Code dev container"""
    container_indicators = [
        "/vscode/vscode-server",
        "/.devcontainer",
        os.environ.get("REMOTE_CONTAINERS", False)
    ]
    return any(indicator for indicator in container_indicators)

async def sync_container_workspace():
    """Sync with container workspace state"""
    if await detect_container_environment():
        workspace_root = "/workspace"
        git_info = await get_git_context(workspace_root)
        docker_info = await get_container_metadata()
        return {
            "container_context": True,
            "workspace_root": workspace_root,
            "git_branch": git_info.get("branch"),
            "container_image": docker_info.get("image"),
            "mount_points": docker_info.get("mounts", [])
        }
```

### Vector Store Migration Plan

#### Current → Target Migration:

```python
# Phase 1: Dual-write implementation
async def store_with_dual_backend(text: str, metadata: dict):
    # Write to current NumPy system
    await store_numpy_vector(text, metadata)
    
    # Write to new specialized vector store  
    await store_specialized_vector(text, metadata)

# Phase 2: Gradual migration with fallback
async def search_with_fallback(query: str, threshold: float):
    try:
        results = await search_specialized_vector(query, threshold)
        if len(results) < 3:  # Fallback if insufficient results
            numpy_results = await search_numpy_vector(query, threshold)
            results.extend(numpy_results)
    except Exception:
        results = await search_numpy_vector(query, threshold)
    return results
```

### Plugin Registry Implementation

```python
# /core/plugin_registry.py
class PluginRegistry:
    def __init__(self):
        self.plugins = {}
        
    def register_plugin(self, name: str, plugin_instance):
        """Register a plugin with the MCP server"""
        self.plugins[name] = plugin_instance
        
    async def get_tools(self):
        """Aggregate all tools from registered plugins"""
        all_tools = []
        for plugin in self.plugins.values():
            all_tools.extend(await plugin.get_tools())
        return all_tools
        
    async def handle_tool_call(self, tool_name: str, arguments: dict):
        """Route tool calls to appropriate plugin"""
        for plugin in self.plugins.values():
            if await plugin.handles_tool(tool_name):
                return await plugin.handle_tool_call(tool_name, arguments)
        raise ToolNotFoundError(tool_name)
```

### Implementation Timeline

#### Week 1: Context Plugin Foundation
- [ ] Implement plugin registry architecture
- [ ] Create core context storage/retrieval tools
- [ ] Add adaptive granularity based on project type
- [ ] Container environment detection

#### Week 2: Semantic Enhancement 
- [ ] Design vector store migration strategy
- [ ] Implement semantic search tools
- [ ] Add episodic event storage with tagging
- [ ] Create dual-backend write system

#### Week 3: Cross-Tool Handoff
- [ ] Build context export/import mechanisms
- [ ] Implement container-aware sync
- [ ] Add working directory context queries
- [ ] Create CLI wrapper integration points

### Success Metrics

#### Technical Validation:
- [ ] Plugin system loads and registers tools correctly
- [ ] Context storage/retrieval works across container restarts
- [ ] Semantic search returns relevant results within 500ms
- [ ] Cross-tool handoff preserves working directory state

#### Workflow Validation:
- [ ] ApexSigma development sessions restore correctly
- [ ] Vida e Caffe analysis contexts use appropriate granularity
- [ ] Container-aware sync works in VS Code dev containers
- [ ] Episodic memory captures meaningful development events

### Integration Readiness

This plugin architecture provides immediate CLI wrapper integration points:

```bash
# Terminal command integration ready:
gmem() {
    # Store context before Gemini CLI session
    curl -X POST memOS/store_session_context -d "{session context}"
    
    # Run Gemini CLI
    gemini-cli "$@"
    
    # Update context after session
    curl -X POST memOS/store_episodic_event -d "{session summary}"
}
```

**Ready to proceed with Week 1 implementation?**