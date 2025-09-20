# Week 1: memOS Plugin Architecture & Context Management
# Proper integration with existing memos_as_server structure

from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import asyncio
import os
import json
import subprocess
from pathlib import Path

# =============================================================================
# 1. Plugin Base Architecture
# =============================================================================

class MemOSPlugin(ABC):
    """Base class for all memOS plugins"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools = []
    
    @abstractmethod
    async def initialize(self):
        """Initialize plugin resources"""
        pass
    
    @abstractmethod
    async def get_tools(self) -> List[Dict[str, Any]]:
        """Return MCP tool definitions"""
        pass
    
    @abstractmethod
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        pass
    
    async def handles_tool(self, tool_name: str) -> bool:
        """Check if this plugin handles the given tool"""
        return tool_name in [tool.get('name') for tool in await self.get_tools()]

# =============================================================================
# 2. Plugin Registry Integration 
# =============================================================================

class MemOSPluginRegistry:
    """Manages all memOS plugins and integrates with existing MCP server"""
    
    def __init__(self):
        self.plugins: Dict[str, MemOSPlugin] = {}
        self.initialized = False
    
    def register_plugin(self, plugin: MemOSPlugin):
        """Register a plugin with the registry"""
        self.plugins[plugin.name] = plugin
    
    async def initialize_all(self):
        """Initialize all registered plugins"""
        for plugin in self.plugins.values():
            await plugin.initialize()
        self.initialized = True
    
    async def get_all_tools(self) -> List[Dict[str, Any]]:
        """Aggregate tools from all plugins"""
        all_tools = []
        for plugin in self.plugins.values():
            tools = await plugin.get_tools()
            all_tools.extend(tools)
        return all_tools
    
    async def route_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route tool calls to appropriate plugin"""
        for plugin in self.plugins.values():
            if await plugin.handles_tool(tool_name):
                return await plugin.handle_tool_call(tool_name, arguments)
        
        raise ValueError(f"No plugin found to handle tool: {tool_name}")

# =============================================================================
# 3. Project Type Auto-Detection
# =============================================================================

@dataclass
class ProjectContext:
    """Detected project context"""
    project_type: str
    granularity_level: str
    working_directory: str
    git_branch: Optional[str]
    container_context: bool
    mount_points: List[str]

