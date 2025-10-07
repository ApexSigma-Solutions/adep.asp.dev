# ApexSigma Deployment & Operations Architecture

## Executive Summary

This document provides comprehensive guidance on deploying, operating, and maintaining the ApexSigma ecosystem in production environments. It covers infrastructure requirements, deployment strategies, monitoring procedures, security protocols, and operational best practices for maintaining enterprise-grade reliability and performance.

## 🏗️ Deployment Architecture

### Production Deployment Topology

```mermaid
graph TB
    subgraph "External Layer"
        INTERNET[Internet]
        DNS[DNS Resolution]
        CDN[CDN - Optional]
    end

    subgraph "Load Balancing Layer"
        LB1[Primary Load Balancer<br/>Nginx/HAProxy]
        LB2[Secondary Load Balancer<br/>Nginx/HAProxy]
        SSL[SSL Termination]
    end

    subgraph "Application Layer"
        DEVENVIRO1[DevEnviro.as<br/>Instance 1]
        DEVENVIRO2[DevEnviro.as<br/>Instance 2]
        MEMOS1[memOS.as<br/>Instance 1]
        MEMOS2[memOS.as<br/>Instance 2]
        INGEST1[InGest-LLM.as<br/>Instance 1]
        INGEST2[InGest-LLM.as<br/>Instance 2]
        TOOLS1[tools.as<br/>Instance 1]
        TOOLS2[tools.as<br/>Instance 2]
    end

    subgraph "Data Layer - Primary"
        POSTGRES_MASTER[(PostgreSQL<br/>Master)]
        POSTGRES_REPLICA[(PostgreSQL<br/>Replica)]
        REDIS_CLUSTER[(Redis<br/>Cluster)]
        QDRANT_CLUSTER[(Qdrant<br/>Cluster)]
        NEO4J_CLUSTER[(Neo4j<br/>Cluster)]
    end

    subgraph "Data Layer - Analytics"
        CLICKHOUSE[(ClickHouse<br/>Analytics)]
        PROMETHEUS[(Prometheus<br/>Metrics)]
        GRAFANA[(Grafana<br/>Dashboards)]
    end

    subgraph "Message Layer"
        RABBITMQ1[RabbitMQ<br/>Node 1]
        RABBITMQ2[RabbitMQ<br/>Node 2]
        RABBITMQ3[RabbitMQ<br/>Node 3]
    end

    subgraph "Observability Layer"
        JAEGER[Jaeger<br/>Tracing]
        LOKI[Loki<br/>Logging]
        LANGFUSE[Langfuse<br/>AI Traces]
    end

    subgraph "Security Layer"
        VAULT[HashiCorp Vault]
        FAIL2BAN[Fail2Ban]
        FIREWALL[Network Firewall]
    end

    INTERNET --> DNS
    DNS --> CDN
    CDN --> LB1
    CDN --> LB2
    
    LB1 --> SSL
    LB2 --> SSL
    SSL --> DEVENVIRO1
    SSL --> DEVENVIRO2
    SSL --> MEMOS1
    SSL --> MEMOS2
    
    DEVENVIRO1 --> RABBITMQ1
    DEVENVIRO2 --> RABBITMQ2
    MEMOS1 --> POSTGRES_MASTER
    MEMOS2 --> POSTGRES_REPLICA
    
    INGEST1 --> MEMOS1
    INGEST2 --> MEMOS2
    TOOLS1 --> POSTGRES_MASTER
    TOOLS2 --> POSTGRES_REPLICA
    
    DEVENVIRO1 --> JAEGER
    MEMOS1 --> LANGFUSE
    
    PROMETHEUS --> GRAFANA
    JAEGER --> GRAFANA
    LOKI --> GRAFANA
```

## 🐳 Container Deployment Strategy

