# GitHub Copilot Instructions for ApexSigma Ecosystem

## ⚠️ **MANDATORY: OMEGA INGEST CONTEXT RETRIEVAL PROTOCOL**

**BEFORE MAKING ANY CODE CHANGES**, you MUST:

1. **Query InGest-LLM API** for relevant context: `http://172.26.0.12:8000/query_context`
2. **Retrieve from memOS Omega Ingest**: `http://172.26.0.13:8090/memory/query`
3. **Validate against immutable truth**: Ensure changes don't conflict with verified infrastructure
4. **Obtain dual verification**: For Tier 1 infrastructure changes, require verification from another AI assistant

**Protected Services (DO NOT MODIFY WITHOUT VERIFICATION)**:
- memOS API (172.26.0.13) - Omega Ingest Guardian
- Neo4j Knowledge Graph (172.26.0.14) - Immutable concept relationships
- PostgreSQL Main (172.26.0.2) - Procedural memory
- InGest-LLM API (172.26.0.12) - Data ingestion gateway

## Project Overview

This directory, `MCP_Server_Builds`, contains the source code and deployment configurations for implementing **Model Context Protocol (MCP) servers** for two core microservices within the ApexSigma ecosystem: `memos.as` and `InGest-LLM.as`. These MCP servers will enable AI assistants to have standardized, secure access to memory operations and data ingestion capabilities, forming the foundation of the "DevEnviro" AI-supported development environment.

### MCP Development Phases

**PHASE 1: Infrastructure Preparation** (Current Focus)
- Docker network configuration for MCP isolation (172.28.0.0/16 subnet)
- JWT authentication and service accounts for AI assistants
- Rate limiting and audit logging for MCP operations
- Langfuse tracing and Prometheus metrics for MCP endpoints

**PHASE 2: memOS MCP Extension**
- Agent-specific memory tiers (MCP_GEMINI, MCP_COPILOT, etc.)
- Omega Ingest integration with POML processing
- Cross-agent knowledge sharing via confidence-scored queries
- Multi-layer caching (In-memory → Redis → DB)

**PHASE 3: InGestLLM MCP Extension**
- Tokenization pipeline with Tekken tokenizer
- Web scraping and GitHub repository ingestion
- Code-aware content extraction using AST parsing
- Token quality validation and context preservation scoring

### Core Projects
- **memos.as**: Memory Operating System (FastAPI, PostgreSQL, Qdrant, Redis) - Cognitive core with persistent memory
- **InGest-LLM.as**: Intelligent content ingestion engine (FastAPI, OpenTelemetry, Langfuse) - Data ingestion gateway

### Infrastructure Stack
- **Databases**: PostgreSQL (procedural memory), Redis (working memory), Qdrant (vector/semantic memory), Neo4j (knowledge graphs)
- **Observability**: Grafana, Prometheus, Jaeger, Loki, Langfuse
- **Monitoring**: OpenTelemetry distributed tracing, structured logging
- **MCP Infrastructure**: Dedicated Docker network, JWT auth, rate limiting, audit logging

## Development Commands

### Prerequisites
- Python 3.13+
- Docker Desktop
- Poetry for dependency management


### Per-Project Development

#### memos.as (Memory System)
```bash
cd memos.as
poetry install && poetry shell
poetry run uvicorn app.main:app --reload

# Quality checks
poetry run ruff check . && poetry run ruff format .
poetry run mypy app/
poetry run pytest
```

#### InGest-LLM.as (Ingestion Engine)
```bash
cd InGest-LLM.as
poetry install && poetry shell
poetry run uvicorn src.ingest_llm_as.main:app --reload

# Code quality
poetry run ruff check . && poetry run ruff format .
poetry run mypy src/
poetry run pytest
```

## Key Development Patterns

### Memory Protocol (memos.as)
All AI agents follow standardized memory interaction patterns:
1. **Session Initialization**: Check existing context, load project state
2. **Retrieve First, Store Last**: Query memory before storing
3. **User Confirmation Required**: All write/update/delete operations need approval
4. **Dynamic Context Retrieval**: RAG with full-text search and semantic search

### Society of Agents Collaboration
- **@Copilot**: Frontend development and integration work
- **@Gemini**: CLI implementation and backend development
- **@Qwen**: Code review and quality assurance
- **Mandatory Agent Review (MAR)**: All artifacts require review before integration

### MCP Development Patterns

**Phase 1 (Infrastructure) Focus:**
- Implement JWT authentication for all MCP endpoints
- Create dedicated service accounts for each AI assistant (MCP_COPILOT, MCP_GEMINI, MCP_QWEN)
- Configure rate limiting per service account
- Set up audit logging for critical MCP operations
- Extend Langfuse configuration for MCP-specific tracing

**Phase 2 (memOS MCP) Patterns:**
- Use agent-specific memory tiers for isolation
- Implement POML processor for knowledge graph nodes
- Apply confidence scoring for cross-agent knowledge sharing
- Follow multi-layer caching strategy (In-memory → Redis → DB)

**Phase 3 (InGestLLM MCP) Patterns:**
- Integrate Tekken tokenizer with custom MCP patterns
- Implement context-aware token weighting
- Use AST parsing for code-aware content extraction
- Apply token quality metrics and validation

## Service Integration Points

