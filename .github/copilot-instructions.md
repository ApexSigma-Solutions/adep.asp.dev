# GitHub Copilot Instructions for ApexSigma Ecosystem

## 🏗️ Architecture Overview

**Society of Agents Architecture**: Multi-agent AI system with specialized roles orchestrated through DevEnviro.as. Four core microservices communicate via RabbitMQ and REST APIs.

### Core Services

- **devenviro.as**: Agent orchestration platform managing Claude/Gemini/Gemma agents
- **memos.as** (memOS): Knowledge management system with memory storage and retrieval
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

### Daily Development Cycle

```powershell
# Start of Day (SOD) - Deploy full ecosystem
.\sod.ps1                    # Basic deployment
.\sod.ps1 -Force             # Force cleanup + deploy
.\sod.ps1 -Verbose           # Verbose logging

# End of Day (EOD) - Capture progress and ingest to knowledge graph
.\eod.ps1                    # Full protocol (tests + git + ingestion)
.\eod.ps1 -SkipTests         # Skip test execution
.\eod.ps1 --project memos.as # Target specific project
```

### Infrastructure Management

```bash
# Start complete ecosystem
docker-compose -f docker-compose.unified.yml up -d

# Check service health
docker-compose -f docker-compose.unified.yml ps

# View logs for specific service
docker-compose -f docker-compose.unified.yml logs apexsigma_memos_api

# Access service dashboards
# Grafana:    http://localhost:8080 (admin/apexsigma123)
# Prometheus: http://localhost:9090
# Jaeger:     http://localhost:16686
# RabbitMQ:   http://localhost:15672
```

### Quality Gates (MANDATORY)

```bash
# Run after ANY code changes - blocks commits if failing
trunk check --ci

# Fix issues automatically where possible
trunk check --fix

# Custom actions defined in trunk.yaml
trunk run run-tests  # Run pytest with JUnit XML output
```

### Development Setup

```bash
# Individual service development
cd services/memos.as
poetry install && poetry shell

# Run service locally
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8090

# Run tests with coverage
poetry run pytest --junit-xml=reports/junit.xml --cov=app --cov-report=html
```

### Database Migrations (Alembic)

```bash
# Generate migration after model changes
cd services/memos.as
poetry run alembic revision --autogenerate -m "Description of changes"

# Apply migrations
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1

# View migration history
poetry run alembic history
```

## 📋 Project-Specific Conventions

### Agent Hierarchy & Protocols

- **Orchestrator (SigmaDev11)**: Human strategic direction
- **Reviewer (Gemini)**: Validates MAR (Mandatory Agent Review) protocol
- **Primary Implementor (Gemini CLI)**: Executes technical tasks
- **Specialized Implementors**: Qwen (code generation), Claude (analysis)
- **Human Augment Tool (GitHub Copilot)**: Pair-programming assistant (not autonomous)

**MAR Protocol**: All operations require dual verification (human + agent review) before integration.

### Valhalla Shield Engineering Standard

- **85% test coverage** minimum across all services
- **Structured JSON logging** to stdout for all services (use `structlog`, never `print`)
- **OpenTelemetry tracing** to Jaeger for distributed operations
- **Prometheus /metrics endpoints** for all services
- **MCP (Model Context Protocol) servers** for AI agent integration

### Dependency Management

```toml
# pyproject.toml pattern - use Poetry, not pip
[tool.poetry.dependencies]
python = ">=3.13,<4.0"
# Local path dependencies for shared libs
apexsigma-core = {path = "../../libs/apexsigma-core", develop = true}

# Example service dependencies
fastapi = ">=0.100.0,<1.0.0"
pydantic = ">=2.0.0,<3.0.0"
pydantic-settings = ">=2.10.1,<3.0.0"
```

**Critical**: All services use Python 3.13+. Services share the `apexsigma-core` library via local path dependencies.

### Service Communication