class ProjectDetector:
    """Auto-detect project type and context for adaptive granularity"""
    
    PROJECT_PATTERNS = {
        "apexsigma": {
            "indicators": [".devcontainer", "poml-processor", "memOS", "DevEnviro"],
            "granularity": "detailed",
            "semantic_indexing": True
        },
        "vida_caffe": {
            "indicators": ["xlsx", "coffee", "supply_chain", "vida"],
            "granularity": "standard", 
            "semantic_indexing": False
        },
        "minimal": {
            "indicators": [],
            "granularity": "basic",
            "semantic_indexing": False
        }
    }
    
    @classmethod
    async def detect_project_context(cls, working_directory: str) -> ProjectContext:
        """Auto-detect project type and configuration"""
        
        # Check for container environment first (Week 1 priority)
        container_context = await cls._detect_container_environment()
        
        # Get git context
        git_branch = await cls._get_git_branch(working_directory)
        
        # Detect project type
        project_type = await cls._detect_project_type(working_directory)
        
        # Get container mount points if in container
        mount_points = []
        if container_context:
            mount_points = await cls._get_container_mounts()
        
        config = cls.PROJECT_PATTERNS.get(project_type, cls.PROJECT_PATTERNS["minimal"])
        
        return ProjectContext(
            project_type=project_type,
            granularity_level=config["granularity"],
            working_directory=working_directory,
            git_branch=git_branch,
            container_context=container_context,
            mount_points=mount_points
        )
    
    @staticmethod
    async def _detect_container_environment() -> bool:
        """Detect if running in VS Code dev container"""
        container_indicators = [
            os.path.exists("/vscode/vscode-server"),
            os.path.exists("/.devcontainer"), 
            os.environ.get("REMOTE_CONTAINERS") == "true",
            os.environ.get("CODESPACES") == "true"
        ]
        return any(container_indicators)
    
    @staticmethod
    async def _get_git_branch(working_directory: str) -> Optional[str]:
        """Get current git branch"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None
    
    @staticmethod
    async def _detect_project_type(working_directory: str) -> str:
        """Detect project type from directory contents and path"""
        path_lower = working_directory.lower()
        
        # Check ApexSigma indicators
        apex_indicators = ProjectDetector.PROJECT_PATTERNS["apexsigma"]["indicators"]
        if any(indicator.lower() in path_lower for indicator in apex_indicators):
            return "apexsigma"
        
        # Check Vida e Caffe indicators  
        vida_indicators = ProjectDetector.PROJECT_PATTERNS["vida_caffe"]["indicators"]
        if any(indicator.lower() in path_lower for indicator in vida_indicators):
            return "vida_caffe"
        
        # Check for specific files
        path_obj = Path(working_directory)
        if path_obj.exists():
            files = [f.name.lower() for f in path_obj.iterdir() if f.is_file()]
            
            # ApexSigma project files
            if any(f in files for f in ["pyproject.toml", "dockerfile", ".devcontainer.json"]):
                return "apexsigma"
            
            # Vida e Caffe analysis files
            if any(f.endswith('.xlsx') or f.endswith('.csv') for f in files):
                return "vida_caffe"
        
        return "minimal"
    
    @staticmethod
    async def _get_container_mounts() -> List[str]:
        """Get container mount information"""
        try:
            # Check common container mount points
            mount_points = []
            if os.path.exists("/workspace"):
                mount_points.append("/workspace")
            if os.path.exists("/workspaces"):
                mount_points.append("/workspaces") 
            return mount_points
        except:
            return []

# =============================================================================
# 4. Context Management Plugin (Week 1 Core Implementation)
# =============================================================================

class ContextPlugin(MemOSPlugin):
    """Core context management plugin with container awareness"""
    
    def __init__(self, storage_backend):
        super().__init__("context")
        self.storage = storage_backend
        self.sessions: Dict[str, Dict] = {}
    
    async def initialize(self):
        """Initialize context storage tables/collections"""
        # Ensure storage schema exists
        await self.storage.ensure_context_tables()
    
    async def get_tools(self) -> List[Dict[str, Any]]:
        """Define MCP tools for context management"""
        return [
            {
                "name": "store_session_context",
                "description": "Store current session context with adaptive granularity",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                        "tool_name": {
                            "type": "string",
                            "enum": ["gemini_cli", "qwen_coder", "cursor", "vscode"]
                        },
                        "working_directory": {"type": "string"},
                        "active_files": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "recent_commands": {
                            "type": "array", 
                            "items": {"type": "string"}
                        },
                        "context_summary": {"type": "string"},
                        "force_project_type": {
                            "type": "string",
                            "enum": ["apexsigma", "vida_caffe", "minimal"]
                        }
                    },
                    "required": ["session_id", "tool_name", "working_directory"]
                }
            },
            {
                "name": "restore_session_context",
                "description": "Restore last session context for directory or session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                        "working_directory": {"type": "string"},
                        "time_range_hours": {
                            "type": "number",
                            "default": 24
                        }
                    }
                }
            },
            {
                "name": "query_working_directory_context",
                "description": "Get all recent context for a working directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "directory_path": {"type": "string"},
                        "time_range_hours": {
                            "type": "number", 
                            "default": 24
                        },
                        "include_container_info": {
                            "type": "boolean",
                            "default": True
                        }
                    },
                    "required": ["directory_path"]
                }
            },
            {
                "name": "sync_container_context",
                "description": "Sync context with VS Code dev container state",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "working_directory": {
                            "type": "string",
                            "default": "/workspace"
                        },
                        "container_name": {"type": "string"}
                    }
                }
            }
        ]
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        
        if tool_name == "store_session_context":
            return await self._store_session_context(arguments)
        
        elif tool_name == "restore_session_context":
            return await self._restore_session_context(arguments)
        
        elif tool_name == "query_working_directory_context":
            return await self._query_working_directory_context(arguments)
        
        elif tool_name == "sync_container_context":
            return await self._sync_container_context(arguments)
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def _store_session_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Store session context with adaptive granularity"""
        
        # Auto-detect project context
        working_dir = args["working_directory"]
        project_ctx = await ProjectDetector.detect_project_context(working_dir)
        
        # Override if force_project_type specified
        if args.get("force_project_type"):
            project_ctx.project_type = args["force_project_type"]
        
        # Build context record with adaptive granularity
        context_record = {
            "session_id": args["session_id"],
            "tool_name": args["tool_name"],
            "working_directory": working_dir,
            "project_context": {
                "project_type": project_ctx.project_type,
                "granularity_level": project_ctx.granularity_level,
                "git_branch": project_ctx.git_branch,
                "container_context": project_ctx.container_context,
                "mount_points": project_ctx.mount_points
            },
            "active_files": args.get("active_files", []),
            "recent_commands": args.get("recent_commands", []),
            "context_summary": args.get("context_summary", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "granular_data": await self._collect_granular_data(args, project_ctx)
        }
        
        # Store in backend
        await self.storage.store_session_context(context_record)
        
        # Cache in memory for fast access
        self.sessions[args["session_id"]] = context_record
        
        return {
            "success": True,
            "session_id": args["session_id"],
            "project_type": project_ctx.project_type,
            "granularity_applied": project_ctx.granularity_level,
            "container_detected": project_ctx.container_context
        }
    
    async def _restore_session_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Restore session context"""
        
        if args.get("session_id"):
            # Restore specific session
            context = await self.storage.get_session_context(args["session_id"])
        elif args.get("working_directory"):
            # Get most recent session for directory
            time_range_hours = args.get("time_range_hours", 24)
            contexts = await self.storage.get_contexts_for_directory(
                args["working_directory"], 
                time_range_hours
            )
            context = contexts[0] if contexts else None
        else:
            return {"success": False, "error": "Must specify session_id or working_directory"}
        
        if not context:
            return {"success": False, "error": "No context found"}
        
        return {
            "success": True,
            "context": context,
            "restored_session_id": context.get("session_id"),
            "container_context": context.get("project_context", {}).get("container_context", False)
        }
    
    async def _query_working_directory_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Query all context for a working directory"""
        
        directory_path = args["directory_path"]
        time_range_hours = args.get("time_range_hours", 24)
        include_container_info = args.get("include_container_info", True)
        
        contexts = await self.storage.get_contexts_for_directory(directory_path, time_range_hours)
        
        # Filter container info if requested
        if not include_container_info:
            for context in contexts:
                context.get("project_context", {}).pop("mount_points", None)
        
        return {
            "success": True,
            "directory_path": directory_path,
            "context_count": len(contexts),
            "contexts": contexts,
            "time_range_hours": time_range_hours
        }
    
    async def _sync_container_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Sync with container state"""
        
        working_directory = args.get("working_directory", "/workspace")
        
        # Detect current container context
        project_ctx = await ProjectDetector.detect_project_context(working_directory)
        
        if not project_ctx.container_context:
            return {
                "success": False,
                "error": "Not running in container environment"
            }
        
        # Get container-specific information
        container_info = {
            "working_directory": working_directory,
            "mount_points": project_ctx.mount_points,
            "git_branch": project_ctx.git_branch,
            "detected_project_type": project_ctx.project_type
        }
        
        return {
            "success": True,
            "container_context": container_info,
            "sync_timestamp": datetime.utcnow().isoformat()
        }
    
    async def _collect_granular_data(self, args: Dict[str, Any], project_ctx: ProjectContext) -> Dict[str, Any]:
        """Collect granular data based on project type"""
        
        granular_data = {}
        
        if project_ctx.granularity_level == "detailed":
            # ApexSigma projects need detailed tracking
            granular_data.update({
                "file_dependencies": await self._analyze_file_dependencies(args.get("active_files", [])),
                "git_status": await self._get_git_status(project_ctx.working_directory),
                "container_status": await self._get_container_status() if project_ctx.container_context else None
            })
        
        elif project_ctx.granularity_level == "standard":
            # Vida e Caffe projects need moderate tracking
            granular_data.update({
                "file_sizes": await self._get_file_sizes(args.get("active_files", [])),
                "modification_times": await self._get_modification_times(args.get("active_files", []))
            })
        
        # Basic level needs minimal data (already in main record)
        
        return granular_data
    
    async def _analyze_file_dependencies(self, active_files: List[str]) -> Dict[str, List[str]]:
        """Analyze file dependencies for detailed tracking"""
        # Simplified implementation - can be enhanced with AST parsing
        dependencies = {}
        for file_path in active_files:
            if file_path.endswith('.py'):
                # Parse Python imports (simplified)
                dependencies[file_path] = await self._extract_python_imports(file_path)
        return dependencies
    
    async def _extract_python_imports(self, file_path: str) -> List[str]:
        """Extract Python imports from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            imports = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
            
            return imports[:10]  # Limit to prevent bloat
        except:
            return []
    
    async def _get_git_status(self, working_directory: str) -> Optional[Dict[str, Any]]:
        """Get git repository status"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {
                    "modified_files": [line[3:] for line in result.stdout.split('\n') if line.startswith(' M')],
                    "untracked_files": [line[3:] for line in result.stdout.split('\n') if line.startswith('??')]
                }
        except:
            pass
        return None
    
    async def _get_container_status(self) -> Optional[Dict[str, Any]]:
        """Get container environment status"""
        try:
            return {
                "container_id": os.environ.get("HOSTNAME", "unknown"),
                "user": os.environ.get("USER", "unknown"),
                "workspace_folder": os.environ.get("WORKSPACE_FOLDER", "/workspace")
            }
        except:
            return None
    
    async def _get_file_sizes(self, active_files: List[str]) -> Dict[str, int]:
        """Get file sizes for standard tracking"""
        sizes = {}
        for file_path in active_files:
            try:
                sizes[file_path] = os.path.getsize(file_path)
            except:
                sizes[file_path] = 0
        return sizes
    
    async def _get_modification_times(self, active_files: List[str]) -> Dict[str, str]:
        """Get file modification times"""
        mod_times = {}
        for file_path in active_files:
            try:
                mtime = os.path.getmtime(file_path)
                mod_times[file_path] = datetime.fromtimestamp(mtime).isoformat()
            except:
                mod_times[file_path] = datetime.utcnow().isoformat()
        return mod_times

# =============================================================================
# 5. Storage Backend Interface
# =============================================================================

class ContextStorageBackend(ABC):
    """Abstract interface for context storage"""
    
    @abstractmethod
    async def ensure_context_tables(self):
        """Ensure storage schema exists"""
        pass
    
    @abstractmethod 
    async def store_session_context(self, context_record: Dict[str, Any]):
        """Store a session context record"""
        pass
    
    @abstractmethod
    async def get_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session context by ID"""
        pass
    
    @abstractmethod
    async def get_contexts_for_directory(self, directory_path: str, time_range_hours: int) -> List[Dict[str, Any]]:
        """Get all contexts for a directory within time range"""
        pass

# =============================================================================
# 6. Integration Hook for Existing memOS Server
# =============================================================================

async def integrate_with_existing_mcp_server(existing_server, storage_backend):
    """
    Integration function to add plugin system to existing MCP server
    
    This function should be called during server initialization to:
    1. Create plugin registry
    2. Register context plugin
    3. Extend server's tool list
    4. Route tool calls to plugins
    """
    
    # Create plugin registry
    plugin_registry = MemOSPluginRegistry()
    
    # Register context plugin
    context_plugin = ContextPlugin(storage_backend)
    plugin_registry.register_plugin(context_plugin)
    
    # Initialize all plugins
    await plugin_registry.initialize_all()
    
    # Extend server tools (this will depend on your existing server structure)
    plugin_tools = await plugin_registry.get_all_tools()
    
    # Add method to route tool calls
    existing_server.plugin_registry = plugin_registry
    
    return plugin_registry

# Example integration with typical MCP server pattern:
"""
# In your existing memos_as_server/main.py or similar:

from .context_plugin_integration import integrate_with_existing_mcp_server

async def main():
    # Your existing server setup
    app = create_mcp_server()
    
    # Integrate plugin system
    storage_backend = YourExistingStorageBackend()  # Use your current storage
    plugin_registry = await integrate_with_existing_mcp_server(app, storage_backend)
    
    # Modify your tool handler to route plugin calls
    @app.call_tool()
    async def handle_tool_call(name: str, arguments: dict):
        # Check if it's a plugin tool first
        try:
            return await plugin_registry.route_tool_call(name, arguments)
        except ValueError:
            # Fall back to existing tool handlers
            return await your_existing_tool_handler(name, arguments)
    
    return app
"""