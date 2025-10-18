# ApexSigma Service Architecture & Data Flow Status

**Date:** October 18, 2025  
**Status:** Infrastructure Deployment Phase

## Current Service Status

### ✅ Infrastructure Services (Running & Healthy)

| Service | Container | Port | Status | Purpose |
|---------|-----------|------|--------|---------|
| PostgreSQL | `apexsigma_postgres` | 5432 | ✅ Healthy | Primary relational database |
| Redis | `apexsigma_redis` | 6379 | ✅ Healthy | Cache & session store |
| Qdrant | `apexsigma_qdrant` | 6333-6334 | ✅ Healthy | Vector similarity search |
| Neo4j | `apexsigma_neo4j` | 7474, 7687 | ✅ Healthy | Knowledge graph database |
| RabbitMQ | `apexsigma_rabbitmq` | 5672, 15672 | ✅ Healthy | Message broker |
| Jaeger | `apexsigma_jaeger` | 16686, 14300 | ✅ Healthy | Distributed tracing |
| Prometheus | `apexsigma_prometheus` | 9090 | ✅ Healthy | Metrics collection |
| Grafana | `apexsigma_grafana` | 3000 | ✅ Running | Metrics visualization |
| Loki | `apexsigma_loki` | 3100 | ✅ Healthy | Log aggregation |

### 🟡 Application Services (In Progress)

| Service | Container | Port | Status | Purpose |
|---------|-----------|------|--------|---------|
| InGest-LLM | `apexsigma_ingest_llm_api` | 8005 | ✅ Healthy | Content ingestion & vectorization |
| Tools API | `apexsigma_tools_api` | 9185 | ✅ Healthy | Tool registry service |
| DevEnviro | `apexsigma_devenviro_api` | 8090 | 🟡 Starting | Agent orchestration platform |
| Memos | `apexsigma_memos_api` | 8090 | 🔴 Restarting | Knowledge management system |

**Note:** Memos service is being rebuilt to fix uvicorn installation issue.

### ⏸️ Services Not Yet Deployed

| Service | Purpose | Dependencies |
|---------|---------|--------------|
| Dagster Webserver | Workflow orchestration UI | Dagster daemon, PostgreSQL |
| Dagster Daemon | Background job executor | PostgreSQL, Redis |
| Dagster Code Server | User code deployment | Dagster daemon |

## Data Flow Architecture

### Primary Data Flows

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTENT INGESTION FLOW                       │
└─────────────────────────────────────────────────────────────────┘

External Content
    │
    ▼
┌──────────────────┐
│  InGest-LLM.as   │ (Port 8005)
│  - Parse content │
│  - Extract meta  │
│  - Vectorize     │
└────────┬─────────┘
         │
         ├─────────────────────┬──────────────────────┐
         │                     │                      │
         ▼                     ▼                      ▼
   ┌─────────┐          ┌──────────┐           ┌─────────┐
   │ Qdrant  │          │  Neo4j   │           │  Memos  │
   │ Vectors │          │  Graph   │           │ Storage │
   └─────────┘          └──────────┘           └─────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│                   KNOWLEDGE RETRIEVAL FLOW                      │
└─────────────────────────────────────────────────────────────────┘

Query Request
    │
    ▼
┌──────────────────┐
│    Memos.as      │ (Port 8090)
│  - Query handler │
│  - Context mgmt  │
└────────┬─────────┘
         │
         ├─────────────────────┬──────────────────────┐
         │                     │                      │
         ▼                     ▼                      ▼
   ┌─────────┐          ┌──────────┐           ┌───────────┐
   │ Qdrant  │          │  Neo4j   │           │PostgreSQL │
   │ Semantic │          │Relations │           │Structured │
   │ Search   │          │ Queries  │           │   Data    │
   └─────────┘          └──────────┘           └───────────┘
         │                     │                      │
         └─────────────────────┴──────────────────────┘
                               │
                               ▼
                         Unified Response
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATION FLOW                     │
└─────────────────────────────────────────────────────────────────┘

User Request
    │
    ▼
┌──────────────────┐
│ DevEnviro.as     │ (Port 8090)
│ - Agent router   │
│ - Task queue     │
└────────┬─────────┘
         │
         ├─────────────────────┬──────────────────────┐
         │                     │                      │
         ▼                     ▼                      ▼
   ┌─────────┐          ┌──────────┐           ┌──────────┐
   │RabbitMQ │          │  Memos   │           │  Tools   │
   │Task Dist│          │ Context  │           │ Registry │
   └─────────┘          └──────────┘           └──────────┘
         │
         ▼
   ┌──────────────┐
   │ Agent Workers│
   │ - Claude     │
   │ - Gemini     │
   │ - Qwen       │
   └──────────────┘
