# Society of Agents Deploy (SOD) - Autonomous Deployment Guide

The `/sod` command provides complete autonomous deployment for the ApexSigma Society of Agents ecosystem, including comprehensive container orchestration, health checks, and service deployment.

## Quick Start

### Windows
```cmd
sod.bat
# or with options:
sod.bat --force --verbose
```

### Linux/macOS
```bash
python sod.py
# or with options:
python sod.py --force --verbose
```

## Command Options

| Option | Description |
|--------|-------------|
| `--force` | Force cleanup of existing containers before deployment |
| `--skip-audit` | Skip the comprehensive health check audit |
| `--verbose` / `-v` | Enable verbose logging for troubleshooting |

## Deployment Phases

The SOD command executes deployment in 8 sequential phases:

### Phase 0: Prerequisites Check
- Verifies Docker and Docker Compose installation
- Checks Python availability
- Validates system requirements

### Phase 1: Network Setup
- Creates the `apexsigma_net` Docker network
- Ensures proper container communication

### Phase 2: Container Cleanup (if --force)
- Stops and removes existing ApexSigma containers
- Cleans up orphaned resources

### Phase 3: Infrastructure Deployment
- Deploys core infrastructure services:
  - PostgreSQL (port 5432)
  - Redis (port 6379) 
  - RabbitMQ (port 15672)
  - Qdrant (port 6333)

### Phase 4: Observability Stack
- Deploys monitoring and observability:
  - Jaeger (port 16686)
  - Prometheus (port 9090)
  - Loki (port 9100)
  - Grafana (port 8080)

### Phase 5: Application Services
- Deploys ApexSigma microservices:
  - Memos API (port 8091)
  - InGest-LLM API (port 8000)
  - Tools API (port 8003)
  - DevEnviro API (port 8090)
  - Agent listeners and bridges

### Phase 6: Database Migrations
- Runs DevEnviro database schema migrations
- Initializes required database structures

### Phase 7: Health Checks & Audit
- Comprehensive health checks for all services
- HTTP endpoint testing
- Performance baseline capture
- Service dependency validation

### Phase 8: Deployment Report
- Generates comprehensive deployment report
- Lists all service statuses and dashboard links
- Provides troubleshooting information

## Dashboard Access

After successful deployment, access these dashboards:

| Service | URL | Credentials |
|---------|-----|-------------|
| DevEnviro API | http://localhost:8090/docs | N/A |
| Grafana | http://localhost:8080 | admin/apexsigma123 |
| Prometheus | http://localhost:9090 | N/A |
| Jaeger Tracing | http://localhost:16686 | N/A |
| RabbitMQ Management | http://localhost:15672 | See .env file |
| Memos API | http://localhost:8091/docs | N/A |
| InGest-LLM API | http://localhost:8000/docs | N/A |
| Tools API | http://localhost:8003/docs | N/A |

## Automatic Issue Resolution

The SOD deployment includes automatic fixes for common issues:

### Database Connection Fix
- Auto-detects correct PostgreSQL host (container vs localhost)
- Tests multiple connection scenarios
- Updates environment variables dynamically
- Handles both containerized and local development setups

### Service Health Monitoring
- Concurrent health checks for faster deployment
- Automatic retry logic with exponential backoff
- Degraded mode operation for non-critical service failures
- Real-time status updates during deployment

### Container Orchestration
- Dependency-aware service startup ordering
- Staggered deployment to prevent resource conflicts
- Automatic cleanup of failed containers
- Network isolation and security

## Troubleshooting

### Common Issues

#### Database Connection Failed
```
Error: psycopg2.OperationalError: could not translate host name "postgres"
```
**Solution**: The SOD command automatically fixes this. If it persists:
1. Ensure Docker containers are running: `docker ps`
2. Check network connectivity: `docker network ls`
3. Run with `--force` to recreate containers

#### Port Conflicts
```
Error: Port 8090 is already in use
```
**Solution**: 
1. Run `sod --force` to cleanup existing containers
2. Or stop conflicting services manually
3. Check which process is using the port: `netstat -tulpn | grep 8090`

#### Service Unhealthy
```
[FAIL] Service failed health check
```
**Solution**:
1. Check Docker logs: `docker logs apexsigma_[service_name]`
2. Verify .env configuration in respective project directory
3. Run `sod --verbose` for detailed diagnostics

### Manual Service Checks

#### Check All Containers
```bash
docker ps --filter "name=apexsigma_"
```

#### Check Service Logs
```bash
docker logs apexsigma_devenviro_api
docker logs apexsigma_prometheus
docker logs apexsigma_grafana
```

#### Check Network
```bash
docker network inspect apexsigma_net
```

#### Test Database Connection
```bash
docker exec -it apexsigma_postgres psql -U apexsigma_user -d apexsigma-memtank
```

## Advanced Usage

### Development Mode
```bash
# Skip health checks for faster startup during development
python sod.py --skip-audit
```

### Clean Deployment
```bash
# Force cleanup and full redeploy
python sod.py --force --verbose
```

### Production Deployment
```bash
# Full deployment with comprehensive health checks
python sod.py --verbose
```

## Integration with Existing Workflows

The SOD command integrates seamlessly with:

- **Pre-boot System Audit**: Runs comprehensive checks before service startup
- **Enhanced Boot Sequence**: Integrates with existing `systems_boot_sequence.sh`
- **Observability Stack**: Full telemetry and monitoring from day one
- **Multi-Agent Communication**: RabbitMQ message routing for agent coordination

## Environment Variables

Ensure these environment variables are configured in each project's `.env` file:

### DevEnviro.as
```env
POSTGRES_DB=apexsigma-memtank
POSTGRES_USER=apexsigma_user
POSTGRES_PASSWORD=your_secure_postgres_password_here
RABBITMQ_USER=myuser
RABBITMQ_PASSWORD=mypassword
```

### InGest-LLM.as
```env
LANGFUSE_PUBLIC_KEY=your_key
LANGFUSE_SECRET_KEY=your_secret
```

### Memos.as & Tools.as
```env
DATABASE_URL=postgresql://apexsigma_user:password@postgres:5432/apexsigma-memtank
```

## Performance Metrics

After deployment, the SOD command provides:

- **Deployment Time**: Total time from start to completion
- **Service Response Times**: HTTP health check latencies
- **Container Status**: Real-time status of all containers
- **Resource Usage**: Memory and CPU utilization baseline

## Security Considerations

The SOD deployment implements security best practices:

- **Network Isolation**: Services communicate via isolated Docker network
- **Credential Management**: Environment variable-based configuration
- **Health Check Validation**: Ensures services are actually functional, not just running
- **Error Handling**: Graceful degradation prevents total system failure

## Monitoring and Observability

The deployed system includes comprehensive observability:

- **Distributed Tracing**: Jaeger for request tracing across services
- **Metrics Collection**: Prometheus for system and application metrics
- **Log Aggregation**: Loki for centralized logging
- **Dashboards**: Grafana for visual monitoring
- **LLM Observability**: Langfuse for AI/ML operation tracking

For support or to report issues with the SOD deployment, check the logs and system status first, then consult the troubleshooting guide above.