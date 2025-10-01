# GitHub Copilot Instructions for ApexSigma Ecosystem

## 🏗️ Architecture Overview

**Society of Agents Architecture**: Multi-agent AI system with specialized roles orchestrated through DevEnviro.as. Four core microservices communicate via RabbitMQ and REST APIs.

### Core Services

- **devenviro.as**: Agent orchestration platform managing Claude/Gemini/Gemma agents
- **memos.as**: Knowledge management system with memory storage and retrieval
- **InGest-LLM.as**: Intelligent content ingestion and vectorization engine
- **tools.as**: Shared utilities and development APIs

### Data Flow Architecture

```mermaid
Content → InGest-LLM → Qdrant (vectors) → Neo4j (knowledge graphs) → PostgreSQL/Redis (memory) → Agent Access
```

### Infrastructure Stack

- **Network**: `apexsigma_net` (172.26.0.0/16) with static IP service discovery
- **Databases**: PostgreSQL (procedural), Redis (cache), Qdrant (vectors), Neo4j (graphs)
- **Messaging**: RabbitMQ for agent-to-agent communication
- **Observability**: Prometheus + Jaeger (tracing) + Loki (logs) + Grafana (dashboards)

## 🔧 Critical Developer Workflows

### Infrastructure Management

```bash
# Start complete ecosystem
docker-compose -f docker-compose.unified.yml up -d

# Check service health
docker-compose -f docker-compose.unified.yml ps

# View logs for specific service
docker-compose -f docker-compose.unified.yml logs apexsigma_memos_api
```

### Quality Gates (MANDATORY)

```bash
# Run after ANY code changes - blocks commits if failing
trunk check --ci

# Fix issues automatically where possible
trunk check --fix
```

### Development Setup

```bash
# Individual service development
cd services/memos.as
poetry install && poetry shell

# Run service locally
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8090

# Run tests
poetry run pytest --junit-xml=reports/junit.xml
```

## 📋 Project-Specific Conventions

### Agent Hierarchy & Protocols

- **Orchestrator**: Human strategic direction
- **Reviewer**: Gemini validates MAR (Mandatory Agent Review) protocol
- **Primary Implementor**: Gemini CLI executes technical tasks
- **Specialized Implementors**: Qwen (code generation), Claude (analysis)

### Valhalla Shield Engineering Standard

- **85% test coverage** minimum across all services
- **Structured JSON logging** to stdout for all services
- **OpenTelemetry tracing** to Jaeger for distributed operations
- **Prometheus /metrics endpoints** for all services
- **MCP (Model Context Protocol) servers** for AI agent integration

### Dependency Management

```toml
# pyproject.toml pattern - use Poetry, not pip
[tool.poetry.dependencies]
python = ">=3.13,<4.0"
# Local path dependencies for shared libs
apexsigma-core = {path = "./libs/apexsigma-core", develop = true}
```

### Service Communication

```python
# REST API pattern - FastAPI with Pydantic models
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Service Name", description="Service purpose")

class RequestModel(BaseModel):
    field: str

@app.post("/endpoint")
async def handler(request: RequestModel) -> dict:
    # Implementation
    pass
```

### Authentication & Security

```python
# JWT service accounts for AI agents
SERVICE_ACCOUNTS = {
    "MCP_COPILOT": "copilot-secret-token",
    "MCP_GEMINI": "gemini-secret-token",
    "MCP_QWEN": "qwen-secret-token"
}
```

## 🔍 Key Integration Points

### Cross-Service Communication

- **Internal DNS**: `apexsigma_postgres`, `apexsigma_redis`, etc.
- **Static IPs**: Documented in `VERIFIED_DOCKER_NETWORK_MAP_V2.md`
- **Health Checks**: `/health` endpoints for all services
- **Metrics**: `/metrics` endpoints with Prometheus format

### External Dependencies

- **Langfuse**: AI operation tracing and monitoring
- **Qdrant**: Vector similarity search for semantic content
- **Neo4j**: Knowledge graph relationships and queries
- **RabbitMQ**: Agent-to-agent messaging and task queues

## 📁 Essential Files & Directories

### Architecture Documentation

- `AGENTS.md`: Agent hierarchy and operational protocols
- `docker-compose.unified.yml`: Complete infrastructure definition
- `VERIFIED_DOCKER_NETWORK_MAP_V2.md`: Network topology and service IPs

### Service Structure (per service)

```bash
services/{service}.as/
├── app/main.py              # FastAPI application
├── pyproject.toml           # Poetry dependencies
├── Dockerfile              # Container definition
├── alembic/                # Database migrations
├── tests/                  # Unit tests
└── docs/                   # MkDocs documentation
```

### Quality & Compliance

- `.github/instructions/codacy.instructions.md`: Trunk quality rules
- `trunk.yaml`: Linting, formatting, and testing configuration
- `pytest.ini`: Test configuration with JUnit output

## ⚡ Development Guidelines

1. **Always run `trunk check --ci`** after code changes - failures block commits
2. **Follow MAR Protocol**: Get agent reviews before integration
3. **MCP-First Design**: Build APIs with AI agent integration in mind
4. **Structured Logging**: JSON format to stdout, never print statements
5. **Test Coverage**: Maintain 85%+ coverage for Valhalla Shield compliance
6. **Dependency Verification**: Check `poetry.lock` and `pyproject.toml` alignment
7. **Network Awareness**: Use documented static IPs for service communication

## 🚨 Critical Patterns to Avoid

- **Never use pip directly** - always use Poetry for dependency management
- **Never hardcode secrets** - use environment variables with `.env` files
- **Never commit without trunk check** - quality gates are mandatory
- **Never modify network IPs** without updating `VERIFIED_DOCKER_NETWORK_MAP_V2.md`
- **Never skip agent review** - MAR protocol requires dual verification

## 🔗 Current Development Context

**Phase 0**: Infrastructure stabilization (critical dependency fixes)
**Active Work Orders**: WO-001 (dependencies), WO-005 (quality gates), WO-007 (compliance)
**Priority**: Fix `ModuleNotFoundError` in memos.as and devenviro.as services
**Blocker**: Missing `langfuse`, `qdrant-client`, `structlog` dependencies
