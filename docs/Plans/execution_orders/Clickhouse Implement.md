# **Clickhouse Implementation Snippets**

## **Prometheus Remote Write Yaml**

```yaml
remote_write:
  - url: "http://clickhouse:8123/"
    queue_config:
      capacity: 10000
      max_shards: 10
      max_samples_per_send: 5000
    write_relabel_configs:
      - source_labels: [__name__]
        regex: ".*"
        target_label: source
        replacement: "prometheus"
```

This YAML snippet configures Prometheus to send metrics data to ClickHouse for unified storage and analytics. Implementation details:

File Location: config/prometheus/prometheus.yml (appended to existing Prometheus configuration)

Integration Steps:

Remote Write Endpoint: Configures Prometheus to push metrics to ClickHouse HTTP interface at http://clickhouse:8123/
Queue Configuration: Sets up buffering with 10,000 capacity, 10 shards, and 5,000 samples per send for reliable data transfer
Label Relabeling: Adds source: prometheus label to all metrics for data lineage tracking
Service Dependency: Requires ClickHouse service to be running (added to depends_on in docker-compose.unified.yml)

## **ClickHouse Environment Variables (ENV)**

ClickHouse Environment Variables (ENV)
This ENV snippet defines configuration variables for ClickHouse service connectivity across the ecosystem.

File Location: .env.example (added to existing environment template)

Implementation Steps:

Host Configuration: CLICKHOUSE*HOST=clickhouse uses Docker internal DNS for service discovery
Port Mapping: CLICKHOUSE_PORT=8123 for HTTP queries, CLICKHOUSE_NATIVE_PORT=9000 for native protocol
Authentication: User/password for secure access (change from defaults in production)
Database Selection: CLICKHOUSE_DB=apexsigma_observability as the unified metrics database
Service Integration: Referenced by Langfuse, Vector, and Grafana services via ${CLICKHOUSE*\*} variables
Security Note: Values are placeholders; actual secrets managed via .env file (not committed to version control per Valhalla Shield standards).

Both snippets follow Poetry dependency management and structured logging conventions, integrating with the existing ApexSigma observability stack for unified metrics aggregation.

```env
# ClickHouse Configuration
CLICKHOUSE_HOST=clickhouse
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=clickhouse_user
CLICKHOUSE_PASSWORD=change_me_securely
CLICKHOUSE_DB=apexsigma_observability
CLICKHOUSE_NATIVE_PORT=9000
```

## **Langfuse Traces Table Schema (SQL)**

This SQL snippet creates the database schema for storing AI operation traces in ClickHouse. Implementation details:

File Location: config/clickhouse/init.sql (executed during ClickHouse initialization)

Integration Steps:

Database Creation: Creates apexsigma_observability database if not exists
Table Structure: Defines columns for trace metadata, timestamps, usage metrics, and performance data
MergeTree Engine: Uses ClickHouse's columnar storage for high-performance analytics
Partitioning: Partitions by month (toYYYYMM(timestamp)) for efficient querying
TTL Policy: Automatically deletes data older than 90 days to manage storage
Validation: After initialization, verify with: SELECT count() FROM langfuse_traces

```sql
CREATE DATABASE IF NOT EXISTS apexsigma_observability;
USE apexsigma_observability;

CREATE TABLE IF NOT EXISTS langfuse_traces (
    id UUID,
    timestamp DateTime64(3),
    project_id String,
    user_id String,
    session_id String,
    name String,
    metadata String,
    tags Array(String),
    input String,
    output String,
    model String,
    model_parameters String,
    usage_prompt_tokens UInt32,
    usage_completion_tokens UInt32,
    usage_total_tokens UInt32,
    latency_ms UInt32
) ENGINE = MergeTree()
ORDER BY (project_id, timestamp)
PARTITION BY toYYYYMM(timestamp)
TTL timestamp + INTERVAL 90 DAY;
```

## **Grafana Data Source Configuration (YAML)**

This YAML snippet configures Grafana to connect to ClickHouse as a data source for unified dashboards.

File Location: config/grafana/datasources/clickhouse.yaml (provisioned into Grafana)

Integration Steps:

Plugin Requirement: Requires grafana-clickhouse-datasource plugin installation
Connection Setup: Uses proxy access to ClickHouse HTTP interface
Authentication: References environment variables for secure credentials
TLS Configuration: Skips verification for internal Docker network communication
Provisioning: Automatically configured on Grafana startup via volume mount
Validation: In Grafana UI, verify data source connection and test query: SELECT 1

