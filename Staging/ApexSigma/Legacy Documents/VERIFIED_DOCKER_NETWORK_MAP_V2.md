# VERIFIED DOCKER NETWORK MAP V2

## Overview
This document provides a verified map of the Docker network configuration for the ApexSigmaProjects.Dev monorepo infrastructure. It includes all service names, images, ports, and volumes as of September 25, 2025.

## Service Inventory

### Infrastructure Services

| Service Name | Container Name | Image | Ports | Volumes | Status |
|--------------|----------------|-------|-------|---------|--------|
| postgres | apexsigma_postgres | postgres:14-alpine | 5432:5432 | postgres_data:/var/lib/postgresql/data | Up (Healthy) |
| redis | apexsigma_redis | redis:7-alpine | 6379:6379 | redis_data:/data | Up (Healthy) |
| rabbitmq | apexsigma_rabbitmq | rabbitmq:3.12-management-alpine | 5672:5672, 15672:15672 | rabbitmq_data:/var/lib/rabbitmq | Up (Healthy) |
| qdrant | apexsigma_qdrant | qdrant/qdrant:v1.8.2 | 6333:6333, 6334:6334 | qdrant_data:/qdrant/storage | Up |
| neo4j | apexsigma_neo4j | neo4j:5.15-community | 7473-7474/tcp, 7687/tcp | neo4j_data:/data, neo4j_logs:/logs | Up (Healthy) |

### Observability Stack

| Service Name | Container Name | Image | Ports | Volumes | Status |
|--------------|----------------|-------|-------|---------|--------|
| jaeger | apexsigma_jaeger | jaegertracing/all-in-one:1.60 | 16686:16686, 14268:14268 | None | Up |
| prometheus | apexsigma_prometheus | prom/prometheus:v2.50.1 | 9090:9090 | ./services/devenviro.as/config/prometheus.yml:/etc/prometheus/prometheus.yml, prometheus_data:/prometheus | Not Running (Port Conflict) |
| grafana | apexsigma_grafana | grafana/grafana:10.4.1 | 8080:3000 | grafana_data:/var/lib/grafana, ./services/devenviro.as/config/grafana.ini:/etc/grafana/grafana.ini, ./services/devenviro.as/config/grafana/provisioning:/etc/grafana/provisioning | Not Running (Dependency) |
| loki | apexsigma_loki | grafana/loki:3.0.0 | 9100:3100 | ./services/devenviro.as/config/loki-config.yml:/etc/loki/local-config.yaml, loki_data:/loki | Not Running (Port Conflict) |
| promtail | apexsigma_promtail | grafana/promtail:3.0.0 | None | ./services/devenviro.as/config/promtail-config.yml:/etc/promtail/config.yml, /var/log:/var/log:ro, /var/lib/docker/containers:/var/lib/docker/containers:ro | Not Running (Dependency) |

### Core Services

| Service Name | Container Name | Image | Ports | Volumes | Status |
|--------------|----------------|-------|-------|---------|--------|
| devenviro-api | apexsigma_devenviro_api | ./services/devenviro.as/Dockerfile | 8090:8090 | ./services/devenviro.as:/app | Not Running |
| devenviro-gemini-cli-listener | apexsigma_devenviro_gemini_cli_listener | ./services/devenviro.as/Dockerfile | None | ./services/devenviro.as:/app | Not Running |
| devenviro-docs | apexsigma_devenviro_docs | python:3.11-slim | 8001:8000 | ./services/devenviro.as:/app | Not Running (Profile) |
| devenviro-a2a-bridge | apexsigma_devenviro_a2a_bridge | ./services/devenviro.as/Dockerfile | 8101:8100 | ./services/devenviro.as:/app | Not Running |
| memos-api | apexsigma_memos_api | ./services/memos.as/Dockerfile | None | ./services/memos.as:/code, ./libs/apexsigma-core:/code/libs/apexsigma-core | Up (Healthy) |
| ingest-llm-api | apexsigma_ingest_llm_api | ./services/InGest-LLM.as/Dockerfile | 18000:8000 | ./services/InGest-LLM.as:/app | Not Running |
| tools-postgres | apexsigma_tools_postgres | postgres:16-alpine | 5433:5432 | tools_postgres_data:/var/lib/postgresql/data, ./services/tools.as/scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql | Not Running |
| tools-api | apexsigma_tools_api | ./services/tools.as/Dockerfile | 8003:8000 | ./services/tools.as:/app | Not Running |

### Dagster Services

| Service Name | Container Name | Image | Ports | Volumes | Status |
|--------------|----------------|-------|-------|---------|--------|
| dagster-webserver | apexsigma_dagster_webserver | ./services/dagster/Dockerfile | 8081:8080 | .:/app/dagster_home | Up |
| dagster-daemon | apexsigma_dagster_daemon | ./services/dagster/Dockerfile | None | .:/app/dagster_home | Restarting |

## Network Configuration

All services are connected through the `apexsigma_net` network which is defined as external in the docker-compose configuration.

## Port Conflict Analysis

A port conflict has been identified on port 9100 which prevents the loki service from starting. This is due to Windows reserved port ranges. The conflict affects the following services:
- loki (configured to use 9100:3100)
- prometheus (configured to use 9090:9090, but affected by the broader port range conflict)

## Verification Notes

1. Core infrastructure services (postgres, redis, rabbitmq, qdrant, neo4j) are all running and healthy.
2. memos-api is running and healthy, which is critical for the core functionality.
3. dagster-webserver is running, but dagster-daemon is in a restart loop.
4. Observability stack services (loki, prometheus, grafana, promtail) are not running due to the port conflict.
5. Most core services are not running, which may be by design or due to dependency issues.

## Triple-Signature Verification

- Implementer: iFlow CLI
- Reviewer: Qwen3-Coder
- SigmaDev11: Pending

---
*Document verified on September 25, 2025*