### Docker Compose Production Configuration

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  # Load Balancer
  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
    depends_on:
      - devenviro-api-1
      - devenviro-api-2
    networks:
      - frontend
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Application Services
  devenviro-api-1:
    build:
      context: ./services/devenviro.as
      dockerfile: Dockerfile.production
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres-primary:5432/apexsigma_db
      - REDIS_URL=redis://redis-cluster:6379/0
      - RABBITMQ_URL=amqp://user:pass@rabbitmq-1:5672/
      - LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}
      - LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}
    volumes:
      - ./logs/devenviro:/app/logs
    networks:
      - backend
      - database
      - message-queue
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  devenviro-api-2:
    build:
      context: ./services/devenviro.as
      dockerfile: Dockerfile.production
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres-replica:5432/apexsigma_db
      - REDIS_URL=redis://redis-cluster:6379/1
      - RABBITMQ_URL=amqp://user:pass@rabbitmq-2:5672/
      - LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}
      - LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}
    volumes:
      - ./logs/devenviro:/app/logs
    networks:
      - backend
      - database
      - message-queue
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # Memory Services
  memos-api-1:
    build:
      context: ./services/memos.as
      dockerfile: Dockerfile.production
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres-primary:5432/apexsigma_db
      - REDIS_URL=redis://redis-cluster:6379/2
      - QDRANT_URL=http://qdrant-1:6333
      - NEO4J_URI=bolt://neo4j-1:7687
    volumes:
      - ./logs/memos:/app/logs
    networks:
      - backend
      - database
      - cache
      - vector-db
      - graph-db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8090/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  memos-api-2:
    build:
      context: ./services/memos.as
      dockerfile: Dockerfile.production
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres-replica:5432/apexsigma_db
      - REDIS_URL=redis://redis-cluster:6379/3
      - QDRANT_URL=http://qdrant-2:6333
      - NEO4J_URI=bolt://neo4j-2:7687
    volumes:
      - ./logs/memos:/app/logs
    networks:
      - backend
      - database
      - cache
      - vector-db
      - graph-db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8090/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # Database Services
  postgres-primary:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: apexsigma_db
      POSTGRES_USER: apexsigma_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_INITDB_WALDIR: /var/lib/postgresql/wal
    volumes:
      - postgres_primary_data:/var/lib/postgresql/data
      - postgres_wal:/var/lib/postgresql/wal
      - ./config/postgres/primary.conf:/etc/postgresql/postgresql.conf
      - ./backups/postgres:/backups
    networks:
      - database
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U apexsigma_user -d apexsigma_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  postgres-replica:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: apexsigma_db
      POSTGRES_USER: apexsigma_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PGUSER: replicator
      POSTGRES_MASTER_SERVICE: postgres-primary
    volumes:
      - postgres_replica_data:/var/lib/postgresql/data
      - ./config/postgres/replica.conf:/etc/postgresql/postgresql.conf
    networks:
      - database
    restart: unless-stopped
    depends_on:
      - postgres-primary
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U apexsigma_user -d apexsigma_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cluster
  redis-cluster:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./config/redis/redis.conf:/etc/redis/redis.conf:ro
      - redis_cluster_data:/data
    networks:
      - cache
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # RabbitMQ Cluster
  rabbitmq-1:
    image: rabbitmq:3.12-management-alpine
    hostname: rabbitmq-1
    environment:
      RABBITMQ_ERLANG_COOKIE: ${RABBITMQ_ERLANG_COOKIE}
      RABBITMQ_DEFAULT_USER: apexsigma_user
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq1_data:/var/lib/rabbitmq
      - ./config/rabbitmq/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf:ro
    networks:
      - message-queue
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  rabbitmq-2:
    image: rabbitmq:3.12-management-alpine
    hostname: rabbitmq-2
    environment:
      RABBITMQ_ERLANG_COOKIE: ${RABBITMQ_ERLANG_COOKIE}
      RABBITMQ_DEFAULT_USER: apexsigma_user
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq2_data:/var/lib/rabbitmq
      - ./config/rabbitmq/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf:ro
    networks:
      - message-queue
    restart: unless-stopped
    depends_on:
      - rabbitmq-1
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Vector Database Cluster
  qdrant-1:
    image: qdrant/qdrant:v1.8.2
    ports:
      - "6333:6333"
    volumes:
      - qdrant1_data:/qdrant/storage
      - ./config/qdrant/config.yaml:/qdrant/config/config.yaml:ro
    networks:
      - vector-db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  qdrant-2:
    image: qdrant/qdrant:v1.8.2
    ports:
      - "6334:6333"
    volumes:
      - qdrant2_data:/qdrant/storage
      - ./config/qdrant/config.yaml:/qdrant/config/config.yaml:ro
    networks:
      - vector-db
    restart: unless-stopped
    depends_on:
      - qdrant-1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Neo4j Cluster
  neo4j-1:
    image: neo4j:5.15-community
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
      - NEO4J_PLUGINS=["graph-data-science"]
      - NEO4J_dbms_memory_heap_initial__size=512m
      - NEO4J_dbms_memory_heap_max__size=2g
    volumes:
      - neo4j1_data:/data
      - neo4j1_logs:/logs
      - ./config/neo4j/neo4j.conf:/var/lib/neo4j/conf/neo4j.conf:ro
    networks:
      - graph-db
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p ${NEO4J_PASSWORD} 'RETURN 1'"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  neo4j-2:
    image: neo4j:5.15-community
    ports:
      - "7475:7474"
      - "7688:7687"
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
      - NEO4J_PLUGINS=["graph-data-science"]
      - NEO4J_dbms_memory_heap_initial__size=512m
      - NEO4J_dbms_memory_heap_max__size=2g
    volumes:
      - neo4j2_data:/data
      - neo4j2_logs:/logs
      - ./config/neo4j/neo4j.conf:/var/lib/neo4j/conf/neo4j.conf:ro
    networks:
      - graph-db
    restart: unless-stopped
    depends_on:
      - neo4j-1
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p ${NEO4J_PASSWORD} 'RETURN 1'"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Observability Stack
  prometheus:
    image: prom/prometheus:v2.50.1
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - monitoring
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3

  grafana:
    image: grafana/grafana:10.4.1
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana/provisioning:/etc/grafana/provisioning:ro
    networks:
      - monitoring
    restart: unless-stopped
    depends_on:
      - prometheus
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  jaeger:
    image: jaegertracing/all-in-one:1.60
    ports:
      - "16686:16686"
      - "14268:14268"
    environment:
      - COLLECTOR_OTLP_ENABLED=true
      - SPAN_STORAGE_TYPE=elasticsearch
    networks:
      - monitoring
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:16686/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  loki:
    image: grafana/loki:3.0.0
    ports:
      - "3100:3100"
    volumes:
      - ./config/loki/loki-config.yml:/etc/loki/local-config.yaml:ro
      - loki_data:/loki
    networks:
      - monitoring
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:3100/ready || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  promtail:
    image: grafana/promtail:3.0.0
    volumes:
      - ./config/promtail/promtail-config.yml:/etc/promtail/config.yml:ro
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    networks:
      - monitoring
    restart: unless-stopped
    depends_on:
      - loki

  # AI Observability
  langfuse:
    image: langfuse/langfuse:2.56.1
    ports:
      - "3001:3000"
    environment:
      DATABASE_URL: postgresql://langfuse_user:${POSTGRES_PASSWORD}@postgres-primary:5432/langfuse_db
      CLICKHOUSE_URL: clickhouse://clickhouse_user:${CLICKHOUSE_PASSWORD}@clickhouse:9000/langfuse_analytics
      NEXTAUTH_URL: http://localhost:3001
      NEXTAUTH_SECRET: ${LANGFUSE_NEXTAUTH_SECRET}
      SALT: ${LANGFUSE_SALT}
      LANGFUSE_PUBLIC_KEY: ${LANGFUSE_PUBLIC_KEY}
      LANGFUSE_SECRET_KEY: ${LANGFUSE_SECRET_KEY}
    volumes:
      - langfuse_data:/app/data
    networks:
      - monitoring
      - database
    restart: unless-stopped
    depends_on:
      - postgres-primary
      - clickhouse
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:3000/api/public/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Analytics Database
  clickhouse:
    image: clickhouse/clickhouse-server:24.3-alpine
    ports:
      - "9123:8123"
      - "9000:9000"
    environment:
      CLICKHOUSE_DB: apexsigma_observability
      CLICKHOUSE_USER: clickhouse_user
      CLICKHOUSE_PASSWORD: ${CLICKHOUSE_PASSWORD}
      CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - clickhouse_logs:/var/log/clickhouse-server
      - ./config/clickhouse/config.xml:/etc/clickhouse-server/config.d/custom.xml:ro
      - ./config/clickhouse/users.xml:/etc/clickhouse-server/users.d/custom.xml:ro
      - ./config/clickhouse/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - monitoring
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "clickhouse-client", "--query", "SELECT 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
  database:
    driver: bridge
    ipam:
      config:
        - subnet: 172.27.0.0/24
  cache:
    driver: bridge
  vector-db:
    driver: bridge
  graph-db:
    driver: bridge
  message-queue:
    driver: bridge
  monitoring:
    driver: bridge

