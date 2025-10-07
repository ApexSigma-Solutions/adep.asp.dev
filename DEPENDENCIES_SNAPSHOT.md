# ApexSigma Services Dependencies Snapshot
# Generated on: October 8, 2025
# This file contains dependency snapshots for all ApexSigma services

## Services Overview

- memos.as: Memory and knowledge management service
- devenviro.as: Agent orchestration and development environment service
- tools.as: Tool execution and API service
- InGest-LLM.as: Content ingestion and LLM processing service
- apexsigma-core: Shared library for common functionality

## Dependency Management

All services use Poetry for dependency management with the following key packages:

### Core Dependencies (across all services)
- FastAPI: Web framework
- Pydantic: Data validation
- SQLAlchemy: Database ORM
- Redis: Caching and session storage
- PostgreSQL: Primary database
- RabbitMQ: Message queuing

### Security & Secrets
- HashiCorp Vault: Secrets management (newly integrated)
- hvac: Vault client library

### Observability
- Langfuse: AI operation tracing
- OpenTelemetry: Distributed tracing
- Prometheus: Metrics collection
- Jaeger: Trace visualization

## Individual Service Dependencies

See the individual dependency files for detailed trees:
- dependencies-memos.txt
- dependencies-devenviro.txt
- dependencies-tools.txt
- dependencies-ingest-llm.txt
- dependencies-apexsigma-core.txt

## Recent Changes

### HashiCorp Vault Integration (October 2025)
- Added Vault service to docker-compose.unified.yml
- Integrated hvac library for secrets management
- Migrated all sensitive credentials from .env files to Vault
- Updated all services to fetch secrets from Vault at runtime
- Enhanced security by removing exposed secrets from codebase

### Configuration Standardization
- Migrated all services to use Pydantic BaseSettings
- Standardized environment variable handling
- Added type-safe configuration validation

## Deployment Notes

- All services run in Docker containers with docker-compose
- Vault service provides centralized secrets management
- Services auto-detect Vault URL (localhost for development, container name for production)
- Dependencies are locked via poetry.lock files for reproducible builds