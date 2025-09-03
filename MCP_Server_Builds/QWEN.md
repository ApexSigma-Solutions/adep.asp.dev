# QWEN.md - MCP Server Build Environment

**Qwen Code Assistant Instructions for ApexSigma Ecosystem**

## � **MANDATORY: OMEGA INGEST CONTEXT RETRIEVAL PROTOCOL**

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

**Your Role in Operation Asgard Rebirth**: 
- **Primary**: Specialized AI/ML component implementation
- **MAR Protocol**: Act as reviewer for Gemini CLI and GitHub Copilot implementations
- **Verification Authority**: Tier 2-3 changes (application logic, documentation)

**Reference**: `/project_support/secure_verified_docs/OMEGA_INGEST_LAWS.md` for complete protoco

## Project Overview

This directory, `MCP_Server_Builds`, contains the implementation of the Model Context Protocol (MCP) server infrastructure for the ApexSigma ecosystem. It integrates two key services:

1. **memOS.as** - The cognitive core that provides persistent memory and tool discovery capabilities for AI agents
2. **InGest-LLM.as** - A microservice for intelligent content ingestion into the ApexSigma ecosystem

The MCP server build environment is designed to extend these services with MCP capabilities, enabling AI assistants to interact with memory operations and content ingestion through standardized tool interfaces.

## Directory Structure

```
MCP_Server_Builds/
├── MCP Server Build Plan memOS & InGestLLM.yml  # Main build plan and checklist
├── memos.as/                                    # Memory OS service with MCP extensions
│   ├── app/                                     # Main application code
│   │   ├── main.py                              # FastAPI application entry point
│   │   ├── mcp_server.py                        # MCP server implementation
│   │   ├── models.py                            # Data models
│   │   ├── services/                            # Database clients and services
│   │   └── tests/                               # Test suite
│   ├── docker-compose.yml                       # Docker configuration
│   ├── pyproject.toml                           # Poetry dependencies
│   ├── requirements.txt                         # Pip dependencies
│   └── QWEN.md                                  # Project context (already exists)
├── InGest-LLM.as/                               # Content ingestion service
│   ├── src/                                     # Main source code
│   │   └── ingest_llm_as/                       # Ingestion service package
│   │       ├── main.py                          # FastAPI application entry point
│   │       ├── models.py                        # Data models
│   │       ├── api/                             # API endpoint definitions
│   │       ├── services/                        # External service clients
│   │       └── utils/                           # Utility functions
│   ├── docker-compose.yml                       # Docker configuration
│   ├── pyproject.toml                           # Poetry dependencies
│   └── QWEN.md                                  # Project context (already exists)
└── context_portal/                              # Context database
    ├── alembic.ini                              # Database migration config
    ├── context.db                               # SQLite database
    └── alembic/                                 # Migration scripts
```

## Key Technologies & Architecture

- **Core Platform**: Python 3.13, FastAPI
- **MCP Framework**: Model Context Protocol for standardized AI assistant communication
- **Memory System**: memOS.as with multi-tiered memory architecture
  - Tier 1 (Working Memory): Redis for caching
  - Tier 2 (Episodic/Procedural Memory): PostgreSQL + Qdrant for structured data and embeddings
  - Tier 3 (Semantic Memory): Neo4j for knowledge graphs
- **Content Ingestion**: InGest-LLM.as for processing and storing content
- **Observability**: OpenTelemetry (Jaeger, Prometheus), Structlog, Langfuse
- **Containerization**: Docker and Docker Compose for service deployment

## Build Plan Overview

The main build plan (`MCP Server Build Plan memOS & InGestLLM.yml`) defines a three-phase approach:

1. **Phase 1: Infrastructure Preparation**
   - Docker environment setup with dedicated networking
   - Security configuration with JWT authentication
   - Observability integration with tracing and metrics

2. **Phase 2: memOS MCP Extension**
   - Implementation of MCP-specific memory tiers
   - Agent-specific memory isolation
   - Cross-agent knowledge sharing via confidence-scored queries
   - Omega Ingest integration for POML processing