volumes:
  postgres_primary_data:
  postgres_replica_data:
  postgres_wal:
  redis_cluster_data:
  rabbitmq1_data:
  rabbitmq2_data:
  qdrant1_data:
  qdrant2_data:
  neo4j1_data:
  neo4j1_logs:
  neo4j2_data:
  neo4j2_logs:
  prometheus_data:
  grafana_data:
  loki_data:
  langfuse_data:
  clickhouse_data:
  clickhouse_logs:
```

## 🔧 Infrastructure Requirements

### Hardware Requirements

#### Minimum Production Requirements
```yaml
production_requirements:
  compute:
    cpu: "8 cores minimum (16 cores recommended)"
    memory: "32GB RAM minimum (64GB recommended)"
    storage: "500GB SSD minimum (1TB recommended)"
    network: "1Gbps network connection"
  
  services_distribution:
    application_servers: "2+ instances for HA"
    database_servers: "2+ instances (primary + replica)"
    cache_servers: "3+ instances for Redis cluster"
    message_queue: "3+ instances for RabbitMQ cluster"
    monitoring: "2+ instances for observability"
```

#### Development/Testing Requirements
```yaml
development_requirements:
  compute:
    cpu: "4 cores"
    memory: "16GB RAM"
    storage: "100GB SSD"
    network: "Standard network connection"
  
  services:
    single_instance: "All services on one machine"
    docker_compose: "Suitable for local development"
