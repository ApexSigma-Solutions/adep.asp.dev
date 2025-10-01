# ApexSigma Development Environment - iFlow Documentation

## Project Overview

This directory represents the unified development environment for the ApexSigma ecosystem, featuring a Society of Agents architecture for intelligent automation and content management. The ecosystem consists of multiple interconnected microservices that work together to provide AI-powered development assistance, content ingestion, knowledge management, and tool integration.

## Architecture

The ApexSigma ecosystem is built around four core services that communicate through a shared infrastructure:

1. **devenviro.as** - AI Society Orchestrator: Manages multiple specialized AI agents (DevOps Engineer, Software Architect, QA Engineer, etc.) that collaborate on development tasks.
2. **InGest-LLM.as** - Data Ingestion Service: Processes and analyzes code repositories, documents, and other content sources.
3. **memos.as** - Knowledge Management Service: Stores and manages insights, progress tracking, and session information.
4. **tools.as** - Tool Registry Service: Provides a centralized registry of development tools and utilities.

These services are supported by a comprehensive infrastructure stack including PostgreSQL, Redis, RabbitMQ, Qdrant, Neo4j for data management, and an observability stack with Jaeger, Prometheus, Grafana, and Loki for monitoring and tracing.

The ecosystem also includes additional supporting services:
- **dagster**: Workflow orchestration and pipeline management
- **apexsigma-core**: Shared core library used across services

## Development Environment Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Git
- Poetry (for Python dependency management)

### Quick Start
1. Clone the repository
2. Navigate to the project root directory
3. Start the unified infrastructure:
   ```bash
   docker-compose -f docker-compose.unified.yml up -d
   ```
4. Check service health:
   ```bash
   docker-compose -f docker-compose.unified.yml ps
   ```

### Directory Structure
```
ApexSigmaProjects.Dev/
├── services/
│   ├── devenviro.as/          # AI society orchestrator
│   ├── InGest-LLM.as/         # Content ingestion service
│   ├── memos.as/              # Knowledge management service
│   ├── tools.as/              # Tool registry service
│   └── dagster/               # Workflow orchestration service
├── libs/
│   └── apexsigma-core/        # Shared core library
├── scripts/                   # Utility scripts
├── docs/                      # Project documentation
├── tests/                     # Integration tests
├── sessions/                  # Development session data
├── logs/                      # Session and progress logs
├── agents/                    # AI agent configurations
├── .taskmaster/               # Task management system
└── docker-compose.unified.yml # Infrastructure definition
```

## Core Services

### devenviro.as
The AI Society Orchestrator manages a collection of specialized AI agents that collaborate on development tasks. Key components include:
- Agent orchestration API
- Multiple specialized agents (DevOps Engineer, Software Architect, QA Engineer, etc.)
- A2A (Agent-to-Agent) bridge for external agent communication
- Gemini CLI listener for command processing
- Comprehensive documentation using MkDocs
- Agent monitoring and management utilities

### InGest-LLM.as
The Data Ingestion Service processes and analyzes content from various sources:
- Repository analysis and documentation
- Content processing and vectorization
- Integration with Memos knowledge management
- Multi-model LLM analysis and summarization
- API endpoint documentation and testing

### memos.as
The Knowledge Management Service provides centralized storage and retrieval of insights:
- Content storage and retrieval
- Progress tracking and session management
- Integration hub for ecosystem components
- Enhanced search and analysis capabilities
- Backup and recovery mechanisms

### tools.as
The Tool Registry Service offers a centralized repository of development tools:
- Tool registration and management
- API endpoints for cross-project integration
- Shared utilities across projects
- Database management for tool metadata

### dagster
The Workflow Orchestration Service provides:
- Pipeline definition and execution
- Workflow scheduling and monitoring
- Data processing orchestration
- Integration with other ecosystem services

## Development Workflow

