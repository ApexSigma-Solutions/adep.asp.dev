# QWEN.md - DevEnviro Society of Agents Project

## Project Overview

This project, `devenviro.as`, is a modular, agentic AI-supported development environment implementing a **"Society of Agents"** architecture. Specialized AI agents collaborate on complex development tasks orchestrated by a central FastAPI service. The primary goal is to improve developer Quality of Life (QoL) by creating persistent, context-aware AI partners that reduce cognitive load and automate workflows.

A foundational principle is **"Hierarchical Context is King."** All agent actions are grounded in the project's documentation stored in the `.md/` directories, which serve as the single source of truth for architecture, rules, and tasks.

## Key Technologies & Architecture

- **Core Platform**: Python 3.11, FastAPI
- **Agent Communication**: RabbitMQ message queue for asynchronous inter-agent messaging
- **Memory Engine**:
  - PostgreSQL: Episodic memory (agent communications)
  - Redis: High-speed working memory (session state, caching)
  - Qdrant: Vector database for semantic memory (semantic search on experiences)
- **Persistence & Configuration**: Docker, Docker Compose, dotenvx for environment management
- **Observability Stack**: OpenTelemetry with Jaeger (traces), Prometheus (metrics), Loki (logs), Grafana (dashboards)
- **Documentation**: MkDocs with Material theme

## Directory Structure

```
devenviro.as/
├── .md/                       # Project knowledge base (rules, personas, plans) - PRIMARY SOURCE OF TRUTH
├── app/                       # Main application code
│   ├── src/                   # Core application source
│   │   ├── core/              # Core services (orchestrator, agent registry, communications, DB)
│   │   ├── listeners/         # Specialized agent listeners (e.g., gemini_cli_listener.py)
│   │   ├── Workflows/         # Multi-agent collaborative workflows
│   │   ├── main.py            # FastAPI application entry point
│   │   └── ...                # Other core modules
│   ├── migrations/            # Database schema migrations (SQL)
│   └── tests/                 # Application tests
├── config/                    # Infrastructure configuration (Prometheus, Grafana, Loki)
├── Dockerfile                 # Application Docker image definition
├── docker-compose.yml         # Full stack service definitions
├── requirements-docker.txt    # Python dependencies for Docker build
└── ...                        # Other configuration and documentation files
```

## Building and Running

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development/tests)
- Node.js and npm (for dotenvx)

### Environment Setup

Environment variables are managed using `dotenvx`.

1.  Install `dotenvx` globally:
    ```bash
    npm install -g @dotenvx/dotenvx
    ```
2.  Set required secrets (you will be prompted):
    ```bash
    dotenvx set POSTGRES_USER myuser
    dotenvx set POSTGRES_PASSWORD mypassword
    dotenvx set RABBITMQ_USER myuser
    dotenvx set RABBITMQ_PASSWORD mypassword
    # Add others as needed, see .env.template
    ```

### Running the Full Stack

The project is designed to run using Docker Compose, which brings up all services defined in `docker-compose.yml`.

```bash
# Build and start all services in detached mode
docker-compose up --build -d
```

### Key Services and Ports

- **API (Orchestrator)**: http://localhost:8090 (API Docs at /docs)
- **Grafana**: http://localhost:8080 (Default login: admin/devenviro123)
- **Prometheus**: http://localhost:9090
- **Jaeger Tracing**: http://localhost:16686
- **RabbitMQ Management**: http://localhost:15672
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Qdrant UI**: http://localhost:6333

### Database Operations

The `devenviro-api` service automatically applies migrations and seeds knowledge on startup.

- **Migrations**: SQL files in `app/migrations/` are applied by `app/src/core/migrations_runner.py`.
- **Knowledge Seeding**: Markdown files from the `.md/` directory are loaded into the `knowledge_documents` table by `app/src/core/seed_knowledge.py`.

## Development Workflow

1.  **Modify Code/Docs**: Edit files in `app/src/` for logic or `.md/` for agent context/rules.
2.  **Run Tests**: Execute specific tests as needed (e.g., `python app/tests/test_telemetry_stack.py`).
3.  **Build & Deploy**: Use `docker-compose up --build` to rebuild and restart services with changes.
4.  **Interact**: Use the FastAPI docs at `http://localhost:8090/docs` or send messages via RabbitMQ to interact with the agent society.

## Testing

Run specific test scripts for different components:

```bash
# Run the comprehensive telemetry stack validation test
python app/tests/test_telemetry_stack.py

# Run a demonstration of the agent communication system and workflow manager
python app/src/demo_agent_communication.py
```

## Core Components (Detailed)

- **Orchestrator (`app/src/core/orchestrator.py`)**: The central nervous system. Decomposes user requests into tasks and delegates them to agents. Manages workflows and task status.
- **Agent Registry (`app/src/core/agent_registry.py`, `app/src/core/enhanced_initialization_manager.py`)**: Loads agent personas from `.md/.agent/.personas/`, manages their lifecycle, registration, and capabilities. Initializes agent listeners.
- **Communications Manager (`app/src/core/communications_manager.py`)**: Handles all RabbitMQ messaging, routing, and logging messages to PostgreSQL.
- **Database Manager (`app/src/core/database_manager.py`)**: Thread-safe singleton for all PostgreSQL interactions.
- **Observability (`app/src/core/observability.py`)**: Sets up OpenTelemetry tracing, metrics, and integrates with LLM monitoring.

This `QWEN.md` provides the essential context for working with the `devenviro.as` project.