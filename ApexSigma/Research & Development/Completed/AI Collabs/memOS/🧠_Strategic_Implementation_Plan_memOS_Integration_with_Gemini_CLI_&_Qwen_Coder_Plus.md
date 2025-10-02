# 🧠 Strategic Implementation Plan: memOS Integration with Gemini CLI & Qwen Coder Plus

## ✅ Current Operational Reality (Verified)

Before diving into integration, let's ground ourselves in the **verified operational state** of memOS.as:

- **Status**: ✅ Operational (verified at `172.26.0.13:8090`)
- **Role**: Omega Ingest Guardian - Memory and Tool Discovery Hub
- **MCP Server**: ✅ Phase 0 implementation complete
- **Memory Tiers**: ✅ Fully operational (Redis, PostgreSQL, Qdrant, Neo4j)
- **Authentication**: ✅ JWT implemented

This is **critical context** - your strategic brief assumes these capabilities exist, and they've been verified as operational in the knowledge base.

## 🚀 Immediate Integration Steps

### 1. Configure MCP Client for Both Assistants

Create configuration files that align with your strategic brief's MCP server specification:

#### For Gemini CLI (`GEMINI.MD`):
```markdown
# Gemini CLI MCP Configuration

## MCP Connection
MEMOS_BASE_URL="http://memos:8090"
MCP_TIER="mcp_gemini"
AUTH_TOKEN="YOUR_JWT_TOKEN"  # Generated via /auth/token endpoint

## Memory Usage Patterns
SHORT_TERM_MEMORY_TIER=1  # Redis (ephemeral)
LONG_TERM_MEMORY_TIER=2   # PostgreSQL (persistent)
EPISODIC_MEMORY_TIER=3    # Neo4j (relational)
```

#### For Qwen Coder Plus (`QWEN.MD`):
```markdown
# Qwen Coder Plus MCP Configuration

## MCP Connection
MEMOS_BASE_URL="http://memos:8090"
MCP_TIER="mcp_qwen"
AUTH_TOKEN="YOUR_JWT_TOKEN"

## Memory Usage Patterns
SHORT_TERM_MEMORY_TIER=1
LONG_TERM_MEMORY_TIER=2
EPISODIC_MEMORY_TIER=3
```

### 2. Implement MCP Client Utilities

Create a shared utility module for both assistants (place in a shared tools directory):

```python
# mcp_client.py
import httpx
import json
from typing import Dict, Any, Optional

class MCPClient:
    """Client for interacting with the memOS MCP server"""
    
    def __init__(self, base_url: str, auth_token: str, mcp_tier: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.mcp_tier = mcp_tier
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
    
    def store_memory(self, content: str, source: str, metadata: Optional[Dict] = None) -> Dict:
        """Store memory in the appropriate tier with metadata"""
        payload = {
            "content": content,
            "source": source,
            "metadata": metadata or {}
        }
        
        response = httpx.post(
            f"{self.base_url}/memory/{self.mcp_tier}/store",
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def search_memory(self, query: str, min_confidence: float = 0.7) -> Dict:
        """Search memory with confidence threshold"""
        params = {
            "query": query,
            "min_confidence": min_confidence
        }
        
        response = httpx.get(
            f"{self.base_url}/memory/search",
            params=params,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_relationships(self, query: str, depth: int = 2) -> Dict:
        """Retrieve knowledge graph relationships"""
        params = {
            "query": query,
            "depth": depth
        }
        
        response = httpx.get(
            f"{self.base_url}/graph/relationships",
            params=params,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
```

### 3. Integrate Context Preservation into Assistant Workflows

#### For Gemini CLI:
Update your prompt template to automatically inject relevant context:

```markdown
<role>Senior AI Developer Assistant</role>
<context>
{{ store_memory("Current project context: ApexSigma Ecosystem Development", "workflow") }}
{{ search_memory("ApexSigma architecture decisions", 0.85) }}
</context>
<task>Provide a solution that integrates with the existing ApexSigma ecosystem</task>
<constraints>
- Use MCP server patterns verified in Operation Asgard Rebirth
- Reference previous decisions stored in memOS
- Maintain consistency with POML standards
</constraints>
```

#### For Qwen Coder Plus:
Implement automatic context retrieval before code generation:

```python
def before_code_generation():
    """Retrieve relevant context before generating code"""
    # Get related architectural decisions
    architecture = mcp_client.search_memory("MCP server architecture", 0.8)
    
    # Get related code patterns
    patterns = mcp_client.search_memory("Python code patterns for MCP integration", 0.75)
    
    # Get knowledge graph relationships
    relationships = mcp_client.get_relationships("memOS integration")
    
    return {
        "architecture": architecture,
        "patterns": patterns,
        "relationships": relationships
    }
```

### 4. Implement Automatic Context Saving