```

### Network Requirements

#### Port Configuration
```yaml
port_requirements:
  external_ports:
    - "80: HTTP traffic"
    - "443: HTTPS traffic"
    - "3000: Grafana dashboards"
    - "3001: Langfuse interface"
    - "9090: Prometheus metrics"
  
  internal_ports:
    application:
      - "8000: DevEnviro API"
      - "8090: memOS API"
      - "8000: InGest-LLM API"
      - "9185: tools API"
    
    databases:
      - "5432: PostgreSQL"
      - "6379: Redis"
      - "6333: Qdrant"
      - "7687: Neo4j"
      - "9000: ClickHouse"
    
    monitoring:
      - "9090: Prometheus"
      - "3000: Grafana"
      - "16686: Jaeger"
      - "3100: Loki"
```

## 🔒 Security Deployment Configuration

### SSL/TLS Configuration

```nginx
# nginx/ssl.conf
server {
    listen 443 ssl http2;
    server_name api.apexsigma.com;
    
    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/apexsigma.crt;
    ssl_certificate_key /etc/nginx/ssl/apexsigma.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    # Proxy Configuration
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

### Security Hardening

```bash
#!/bin/bash
# security-hardening.sh

# System Updates
echo "Applying system security updates..."
apt-get update && apt-get upgrade -y

# Firewall Configuration
echo "Configuring firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw --force enable

# Fail2Ban Configuration
echo "Configuring Fail2Ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3

[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log
maxretry = 6
EOF

systemctl enable fail2ban
systemctl start fail2ban

# Docker Security
echo "Configuring Docker security..."
# Run Docker daemon with security options
cat > /etc/docker/daemon.json << EOF
{
  "live-restore": true,
  "userland-proxy": false,
  "no-new-privileges": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

systemctl restart docker

# File Permissions
echo "Setting secure file permissions..."
chmod 600 /etc/nginx/ssl/*.key
chmod 644 /etc/nginx/ssl/*.crt
chmod 600 .env
chmod 700 scripts/
```

## 📊 Monitoring & Alerting Setup

### Prometheus Configuration

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'apexsigma-services'
    static_configs:
      - targets: ['devenviro-api-1:8000', 'devenviro-api-2:8000']
        labels:
          service: 'devenviro'
          environment: 'production'
      - targets: ['memos-api-1:8090', 'memos-api-2:8090']
        labels:
          service: 'memos'
          environment: 'production'
    scrape_interval: 30s
    metrics_path: /metrics
    
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-primary:5432', 'postgres-replica:5432']
    scrape_interval: 30s
    
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-cluster:6379']
    scrape_interval: 30s
    
  - job_name: 'rabbitmq'
    static_configs:
      - targets: ['rabbitmq-1:15672', 'rabbitmq-2:15672']
    scrape_interval: 30s
```

### Alert Rules

```yaml
# prometheus/rules/apexsigma-alerts.yml
groups:
  - name: apex-sigma-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is above 90%"

      - alert: DatabaseConnectionFailure
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database connection failure"
          description: "PostgreSQL database is unreachable"

      - alert: RabbitMQQueueDepth
        expr: rabbitmq_queue_messages > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "RabbitMQ queue depth high"
          description: "Queue {{ $labels.queue }} has {{ $value }} messages"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "Service {{ $labels.instance }} is unreachable"
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "ApexSigma Production Monitoring",
    "panels": [
      {
        "title": "Service Health Overview",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"apexsigma-services\"}",
            "legendFormat": "{{ service }} - {{ instance }}"
          }
        ]
      },
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{ service }} - {{ method }}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "{{ service }} - {{ status }}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile - {{ service }}"
          }
        ]
      }
    ]
  }
}
```

## 🔄 Backup & Disaster Recovery

### Database Backup Strategy

```bash
#!/bin/bash
# backup-databases.sh

