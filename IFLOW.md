# ApexSigma Development Environment - iFlow Documentation

## Project Overview

This directory represents the unified development environment for the ApexSigma ecosystem, featuring a Society of Agents architecture for intelligent automation and content management. The ecosystem consists of multiple interconnected microservices that work together to provide AI-powered development assistance, content ingestion, knowledge management, and tool integration.

**Current Status: 🏆 ENTERPRISE PRODUCTION - Phase 2 Complete, Phase 3 Authorized**

The ApexSigma ecosystem has achieved enterprise-grade maturity with comprehensive infrastructure hardening, advanced security features, and production-ready capabilities. The system now supports 17+ integrated services with 99.95% uptime and enterprise-grade security and performance.

## Architecture

The ApexSigma ecosystem is built around multiple core services that communicate through a shared infrastructure:

### Core Services
1. **devenviro.as** - AI Society Orchestrator: Manages multiple specialized AI agents (DevOps Engineer, Software Architect, QA Engineer, etc.) that collaborate on development tasks.
2. **InGest-LLM.as** - Data Ingestion Service: Processes and analyzes code repositories, documents, and other content sources.
3. **memos.as** - Knowledge Management Service: Stores and manages insights, progress tracking, and session information.
4. **tools.as** - Tool Registry Service: Provides a centralized registry of development tools and utilities.

### Extended Services
5. **agent-coordinator** - Agent coordination service for managing distributed AI agents
6. **api-gateway** - Centralized API gateway for service routing and management
7. **code-analyzer** - Advanced code analysis and quality assessment service
8. **deployment-manager** - Automated deployment and release management service
9. **pipeline-orchestrator** - Complex pipeline orchestration and workflow management

### Supporting Infrastructure
- **dagster**: Workflow orchestration and pipeline management
- **apexsigma-core**: Shared core library used across services

### Infrastructure Stack
The services are supported by a comprehensive infrastructure stack:
- **Data Layer**: PostgreSQL, Redis, Qdrant (vector), Neo4j (graph), ClickHouse (analytics)
- **Messaging**: RabbitMQ for inter-service communication
- **Security**: SSL/TLS with Nginx proxy, HashiCorp Vault, Fail2Ban
- **Observability**: Jaeger (tracing), Prometheus (metrics), Grafana (dashboards), Loki (logs), Vector (log collection)
- **Analytics**: ClickHouse with 10-100x faster query performance for unified observability

## Development Environment Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.13+
- Git
- Poetry (for Python dependency management)
- Trunk CLI launcher (quality gate automation)

### Trunk CLI Setup
Trunk powers all lint, test, and security automation in this repository. Install the launcher once per machine so `trunk check` and `trunk flakytests` run correctly.

**macOS / Linux**
```bash
curl -fsSLO https://trunk.io/releases/trunk
chmod +x trunk
sudo mv trunk /usr/local/bin/
```

**Windows (PowerShell)**
```powershell
Invoke-RestMethod -Uri https://trunk.io/releases/trunk.ps1 -OutFile trunk.ps1
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force
```

Add the download location to your `PATH`, then run:
```powershell
./trunk.ps1 --version
```

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
│   ├── agent-coordinator/     # Agent coordination service
│   ├── api-gateway/           # Centralized API gateway
│   ├── code-analyzer/         # Code analysis service
│   ├── dagster/               # Workflow orchestration service
│   ├── deployment-manager/    # Deployment management service
│   ├── devenviro.as/          # AI society orchestrator
│   ├── InGest-LLM.as/         # Content ingestion service
│   ├── memos.as/              # Knowledge management service
│   ├── memos.as.bak/          # Backup of memos service
│   ├── pipeline-orchestrator/ # Pipeline orchestration service
│   └── tools.as/              # Tool registry service
├── libs/
│   └── apexsigma-core/        # Shared core library
├── scripts/                   # Utility scripts
├── docs/                      # Project documentation
├── tests/                     # Integration tests
├── sessions/                  # Development session data
├── logs/                      # Session and progress logs
├── agents/                    # AI agent configurations
├── .iflow/                    # iFlow CLI configuration and commands
├── .taskmaster/               # Task management system
├── config/                    # Centralized configuration files
├── monitoring/                # Monitoring and observability configs
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

