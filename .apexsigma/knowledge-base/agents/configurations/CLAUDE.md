# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `tools.as` - a standalone, modular microservice providing essential, reusable tools for a "Society of Agents" ecosystem. The server is designed to be fully decoupled, API-first, and self-contained, built with FastAPI and SQLAlchemy.

## Architecture

### Directory Structure
```
/app/                    # Application code
  ├── main.py           # FastAPI application
  ├── database.py       # Database configuration  
  ├── models.py         # SQLAlchemy models
  ├── schemas.py        # Pydantic schemas
  └── tests/            # Test suite
/.md/                   # Source of Truth documentation
/Ingest_LLM/           # Agent ingestion artifacts
/scripts/              # Utility scripts
docker-compose.yml     # Production setup (PostgreSQL)
docker-compose.dev.yml # Development setup (SQLite)
```

### Core Components
- **FastAPI Application** (`app/main.py`): Main server with dependency injection
- **Database Layer**: SQLAlchemy ORM supporting SQLite (dev) and PostgreSQL (prod)
- **API Schemas**: Pydantic models for request/response validation (`app/schemas.py`)
- **Multi-tenant Design**: Agent-specific data isolation using `owner_agent_id` fields

### Key Features
1. **Web Search Tool**: Stateless search via Serper API
2. **Multi-Tenant To-Do Lists**: Persistent planning tool with agent-specific lists and items
3. **Multi-Tenant Scratch Pad**: Persistent unstructured storage per agent
4. **Database Migrations**: Alembic integration for schema management

### Database Schema
- `TodoList`: Agent-owned lists with cascading item deletion
- `TodoItem`: Individual tasks linked to lists  
- `Scratchpad`: Agent-specific text storage with timestamp tracking

## Development Commands

### Docker Compose (Recommended)
```bash
# Development with SQLite
./scripts/docker-dev.sh up

# Production with PostgreSQL  
./scripts/docker-dev.sh up-prod

# Stop all services
./scripts/docker-dev.sh down

# Run tests in container
./scripts/docker-dev.sh test

# Open shell in app container
./scripts/docker-dev.sh shell

# Access PostgreSQL shell (prod mode)
./scripts/docker-dev.sh db-shell
```

### Poetry-based Development (Local)
```bash
# Install Poetry dependencies
poetry install

# Run development server with auto-reload
poetry run uvicorn app.main:app --reload

# Run tests
poetry run pytest app/tests/

# Run specific test
poetry run pytest app/tests/test_main.py::test_web_search_success

# Format code with Ruff
poetry run ruff format app/ 

# Lint and fix code with Ruff
poetry run ruff check --fix app/
```

### Legacy Development (pip-based)
```bash
# Install dependencies (if not using Poetry)
pip install -r requirements.txt

# Run development server with auto-reload
uvicorn app.main:app --reload

# Run tests
python -m pytest app/tests/
```

### Database Operations
```bash
# Database migrations are handled automatically on startup
# Manual migration operations would use alembic in context_portal/ directory
```

## Environment Configuration

Required environment variables:
- `SERPER_API_KEY`: API key for Google Serper search service
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)

Create `.env` file in project root:
```
SERPER_API_KEY="your_api_key_here"
# For PostgreSQL (production)
DATABASE_URL="postgresql://tools_user:tools_pass@localhost:5432/tools_db"
# For SQLite (development) - default if not set
# DATABASE_URL="sqlite:///./toolkit.db"
```

## API Structure

All endpoints follow REST conventions:
- Web Search: `POST /tools/search`
- To-Do Lists: `/todos/{agent_id}/lists`, `/todos/lists/{list_id}/items`, `/todos/items/{item_id}`
- Scratch Pad: `/scratchpad/{agent_id}` (GET/POST/DELETE)

Interactive API documentation available at `/docs` when server is running.

## Testing

- Test database: `test.db` (separate from production `toolkit.db`)
- Mocked external dependencies (Serper API)
- FastAPI TestClient for endpoint testing
- Database dependency overrides for test isolation

## Modern Python Toolchain

This project follows the ApexSigma ecosystem standards using:
- **Poetry**: Dependency management and packaging
- **Ruff**: Fast Python linter and formatter (replaces Black, isort, flake8)
- **Python 3.13+**: Latest Python version for optimal performance

## Key Dependencies

- **FastAPI**: Web framework with automatic OpenAPI docs
- **SQLAlchemy**: ORM supporting SQLite and PostgreSQL
- **Pydantic**: Data validation and settings management
- **Alembic**: Database migration management
- **psycopg2-binary**: PostgreSQL adapter for production
- **pytest**: Testing framework with mocking support

## Docker & Production

- **Multi-stage setup**: Development (SQLite) and Production (PostgreSQL)
- **Health checks**: Built-in container health monitoring
- **Database initialization**: Automatic schema creation and seeding
- **Security**: Non-root user, minimal container surface

## Code Quality

All code is formatted and linted with Ruff for consistency. The codebase follows:
- PEP 8 style guidelines
- Automatic import sorting
- Consistent code formatting
- Linting rules for code quality