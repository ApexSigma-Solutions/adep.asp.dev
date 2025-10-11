# GitHub Copilot Instructions for ApexSigma Ecosystem

## ⚠️ CRITICAL: Omega Ingest Protocol

**BEFORE ANY CODE CHANGES**, you MUST understand the governance model:

1. **Query Context APIs**: Check InGest-LLM (`http://172.26.0.12:8000/query_context`) and memOS (`http://172.26.0.13:8090/memory/query`) for existing verified knowledge
2. **Validate Against Immutable Truth**: Omega Ingest (memOS + Neo4j) is the ONLY authoritative source
3. **Dual Verification**: Infrastructure changes require verification from 2 AI assistants OR 1 AI + 1 human
4. **Protected Services**: Never modify without verification: memOS API (172.26.0.13), Neo4j (172.26.0.14), PostgreSQL (172.26.0.2), InGest-LLM (172.26.0.12)

**Reference**: `docs/protocols/The_Laws_of_Asgard_A_Primer_for_Agents_of_the_ApexSigma_Ecosystem.md`

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

### Daily Development Cycle (SOD/EOD Protocol)

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

**Why SOD/EOD**: These scripts maintain knowledge graph continuity by automatically ingesting development progress into memOS. Bypassing this cycle breaks the Omega Ingest audit trail.

### Infrastructure Management

```bash
# Start complete ecosystem (17+ services)
docker-compose -f docker-compose.unified.yml up -d

# Check service health (all services have health checks)
docker-compose -f docker-compose.unified.yml ps

# View logs for specific service (use container names from docker-compose.unified.yml)
docker-compose -f docker-compose.unified.yml logs apexsigma_memos_api

# Access service dashboards
# Grafana:    http://localhost:8080 (admin/apexsigma123)
# Prometheus: http://localhost:9090
# Jaeger:     http://localhost:16686
# RabbitMQ:   http://localhost:15672 (apexsigma_user/Apexsigma123_)
```

**Critical**: Use `docker-compose.unified.yml` NOT individual compose files. Services depend on shared network infrastructure.

### Quality Gates (MANDATORY)

```bash
# Run after ANY code changes - blocks commits if failing
trunk check --ci

# Fix issues automatically where possible
trunk check --fix

# Custom actions defined in trunk.yaml
trunk run run-tests          # Run all service test suites
trunk run run-memos-tests    # Run specific service tests
trunk run run-integration-tests  # Integration tests (starts docker-compose.ci.yml)
```

**Why trunk check is mandatory**:

- Enforces 85% test coverage (Valhalla Shield standard)
- Validates JUnit XML format (`junit_family = xunit1`)
- Runs linters: ruff, black, isort, mypy, flake8
- Outputs to `reports/junit-*.xml` for CI/CD

### Development Setup (Per-Service)

```bash
# Individual service development (all services use Poetry, NOT pip)
cd services/memos.as
poetry install && poetry shell

# Run service locally (FastAPI with uvicorn)
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8090

# Run tests with coverage (outputs JUnit XML)
poetry run pytest --junit-xml=reports/junit.xml --cov=app --cov-report=html

# Quality checks (use ruff, not pylint/flake8 standalone)
poetry run ruff check . && poetry run ruff format .
poetry run mypy app/
```

**Service ports** (from docker-compose.unified.yml):

- devenviro.as: 8001 (API), 8002 (Gemini listener)
- memos.as: 8090
- InGest-LLM.as: 8000
- tools.as: 8003
- PostgreSQL: 5432
- Redis: 6379
- RabbitMQ: 5672 (AMQP), 15672 (Management UI)
- Qdrant: 6333
- Neo4j: 7474 (HTTP), 7687 (Bolt)
- Prometheus: 9090
- Grafana: 3000 (default login: admin/apexsigma123)
- Jaeger: 16686

### Database Migrations (Alembic)

```bash
# Only memos.as currently uses Alembic
cd services/memos.as

# Generate migration after model changes
poetry run alembic revision --autogenerate -m "Description of changes"

# Apply migrations
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1

# View migration history
poetry run alembic history
```

**Why Alembic**: Manual SQL changes bypass the immutable audit trail. Alembic migrations are version-controlled and verifiable.

### DevContainer Setup (VS Code Remote Development)