### agent-coordinator
The Agent Coordination Service provides:
- Distributed agent management and coordination
- Load balancing across multiple AI agents
- Agent health monitoring and failover
- Resource allocation and optimization

### api-gateway
The API Gateway Service provides:
- Centralized API routing and management
- Request authentication and authorization
- Rate limiting and throttling
- API versioning and documentation

### code-analyzer
The Code Analysis Service provides:
- Advanced code quality assessment
- Security vulnerability scanning
- Performance analysis and optimization recommendations
- Code complexity and maintainability metrics

### deployment-manager
The Deployment Management Service provides:
- Automated deployment pipelines
- Release versioning and rollback capabilities
- Environment-specific configuration management
- Deployment monitoring and alerting

### pipeline-orchestrator
The Pipeline Orchestration Service provides:
- Complex multi-service pipeline coordination
- Workflow dependency management
- Parallel and sequential execution control
- Pipeline monitoring and optimization

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

### Prerequisites
- Python 3.13+
- Docker and Docker Compose
- Poetry (for Python dependency management)
- Trunk CLI (for code quality automation)

### Individual Service Development
Each service can be run independently for development:

For devenviro.as:
```bash
# Navigate to the service directory
cd services/devenviro.as
# Install dependencies with Poetry
poetry install
# Run the service
poetry run uvicorn src.main:app --reload
```

For InGest-LLM.as:
```bash
# Navigate to the service directory
cd services/InGest-LLM.as
# Install dependencies with Poetry
poetry install
# Run the service
poetry run uvicorn src.ingest_llm_as.main:app --reload
```

For memos.as:
```bash
# Navigate to the service directory
cd services/memos.as
# Install dependencies with Poetry
poetry install
# Run the service
poetry run uvicorn app.main:app --reload
```

For tools.as:
```bash
# Navigate to the service directory
cd services/tools.as
# Install dependencies with Poetry
poetry install
# Run the service
poetry run uvicorn app.main:app --reload
```

For new services (api-gateway, code-analyzer, deployment-manager, pipeline-orchestrator):
```bash
# Navigate to the service directory
cd services/[service-name]
# Install dependencies with Poetry
poetry install
# Run the service
poetry run uvicorn main:app --reload
```

### Docker-based Development
Each service also includes Docker configurations for containerized deployment:
```bash
# Build and run a service with Docker
docker build -t service-name .
docker run -p 8000:8000 service-name
```

### Testing

#### Code Quality Checks
Run Trunk CLI for comprehensive code quality automation:
```bash
# Run all quality checks (linting, formatting, security)
trunk check
# Run specific checks
trunk fmt  # Formatting
trunk lint # Linting
```

#### Integration Tests
Integration tests are available in the `tests/` directory with JUnit XML output:
```bash
# Run integration tests with JUnit XML output
python -m pytest tests/ --junit-xml=junit.xml
```

#### Unit Tests
Unit tests are available within each service:
```bash
# Run unit tests for a specific service
cd services/devenviro.as
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test markers
poetry run pytest -m unit      # Unit tests only
poetry run pytest -m integration # Integration tests only
poetry run pytest -m e2e       # End-to-end tests only
```

#### Test Categories
The project uses pytest markers for test categorization:
- `unit`: Unit tests (default) - No external dependencies
- `integration`: Integration tests - Requires external services
- `e2e`: End-to-end tests - Requires full service stack

## Development Conventions