```

### Observability & Tracing Flow

```
All Services
    │
    ├──────────────┬──────────────┬──────────────┐
    │              │              │              │
    ▼              ▼              ▼              ▼
┌────────┐   ┌─────────┐   ┌──────────┐   ┌─────────┐
│ Jaeger │   │  Loki   │   │Prometheus│   │Langfuse │
│ Traces │   │  Logs   │   │ Metrics  │   │AI Traces│
└────┬───┘   └────┬────┘   └────┬─────┘   └────┬────┘
     │            │             │              │
     └────────────┴─────────────┴──────────────┘
                      │
                      ▼
                ┌──────────┐
                │ Grafana  │
                │Dashboard │
                └──────────┘
```

## Service Dependencies

### InGest-LLM.as Dependencies
- **Required:** Qdrant (vectors), Neo4j (graphs), Memos (storage)
- **Optional:** LM Studio (local embeddings), Jaeger (tracing)
- **Ports:** 8005 (API)

### Memos.as Dependencies
- **Required:** PostgreSQL (data), Redis (cache), Neo4j (graphs), Qdrant (vectors)
- **Optional:** Jaeger (tracing), Prometheus (metrics)
- **Ports:** 8090 (API)

### DevEnviro.as Dependencies
- **Required:** RabbitMQ (messaging), PostgreSQL (state), Memos (context)
- **Optional:** Tools API (registry), Jaeger (tracing)
- **Ports:** 8090 (API), 8002 (Gemini listener)

### Tools.as Dependencies
- **Required:** PostgreSQL (tool registry)
- **Optional:** Jaeger (tracing)
- **Ports:** 9185 (API)

## Data Storage Strategy

### PostgreSQL
- **Memos DB:** Memory entries, sessions, user data
- **Tools DB:** Tool registry, API definitions
- **DevEnviro DB:** Agent state, task queue
- **Dagster DB:** Workflow runs, schedules

### Redis
- **Session cache:** Active user sessions
- **Query cache:** Frequently accessed queries
- **Rate limiting:** API throttling

### Qdrant
- **Document vectors:** Embedded content
- **Semantic search:** Similarity queries
- **Collections:** Organized by content type

### Neo4j
- **Knowledge graph:** Entity relationships
- **Dependency graphs:** Service dependencies
- **Task graphs:** Workflow dependencies

## Port Allocation

| Port | Service | Protocol | Access |
|------|---------|----------|--------|
| 5432 | PostgreSQL | TCP | Internal |
| 6379 | Redis | TCP | Internal |
| 5672 | RabbitMQ | AMQP | Internal |
| 15672 | RabbitMQ UI | HTTP | External |
| 6333-6334 | Qdrant | HTTP | Internal |
| 7474 | Neo4j HTTP | HTTP | Internal |
| 7687 | Neo4j Bolt | Bolt | Internal |
| 8005 | InGest-LLM | HTTP | External |
| 8090 | Memos/DevEnviro | HTTP | External |
| 9185 | Tools API | HTTP | External |
| 9090 | Prometheus | HTTP | External |
| 3000 | Grafana | HTTP | External |
| 16686 | Jaeger UI | HTTP | External |
| 14300 | Jaeger Collector | HTTP | Internal |

**Note:** Port 8000 is used by Portainer, so InGest-LLM was moved to 8005.

## Next Steps

1. ✅ **Complete Memos rebuild** - Fix uvicorn installation issue
2. 🔄 **Verify all services healthy** - Health checks passing
3. ⏭️ **Deploy Dagster services** - Workflow orchestration
4. ⏭️ **Configure data flows** - Set up inter-service communication
5. ⏭️ **Test end-to-end flows** - Verify complete data pipelines
6. ⏭️ **Document API contracts** - OpenAPI specs for all services
7. ⏭️ **Set up monitoring dashboards** - Grafana dashboards for each service

## Known Issues

- **Memos.as:** Currently restarting due to uvicorn not found (rebuild in progress)
- **Port Conflict:** Port 8000 was allocated to Portainer, InGest-LLM moved to 8005
- **EOD Script:** Updated to use new InGest-LLM port (8005)

## Configuration Updates Made

1. Updated `docker-compose.unified.yml`: InGest-LLM port 8000 → 8005
2. Updated `scripts/eod_command.py`: InGest-LLM endpoint → localhost:8005
3. Enabled EOD logs router in InGest-LLM service
4. Simplified EODLogService to remove KnowledgeGraphService dependency

---

**Last Updated:** October 18, 2025, 16:20
**Author:** GitHub Copilot (Human Augment Tool)
**Status:** Infrastructure deployment in progress