set -e

# Configuration
BACKUP_DIR="/backups/postgres"
S3_BUCKET="apexsigma-backups"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# PostgreSQL Primary Backup
echo "Backing up PostgreSQL primary database..."
docker exec postgres-primary pg_dump -U apexsigma_user -d apexsigma_db \
  --format=custom \
  --verbose \
  --file=/tmp/backup_primary_$DATE.dump

docker cp postgres-primary:/tmp/backup_primary_$DATE.dump $BACKUP_DIR/

# PostgreSQL Replica Backup (for verification)
echo "Backing up PostgreSQL replica database..."
docker exec postgres-replica pg_dump -U apexsigma_user -d apexsigma_db \
  --format=custom \
  --verbose \
  --file=/tmp/backup_replica_$DATE.dump

docker cp postgres-replica:/tmp/backup_replica_$DATE.dump $BACKUP_DIR/

# Redis Backup
echo "Backing up Redis data..."
docker exec redis-cluster redis-cli BGSAVE
sleep 10  # Wait for background save to complete
docker cp redis-cluster:/data/dump.rdb $BACKUP_DIR/redis_backup_$DATE.rdb

# Neo4j Backup
echo "Backing up Neo4j database..."
docker exec neo4j-1 neo4j-admin database dump --to-path=/tmp neo4j
docker cp neo4j-1:/tmp/neo4j.dump $BACKUP_DIR/neo4j_backup_$DATE.dump

# Compress backups
echo "Compressing backups..."
cd $BACKUP_DIR
tar -czf apex-sigma-backup-$DATE.tar.gz *.dump *.rdb

