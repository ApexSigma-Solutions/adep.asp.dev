---
aliases: [CLAUDE.md]
linter-yaml-title-alias: CLAUDE.md
date created: 266,23O September9 2025 12:16 pm 
date modified: 266,23O September9 2025 11:34 pm 
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[byterover-mcp]

# Important

Always use byterover-retrive-knowledge tool to get the related context before any tasks

Always use byterover-store-knowledge to store all the critical informations after sucessful tasks

## HOUSEKEEPING

**PROJECT DEVELOPMENT KNOWLEDGE**

   - PROJECT KNOWLDGE : All markdonwn documents pertaining to the project are stored in the `.md/.project` directory.
   - AGENT PERSONAS & ROLES : All markdown documents pertaining to the agents are stored in the `.md/.agents` directory.
   - RULESETS : All markdown documents pertaining to the immutable rules for the projects are stored in the `.md/.rules` directory.
   - SCAFFOLDING : All markdown templates used to the scaffold a new project are stored in the `.md/.scaffold` directory.
   - PERSISTANT KNOWLEDGE : All markdown documents pertaining to the persistence of the projects context across sessions, are stored in the `.md/.persist` directory.
   - TESTING : All markdown documents and python sctipts pertaining to the testing of the projects are stored in the `.md/.tests` directory.
   - PROJECT TEMPLATES : All project templates will be stored under `.md/.temp` directory.

# DevEnviro: AI Society of Agents Platform

DevEnviro is a modular, agentic AI-supported development environment implementing a "Society of Agents" architecture where specialized AI agents (Claude, Gemini, Gemma) collaborate through centralized orchestration.

## Core Architecture

### Agent Hierarchy

- **Claude**: Strategic Architect - System design, complex problem decomposition, code review
- **Gemini**: Implementer Agent - Full-stack development and code generation
- **Gemma**: Local Assistant - Routine tasks via Ollama integration

### Central Infrastructure

- **FastAPI Orchestrator**: Central nervous system at `app/src/core/orchestrator.py`
- **DatabaseManager**: Thread-safe singleton PostgreSQL manager with connection pooling at `app/src/core/database_manager.py`
- **CommunicationsManager**: RabbitMQ message routing with PostgreSQL episodic memory logging at `app/src/core/communications_manager.py`
- **Message Schema**: Pydantic models for inter-agent communication at `app/src/core/schemas.py`

### Multi-Tiered Memory Engine

- **Redis**: Working memory for session state (port 6379)
- **PostgreSQL**: Episodic memory with `agent_communications` table (port 5432)
- **Qdrant**: Vector database for semantic memory (ports 6333/6334)
- **RabbitMQ**: Asynchronous message queuing (ports 5672/15672)

### Observability Stack

- **Dual Observability**: Opik for LLM tracking + OpenTelemetry for system tracing
- **trace_span**: Context manager for distributed tracing
- **track_llm**: Decorator for LLM operation monitoring
- **DevEnviroObservability**: Central observability coordination class

## Development Commands

### Environment Setup & Secrets

```bash
# Install dotenvx for environment management
npm install -g @dotenvx/dotenvx

# Configure secrets via dotenvx
dotenvx set POSTGRES_USER myuser
dotenvx set GEMINI_API_KEYS "key1,key2"

# Build and start all services
docker-compose up --build -d
```

### Service Management

```bash
# Check service status
docker-compose ps

# View service logs
docker-compose logs -f devenviro_postgres
docker-compose logs -f devenviro_rabbitmq

# Rebuild specific service
docker-compose build cli-agent
docker-compose up -d --no-deps cli-agent
```

### Database Operations

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# Check agent communications
docker-compose exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT * FROM agent_communications ORDER BY timestamp DESC LIMIT 10;"
```

### Agent Testing

```bash
# Test multi-model CLI agent
docker-compose exec cli-agent python core/multi_model_cli_agent.py

# Check RabbitMQ queues
docker-compose exec rabbitmq rabbitmqctl list_queues
```

## Key Development Patterns

### Agent Communication Flow

1. Messages created using `create_message()` from `schemas.py`
2. Routed via `CommunicationsManager.send_message()` through RabbitMQ
3. Automatically logged to PostgreSQL via `log_message_to_db()`
4. Consumed by target agents with validation via `validate_payload()`

### Database Architecture

- **Singleton Pattern**: `DatabaseManager` with thread-safe connection pooling
- **Connection Pool**: Configurable min/max connections (2-15 default)
- **Retry Logic**: Exponential backoff for failed operations
- **Schema**: `agent_communications` table with JSONB message_payload column

### MAR Protocol (Mandatory Artifact Review)

- All artifacts require peer review by another agent
- Implemented in `app/src/core/mar_protocol.py`
- Integrates with database logging for audit trails

### Observability Integration

- **LLM Operations**: Use `@track_llm()` decorator for Opik tracking
- **System Operations**: Use `trace_span()` context manager for OpenTelemetry
- **Dual Export**: Jaeger + OTLP exporters for comprehensive monitoring

## Environment Variables

Critical configuration via dotenvx:

- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: Database credentials
- `RABBITMQ_URL`: Message queue connection string
- `GEMINI_API_KEYS`: Comma-separated API keys for Gemini models
- `DB_MIN_CONN`, `DB_MAX_CONN`: Database connection pool sizing
- `OPIK_API_KEY`, `OPIK_PROJECT_NAME`: LLM observability configuration

## Service Endpoints

- **FastAPI Orchestrator**: <http://localhost:8090/docs>
- **RabbitMQ Management**: <http://localhost:15672> (guest/guest)
- **Qdrant Console**: <http://localhost:6333/dashboard>
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Agent Container Architecture

Each agent runs in isolated Docker containers with:

- **Base Image**: Python 3.11-slim with Node.js for CLI tools
- **Environment**: dotenvx for secure secret management
- **Dependencies**: Optimized with UV package installer
- **Networking**: Docker Compose service discovery
- **Persistence**: Shared volumes for data persistence

## Multi-Model CLI Integration

The `multi_model_cli_agent.py` provides:

- **Model Routing**: Intelligent selection between Claude, Gemini, Gemma
- **Queue Processing**: Consumes from RabbitMQ agent queues
- **Local LLM**: Ollama integration for cost-effective local processing
- **Fallback Logic**: Graceful degradation between model providers

## Architecture Philosophy

**"Solve problems, not create new ones"** - Every component emphasizes:
- Persistent context across agent interactions
- Automatic observability and episodic memory
- Self-regulating behavior through peer review
- Modular, containerized deployment
- Multi-tiered memory for different cognitive functions