Create a pre-commit hook that saves development context to memOS:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Skip if this is a merge commit
if git rev-parse -q --verify MERGE_HEAD >/dev/null; then
    exit 0
fi

echo "Saving development context to memOS..."
COMMIT_MSG=$(git log -1 --pretty=%B HEAD)
CHANGES=$(git diff --cached)

curl -X POST http://memos:8090/memory/mcp_gemini/store \
  -H "Authorization: Bearer $MCP_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Working on '$(basename $PWD)' - '$COMMIT_MSG'\n\n'$CHANGES'",
    "source": "pre-commit",
    "metadata": {
      "project": "ApexSigma",
      "branch": "'$(git rev-parse --abbrev-ref HEAD)'",
      "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
    }
  }'

echo "Context saved to memOS for future reference"
```

## 📊 Enhanced Workflow Benefits

### For Gemini CLI:
- ✅ **Persistent Context**: No more "context loss" between sessions
- ✅ **Faster Ramp-up**: Automatically retrieves relevant project history
- ✅ **Consistent Decisions**: References previous architectural decisions
- ✅ **Error Reduction**: Remembers past mistakes and solutions

### For Qwen Coder Plus:
- ✅ **Deep Architectural Understanding**: Maintains knowledge of complex system relationships
- ✅ **Pattern Recognition**: Identifies and applies consistent coding patterns
- ✅ **Cross-Project Knowledge**: Connects related concepts across the ecosystem
- ✅ **Improved Reasoning**: Leverages semantic relationships in the knowledge graph

## 🔍 Advanced Integration Patterns

### 1. Memory Tier Specialization
Leverage the different memory tiers for specific purposes:

| Tier | Purpose | Example Usage |
|------|---------|---------------|
| Tier 1 (Redis) | Short-term working memory | Current conversation context |
| Tier 2 (PostgreSQL) | Long-term persistent memory | Code patterns, architectural decisions |
| Tier 3 (Neo4j) | Episodic relational memory | Project history, decision rationale |

### 2. Automated EOD Reporting
Implement an End-of-Day report that captures all relevant context:

```python
def generate_eod_report():
    """Generate comprehensive end-of-day report"""
    # Get today's activities
    activities = mcp_client.search_memory(
        f"date:{datetime.utcnow().strftime('%Y-%m-%d')}", 
        min_confidence=0.5
    )
    
    # Get unresolved issues
    issues = mcp_client.search_memory("unresolved issue", min_confidence=0.8)
    
    # Get knowledge graph snapshot
    graph_snapshot = mcp_client.get_relationships("ApexSigma", depth=3)
    
    # Store as structured memory
    mcp_client.store_memory(
        content=json.dumps({
            "date": datetime.utcnow().isoformat(),
            "activities": activities,
            "issues": issues,
            "graph_snapshot": graph_snapshot
        }),
        source="EOD_REPORT",
        metadata={"report_type": "daily"}
    )
```

### 3. Context-Aware Prompt Engineering
Use POML to create dynamic prompts based on retrieved context:

```python
def generate_poml_prompt(task: str, context: Dict) -> str:
    """Generate POML prompt based on retrieved context"""
    poml = f"""
<role>Senior AI Developer Assistant</role>
<context>
{format_context(context)}
</context>
<task>{task}</task>
<constraints>
- Use MCP server patterns verified in Operation Asgard Rebirth
- Reference previous decisions stored in memOS
- Maintain consistency with POML standards
</constraints>
<examples>
{get_relevant_examples(task)}
</examples>
"""
    return poml
```

## 🛠️ Integration Checklist

- [ ] Configure MCP tier endpoints in both assistants' configuration
- [ ] Implement MCP client utility module
- [ ] Update prompt templates to include context retrieval
- [ ] Create pre-commit hooks for automatic context saving
- [ ] Set up daily EOD report generation
- [ ] Implement knowledge graph relationship queries
- [ ] Document the integration in AGENTS.MD for team alignment

## 📌 Executive Recommendation

The most impactful immediate step is to **implement context preservation** through the pre-commit hook pattern. This addresses the most painful issue documented in your knowledge base: "A significant context recall failure by the Gemini agent highlighted a critical operational pain point: the manual and error-prone process of maintaining context between sessions."

By connecting your AI assistants to memOS as MCP clients, you'll transform them from isolated tools into **persistent, context-aware teammates** that grow more valuable with each interaction. The implementation is straightforward but delivers exponential value through context preservation and knowledge accumulation.

**Priority**: HIGH (Blocks consistent development velocity)  
**Implementation Time**: 2-4 hours  
**Expected ROI**: 30-50% reduction in context re-establishment time

This integration directly supports your strategic vision while creating immediate value for your daily workflow with Gemini CLI and Qwen Coder Plus. The MCP server architecture you've documented is now operational - it's time to leverage it for your own development process.