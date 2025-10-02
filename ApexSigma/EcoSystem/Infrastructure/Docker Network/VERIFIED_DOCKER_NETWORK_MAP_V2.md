# 🌐 **ApexSigma Docker Network Topology - VERIFIED INFRASTRUCTURE MAP V2**
> **MAR Notice (2025-09-25)**: This is the updated, verified Docker network map reflecting the current operational status of the ApexSigma ecosystem. This map supersedes the previous version and represents the current state as of September 25, 2025.

**Verification Date**: September 25, 2025  
**Network Status**: OPERATIONAL  
**Security Level**: PROTECTED - Single Source of Truth  
**Total Services**: 9 Active Containers + 4 External Tools

---

## ⚡ **Network Configuration**

### **Primary Network**
- **Network Name**: `apexsigma_net`
- **Network Type**: Bridge Network
- **Subnet**: `172.26.0.0/16`
- **Gateway**: `172.26.0.1`
- **DNS Resolution**: Container name-based service discovery

---

## 🏗️ **CORE INFRASTRUCTURE SERVICES**

### **1. PostgreSQL Database (Main)**
- **Container**: `apexsigma_postgres`
- **Image**: `postgres:14-alpine`
- **Internal IP**: `172.26.0.2/16`
- **Internal Port**: `5432`
- **External Port**: `5432` (host)
- **Status**: ✅ HEALTHY
- **Health Check**: `pg_isready -U apexsigma_user -d apexsigma-memtank`
- **Databases**: `apexsigma-memtank`, `memos`, `postgres`
- **Primary Use**: Agent registry, DevEnviro orchestrator data, memOS procedural memory

### **2. Redis Cache**
- **Container**: `apexsigma_redis`
- **Image**: `redis:7-alpine`
- **Internal IP**: `172.26.0.5/16`
- **Internal Port**: `6379`
- **External Port**: `6379` (host)
- **Status**: ✅ HEALTHY
- **Health Check**: `redis-cli ping`
- **Primary Use**: Working memory, LLM response caching, session storage

### **3. Qdrant Vector Database**
- **Container**: `apexsigma_qdrant`
- **Image**: `qdrant/qdrant:v1.8.2`
- **Internal IP**: `172.26.0.6/16`
- **Internal Ports**: `6333` (REST), `6334` (gRPC)
- **External Ports**: `6333-6334` (host)
- **Status**: ✅ OPERATIONAL
- **API Endpoint**: `http://localhost:6333`
- **Primary Use**: Semantic memory, embeddings storage, vector similarity search

### **4. Neo4j Knowledge Graph**
- **Container**: `apexsigma_neo4j`
- **Image**: `neo4j:5.15-community`
- **Internal IP**: `172.26.0.4/16`
- **Internal Ports**: `7474` (Browser), `7687` (Bolt)
- **External Ports**: `7473-7474` (host), `7687` (host)
- **Status**: ✅ HEALTHY
- **Health Check**: `cypher-shell -u neo4j -p apexsigma_neo4j_password 'RETURN 1'`
- **Bolt URI**: `bolt://neo4j:7687` (internal)
- **Credentials**: `neo4j:apexsigma_neo4j_password`
- **Primary Use**: Omega Ingest knowledge graph, concept relationships, episodic memory links

---

## 🚀 **APPLICATION SERVICES**

### **5. memOS API (Memory Operations System)**
- **Container**: `apexsigma_memos_api`
- **Image**: `apexsigmaprojectsdev-memos-api`
- **Internal IP**: `172.26.0.8/16`
- **Internal Port**: `8090`
- **External Port**: DISABLED (internal networking only)
- **Status**: ✅ HEALTHY (Full operational mode)
- **Health Check**: `curl -f http://localhost:8090/health`
- **API Endpoints**:
  - **Health**: `/health` - Complete system health status
  - **Memory Operations**: `/memory/store`, `/memory/query`, `/memory/{id}`
  - **Tool Registry**: `/tools/register`, `/tools/search`
  - **Knowledge Graph**: `/graph/query`, `/graph/related`
  - **LLM Cache**: `/llm/cache`, `/llm/usage`
  - **Metrics**: `/metrics` - Prometheus metrics endpoint
- **Database Connections**:
  - PostgreSQL: ✅ Connected (`memos` database)
  - Redis: ✅ Connected (cache tier)
  - Qdrant: ✅ Connected (vector storage)
  - Neo4j: ✅ Connected (knowledge graph)
- **Primary Use**: **OMEGA INGEST GUARDIAN** - Single source of truth for all ApexSigma knowledge

---

## 📊 **OBSERVABILITY STACK**

### **6. Dagster Webserver**
- **Container**: `apexsigma_dagster_webserver`
- **Image**: `apexsigmaprojectsdev-dagster-webserver`
- **Internal IP**: `172.26.0.3/16`
- **Internal Port**: `8080`
- **External Port**: `8081` (host)
- **Status**: ✅ OPERATIONAL
- **UI**: `http://localhost:8081`
- **Primary Use**: Data pipeline orchestration, asset management

---

## ⚠️ **PROBLEMATIC SERVICES**