1. **Infrastructure**: All services run in a unified Docker stack defined by `docker-compose.unified.yml`
2. **Agents**: devenviro.as orchestrates multiple specialized agents (Claude, Gemini, etc.)
3. **Content**: InGest-LLM.as processes and analyzes code/documentation
4. **Knowledge**: memos.as stores and manages insights and progress
5. **Tools**: tools.as provides shared utilities and tooling
6. **Orchestration**: dagster manages complex workflows and data pipelines

## Running and Testing Services

### Individual Service Development
Each service can be run independently for development:

For devenviro.as:
```bash
# Navigate to the service directory
cd services/devenviro.as
# Install dependencies
poetry install
# Run the service
poetry run uvicorn src.main:app --reload
```

For InGest-LLM.as:
```bash
# Navigate to the service directory
cd services/InGest-LLM.as
# Install dependencies
poetry install
# Run the service
poetry run uvicorn src.ingest_llm_as.main:app --reload
```

For memos.as:
```bash
# Navigate to the service directory
cd services/memos.as
# Install dependencies
poetry install
# Run the service
poetry run uvicorn app.main:app --reload
```

For tools.as:
```bash
# Navigate to the service directory
cd services/tools.as
# Install dependencies
poetry install
# Run the service
poetry run uvicorn app.main:app --reload
```

### Docker-based Development
Each service also includes Docker configurations for containerized deployment:
```bash
# Build and run a service with Docker
docker build -t service-name .
docker run -p 8000:8000 service-name
```

### Testing
Integration tests are available in the `tests/` directory:
```bash
# Run integration tests
python -m pytest tests/
```

Unit tests are also available within each service:
```bash
# Run unit tests for a specific service
cd services/devenviro.as
poetry run pytest
```

## Development Conventions

1. **Python Development**: Services use Python 3.11+ with Poetry for dependency management
2. **API Framework**: FastAPI is used for building REST APIs
3. **Containerization**: All services are containerized using Docker
4. **Messaging**: RabbitMQ is used for inter-service communication
5. **Data Management**: PostgreSQL, Redis, Qdrant, and Neo4j are used for different data storage needs
6. **Observability**: Comprehensive logging, tracing, and monitoring using Jaeger, Prometheus, Grafana, and Loki
7. **Documentation**: MkDocs is used for service documentation
8. **Code Quality**: Trunk is used for linting, formatting, and security checks
9. **Task Management**: TaskMaster AI is used for project planning and task tracking

## Key Scripts and Utilities

The `scripts/` directory contains various utility scripts for development:
- `eod.py` and `sod.py`: End-of-day and start-of-day scripts
- `build_ecosystem_docs.py`: Documentation generation
- `langfuse_trace_explorer.py`: Observability tooling
- `session_manager.py`: Development session management and progress tracking
- `agent_system_monitor.py`: AI agent monitoring and management
- `start_integration_services.py`: Integration service startup
- Various deployment and setup scripts

## Observability and Monitoring

The ecosystem includes a comprehensive observability stack:
- **Jaeger**: Distributed tracing
- **Prometheus**: Metrics collection
- **Grafana**: Dashboard and visualization
- **Loki**: Log aggregation
- **Promtail**: Log shipping

Services are configured with health checks and tracing integrations to provide full visibility into the system's operation.

## Task Management

The project uses TaskMaster AI for project planning and task tracking:
- Tasks are defined in `.taskmaster/tasks/tasks.json`
- Task complexity analysis is available in `.taskmaster/reports/task-complexity-report.json`
- Task templates are available in `.taskmaster/templates/`

## Session Management

Development sessions are tracked in the `sessions/` directory:
- Session data is stored in JSON format
- Session progress is logged and tracked
- Integration with memos.as for knowledge persistence

## Agent Management

AI agents are configured and managed through:
- Agent definitions in the `agents/` directory
- Agent monitoring through `agent_system_monitor.py`
- Agent communication via RabbitMQ message queues