# QWEN.md - ApexSigma Ecosystem Development Environment

## Project Overview

This is the unified development environment for the **ApexSigma ecosystem**, featuring a Society of Agents architecture for intelligent automation and content management. The monorepo contains four main interconnected services that work together to provide an AI-powered development environment:

- **devenviro.as**: Agent orchestration and management platform
- **InGest-LLM.as**: Intelligent content ingestion engine  
- **memos.as**: Knowledge management system
- **tools.as**: Development utilities and APIs

## Architecture & Technologies

### Core Platform
- **Language**: Python 3.13 (primary), with some services using Python 3.9+
- **Framework**: FastAPI for all main services
- **Package Management**: Poetry (primary) and npm for some utilities
- **Infrastructure**: Docker Compose for unified deployment (17+ services)

### Infrastructure Stack
- **Database Layer**: PostgreSQL (primary), Redis (caching), Qdrant (vector database), Neo4j (graph database)
- **Message Queue**: RabbitMQ for agent communication
- **Observability**: Langfuse (tracing), Jaeger (distributed tracing), Prometheus (metrics), Grafana (visualization), Loki/Promtail (logging)
- **Data Orchestration**: Dagster for data pipeline management

### Key Dependencies (Across Services)
- FastAPI, Uvicorn
- Pydantic (validation/settings)
- OpenTelemetry (observability)
- Langfuse (LLM tracing)
- SQLAlchemy, Redis, Qdrant Client
- Various AI/ML libraries (OpenAI, Google Generative AI)

## Directory Structure

```
ApexSigmaProjects.Dev/
├── services/                 # Main service implementations
│   ├── devenviro.as/         # Agent orchestration platform
│   ├── InGest-LLM.as/        # Content ingestion engine
│   ├── memos.as/             # Knowledge management
│   └── tools.as/             # Development utilities
├── agents/                   # AI agent definitions and tools
├── docs/                     # Project documentation
├── libs/                     # Shared libraries (apexsigma-core)
├── scripts/                  # Utility and deployment scripts
├── tests/                    # Integration tests
├── monitoring/               # Observability configurations
├── .taskmaster/              # Task management system
└── docker-compose.unified.yml # Unified infrastructure definition
```

## Services Overview

### 1. devenviro.as - Agent Orchestration
- **Purpose**: Society of Agents platform for AI collaboration
- **Architecture**: Multi-agent system with RabbitMQ messaging
- **Agents**: Claude, Gemini, and Gemma agents with role-specific tokens
- **Components**: API service, CLI listeners, A2A bridge, documentation server
- **Status**: Agent foundation operational, CLI integration pending

### 2. InGest-LLM.as - Content Ingestion Engine
- **Purpose**: Intelligent content processing and analysis
- **Features**: Repository analysis, documentation processing, vectorization
- **Integrations**: LM Studio for embeddings, Memos for storage
- **Status**: Core ingestion pipeline operational
- **API**: Available on port 18000

### 3. memos.as - Knowledge Management
- **Purpose**: Centralized content storage and retrieval
- **Features**: Multi-tier storage (PostgreSQL, Qdrant, Neo4j), progress tracking
- **Status**: Production-ready with progress logging
- **API**: Available on port 8090

### 4. tools.as - Utilities Service
- **Purpose**: Shared tools and cross-project integration APIs
- **Features**: Tool registry, API endpoints for ecosystem components
- **Status**: Core functionality operational

## Infrastructure & Deployment

### Docker Compose Setup
The ecosystem uses a unified Docker Compose file (`docker-compose.unified.yml`) that orchestrates all services:

**Infrastructure Services**:
- PostgreSQL (port 5432)
- Redis (port 6379) 
- RabbitMQ (ports 5672, 15672)
- Qdrant (ports 6333, 6334)
- Neo4j (port 7687)

**Observability Stack**:
- Jaeger (port 16686)
- Prometheus (port 9090)
- Grafana (port 8080)
- Loki (port 9100)

### Quick Start Commands
```bash
# Start the unified infrastructure
docker-compose -f docker-compose.unified.yml up -d

# Check service health
docker-compose -f docker-compose.unified.yml ps

# View observability
# Langfuse: http://localhost:3000
# Grafana: http://localhost:8080
# Jaeger: http://localhost:16686
```

## Development Workflow

1. **Setup**: Install Docker, Docker Compose, Python 3.13+, Poetry
2. **Initialize**: Run the unified Docker stack
3. **Develop**: Work on individual services in the `services/` directory
4. **Test**: Use integrated testing frameworks (pytest, etc.)
5. **Monitor**: Use Langfuse, Grafana, and other observability tools

## Quality Assurance

- **Trunk CLI**: Used for linting, testing, and security automation
- **Testing**: Pytest with coverage reports
- **Code Quality**: Ruff, mypy, pre-commit hooks
- **Documentation**: MkDocs for API references and guides

## Key Files & Configuration

- `docker-compose.unified.yml`: Core infrastructure definition
- `pyproject.toml`: Main monorepo package definition
- `trunk.yaml`: Quality gate automation configuration
- `apexsigma.code-workspace`: VS Code workspace configuration
- Individual service `pyproject.toml` files for service-specific dependencies

## Support & Documentation

- **Project Docs**: Each service has comprehensive documentation in respective `docs/` directories
- **API Reference**: Available via FastAPI docs (each service on its port)
- **Session Logs**: Progress tracking in `logs/` directory
- **Health Status**: Monitor via unified Docker stack and observability tools

---
**Last Analysis**: September 29, 2025  
**Ecosystem Status**: Operational - Ready for advanced agent integration