# Upload to S3 (if configured)
if [ ! -z "$S3_BUCKET" ]; then
    echo "Uploading to S3..."
    aws s3 cp apex-sigma-backup-$DATE.tar.gz s3://$S3_BUCKET/postgres/apex-sigma-backup-$DATE.tar.gz
fi

# Clean up old backups
echo "Cleaning up old backups..."
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.dump" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.rdb" -mtime +$RETENTION_DAYS -delete

echo "Backup completed successfully!"
```

### Disaster Recovery Procedures

#### Database Recovery
```bash
#!/bin/bash
# restore-database.sh

set -e

# Configuration
BACKUP_FILE="$1"
RESTORE_DIR="/tmp/restore"
DATE=$(date +%Y%m%d_%H%M%S)

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Create restore directory
mkdir -p $RESTORE_DIR

# Extract backup
echo "Extracting backup..."
tar -xzf $BACKUP_FILE -C $RESTORE_DIR

# Stop application services
echo "Stopping application services..."
docker-compose -f docker-compose.production.yml stop devenviro-api-1 devenviro-api-2 memos-api-1 memos-api-2

# Restore PostgreSQL
echo "Restoring PostgreSQL database..."
docker exec -i postgres-primary pg_restore -U apexsigma_user -d apexsigma_db -v < $RESTORE_DIR/backup_primary_*.dump

# Restore Redis
echo "Restoring Redis data..."
docker cp $RESTORE_DIR/redis_backup_*.rdb redis-cluster:/data/dump.rdb
docker restart redis-cluster

# Restore Neo4j
echo "Restoring Neo4j database..."
docker exec -i neo4j-1 neo4j-admin database load --from-path=/tmp --overwrite-destination=true neo4j < $RESTORE_DIR/neo4j_backup_*.dump

# Restart application services
echo "Restarting application services..."
docker-compose -f docker-compose.production.yml start

# Verify restoration
echo "Verifying restoration..."
sleep 30  # Wait for services to start
curl -f http://localhost:8000/health || exit 1
curl -f http://localhost:8090/health || exit 1

echo "Database restoration completed successfully!"
```

## 🔧 Operational Procedures

### Service Startup Sequence

```bash
#!/bin/bash
# startup-sequence.sh

echo "Starting ApexSigma ecosystem..."

# 1. Start infrastructure services
echo "Starting infrastructure services..."
docker-compose -f docker-compose.production.yml up -d postgres-primary postgres-replica
sleep 30  # Wait for database initialization

docker-compose -f docker-compose.production.yml up -d redis-cluster
sleep 10

docker-compose -f docker-compose.production.yml up -d rabbitmq-1 rabbitmq-2
sleep 20

# 2. Start data layer services
echo "Starting data layer services..."
docker-compose -f docker-compose.production.yml up -d qdrant-1 qdrant-2
sleep 15

docker-compose -f docker-compose.production.yml up -d neo4j-1 neo4j-2
sleep 30

# 3. Start observability services
echo "Starting observability services..."
docker-compose -f docker-compose.production.yml up -d prometheus grafana jaeger loki clickhouse
sleep 20

# 4. Start application services
echo "Starting application services..."
docker-compose -f docker-compose.production.yml up -d memos-api-1 memos-api-2
sleep 30

docker-compose -f docker-compose.production.yml up -d devenviro-api-1 devenviro-api-2
sleep 20

docker-compose -f docker-compose.production.yml up -d ingest-llm-api-1 ingest-llm-api-2
sleep 15

docker-compose -f docker-compose.production.yml up -d tools-api-1 tools-api-2
sleep 15

# 5. Start load balancer
echo "Starting load balancer..."
docker-compose -f docker-compose.production.yml up -d nginx-lb

# 6. Health check
echo "Performing health checks..."
sleep 60  # Wait for all services to start

# Check all services
services=(
  "devenviro-api-1:8000"
  "devenviro-api-2:8000"
  "memos-api-1:8090"
  "memos-api-2:8090"
  "prometheus:9090"
  "grafana:3000"
  "jaeger:16686"
)

