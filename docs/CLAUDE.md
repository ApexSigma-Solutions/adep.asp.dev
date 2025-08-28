# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ApexSigmaProjects.Dev is a multi-project workspace implementing the **ApexSigma "Society of Agents" Ecosystem** - an AI-powered development platform where specialized AI agents collaborate on complex development tasks. The workspace contains four interconnected microservices that form a complete agentic development environment.

## Workspace Architecture

### 🏗️ Core Projects Structure

| Project | Purpose | Tech Stack | Port |
|---------|---------|------------|------|
| **devenviro.as** | AI Society orchestrator & agent management | FastAPI, PostgreSQL, Redis, Qdrant, Neo4j, RabbitMQ | 8090 |
| **memos.as** | Persistent memory & knowledge management (MemOS) | FastAPI, PostgreSQL, Qdrant, Redis | TBD |
| **InGest-LLM.as** | Data ingestion service for ecosystem | FastAPI, OpenTelemetry, Langfuse | 8000 |
| **tools.as** | Tool registry & utility services | FastAPI, SQLAlchemy, PostgreSQL | TBD |

### 🧠 System Philosophy

**Core Principle**: *"Solve problems, not create new ones"* - Every architectural choice improves developer Quality of Life (QoL) by reducing friction and enabling AI agents to learn and self-regulate.

## Development Environment Setup

### Prerequisites
- **Python 3.13+** (all projects require Python 3.13)
- **Docker Desktop**
- **Poetry** for dependency management
- **dotenvx** for environment variable management: `npm install -g dotenvx`

### Environment Variables
Each project uses dotenvx for secret management:
```bash
# Configure secrets per project
dotenvx set POSTGRES_USER myuser
dotenvx set POSTGRES_PASSWORD mypass
dotenvx set GEMINI_API_KEY your_key
dotenvx set OPENAI_API_KEY your_key
```

## Development Commands by Project

### devenviro.as (Main Orchestrator)
```bash
# Environment setup
pip install -r requirements.txt
dotenvx run -- python app/src/main.py

# Docker development
docker-compose up --build -d
docker-compose -f docker-compose.yml -f docker-compose.telemetry.yml up --build -d

# Database operations
cd app && python -c "from src.core.migrations_runner import apply_migrations; apply_migrations()"
cd app && python src/seed_knowledge.py

# Individual tests (no unified test runner)
cd app && python tests/test_telemetry_stack.py
cd app && python tests/test_review_manager.py
cd app && python tests/test_observability.py

# Demo workflows
cd app && python src/demo_agent_communication.py
```

### InGest-LLM.as (Data Ingestion)
```bash
# Development
poetry install && poetry shell
poetry run uvicorn src.ingest_llm_as.main:app --reload

# Code quality
poetry run ruff check . && poetry run ruff format .
poetry run mypy src/
poetry run pre-commit run --all-files

# Testing
poetry run pytest
poetry run pytest --cov=src/ingest_llm_as

# Docker
docker build -t ingest-llm-as .
docker run -d -p 8000:8000 --name ingest-llm-as ingest-llm-as
```

### memos.as (Memory Service)
```bash
# Environment setup using uv
uv venv && uv pip install -r requirements.txt
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Development (FastAPI main.py needs to be implemented)
# Database migrations handled by the migration system
```

### tools.as (Tool Registry)
```bash
# Poetry setup
poetry install
poetry shell

# Development
poetry run uvicorn app.main:app --reload

# Code quality
poetry run ruff check .
poetry run pytest

# Docker
docker-compose up --build -d
```

## Service Architecture

### DevEnviro Society of Agents
The main orchestrator manages 12+ specialized AI agent personas:
- **backend-specialist**, **frontend-specialist**, **devops-engineer**
- **qa-engineer**, **security-engineer**, **software-architect**
- **product-owner**, **project-manager**, **engineering-manager**
- **enterprise-cto**, **technical-writer**, **senior-fullstack-developer**

### Multi-Tiered Memory Engine
- **Redis**: Working memory and caching
- **PostgreSQL**: Procedural memory with complex schemas
- **Qdrant**: Vector database for episodic/semantic search
- **Neo4j**: Semantic relationships and knowledge graphs

### Service Ports & URLs
- **DevEnviro API**: http://localhost:8090 (/docs)
- **InGest-LLM**: http://localhost:8000 (/health)
- **Grafana**: http://localhost:8080 (admin/devenviro123)
- **Prometheus**: http://localhost:9090
- **Jaeger**: http://localhost:16686
- **RabbitMQ**: http://localhost:15672

## Key Development Patterns

### Agent Memory Protocol (memos.as)
**Best Practices for AI Agent Memory Interaction:**
1. **Session Initialization**: Check for existing context, load project state
2. **Retrieve First, Store Last**: Always check existing memory before storing
3. **User Confirmation Required**: All write/update/delete operations need approval
4. **Dynamic Context Retrieval**: Use RAG with FTS and semantic search

