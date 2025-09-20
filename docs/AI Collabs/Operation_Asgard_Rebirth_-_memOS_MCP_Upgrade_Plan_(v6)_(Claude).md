# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6) (Claude)

## Executive Summary

This enhanced plan incorporates strategic insights from multiple AI analyses following the successful completion of Operation Monorepo Genesis. The monorepo restructuring fundamentally changes our approach to the memOS MCP upgrade, enabling shared infrastructure, unified orchestration, and improved scalability. This v6 plan introduces a critical Phase 0 for monorepo integration and updates all subsequent phases to leverage the new architecture.

## Workflow Protocol

1. **Strict Sequential Order**: The workflow for each task is strictly sequential. The Implementer and Reviewer roles are not concurrent. The project cannot proceed to the next task until the Reviewer has formally approved the current task and marked its checkbox as complete.

2. **Synchronous Execution**: Tasks must be completed sequentially within each phase. The only exception is if the task plan explicitly defines a multi-agent team for a specific task.

3. **Handoff Procedure**: The Reviewer's role for any given task must not begin until the Implementer has formally completed and submitted their work with an implementation report.

4. **Monorepo Context**: All tasks must consider the new monorepo structure, with services located in `services/` and shared code in `libs/`.

---

## Phase 0: Monorepo Foundation & Integration

-   [ ] **Task ID: MEMOS-P0-T1**
    -   **Description**: Scaffold the `libs/apexsigma-core` shared library package. This will house all common MCP abstractions, storage interfaces, Pydantic models, protocol enums, and shared utilities.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create the package structure with proper Python packaging configuration. Include base classes for storage backends, common exceptions, and MCP protocol definitions.
    -   **Reviewer**: Qwen
        -   **Role**: Verify package structure, import functionality, and compliance with Python best practices.
    -   **Done means Done**: 
        - The `apexsigma-core` package exists with proper `pyproject.toml` or `setup.py`
        - Package is installable via `pip install -e libs/apexsigma-core`
        - Base storage interface classes are defined
        - CI pipeline recognizes and can build the package