### **1. Dagster Daemon**
- **Container**: `apexsigma_dagster_daemon`
- **Image**: `apexsigmaprojectsdev-dagster-daemon`
- **Status**: ❌ RESTARTING (exit code 1)
- **Issue**: Service restart loop - requires investigation
- **Impact**: Background job processing may be affected

### **2. DevEnviro Services**
- **Status**: ❌ NOT RUNNING
- **Issue**: Services not started in current configuration
- **Impact**: AI agent orchestration unavailable

### **3. InGest-LLM API**
- **Status**: ❌ NOT RUNNING
- **Issue**: Service not started in current configuration
- **Impact**: Data ingestion pipelines unavailable

### **4. Tools API**
- **Status**: ❌ NOT RUNNING
- **Issue**: Service not started in current configuration
- **Impact**: Tool registry and discovery unavailable

### **5. Observability Stack (Jaeger, Prometheus, Grafana, Loki, Promtail)**
- **Status**: ❌ NOT RUNNING
- **Issue**: Services not started in current configuration
- **Impact**: Distributed tracing and monitoring unavailable

---

## 🔗 **SERVICE INTERCONNECTIONS**

### **memOS Integration Pattern**
```
memOS (172.26.0.8) ←→ PostgreSQL (172.26.0.2:5432) [Procedural Memory]
memOS (172.26.0.8) ←→ Redis (172.26.0.5:6379) [Working Memory/Cache]  
memOS (172.26.0.8) ←→ Qdrant (172.26.0.6:6333) [Vector Embeddings]
memOS (172.26.0.8) ←→ Neo4j (172.26.0.4:7687) [Knowledge Graph]
```

---

## 🛡️ **CRITICAL INFRASTRUCTURE PROTECTION**

### **Tier 1: PROTECTED SERVICES (Immutable Truth)**
These services contain the Omega Ingest and require **dual verification** for any changes:

1. **memOS API** (`172.26.0.8`) - Omega Ingest Guardian
2. **Neo4j Knowledge Graph** (`172.26.0.4`) - Concept relationships
3. **PostgreSQL Main** (`172.26.0.2`) - Procedural memory

### **Health Monitoring Requirements**
- **Continuous Monitoring**: All Tier 1 services require 24/7 health monitoring
- **Alert Thresholds**: <99% uptime triggers immediate alerts
- **Recovery Protocols**: Automated recovery with manual verification requirements
- **Backup Requirements**: Real-time backup of knowledge graph and memory systems

---

## 📍 **EXTERNAL TOOL INTEGRATION**

### **GitHub MCP Server**
- **Container**: `cool_murdock`, `trusting_visvesvaraya`
- **Image**: `ghcr.io/github/github-mcp-server`
- **Status**: ✅ Up 12+ hours
- **Primary Use**: GitHub integration, repository management

### **Docker LSP Services**
- **Container**: `docker_labs-vscode-installer-desktop-extension-service`
- **Image**: `docker/labs-vscode-installer:0.0.9`
- **Status**: ✅ Up 3+ days
- **Primary Use**: Docker Desktop integration

### **Portainer Docker Extension**
- **Container**: `portainer_portainer-docker-extension-desktop-extension-service`
- **Image**: `portainer/portainer-docker-extension:2.33.1`
- **Status**: ✅ Up 3+ days
- **Primary Use**: Docker container management UI

---

## 🎯 **OPERATIONAL PROCEDURES**

### **Service Restart Sequence**
1. **Infrastructure First**: PostgreSQL → Redis → Qdrant → Neo4j
2. **Applications**: memOS
3. **Orchestration**: Dagster Webserver → Dagster Daemon
4. **Observability**: Prometheus → Loki → Jaeger → Grafana

### **Health Check Endpoints**
- **memOS**: `http://172.26.0.8:8090/health`
- **Dagster Webserver**: `http://172.26.0.3:8080`
- **Neo4j**: `http://172.26.0.4:7474`

### **Emergency Procedures**
- **Omega Ingest Corruption**: Stop all writes to memOS, restore from Neo4j backup
- **Network Segmentation**: Isolate Tier 1 services, maintain internal connectivity
- **Service Failure**: Follow restart sequence, verify health checks before proceeding

---

## ✅ **VERIFICATION STATUS**

**Last Verified**: September 25, 2025, 14:30 UTC  
**Verification Method**: Direct container inspection, health check validation, network topology mapping  
**Status**: CRITICAL SERVICES OPERATIONAL  
**Next Verification**: Required before any infrastructure changes

**Verified By**: iFlow CLI - ApexSigma Infrastructure Analysis  
**Authority**: Single Source of Truth for ApexSigma Docker Network Topology

---

## 📝 Audit Addendum (2025-09-25)
- Current configuration reflects a minimal operational setup focused on core memory services
- Extended services (DevEnviro, InGest-LLM, Tools, Observability stack) are not currently running
- Dagster daemon requires troubleshooting due to restart loop
- All critical data storage services (PostgreSQL, Redis, Qdrant, Neo4j) are healthy and operational
- memOS API is fully functional with all database connections active

*This updated map reflects the current operational state of the ApexSigma ecosystem as verified on September 25, 2025.*