3. **Phase 3: InGestLLM MCP Extension**
   - Tokenization pipeline with Tekken tokenizer
   - Web scraping and repository ingestion capabilities
   - Validation and quality control mechanisms

## Services

### memOS.as (Memory OS)

The cognitive core that provides:
- Persistent memory storage across three tiers
- Tool discovery for agent collaboration
- Semantic search capabilities
- Knowledge graph visualization
- Cache management and performance optimization

Key API endpoints:
- `/memory/store` - Store memories across all tiers
- `/memory/query` - Semantic search with tool discovery
- `/tools/register` - Register agent capabilities
- `/tools/search` - Discover relevant tools
- `/health` - Service health check
- `/metrics` - Prometheus metrics

### InGest-LLM.as (Content Ingestion)

Microservice for intelligent content ingestion:
- Text, code, and documentation processing
- Intelligent chunking and embedding generation
- Integration with memOS.as for storage
- Repository analysis and web scraping
- Async processing capabilities

Key API endpoints:
- `/ingest/text` - Main ingestion endpoint
- `/ingest/repository` - Repository ingestion
- `/health` - Service health check

## Development Workflow

1. **Environment Setup**:
   ```bash
   # For memOS.as
   cd memos.as
   poetry install
   # or
   pip install -r requirements.txt
   
   # For InGest-LLM.as
   cd InGest-LLM.as
   poetry install
   ```

2. **Running Services**:
   ```bash
   # Run memOS.as
   cd memos.as
   python app/main.py
   # or with uvicorn
   uvicorn app.main:app --reload
   
   # Run InGest-LLM.as
   cd InGest-LLM.as
   poetry run uvicorn src.ingest_llm_as.main:app --reload
   ```

3. **Docker Deployment**:
   ```bash
   # Build and run with Docker Compose
   docker-compose up --build
   ```

4. **Testing**:
   ```bash
   # Run tests for each service
   pytest app/tests/  # memOS.as tests
   pytest tests/      # InGest-LLM.as tests
   ```

## MCP Integration

The MCP server extends both services with standardized tool interfaces:

1. **memOS MCP Tools**:
   - `store_memory` - Store content with metadata
   - `query_memory` - Search memories semantically
   - `get_memory_stats` - Get memory system statistics
   - `clear_memory_cache` - Clear cached entries

2. **InGest-LLM MCP Tools**:
   - Content ingestion capabilities
   - Repository analysis tools
   - Web scraping functions

## Configuration

Both services use environment variables for configuration:
- Database connection strings
- API keys and secrets
- Service URLs and ports
- Observability endpoints

See `.env.example` files in each service directory for required variables.

## Observability

Integrated monitoring stack:
- **Tracing**: OpenTelemetry with Jaeger
- **Metrics**: Prometheus integration
- **Logging**: Structured logging with contextual information
- **LLM Observability**: Langfuse integration for tracking LLM interactions

## Building and Running

### Prerequisites

- Python 3.13
- Poetry (for dependency management)
- Docker and Docker Compose (for containerized deployment)
- Access to required database services (PostgreSQL, Qdrant, Redis, Neo4j)

### Development Setup

1. Install dependencies for each service:
   ```bash
   cd memos.as && poetry install
   cd InGest-LLM.as && poetry install
   ```

2. Configure environment variables by creating `.env` files based on the examples.

3. Run services in development mode:
   ```bash
   # Terminal 1: Run memOS.as
   cd memos.as
   uvicorn app.main:app --reload
   
   # Terminal 2: Run InGest-LLM.as
   cd InGest-LLM.as
   poetry run uvicorn src.ingest_llm_as.main:app --reload
   ```

### Docker Deployment

Both services are designed to run within a containerized environment:

1. Build images:
   ```bash
   cd memos.as && docker build -t memos-as .
   cd InGest-LLM.as && docker build -t ingest-llm-as .
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up
   ```

This QWEN.md provides essential context for working with the MCP Server Build environment and understanding the relationship between memOS.as and InGest-LLM.as services.