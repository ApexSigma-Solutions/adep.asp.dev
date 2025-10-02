---
title: DockerComposeUnified
date created: Sunday, September 21st 2025, 3:14:23 pm
date modified: Sunday, September 21st 2025, 3:15:52 pm
---

# DockerComposeUnified

```dockerfile
# ApexSigma Unified Container Ecosystem
# Single Source of Truth for All Services - STANDARDIZED NAMING
# Version: 3.0 - Eliminates Naming Chaos & Network Confusion
version: '3.8'

# UNIFIED NETWORK CONFIGURATION - SINGLE SOURCE OF TRUTH
networks:
  apexsigma_network:
    name: apexsigma_unified_network
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1

# SHARED VOLUMES
volumes:
  postgres_main_data:
  postgres_tools_data:
  redis_data:
  neo4j_data:
  qdrant_data:
  grafana_data:
  prometheus_data:
  loki_data:

# SERVICES DEFINITIONS
services:
  # =============================================================================
  # API SERVICES
  # =============================================================================

  ingest_llm_api:
    container_name: unified_ingest_llm_api
    build: ./InGest-LLM.as
    networks:
      unified_net:
        ipv4_address: 172.25.0.10
    ports:
      - "8000:8000"
    environment:
      - MEMOS_BASE_URL=http://unified_memos_api:8090
      - POSTGRES_HOST=unified_postgres
      - REDIS_HOST=unified_redis
      - NEO4J_HOST=unified_neo4j
      - QDRANT_HOST=unified_qdrant
      - PROMETHEUS_URL=http://unified_prometheus:9090
      - JAEGER_ENDPOINT=http://unified_jaeger:14268
    depends_on:
      - memos_api
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  memos_api:
    container_name: unified_memos_api
    build: ./memos.as
    networks:
      unified_net:
        ipv4_address: 172.25.0.12
    ports:
      - "8090:8090"
    environment:
      - POSTGRES_HOST=unified_postgres
      - REDIS_HOST=unified_redis
      - NEO4J_HOST=unified_neo4j
      - QDRANT_HOST=unified_qdrant
    depends_on:
      - postgres
      - redis
      - neo4j
      - qdrant
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8090/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  tools_api:
    container_name: apexsigma_tools_api
    build: ./tools.as
    networks:
      services_net:
        ipv4_address: 172.22.0.6
    ports:
      - "8003:8000"
    environment:
      - POSTGRES_HOST=apexsigma_tools_postgres
      - POSTGRES_PORT=5432
    depends_on:
      - tools_postgres
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  agent_bridge:
    container_name: apexsigma_devenviro_a2a_bridge
    build: ./devenviro.as/bridge
    networks:
      services_net:
        ipv4_address: 172.22.0.4
    ports:
      - "8100:8100"
    environment:
      - RABBITMQ_HOST=apexsigma_rabbitmq
      - TOOLS_API_URL=http://apexsigma_tools_api:8000
      - MEMOS_API_URL=http://unified_memos_api:8090
    depends_on:
      - rabbitmq
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8100/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =============================================================================
  # DATABASE SERVICES
  # =============================================================================

  postgres:
    container_name: unified_postgres
    image: postgres:14-alpine
    networks:
      unified_net:
        ipv4_address: 172.25.0.7
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=apexsigma
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  neo4j:
    container_name: unified_neo4j
    image: neo4j:5.15-community
    networks:
      unified_net:
        ipv4_address: 172.25.0.5
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/password
      - NEO4J_PLUGINS=["apoc"]
    volumes:
      - neo4j_data:/data
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "password", "RETURN 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    container_name: unified_redis
    image: redis:7-alpine
    networks:
      unified_net:
        ipv4_address: 172.25.0.3
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  qdrant:
    container_name: unified_qdrant
    image: qdrant/qdrant:v1.8.2
    networks:
      unified_net:
        ipv4_address: 172.25.0.4
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  tools_postgres:
    container_name: apexsigma_tools_postgres
    image: postgres:16-alpine
    networks:
      services_net:
        ipv4_address: 172.22.0.14
    ports:
      - "5433:5432"
    environment:
      - POSTGRES_DB=tools
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - tools_postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =============================================================================
  # OBSERVABILITY STACK
  # =============================================================================

  prometheus:
    container_name: unified_prometheus
    image: prom/prometheus:v2.50.1
    networks:
      unified_net:
        ipv4_address: 172.25.0.8
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3

  grafana:
    container_name: unified_grafana
    image: grafana/grafana:10.4.1
    networks:
      unified_net:
        ipv4_address: 172.25.0.11
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana/provisioning:/etc/grafana/provisioning
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  jaeger:
    container_name: unified_jaeger
    image: jaegertracing/all-in-one:1.60
    networks:
      unified_net:
        ipv4_address: 172.25.0.2
    ports:
      - "16686:16686"
      - "14268:14268"
      - "6831:6831/udp"
      - "6832:6832/udp"
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:16686/"]
      interval: 30s
      timeout: 10s
      retries: 3

  loki:
    container_name: unified_loki
    image: grafana/loki:2.9.0
    networks:
      unified_net:
        ipv4_address: 172.25.0.6
    ports:
      - "3100:3100"
    volumes:
      - ./config/loki-config.yml:/etc/loki/local-config.yaml
      - loki_data:/loki
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    container_name: unified_promtail
    image: grafana/promtail:2.9.0
    networks:
      unified_net:
        ipv4_address: 172.25.0.9
    volumes:
      - ./config/promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml

  # =============================================================================
  # MESSAGE QUEUE & AGENTS
  # =============================================================================

  rabbitmq:
    container_name: apexsigma_rabbitmq
    image: rabbitmq:3.12-management-alpine
    networks:
      services_net:
        ipv4_address: 172.22.0.5
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=admin
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  gemini_listener:
    container_name: apexsigma_devenviro_gemini_cli_listener
    build: ./devenviro.as/agents/gemini
    networks:
      services_net:
        ipv4_address: 172.22.0.12
    environment:
      - RABBITMQ_HOST=apexsigma_rabbitmq
      - AGENT_BRIDGE_URL=http://apexsigma_devenviro_a2a_bridge:8100
    depends_on:
      - rabbitmq
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8090/health"]
      interval: 30s
      timeout: 10s
      retries: 3

# VOLUMES
volumes:
  postgres_data:
    name: unified_postgres_data
  neo4j_data:
    name: unified_neo4j_data
  redis_data:
    name: unified_redis_data
  qdrant_data:
    name: unified_qdrant_data
  tools_postgres_data:
    name: apexsigma_tools_postgres_data
  prometheus_data:
    name: unified_prometheus_data
  grafana_data:
    name: unified_grafana_data
  loki_data:
    name: unified_loki_data
  rabbitmq_data:
    name: apexsigma_rabbitmq_data
```
