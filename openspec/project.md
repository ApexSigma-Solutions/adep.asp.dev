# Project Context

## Purpose
The ApexSigma Ecosystem is a multi-agent AI system designed for collaborative development and knowledge management. It implements a Society of Agents Architecture where specialized AI agents (Claude, Gemini, Gemma) work together through orchestrated microservices to build, maintain, and evolve complex software systems. The system focuses on maintaining an immutable knowledge graph (Omega Ingest) for audit trails, automated testing with 85% coverage minimum, and production-ready infrastructure with observability and security hardening.

Key goals include:
- Agent-driven development with human oversight
- Knowledge continuity through automated ingestion
- Valhalla Shield engineering standards (85% test coverage, structured logging, OpenTelemetry tracing)
- MCP (Model Context Protocol) integration for AI agent communication

## Tech Stack
- **Programming Language**: Python 3.13+ (mandatory across all services)
- **Dependency Management**: Poetry (never use pip directly)
- **Web Framework**: FastAPI with Pydantic for API development
- **Databases**: PostgreSQL (procedural data), Redis (cache), Qdrant (vector search), Neo4j (knowledge graphs)
- **Messaging**: RabbitMQ for agent-to-agent communication
- **Containerization**: Docker with docker-compose.unified.yml for full ecosystem deployment
- **Observability**: Prometheus + Jaeger (tracing) + Loki (logs) + Grafana (dashboards)
- **Quality Gates**: Trunk (linting, formatting, testing with ruff, black, isort, mypy, flake8)
- **Testing**: pytest with JUnit XML output, 85% minimum coverage
- **Migrations**: Alembic for database schema changes
- **Logging**: structlog with JSON format to stdout (never use print statements)
- **AI Integration**: Langfuse for operation tracing, MCP servers for agent communication

## Project Conventions

### Code Style
- **Formatting**: Black for code formatting, isort for import sorting
- **Linting**: ruff for fast Python linting (replaces flake8, pylint)
- **Type Checking**: mypy for static type analysis
- **Quality Checks**: `trunk check --ci` mandatory before commits (enforces Valhalla Shield standards)
- **Naming**: snake_case for variables/functions, PascalCase for classes, UPPER_CASE for constants
- **Imports**: Absolute imports preferred, relative imports only within same package
- **Docstrings**: Google-style docstrings for all public functions/classes
- **Line Length**: 88 characters (Black default)

### Architecture Patterns
- **Microservices**: Each service runs in separate Docker container with static IP addresses
- **Shared Models**: All services import from `apexsigma_core.models` (StoreRequest, QueryRequest, AgentPersona, Task)
- **API Design**: RESTful APIs with OpenAPI/Swagger documentation
- **Dependency Injection**: FastAPI dependency injection for services
- **CORS**: Enabled for cross-service communication in development
- **Health Checks**: `/health` endpoint required for all services
- **Metrics**: `/metrics` endpoint with Prometheus format for monitoring
- **Error Handling**: Structured error responses with appropriate HTTP status codes
- **Configuration**: Environment variables via `.env` files, never hardcoded

### Testing Strategy
- **Framework**: pytest with fixtures and parametrization
- **Coverage**: Minimum 85% coverage across all services (Valhalla Shield requirement)
- **Output**: JUnit XML format (`junit_family = xunit1`) for CI/CD integration
- **Types**: Unit tests, integration tests (via docker-compose.ci.yml), end-to-end tests
- **Mocking**: Use pytest-mock for external dependencies
- **CI/CD**: Tests run via `trunk run run-tests` and in GitHub Actions
- **Quality Gates**: Tests must pass before commits (enforced by trunk check)

### Git Workflow
- **Branching**: Feature branches from `alpha`, PRs require MAR (Mandatory Agent Review) protocol
- **Commits**: Conventional commits with type/scope/description
- **Reviews**: Dual verification (human + AI agent) before merge
- **SOD/EOD Cycle**: Start of Day (`sod.ps1`) deploys ecosystem, End of Day (`eod.ps1`) captures progress and ingests to knowledge graph
- **Merge Strategy**: Squash merges to maintain clean history
- **Protection**: Branch protection on `alpha` with required checks

## Domain Context
The ApexSigma Ecosystem operates in the domain of AI-driven software development, where multiple AI agents collaborate on complex projects. Key concepts include:
- **Omega Ingest**: Immutable knowledge graph maintained through automated ingestion of development progress
- **Society of Agents**: Hierarchical agent structure with specialized roles (Orchestrator, Reviewer, Implementor)
- **Valhalla Shield**: Engineering excellence standard with high test coverage and observability
- **MCP Protocol**: Model Context Protocol for standardized AI agent communication
- **Knowledge Continuity**: Automated capture of development sessions to prevent knowledge loss

## Important Constraints
- **Python Version**: 3.13+ only (entire ecosystem standardized)
- **Dependency Management**: Poetry exclusively, no pip usage
- **Network Topology**: Fixed static IPs in `apexsigma_net` (172.26.0.0/16) - documented in VERIFIED_DOCKER_NETWORK_MAP_V3.md
- **Security**: No hardcoded secrets, environment variables only
- **Quality Gates**: trunk check failures block commits
- **Agent Protocols**: MAR (Mandatory Agent Review) required for all changes
- **Knowledge Graph**: All progress must be ingested via SOD/EOD cycle

## External Dependencies
- **Langfuse**: AI operation tracing and monitoring (separate projects per service)
- **Qdrant**: Vector similarity search for semantic content ingestion
- **Neo4j**: Knowledge graph storage and Cypher queries
- **RabbitMQ**: Message queuing for agent-to-agent communication
- **Prometheus/Grafana**: Monitoring and visualization stack
- **Jaeger**: Distributed tracing for microservices
- **Docker Hub**: Container registry for base images
- **GitHub**: Version control and CI/CD pipelines
