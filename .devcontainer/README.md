# ApexSigma DevContainer Setup

This DevContainer configuration provides a complete development environment for the ApexSigma ecosystem, implementing all Valhalla Shield quality standards and Omega Ingest Protocol compliance.

## 🚀 Quick Start

1. **Prerequisites**: Docker Desktop + VS Code Remote-Containers extension
2. **Open in DevContainer**: `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
3. **Wait for setup**: The automated setup takes ~5-10 minutes
4. **Start developing**: Use the provided aliases and VS Code tasks

## 🏗️ What's Included

### Development Environment

- **Python 3.13+** with Poetry dependency management
- **Node.js 20** for any JavaScript/TypeScript services
- **PowerShell** for SOD/EOD workflow automation
- **Comprehensive tooling**: Trunk, pre-commit, mypy, ruff, black, isort

### Database Clients

- **PostgreSQL**: `psql-connect` alias
- **Redis**: `redis-connect` alias
- **Neo4j**: `neo4j-connect` alias
- **ClickHouse**: `clickhouse-connect` alias

### VS Code Extensions

- Python development (ruff, mypy, black, isort)
- Docker and container tools
- Database clients and SQL support
- Testing and debugging tools
- Git and GitHub integration

### Quality Gates (Valhalla Shield)

- **85% test coverage** enforcement
- **Trunk CLI** for linting and formatting
- **JUnit XML** output for CI/CD integration
- **Pre-commit hooks** for quality enforcement

## 📋 Available Commands

### SOD/EOD Protocol

```bash
sod              # Start ecosystem (basic)
sod-force        # Start ecosystem (force cleanup)
sod-verbose      # Start ecosystem (verbose logging)
eod              # End of day protocol
eod-skip-tests   # End of day (skip tests)
```

### Service Management

```bash
services-up      # Start all services
services-down    # Stop all services
services-logs    # View service logs
services-ps      # Show service status
```

### Development

```bash
memos-run        # Start memOS service
tools-run        # Start tools service
ingest-run       # Start InGest-LLM service
devenviro-run    # Start DevEnviro service
```

### Quality & Testing

```bash
quality-check    # Run all quality checks
quality-fix      # Auto-fix issues
test-all         # Run all tests with coverage
test-memos       # Test memOS service
test-tools       # Test tools service
test-ingest      # Test InGest-LLM service
```

### Health Checks

```bash
health-check     # Check all local APIs
omega-check      # Check Omega Ingest services
```

## 🔧 Configuration Files

### devcontainer.json

- **Features**: Docker-in-Docker, GitHub CLI, Node.js, PowerShell, Python 3.13
- **Extensions**: 25+ VS Code extensions for comprehensive development
- **Ports**: All 17+ service ports forwarded with proper labeling
- **Environment**: Complete environment variable setup

### Dockerfile

- **Base**: Python 3.13-slim with comprehensive system dependencies
- **Tools**: Poetry, Node.js, PowerShell, database clients
- **Optimization**: Multi-stage build with layer caching

### setup.sh

- **12 phases** of automated environment setup
- **Quality enforcement**: Python 3.13+, Poetry config, Trunk CLI
- **Omega Ingest verification**: Health checks for protected services
- **Development aliases**: 25+ convenience commands
- **VS Code integration**: Tasks and debugging configurations

## 🐛 Debugging

### VS Code Launch Configurations

- **Service debugging**: Debug any of the 4 main services
- **Test debugging**: Debug pytest execution
- **File debugging**: Debug current Python file

### VS Code Tasks

- **Service startup**: Background tasks for each service
- **Health checks**: Automated service verification
- **Quality gates**: Integrated linting and testing

## 🔒 Governance Compliance

### Omega Ingest Protocol

- **Query verification**: InGest-LLM and memOS health checks
- **Dual verification**: MAR Protocol reminders
- **Immutable truth**: Context validation before changes

### Valhalla Shield Standards

- **85% coverage**: Enforced test coverage minimum
- **Quality gates**: Trunk CLI integration
- **Structured logging**: JSON logging configuration

## 🌐 Network Architecture

### Service Discovery

- **apexsigma_net**: Docker network for service communication
- **Static IPs**: Protected services have fixed IP addresses
- **DNS resolution**: Service names resolve within container network

### Port Mapping

```bash
8001  → DevEnviro API
8002  → Gemini Listener
8090  → memOS API
8000  → InGest-LLM API
8003  → Tools API
5432  → PostgreSQL
6379  → Redis
5672  → RabbitMQ AMQP
15672 → RabbitMQ Management
6333  → Qdrant
7474  → Neo4j Browser
7687  → Neo4j Bolt
9090  → Prometheus
3000  → Grafana
16686 → Jaeger
8200  → Vault
8889  → Dagster
3001  → Langfuse
9123  → ClickHouse
3080  → Dagster Web
```

## 📊 Monitoring & Observability

### Health Checks

- **Docker health checks**: All services have health endpoints
- **API monitoring**: Automated health verification
- **Omega Ingest**: Protected service monitoring

### Logging

- **Structured logging**: JSON format to stdout
- **Centralized aggregation**: Loki integration
- **Tracing**: Jaeger distributed tracing

## 🚨 Troubleshooting

### Common Issues

**Services not starting**:

```bash
# Check Docker network
docker network ls | grep apexsigma

# Verify service health
services-ps

# View service logs
services-logs
```

**Quality gates failing**:

```bash
# Check what failed
quality-check

# Auto-fix where possible
quality-fix

# Manual fixes
trunk check --fix
```

**Omega Ingest unavailable**:

```bash
# Check protected services
omega-check

# Start full ecosystem
sod-force
```

### Reset Environment

```bash
# Clean restart
services-down
docker system prune -f
sod-force
```

## 📚 Related Documentation

- [`.github/copilot-instructions.md`](../.github/copilot-instructions.md) - Complete development guide
- [`docs/protocols/The_Laws_of_Asgard_A_Primer_for_Agents_of_the_ApexSigma_Ecosystem.md`](../docs/protocols/The_Laws_of_Asgard_A_Primer_for_Agents_of_the_ApexSigma_Ecosystem.md) - Governance protocols
- [`AGENTS.md`](../AGENTS.md) - Agent hierarchy and protocols
- [`docker-compose.unified.yml`](../docker-compose.unified.yml) - Infrastructure definition

---

**Status**: ✅ **PRODUCTION READY** - Implements all Valhalla Shield standards and Omega Ingest Protocol compliance.