### Society of Agents Collaboration
- **@Claude**: Architect role
- **@Gemini**: Implementer role  
- **@Qodo**: QA role
- **Mandatory Agent Review (MAR)**: All artifacts require review before integration

### Message Flow Architecture
1. Tasks arrive at FastAPI orchestrator (devenviro.as)
2. Orchestrator analyzes and delegates to appropriate agents
3. Agents communicate via RabbitMQ message queue
4. Memory operations flow through memos.as
5. Tool discovery handled by tools.as
6. Data ingestion processed by InGest-LLM.as

## Database Schemas

### DevEnviro Migrations (app/migrations/)
- `001_create_agent_communications.sql`: Message routing
- `002_knowledge_documents.sql`: Knowledge storage
- `003_create_agents_table.sql`: Agent registry
- `004_add_token_to_agent.sql`: Authentication
- `005_add_capabilities_to_agents.sql`: Agent capabilities

### Memos Schema Features
- Context management with versioning (`active_context`, `product_context`)
- Full-text search via SQLite FTS5 with automatic triggers
- Progress tracking with hierarchical relationships
- Custom data storage with category-based organization

## Observability Stack

### Telemetry Integration
- **OpenTelemetry**: Distributed tracing across all services
- **Prometheus**: Metrics collection and monitoring
- **Grafana**: Dashboards and visualization
- **Jaeger**: Request tracing and performance monitoring
- **Loki**: Centralized logging
- **Langfuse**: LLM-specific observability

### Health Monitoring
Each service provides comprehensive health endpoints with dependency status and observability integration details.

## Development Notes

### Context Portal System
The `context_portal/` directories contain:
- **Alembic migrations**: Database schema evolution
- **Vector data storage**: ChromaDB/Qdrant vector collections  
- **Context databases**: SQLite context storage

### Modern Python Toolchain
All projects follow ApexSigma standards:
- **Ruff**: High-performance linting and formatting
- **mypy**: Static type checking
- **Poetry**: Dependency management
- **pre-commit**: Automated quality checks
- **pytest**: Testing framework

### Project Status
- **devenviro.as**: Active development, full orchestration system
- **InGest-LLM.as**: Scaffolded with observability, ready for ingestion endpoints
- **memos.as**: Database schema complete, FastAPI implementation needed
- **tools.as**: Basic tool registry with todo/scratchpad functionality

### Integration Points
- All services integrate through the DevEnviro orchestrator
- Memory operations centralized through memos.as memory protocol  
- Tool discovery handled by tools.as registry
- Data flows processed through InGest-LLM.as pipelines
- Full observability stack provides end-to-end monitoring

## Documentation System

### Three-Part Documentation Strategy
1. **Source of Truth** (`/.md/` & Code Docstrings): Internal collaborative Markdown files and Python docstrings
2. **Agent Ingestion** (`/.ingest/`): Token-efficient JSON files for AI agents  
3. **Public Documentation** (`/docs/`): Curated content built with MkDocs from source files

### MkDocs Integration
All projects now include comprehensive MkDocs configuration with:
- **Material Theme**: Modern, responsive documentation theme
- **mkdocstrings Plugin**: Automatic API documentation from Python docstrings
- **Unified Build System**: `build_ecosystem_docs.py` for cross-project documentation management

### Documentation Commands

```bash
# Build all project documentation
python build_ecosystem_docs.py build

# Serve specific project documentation
python build_ecosystem_docs.py serve devenviro.as
python build_ecosystem_docs.py serve InGest-LLM.as  
python build_ecosystem_docs.py serve memos.as
python build_ecosystem_docs.py serve tools.as
python build_ecosystem_docs.py serve embedding-agent.as

# List available projects
python build_ecosystem_docs.py list

# Individual project builds (from project directory)
mkdocs serve                    # Development server
mkdocs build --clean           # Production build
```

### Per-Project Documentation
Each project includes:
- **API Reference**: Auto-generated from docstrings using `:::` directives
- **Tutorial & How-To Sections**: Curated user-facing guides  
- **Integration Documentation**: Service-specific implementation details

## Development Workflow

When working on any project in this workspace:
1. **Start with the appropriate project's existing CLAUDE.md** for specific guidance
2. **Use the memory protocol** for any memory/context operations
3. **Follow the Society of Agents pattern** for multi-agent collaboration
4. **Leverage the observability stack** for monitoring and debugging
5. **Respect the modular architecture** - each service has a specific role
6. **Document as you code** - update docstrings and markdown files for automatic documentation generation

The workspace represents a complete AI development ecosystem where agents learn, remember, and collaborate to solve complex development challenges.