The project supports DevContainer development for consistent, isolated environments:

```bash
# Prerequisites: Docker Desktop + VS Code Remote-Containers extension

# Open in DevContainer (VS Code Command Palette)
# > Dev Containers: Reopen in Container

# DevContainer configuration features:
# - Python 3.13 with Poetry pre-installed
# - Docker-in-Docker for running docker-compose.unified.yml
# - All services auto-forwarded (8000, 8090, 5432, 6379, 5672, 9090, 3000)
# - Pre-commit hooks automatically installed
# - Environment variables passed from host (.env)
```

**DevContainer benefits**:

- **Consistency**: Same Python 3.13, Poetry, and tool versions across all developers
- **Isolation**: Doesn't pollute host system with dependencies
- **Integration**: Direct access to `docker-compose.unified.yml` services via Docker-in-Docker
- **Automation**: `setup.sh` installs all service dependencies and starts infrastructure

**Configuration files** (see `.devcontainer/`):

- `devcontainer.json`: VS Code extensions, port forwarding, environment setup
- `setup.sh`: Post-create automation script
- `Dockerfile`: Custom Python 3.13 image with Poetry and pre-commit

**Why DevContainer**: Eliminates "works on my machine" issues - all developers and AI agents share identical environment setup.

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
# pyproject.toml pattern - ALL services use Poetry, NEVER pip
[tool.poetry.dependencies]
python = ">=3.13,<4.0"

# Local path dependencies for shared libs (see libs/apexsigma-core)
apexsigma-core = {path = "../../libs/apexsigma-core", develop = true}

# Standard service dependencies
fastapi = ">=0.100.0,<1.0.0"
pydantic = ">=2.0.0,<3.0.0"
pydantic-settings = ">=2.10.1,<3.0.0"
```

**Critical**:

- **Python 3.13+ only** - entire ecosystem standardized
- **Never use pip directly** - always `poetry add <package>`
- **Shared models**: All services import from `apexsigma_core.models` (StoreRequest, QueryRequest, AgentPersona, Task)
- **Local dependencies**: Use `develop = true` so changes to `libs/apexsigma-core` reflect immediately

**Common pattern violation**: Running `pip install -r requirements.txt` - this breaks Poetry's lock file integrity.

### Service Communication Patterns

```python
# FastAPI pattern with Pydantic models (see services/*/app/main.py)
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from apexsigma_core.models import StoreRequest, QueryRequest

app = FastAPI(
    title="Service Name",
    description="Service purpose",
    version="1.0.0"
)

# CORS is REQUIRED for cross-service communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Locked-down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint (required for Docker healthcheck)
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "service-name"}

# Prometheus metrics endpoint (required for observability)
@app.get("/metrics", tags=["Metrics"])
async def metrics():
    # Implementation in app/services/observability.py
    pass
```

**Why these patterns**:

- **CORS middleware**: Services run in separate containers, cross-origin requests are default
- **/health endpoint**: Docker healthchecks use this (see docker-compose.unified.yml `healthcheck` sections)
- **/metrics endpoint**: Prometheus scrapes this for monitoring (Grafana dashboards depend on it)
- **Shared models**: Prevents drift between service contracts

### Container Build Pattern

```dockerfile
# Dockerfile pattern (see services/*/Dockerfile)
FROM python:3.13-slim

WORKDIR /app

# Install Poetry (version-pinned for reproducibility)
RUN pip install --no-cache-dir poetry==1.7.1

# Configure Poetry to NOT create virtual env (we're in container)
RUN poetry config virtualenvs.create false

# Copy dependencies FIRST (better layer caching)
COPY pyproject.toml poetry.lock* ./
RUN poetry install --without dev --no-interaction --no-ansi

# Copy application code AFTER dependencies
COPY app/ ./app/

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8090"]
```

**Why this pattern**:

- **Poetry in containers**: `virtualenvs.create false` prevents nested venvs
- **Layer caching**: Dependencies change less than code, so copy `pyproject.toml` first
- **No dev dependencies**: `--without dev` reduces image size
- **Port binding**: `0.0.0.0` required for Docker network access (not `127.0.0.1`)

**Common mistake**: Copying entire codebase before `poetry install` - invalidates Docker cache on every code change.

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