for service in "${services[@]}"; do
    IFS=':' read -r container port <<< "$service"
    echo "Checking $container on port $port..."
    curl -f "http://localhost:$port/health" || echo "WARNING: $container health check failed"
done

echo "ApexSigma ecosystem startup completed!"
```

### Service Shutdown Sequence

```bash
#!/bin/bash
# shutdown-sequence.sh

echo "Shutting down ApexSigma ecosystem..."

# 1. Stop load balancer first
echo "Stopping load balancer..."
docker-compose -f docker-compose.production.yml stop nginx-lb

# 2. Stop application services
echo "Stopping application services..."
docker-compose -f docker-compose.production.yml stop tools-api-1 tools-api-2
docker-compose -f docker-compose.production.yml stop ingest-llm-api-1 ingest-llm-api-2
docker-compose -f docker-compose.production.yml stop devenviro-api-1 devenviro-api-2
docker-compose -f docker-compose.production.yml stop memos-api-1 memos-api-2

# 3. Stop observability services
echo "Stopping observability services..."
docker-compose -f docker-compose.production.yml stop promtail
docker-compose -f docker-compose.production.yml stop prometheus grafana jaeger loki clickhouse

# 4. Stop data layer services
echo "Stopping data layer services..."
docker-compose -f docker-compose.production.yml stop neo4j-1 neo4j-2
docker-compose -f docker-compose.production.yml stop qdrant-1 qdrant-2
docker-compose -f docker-compose.production.yml stop rabbitmq-1 rabbitmq-2
docker-compose -f docker-compose.production.yml stop redis-cluster

# 5. Stop database services
echo "Stopping database services..."
docker-compose -f docker-compose.production.yml stop postgres-replica
docker-compose -f docker-compose.production.yml stop postgres-primary

echo "ApexSigma ecosystem shutdown completed!"
```

### Maintenance Mode

```bash
#!/bin/bash
# maintenance-mode.sh

MODE="$1"

case $MODE in
    "enable")
        echo "Enabling maintenance mode..."
        # Update nginx configuration to serve maintenance page
        cat > nginx/maintenance.conf << 'EOF'
server {
    listen 80;
    server_name _;
    return 503;
    
    location / {
        root /var/www/maintenance;
        try_files $uri $uri/ /index.html;
    }
    
    error_page 503 @maintenance;
    location @maintenance {
        root /var/www/maintenance;
        rewrite ^(.*)$ /index.html break;
    }
}
EOF
        
        # Reload nginx configuration
        docker-compose -f docker-compose.production.yml exec nginx-lb nginx -s reload
        echo "Maintenance mode enabled"
        ;;
        
    "disable")
        echo "Disabling maintenance mode..."
        # Remove maintenance configuration
        rm -f nginx/maintenance.conf
        
        # Reload nginx configuration
        docker-compose -f docker-compose.production.yml exec nginx-lb nginx -s reload
        echo "Maintenance mode disabled"
        ;;
        
    *)
        echo "Usage: $0 {enable|disable}"
        exit 1
        ;;
esac
```

## 📋 Operational Checklists

### Daily Operations Checklist

- [ ] Review overnight system alerts
- [ ] Check service health status
- [ ] Monitor resource utilization (CPU, memory, disk)
- [ ] Review backup completion status
- [ ] Check log aggregation for errors
- [ ] Verify SSL certificate expiration dates
- [ ] Review security logs for anomalies

### Weekly Operations Checklist

- [ ] Performance trend analysis
- [ ] Capacity planning review
- [ ] Security patch assessment
- [ ] Backup restoration test
- [ ] Disaster recovery procedure review
- [ ] Cost optimization review
- [ ] Documentation updates

### Monthly Operations Checklist

- [ ] Complete security audit
- [ ] Performance benchmarking
- [ ] Disaster recovery drill
- [ ] Backup strategy review
- [ ] Infrastructure scaling assessment
- [ ] Vendor relationship review
- [ ] Compliance audit

This comprehensive operational guide provides the foundation for maintaining a production-ready ApexSigma deployment with enterprise-grade reliability, security, and performance characteristics.