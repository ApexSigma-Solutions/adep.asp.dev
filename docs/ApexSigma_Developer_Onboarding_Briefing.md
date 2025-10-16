# ApexSigma Developer Onboarding Briefing

## Welcome to ApexSigma! 🚀

This briefing provides essential knowledge for new developers joining the ApexSigma ecosystem. The project implements a Society of Agents architecture with multi-agent AI collaboration, secure secrets management, and a comprehensive microservices ecosystem.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Development Environment Setup](#development-environment-setup)
3. [Secrets Management with HVAC](#secrets-management-with-hvac)
4. [Configuration Management with Pydantic](#configuration-management-with-pydantic)
5. [Service Architecture Overview](#service-architecture-overview)
6. [Development Workflow](#development-workflow)
7. [Quality Gates & Standards](#quality-gates--standards)

---

## Project Overview

ApexSigma is a Society of Agents architecture featuring intelligent automation and content management. The ecosystem consists of specialized microservices that collaborate through RabbitMQ messaging, with comprehensive observability and secure secrets management.

### Core Principles
- **Society of Agents**: Multi-agent AI collaboration (Claude, Gemini, Gemma)
- **Omega Ingest Protocol**: Immutable knowledge graph with dual verification
- **Valhalla Shield Standard**: 85% test coverage, structured logging, OpenTelemetry
- **MAR Protocol**: Mandatory Agent Review for all changes

---

## Development Environment Setup

### Prerequisites
- **Docker & Docker Compose**: Containerized development environment
- **Python 3.13+**: All services standardized on Python 3.13
- **VS Code**: With Remote-Containers extension for DevContainer development
- **Trunk CLI**: Quality gate automation

### Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ApexSigma-Solutions/adep.asp.dev.git
   cd adep.asp.dev
   ```

2. **Start the unified ecosystem**:
   ```bash
   # Start all 24+ services
   docker compose -f docker-compose.unified.yml up -d

   # Verify services are healthy
   docker compose -f docker-compose.unified.yml ps
   ```

3. **Enter DevContainer environment**:
   - Open in VS Code
   - `Ctrl+Shift+P` → "Dev Containers: Rebuild and Reopen in Container"
   - Verify: `whoami` shows `vscode`, `pwd` shows `/workspace`

4. **Install dependencies** (per service):
   ```bash
   cd services/{service-name}
   poetry install
   ```

---

## Secrets Management with HVAC

ApexSigma uses HashiCorp Vault (via the `hvac` Python library) for secure secrets management across all services. Secrets are abstracted from code and environment variables, with automatic fallback to Vault when local values aren't provided.

### Architecture Overview

```
Application Code → Pydantic Settings → Vault Client → HashiCorp Vault
                                      ↓
                               Environment Variables (fallback)
```

### Vault Integration Pattern

```python
# apexsigma_core/vault.py - Core Vault client
from functools import lru_cache
import hvac

class VaultClient:
    def __init__(self, url=None, token=None, mount_point="secret"):
        # Auto-detects environment (container vs host)
        # Uses apexsigma-root-token-2025 as default token

    def get_secret(self, path: str, key: str) -> Optional[str]:
        """Retrieve secret from Vault KV v2 engine"""

@lru_cache(maxsize=1)
def get_vault_client() -> VaultClient:
    return VaultClient()

def get_secret(path: str, key: str) -> Optional[str]:
    """Convenience function for secret retrieval"""
```

### Usage in Services

```python
# services/memos.as/app/settings.py
from apexsigma_core.vault import get_secret

class MemosSettings(BaseSettings):
    postgres_password: Optional[str] = None

    @field_validator("postgres_password", mode="before")
    @classmethod
    def get_postgres_password(cls, v):
        """Fetch from Vault if not provided in environment"""
        if v is None:
            return get_secret("services/memos/database", "postgres_password")
        return v
```

### Vault Path Structure

```
secret/
├── monorepo/api_keys/          # Global API keys
│   ├── gemini_api_key
│   ├── openrouter_api_key
│   └── serper_api_key
├── services/
│   ├── memos/
│   │   ├── database/postgres_password
│   │   ├── cache/redis_password
│   │   ├── graph/neo4j_password
│   │   ├── security/jwt_secret_key
│   │   └── observability/
│   │       ├── langfuse_public_key
│   │       └── langfuse_secret_key
│   ├── devenviro/
│   └── ingest-llm/
```

### Best Practices

1. **Never commit secrets** to version control
2. **Use Vault paths** that match service structure
3. **Provide environment fallbacks** for local development
4. **Document required secrets** in `.env.example` files
5. **Test with mock secrets** in CI/CD pipelines

---

## Configuration Management with Pydantic

All services use Pydantic v2 with `pydantic-settings` for type-safe configuration management. Settings automatically load from environment variables and integrate with Vault for secrets.

### Base Settings Pattern

```python
# services/{service}/app/settings.py
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class ServiceSettings(BaseSettings):
    """Configuration settings for {service}."""

    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file
        env_file_encoding="utf-8",
        case_sensitive=False,      # Case-insensitive env vars
        extra="ignore",            # Ignore extra env vars
    )

    # Database Configuration
    postgres_host: str = Field(default="apexsigma_postgres")
    postgres_port: int = Field(default=5432)
    postgres_password: Optional[str] = None  # Vault-managed

    @field_validator("postgres_password", mode="before")
    @classmethod
    def get_postgres_password(cls, v):
        if v is None:
            return get_secret("services/{service}/database", "postgres_password")
        return v

# Singleton instance
settings = ServiceSettings()
```

### Environment File Structure

```bash
# .env.example - Template file (committed to git)
# Copy to .env and fill in actual values

# === Database Configuration ===
POSTGRES_HOST=apexsigma_postgres
POSTGRES_PORT=5432
POSTGRES_DB={service}
POSTGRES_USER=apexsigma_user
POSTGRES_PASSWORD=  # Leave empty - fetched from Vault

# === Service Configuration ===
API_HOST=localhost
JWT_SECRET_KEY=  # Leave empty - fetched from Vault

# === Observability ===
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=  # Leave empty - fetched from Vault
LANGFUSE_SECRET_KEY=  # Leave empty - fetched from Vault
```

### Key Features

1. **Type Safety**: All settings are strongly typed
2. **Validation**: Automatic validation of configuration values
3. **Vault Integration**: Seamless secrets abstraction
4. **Environment Fallbacks**: Local development support
5. **Documentation**: Self-documenting with Field descriptions

---

## Service Architecture Overview

### 🤖 devenviro.as - Agent Orchestration Platform

**Purpose**: Multi-agent AI collaboration and orchestration platform.

**Architecture**:
```
devenviro.as/
├── app/
│   ├── agents/          # Individual agent implementations
│   ├── bridge/          # Cross-agent communication
│   ├── src/            # Core orchestration logic
│   └── config.py       # Service configuration
├── agentsmith/         # Agent management utilities
└── telemetry/          # Observability and monitoring
```

**Key Components**:
- **Agent Society**: Claude, Gemini, Gemma agents with specialized roles
- **RabbitMQ Integration**: Message bus for agent communication
- **Gemini CLI Listener**: Real-time agent command processing
- **A2A Bridge**: Agent-to-agent communication protocols

**Ports**: 8001 (API), 8002 (Gemini listener)

### 📥 InGest-LLM.as - Content Ingestion Engine

**Purpose**: Intelligent content processing and vectorization for the knowledge graph.

**Architecture**:
```
InGest-LLM.as/
├── app/                # FastAPI application
├── src/                # Core ingestion logic
├── prompts/            # LLM prompt templates
├── integration/        # External service integrations
└── test_output/        # Test artifacts
```

**Key Components**:
- **Content Vectorization**: Multi-model LLM analysis
- **Repository Analysis**: Automated codebase documentation
- **Knowledge Graph Integration**: Neo4j graph updates
- **Progress Tracking**: Integration with memos.as

**Ports**: 8000

### 📝 memos.as - Knowledge Management System

**Purpose**: Centralized knowledge storage, retrieval, and progress tracking.

**Architecture**:
```
memos.as/
├── app/
│   ├── main.py         # FastAPI application
│   ├── settings.py     # Pydantic configuration
│   ├── services/       # Business logic
│   ├── schemas.py      # Data models
│   └── mcp_server.py  # Model Context Protocol
├── alembic/            # Database migrations
├── memory-bank/        # Knowledge storage
└── progress_logs/      # Session tracking
```

**Key Components**:
- **Memory Management**: Redis + PostgreSQL + Qdrant vector storage
- **Progress Logging**: Session and development tracking
- **MCP Server**: AI agent integration
- **Knowledge Graph**: Neo4j integration

**Ports**: 8090

### 🔧 tools.as - Development Utilities

**Purpose**: Shared utilities and APIs for cross-project integration.

**Architecture**:
```
tools.as/
├── app/                # FastAPI application
├── config/             # Configuration management
└── tests/              # Service tests
```

**Key Components**:
- **API Endpoints**: Cross-service integration APIs
- **Utility Functions**: Shared development tools
- **Testing Frameworks**: Common test utilities

**Ports**: 8003

### 📊 dagster - Data Pipeline Orchestration

**Purpose**: Workflow orchestration and data pipeline management.

**Architecture**:
```
dagster/
├── definitions.py      # Pipeline definitions
├── dagster.yaml        # Dagster configuration
└── workspace.yaml      # Workspace configuration
```

**Key Components**:
- **Pipeline Definitions**: Data processing workflows
- **Job Scheduling**: Automated task execution
- **Asset Management**: Data asset tracking

**Ports**: 3000 (webserver), 4000+ (daemons)

---

## Development Workflow

### Daily Development Cycle (SOD/EOD Protocol)

```powershell
# Start of Day (SOD) - Deploy ecosystem
.\sod.ps1                    # Basic deployment
.\sod.ps1 -Force             # Force cleanup + deploy
.\sod.ps1 -Verbose           # Verbose logging

# End of Day (EOD) - Capture progress
.\eod.ps1                    # Full protocol (tests + git + ingestion)
.\eod.ps1 -SkipTests         # Skip test execution
.\eod.ps1 --project memos.as # Target specific project
```

### Code Quality Workflow

```bash
# Run quality gates (MANDATORY before commits)
trunk check --ci

# Fix issues automatically where possible
trunk check --fix

# Run service-specific tests
cd services/{service}
poetry run pytest --junit-xml=reports/junit.xml --cov=app --cov-report=html
```

### Service Development Pattern

```bash
# 1. Navigate to service
cd services/{service-name}

# 2. Install dependencies
poetry install

# 3. Copy environment template
cp .env.example .env
# Edit .env with your local values

# 4. Run locally
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port {port}

# 5. Run tests
poetry run pytest

# 6. Quality check
poetry run ruff check . && poetry run ruff format .
poetry run mypy app/
```

---

## Quality Gates & Standards

### Valhalla Shield Engineering Standard

- **85% Test Coverage**: Minimum across all services
- **Structured JSON Logging**: To stdout only, never `print()`
- **OpenTelemetry Tracing**: Jaeger integration for distributed operations
- **Prometheus Metrics**: `/metrics` endpoints for all services

### Code Quality Tools

- **ruff**: Linting and formatting (replaces flake8, black, isort)
- **mypy**: Static type checking
- **pytest**: Testing framework with JUnit XML output
- **trunk**: Unified quality gate automation

### Commit Standards

```bash
# Before committing - ALWAYS run quality gates
trunk check --ci

# Commit message format
feat: add new feature
fix: resolve bug
docs: update documentation
refactor: improve code structure
test: add tests
```

### Testing Standards

- **Unit Tests**: 85% coverage minimum
- **Integration Tests**: Cross-service functionality
- **Junit XML Output**: `reports/junit-*.xml` for CI/CD
- **Test Fixtures**: Reusable test data and mocks

---

## Getting Help

### Documentation Resources
- `docs/` - Project documentation
- `AGENTS.md` - Agent hierarchy and protocols
- `README.md` - Project overview
- Service-specific READMEs in each service directory

### Communication Channels
- **Issues**: GitHub issues for bugs and features
- **Discussions**: GitHub discussions for questions
- **MAR Protocol**: Mandatory Agent Review for all changes

### Emergency Contacts
- **Infrastructure Issues**: Check `docker-compose.unified.yml` logs
- **Service Health**: Visit Grafana dashboard (http://localhost:3000)
- **Agent Issues**: Check RabbitMQ management (http://localhost:15672)

---

## Next Steps

1. **Complete DevContainer Setup**: Follow `docs/DevContainer_Access_Final_Steps.md`
2. **Run Quality Gates**: Execute `trunk check --ci`
3. **Explore Services**: Start with memos.as for knowledge management patterns
4. **Study Agent Architecture**: Review devenviro.as for multi-agent patterns
5. **Contribute**: Follow MAR protocol for all changes

Welcome to the ApexSigma ecosystem! The Society of Agents awaits your contributions. 🤖✨