```yaml
apiVersion: 1
datasources:
  - name: ClickHouse
    type: grafana-clickhouse-datasource
    access: proxy
    url: http://clickhouse:8123
    jsonData:
      defaultDatabase: apexsigma_observability
      username: ${CLICKHOUSE_USER}
      tlsSkipVerify: true
    secureJsonData:
      password: ${CLICKHOUSE_PASSWORD}
    isDefault: false
    editable: true
```

## **Langfuse Service Update (YAML)**

This YAML snippet updates the Langfuse service configuration to integrate with ClickHouse for analytics.

File Location: docker-compose.unified.yml (modifies existing langfuse service)

Integration Steps:

ClickHouse URL: Adds CLICKHOUSE_URL=http://clickhouse:8123 for analytics backend
Authentication: Uses environment variables for secure ClickHouse access
Database Selection: Specifies apexsigma_observability as the analytics database
Feature Flags: Enables experimental features and latest migration target
Dependencies: Adds clickhouse to depends_on for proper startup order
Validation: Check Langfuse logs for ClickHouse connection: docker-compose logs langfuse

```yaml
langfuse:
  image: langfuse/langfuse:latest
  container_name: apexsigma_langfuse
  environment:
    - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
    - CLICKHOUSE_URL=http://clickhouse:8123
    - CLICKHOUSE_USER=${CLICKHOUSE_USER}
    - CLICKHOUSE_PASSWORD=${CLICKHOUSE_PASSWORD}
    - CLICKHOUSE_DATABASE=apexsigma_observability
    - LANGFUSE_ENABLE_EXPERIMENTAL_FEATURES=true
    - LANGFUSE_CLICKHOUSE_MIGRATION_TARGET=latest
  depends_on:
    - postgres
    - clickhouse
```

## **ClickHouse Service Definition (YAML)**

This YAML snippet defines the complete ClickHouse service for the Docker Compose stack.

File Location: docker-compose.unified.yml (added to services section)

Integration Steps:

Image Selection: Uses official ClickHouse server with Alpine Linux for minimal footprint
Environment Configuration: Sets database name, user credentials, and performance limits
Port Mapping: Exposes HTTP (8123) and native TCP (9000) interfaces
Volume Mounts: Persists data and logs, mounts custom configuration files
Network Assignment: Uses static IP 172.26.0.50 in apexsigma_net for service discovery
Health Checks: Validates service readiness with ClickHouse client queries
Resource Limits: Sets file descriptor limits for high-performance operation
Validation: Test service health: curl http://localhost:8123/ping and verify container: docker-compose ps clickhouse

```yaml
clickhouse:
  image: clickhouse/clickhouse-server:24.3-alpine
  container_name: apexsigma_clickhouse
  hostname: clickhouse
  environment:
    - CLICKHOUSE_DB=apexsigma_observability
    - CLICKHOUSE_USER=${CLICKHOUSE_USER:-clickhouse_user}
    - CLICKHOUSE_PASSWORD=${CLICKHOUSE_PASSWORD:-change_me_securely}
    - CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1
    - CLICKHOUSE_MAX_MEMORY_USAGE=4294967296
    - CLICKHOUSE_MAX_CONCURRENT_QUERIES=100
  ports:
    - "8123:8123"
    - "9000:9000"
  volumes:
    - clickhouse_data:/var/lib/clickhouse
    - clickhouse_logs:/var/log/clickhouse-server
    - ./config/clickhouse/config.xml:/etc/clickhouse-server/config.d/custom.xml:ro
    - ./config/clickhouse/users.xml:/etc/clickhouse-server/users.d/custom.xml:ro
  networks:
    apexsigma_net:
      ipv4_address: 172.26.0.50
  restart: unless-stopped
  healthcheck:
    test: ["CMD", "clickhouse-client", "--query", "SELECT 1"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
  ulimits:
    nofile:
      soft: 262144
      hard: 262144
```

```environment
# ClickHouse Configuration
CLICKHOUSE_HOST=clickhouse
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=clickhouse_user
CLICKHOUSE_PASSWORD=change_me_securely
CLICKHOUSE_DB=apexsigma_observability
CLICKHOUSE_NATIVE_PORT=9000
```