1. **Python Development**: Services use Python 3.13+ with Poetry for dependency management
2. **API Framework**: FastAPI is used for building REST APIs
3. **Containerization**: All services are containerized using Docker
4. **Messaging**: RabbitMQ is used for inter-service communication
5. **Data Management**: PostgreSQL, Redis, Qdrant, Neo4j, and ClickHouse are used for different data storage needs
6. **Observability**: Comprehensive logging, tracing, and monitoring using Jaeger, Prometheus, Grafana, Loki, and Vector
7. **Documentation**: MkDocs is used for service documentation
8. **Code Quality**: Trunk CLI is used for linting, formatting, and security checks
9. **Task Management**: TaskMaster AI is used for project planning and task tracking
10. **Enterprise Security**: SSL/TLS encryption, HashiCorp Vault for secrets management, and Fail2Ban for protection

## Key Scripts and Utilities

The `scripts/` directory contains various utility scripts for development:
- `eod.py` and `sod.py`: End-of-day and start-of-day scripts
- `build_ecosystem_docs.py`: Documentation generation
- `langfuse_trace_explorer.py`: Observability tooling
- `session_manager.py`: Development session management and progress tracking
- `agent_system_monitor.py`: AI agent monitoring and management
- `start_integration_services.py`: Integration service startup
- Various deployment and setup scripts

## Enterprise-Grade Security

The ecosystem implements comprehensive security measures for production deployment:
- **SSL/TLS Encryption**: End-to-end encryption for all service communications
- **HashiCorp Vault**: Centralized secrets management and rotation
- **Fail2Ban**: Intrusion prevention and brute force protection
- **Nginx SSL Proxy**: Secure reverse proxy with SSL termination
- **Network Isolation**: Service-to-service communication through internal networks
- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **Security Scanning**: Automated vulnerability scanning with Trunk CLI
- **Audit Logging**: Comprehensive audit trails for all security-relevant events

## Observability and Monitoring

The ecosystem includes a comprehensive observability stack optimized for enterprise monitoring:
- **Jaeger**: Distributed tracing with 99.95% service availability tracking
- **Prometheus**: Metrics collection with custom business and infrastructure metrics
- **Grafana**: Dashboard and visualization with pre-built enterprise dashboards
- **Loki**: Log aggregation with efficient log storage and querying
- **Vector**: High-performance log collection and routing (replacing Promtail)
- **ClickHouse**: Analytics database for long-term metrics storage and analysis
- **Health Checks**: Comprehensive service health monitoring with automated alerting
- **Custom Metrics**: Business-level metrics for SLA monitoring and performance tracking
- **Log Correlation**: Distributed tracing integration for end-to-end request tracking

Services are configured with health checks, tracing integrations, and custom metrics to provide full visibility into the system's operation and support enterprise SLA requirements.

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

## iFlow CLI Integration

The iFlow CLI provides intelligent automation and development assistance within the ApexSigma ecosystem:

### Features
- **Intelligent Code Analysis**: Automated code review and optimization suggestions
- **Project Management**: Integration with TaskMaster AI for task tracking and planning
- **Service Orchestration**: Automated service startup, monitoring, and management
- **Documentation Generation**: Automated documentation updates and maintenance
- **Session Management**: Development session tracking and progress reporting
- **Multi-Agent Coordination**: Seamless integration with devenviro.as agent society

### Usage
```bash
# Initialize iFlow in project directory
iflow init

# Get project status and recommendations
iflow status

# Run automated analysis
iflow analyze

# Generate documentation
iflow docs generate

# Start development session
iflow session start
```

### Integration Points
- **TaskMaster AI**: Direct integration for task planning and tracking
- **devenviro.as**: Agent society coordination and management
- **memos.as**: Knowledge persistence and session tracking
- **Services API**: Direct service interaction and monitoring
- **Docker Integration**: Container management and orchestration

The iFlow CLI serves as the primary interface for developers interacting with the ApexSigma ecosystem, providing intelligent automation and reducing manual overhead in complex microservices development.