### Database Layer
- **PostgreSQL**: Procedural memory with complex schemas (agent_communications, knowledge_documents)
- **Redis**: Working memory and caching (session state, LLM responses)
- **Qdrant**: Vector database for episodic/semantic search (embeddings, RAG)
- **Neo4j**: Semantic relationships and knowledge graphs (concept relationships)

### API Endpoints
- **memOS API**: http://localhost:8090 (/docs) - Memory operations, tool registry
- **InGest-LLM**: http://localhost:8000 (/docs) - Data ingestion, context retrieval
- **Grafana**: http://localhost:3000 - Monitoring dashboards
- **Prometheus**: http://localhost:9090 - Metrics collection
- **Jaeger**: http://localhost:16686 - Distributed tracing

### Cross-Service Communication
- **OpenTelemetry**: Distributed tracing across all services
- **Langfuse**: LLM-specific observability and performance monitoring

### MCP Service Integration
- **MCP Network**: Dedicated Docker network (172.28.0.0/16) for isolation
- **Service Accounts**: Dedicated accounts for each AI assistant (MCP_COPILOT, MCP_GEMINI, MCP_QWEN)
- **Authentication**: JWT-based authentication for all MCP endpoints
- **Rate Limiting**: Per-service account rate limiting and audit logging
- **MCP Endpoints**: Standardized protocol endpoints for memory and ingestion operations

## Code Quality Standards

### Modern Python Toolchain
All projects use:
- **Poetry**: Dependency management and virtual environments
- **Ruff**: Lightning-fast linting and formatting (replaces flake8, black, isort)
- **mypy**: Static type checking with strict mode
- **pytest**: Testing framework with async support
- **pre-commit**: Automated quality checks on commits

### FastAPI Patterns
- **Dependency Injection**: Use FastAPI's dependency system for database clients, observability
- **Pydantic Models**: Strict validation for all request/response models
- **Middleware**: CORS, observability, error handling
- **Async/Await**: All I/O operations are async for performance

### Observability Integration
- **Structured Logging**: Use structlog for consistent log format
- **Metrics**: Prometheus client for custom metrics
- **Tracing**: OpenTelemetry spans for request tracing
- **Health Checks**: Comprehensive health endpoints for all services

## Project-Specific Conventions

### Memory Operations
```python
# Always retrieve before storing
existing = await memory_client.query_memory(context_id)
if existing:
    # Update existing memory
    await memory_client.update_memory(memory_id, new_data)
else:
    # Store new memory
    await memory_client.store_memory(context_data)
```


## Development Workflow

When working in this workspace:
1. **Follow OMEGA Protocol**: Query context APIs before changes
2. **Use unified Docker stack** for infrastructure development
3. **Respect memory protocol** for context operations
4. **Leverage observability stack** for monitoring and debugging
5. **Document as you code** - update docstrings and markdown for automatic docs
6. **Test individually per project** - no workspace-wide test runner
7. **Follow MAR Protocol** - get reviews from other AI assistants

### Phase-Specific Development Guidance

**Current Phase (Infrastructure Preparation):**
- Focus on Docker network configuration (172.28.0.0/16 subnet)
- Implement JWT authentication and service accounts
- Set up rate limiting and audit logging
- Configure MCP-specific observability (Langfuse, Prometheus)

**When Moving to Phase 2 (memOS MCP):**
- Implement agent-specific memory tiers
- Integrate Omega Ingest with POML processing
- Develop cross-agent knowledge sharing
- Optimize with multi-layer caching

**When Moving to Phase 3 (InGestLLM MCP):**
- Build tokenization pipeline with Tekken tokenizer
- Implement web scraping and GitHub ingestion
- Add code-aware content extraction
- Develop quality validation and scoring

## Key Files and Directories

### Core Architecture Files
- `memos.as/app/main.py`: Memory service FastAPI application
- `InGest-LLM.as/src/ingest_llm_as/main.py`: Ingestion service entry point
- `memos.as/app/mcp_server.py`: MCP server implementation for memory operations
- `InGest-LLM.as/src/ingest_llm_as/mcp_server.py`: MCP server implementation for ingestion
- `docker-compose.unified.yml`: Complete infrastructure definition

### MCP Development Files
- `MCP Server Build Plan memOS & InGestLLM.yml`: Comprehensive MCP implementation roadmap
- `.github/copilot-instructions.md`: These AI agent instructions
- `memos.as/config/`: Observability and infrastructure configs

### Configuration Files
- `memos.as/pyproject.toml`: Poetry dependencies and scripts
- `InGest-LLM.as/pyproject.toml`: Project configuration
- `memos.as/config/prometheus.yml`: Metrics collection configuration
- `memos.as/config/otel-collector-config.yaml`: OpenTelemetry configuration

### Documentation
- `COPILOT.md`, `GEMINI.md`, `QWEN.md`: Agent-specific instructions
- `docs/`: Project-specific documentation
- `README.md`: Project overviews
- `OPERATION_ASGARD_REBIRTH_BASELINE.md`: Operation baseline documentation

The ecosystem represents a complete AI development platform where agents learn, remember, and collaborate to solve complex development challenges through structured multi-agent workflows.</content>
<parameter name="filePath">c:\Users\steyn\ApexSigmaProjects.Dev\MCP_Server_Builds\.github\copilot-instructions.md