-   [ ] **Task ID: MEMOS-P0-T2**
    -   **Description**: Update all path dependencies, import statements, and environment configurations to align with the monorepo structure.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Audit and update all Python imports, Docker paths, and configuration files to reflect the new `services/` and `libs/` structure.
    -   **Reviewer**: Qwen
        -   **Role**: Verify all imports resolve correctly and services can locate shared resources.
    -   **Done means Done**:
        - All Python imports updated to reflect monorepo paths
        - Environment variables consolidated with clear hierarchy (.env for shared, services/*/env for specific)
        - Docker Compose files updated with correct volume mounts and build contexts
        - No import errors when running basic tests

-   [ ] **Task ID: MEMOS-P0-T3**
    -   **Description**: Create unified root-level Docker Compose configuration for the entire ecosystem.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Consolidate service definitions into `docker-compose.dev.yml` and `docker-compose.prod.yml` at repository root.
    -   **Reviewer**: Qwen
        -   **Role**: Verify all services start correctly and can communicate via Docker network.
    -   **Done means Done**:
        - `docker-compose.dev.yml` exists with development configurations (volume mounts, hot reload)
        - `docker-compose.prod.yml` exists with production configurations (built images, no mounts)
        - All services can resolve each other by name (e.g., `http://memos-as:8090`)
        - Redis and PostgreSQL services included and accessible

-   [ ] **Task ID: MEMOS-P0-T4**
    -   **Description**: Initialize unified Dagster workspace configuration at monorepo root.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create Dagster workspace with initial configuration treating services as code locations.
    -   **Reviewer**: Qwen
        -   **Role**: Verify Dagster UI loads and recognizes service code locations.
    -   **Done means Done**:
        - `workspace.yaml` configured with services as code locations
        - Dagster UI accessible and shows workspace structure
        - Basic asset definitions loadable from `libs/apexsigma-core`
        - Docker Compose includes Dagster services (dagit, daemon, postgres for metadata)

---

## Phase 1: Solidify the Core (memOS.as Service / "Tools" Layer)

-   [ ] **Task ID: MEMOS-P1-T1**
    -   **Description**: Scaffold the new `memOS.as` service using **FastMCP 2.0 (FastAPI)** template, leveraging `libs/apexsigma-core` for shared components.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create FastAPI service structure with MCP endpoints, utilizing shared library for models and interfaces.
    -   **Reviewer**: Qwen
        -   **Role**: Verify service structure, shared library usage, and endpoint accessibility.
    -   **Done means Done**:
        - FastAPI service scaffolded in `services/memos.as/`
        - Imports and uses models from `libs/apexsigma-core`
        - "Hello World" MCP endpoint accessible at defined port
        - Redis connection initialized using shared client from library
        - CI pipeline passes with new service

-   [ ] **Task ID: MEMOS-P1-T2**
    -   **Description**: Implement **Pluggable Storage Backend - Tier 1 & 2** (Redis for caching/session & PostgreSQL for persistence) using interfaces from `libs/apexsigma-core`.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Implement storage adapters following the abstract interfaces defined in shared library.
    -   **Reviewer**: Qwen
        -   **Role**: Verify storage operations, data persistence, and interface compliance.
    -   **Done means Done**:
        - Redis adapter implements caching and session management
        - PostgreSQL adapter implements persistent storage for agent metadata
        - Both adapters follow interfaces from `apexsigma-core`
        - API endpoints for CRUD operations fully functional
        - Unit tests pass with >80% coverage
        - Cross-service session sharing demonstrated

-   [ ] **Task ID: MEMOS-P1-T3**
    -   **Description**: Implement **Pluggable Storage Backend - Tier 3 & 4** (Qdrant for vectors & Neo4j for relationships).
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Extend storage backend with vector and graph database support.
    -   **Reviewer**: Qwen
        -   **Role**: Verify semantic search and relationship query functionality.
    -   **Done means Done**:
        - Qdrant adapter implements semantic/vector search
        - Neo4j adapter implements relationship queries
        - Both integrated into the pluggable backend system
        - API endpoints for vector similarity and graph traversal functional
        - Performance benchmarks documented (baseline QPS, P95 latency)

-   [ ] **Task ID: MEMOS-P1-OMEGA**
    -   **Description**: Perform **Omega Ingest** of Phase 1 architecture, API documentation, storage backend designs, and all MAR reports.
    -   **Done means Done**: All Phase 1 artifacts synthesized and accessible in master knowledge graph.

---

## Phase 2: Integrate the Orchestrator (Dagster)

-   [ ] **Task ID: MEMOS-P2-T1**
    -   **Description**: Integrate `memOS.as` as a code location in the monorepo-wide Dagster workspace.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Define memOS assets and integrate with existing workspace configuration.
    -   **Reviewer**: Qwen
        -   **Role**: Verify asset definitions load and are visible in Dagster UI.
    -   **Done means Done**:
        - `services/memos.as/dagster/` directory contains asset definitions
        - Workspace.yaml updated to include memOS code location
        - Dagster UI displays memOS assets alongside other services
        - Basic materialization job runs successfully

-   [ ] **Task ID: MEMOS-P2-T2**
    -   **Description**: Define cross-service Dagster assets and implement data pipeline orchestration.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create assets that span multiple services and implement maintenance/sync jobs.
    -   **Reviewer**: Qwen
        -   **Role**: Verify cross-service dependencies and job execution.
    -   **Done means Done**:
        - Cross-service asset dependencies defined (e.g., memOS → tools.as data flow)
        - Scheduled jobs for data synchronization implemented
        - Maintenance jobs for cleanup and optimization created
        - All jobs execute successfully with proper error handling

-   [ ] **Task ID: MEMOS-P2-OMEGA**
    -   **Description**: Perform **Omega Ingest** of Dagster configuration, asset catalog, and job definitions.
    -   **Done means Done**: All Phase 2 artifacts synthesized and accessible.

---

## Phase 3: Deploy the Intelligence ("Workers" Layer)

-   [ ] **Task ID: MEMOS-P3-T1**
    -   **Description**: Scaffold **Agent Swarm** project with core classes, utilizing `libs/apexsigma-core` for shared agent definitions.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Implement `AgentRole`, `AgentContext`, and `MCPAgent` base classes in shared library.
    -   **Reviewer**: Qwen
        -   **Role**: Verify agent initialization and basic functionality.
    -   **Done means Done**:
        - Core agent classes defined in `libs/apexsigma-core`
        - Single MCPAgent can be initialized and configured
        - Agent can connect to memOS.as via MCP protocol
        - Basic agent lifecycle methods implemented

-   [ ] **Task ID: MEMOS-P3-T2**
    -   **Description**: Implement `MCPAgentSwarm` with RabbitMQ/Redis Pub-Sub for inter-agent communication.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create swarm orchestration with message-based coordination between agents.
    -   **Reviewer**: Qwen
        -   **Role**: Verify multi-agent task delegation and communication.
    -   **Done means Done**:
        - MCPAgentSwarm manages multiple agent instances
        - Agents communicate via RabbitMQ queues or Redis Pub/Sub
        - Task delegation and result aggregation functional
        - Integration with tools.as service registry complete
        - Load testing shows successful scaling to 10+ agents

-   [ ] **Task ID: MEMOS-P3-OMEGA**
    -   **Description**: Perform final **Omega Ingest** of agent swarm architecture and all implementation artifacts.
    -   **Done means Done**: Complete memOS ecosystem documented and verified in master knowledge graph.

---

## Risk Assessment & Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Path dependency conflicts | High | Medium | Complete P0-T2 thoroughly before proceeding |
| Docker networking issues | Medium | High | Test service discovery in P0-T3 extensively |
| Storage adapter complexity | Medium | Medium | Define clear interfaces in apexsigma-core first |
| Dagster workspace conflicts | Low | Medium | Start with minimal code locations, expand gradually |
| Agent communication bottlenecks | Medium | High | Design for both Redis Pub/Sub and RabbitMQ from start |

---

## Future-Ready Technologies

### Immediate Consideration (Phase 1-2)
- **OpenTelemetry**: Instrument all services from the start for observability
- **Redis Streams**: Consider as alternative to basic Pub/Sub for event sourcing
- **pgvector**: Evaluate as PostgreSQL-native alternative to Qdrant

### Medium-term (Phase 3+)
- **Apache Kafka/Pulsar**: For high-throughput event streaming beyond RabbitMQ
- **Temporal.io**: For complex, long-running workflow orchestration
- **MLflow**: For ML model lifecycle management in agent swarm

### Long-term Exploration
- **Kubernetes**: For production orchestration beyond Docker Compose
- **Service Mesh (Istio/Linkerd)**: For advanced traffic management
- **Feature Store (Feast)**: For consistent ML feature serving across agents

---

## Implementation Checklist

### Immediate Actions (Before Phase 0)
1. ✓ Review and understand monorepo structure from Operation Monorepo Genesis
2. ✓ Identify all services requiring path updates
3. ✓ Document current environment variable usage
4. ✓ Plan Redis and RabbitMQ integration points

### Phase 0 Prerequisites
- [ ] Update CI/CD pipelines for monorepo structure
- [ ] Create development environment setup documentation
- [ ] Establish Python path management strategy
- [ ] Define service naming conventions for Docker network

### Success Metrics
- **Phase 0**: All services communicating via Docker network
- **Phase 1**: Storage backends operational with <100ms latency
- **Phase 2**: Dagster orchestrating cross-service workflows
- **Phase 3**: Agent swarm handling concurrent tasks successfully

---

## Conclusion

This v6 plan transforms the memOS MCP upgrade from a service-specific enhancement to an ecosystem-wide architectural evolution. By leveraging the monorepo structure established in Operation Monorepo Genesis, we create a unified, scalable, and maintainable system ready for future growth. The addition of Phase 0 ensures a solid foundation, while the enhanced phases 1-3 maximize the benefits of shared infrastructure and unified orchestration.