```python
# FastAPI pattern with Pydantic models (see services/*/app/main.py)
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from apexsigma_core.models import StoreRequest, QueryRequest

app = FastAPI(
    title="Service Name",
    description="Service purpose",
    version="1.0.0"
)

# CORS configuration for cross-service communication
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics", tags=["Metrics"])
async def metrics():
    # Prometheus metrics endpoint
    pass
```

### Container Build Pattern

```dockerfile
# Dockerfile pattern (see services/*/Dockerfile)
FROM python:3.13-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry to not create virtual env (we're in container)
RUN poetry config virtualenvs.create false

# Copy dependencies first (better layer caching)
COPY pyproject.toml poetry.lock* ./
RUN poetry install --without dev

# Copy application code
COPY app/ ./app/

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8090"]
```

## 🔍 Key Integration Points

### Cross-Service Communication

- **Internal DNS**: `apexsigma_postgres`, `apexsigma_redis`, `apexsigma_qdrant`, `apexsigma_neo4j`, `apexsigma_rabbitmq`
- **Static IPs**: Documented in `docs/Config Files/Infrastructure/Docker Network/VERIFIED_DOCKER_NETWORK_MAP_V3.md`
- **Health Checks**: `/health` endpoints for all services (checked by Docker healthcheck)
- **Metrics**: `/metrics` endpoints with Prometheus format

### Environment Configuration

All services use `.env` files for configuration. Copy `.env.example` to `.env` and populate:

```bash
# Database connections use service names as hostnames
POSTGRES_HOST=apexsigma_postgres
REDIS_HOST=apexsigma_redis
QDRANT_HOST=apexsigma_qdrant
NEO4J_HOST=apexsigma_neo4j
RABBITMQ_HOST=apexsigma_rabbitmq

# Langfuse observability (per-service keys)
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=<your-key>
LANGFUSE_SECRET_KEY=<your-secret>
```

### External Dependencies

- **Langfuse**: AI operation tracing and monitoring (separate projects per service)
- **Qdrant**: Vector similarity search for semantic content
- **Neo4j**: Knowledge graph relationships and queries
- **RabbitMQ**: Agent-to-agent messaging and task queues

## 📁 Essential Files & Directories

### Architecture Documentation

- `AGENTS.md`: Agent hierarchy and operational protocols
- `README.md`: Project overview and recent achievements
- `docker-compose.unified.yml`: Complete infrastructure definition (700+ lines)
- `docs/Config Files/Infrastructure/Docker Network/VERIFIED_DOCKER_NETWORK_MAP_V3.md`: Network topology

### Service Structure (per service)

```bash
services/{service}.as/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic request/response models
│   ├── schemas.py           # Database schemas
│   └── services/            # Business logic
│       ├── postgres_client.py
│       ├── redis_client.py
│       ├── qdrant_client.py
│       ├── neo4j_client.py
│       └── observability.py # Langfuse integration
├── pyproject.toml           # Poetry dependencies
├── poetry.lock              # Locked dependency versions
├── Dockerfile               # Container definition
├── alembic/                 # Database migrations
│   ├── env.py
│   └── versions/
├── tests/                   # Unit tests
├── docs/                    # MkDocs documentation
└── .env.example             # Environment template
```

### Shared Libraries

```bash
libs/apexsigma-core/         # Shared Pydantic models and utilities
├── apexsigma_core/
│   ├── models.py            # AgentPersona, Task, StoreRequest, QueryRequest
│   └── __init__.py
└── pyproject.toml
```

### Scripts & Automation

- `sod.ps1` / `sod.py`: Society of Agents Deploy (start ecosystem)
- `eod.ps1` / `eod.py`: End of Day protocol (capture progress, run tests, ingest to knowledge graph)
- `scripts/session_manager.py`: Session logging and tracking
- `scripts/log_progress_to_ingest.py`: Progress ingestion to InGest-LLM

### Quality & Compliance

- `trunk.yaml`: Linting, formatting, and testing configuration
- `pytest.ini`: Test configuration (`junit_family = xunit1`)
- `.github/workflows/`: CI/CD pipelines (currently on `feat/ci-security-pipelines` branch)

## ⚡ Development Guidelines

1. **Always run `trunk check --ci`** after code changes - failures block commits
2. **Follow MAR Protocol**: Get agent reviews before integration
3. **Use SOD/EOD Cycle**: `.\sod.ps1` to start, `.\eod.ps1` to capture progress
4. **MCP-First Design**: Build APIs with AI agent integration in mind
5. **Structured Logging**: Use `structlog` with JSON format to stdout, never print statements
6. **Test Coverage**: Maintain 85%+ coverage for Valhalla Shield compliance
7. **Dependency Verification**: Check `poetry.lock` and `pyproject.toml` alignment
8. **Network Awareness**: Use documented static IPs for service communication
9. **Database Migrations**: Use Alembic for schema changes, never manual SQL
10. **Environment Isolation**: Use `.env` files, never hardcode configuration

## 🚨 Critical Patterns to Avoid

- **Never use pip directly** - always use Poetry for dependency management
- **Never hardcode secrets** - use environment variables with `.env` files
- **Never commit without trunk check** - quality gates are mandatory
- **Never modify network IPs** without updating `VERIFIED_DOCKER_NETWORK_MAP_V3.md`
- **Never skip agent review** - MAR protocol requires dual verification
- **Never use print()** - use structured logging with `structlog`
- **Never bypass SOD/EOD cycle** - maintains knowledge graph continuity
- **Never use Python < 3.13** - entire ecosystem standardized on 3.13+

## 🔗 Current Development Context

**Repository**: `ApexSigma-Solutions/adep.asp.dev`
**Current Branch**: `feat/ci-security-pipelines`
**Default Branch**: `alpha`

**Current Phase**: 🎊 **Operation Valhalla Shield - Phase 0 COMPLETE** 🎊

**Phase 0 Final Status** (October 4, 2025):
- 🎉 **OVS-T02**: tools-api Restart Loop - ✅ RESOLVED (12+ min uptime, healthy)
- 🎉 **OVS-T03**: dagster_webserver Unhealthy - ✅ RESOLVED (58s uptime, healthy)
- 🎉 **OVS-T04**: memos-api Neo4j - ✅ VERIFIED (38 hours stable)
- ✅ **OVS-T01**: Dev Container Setup - ✅ IMPLEMENTED (functional test deferred to Phase 1)

**Mission Status**: ✅ **MISSION ACCOMPLISHED**
- Critical Incidents Resolved: 3/3 (100%)
- Container Health: 20+/24 healthy (83-100%)
- Infrastructure Stability: 100% (0 restart loops)
- All critical APIs responding HTTP 200

**Phase 1 Status**: 🟢 **UNBLOCKED - READY TO PROCEED**

**Next Steps**:
1. Execute git commits (see `docs/Phase0_Completion_Report.md`)
2. Push to `feat/ci-security-pipelines` branch
3. Create PR to `alpha` for MAR protocol review
4. Begin Phase 1: Production Container ("Valhalla Forge")

**Phase 0 Documentation**:
- `docs/Phase0_Completion_Report.md` - Final status report
- `docs/Phase0_Stabilization_Report.md` - Implementation details
- `PHASE0_QUICKREF.md` - Quick reference guide

**Recent Achievements (Oct 2025)**:
- ✅ Phase 0 Stabilization COMPLETE (< 4 hours)
- ✅ Phase 2 Infrastructure Hardening COMPLETE
- ✅ ClickHouse integration operational
- ✅ SSL/TLS security with Nginx proxy
- ✅ PgBouncer connection pooling
- ✅ HashiCorp Vault + Fail2Ban security
- ✅ Multi-database automated backups

**Active Focus**: Phase 1 preparation - Production container implementation
