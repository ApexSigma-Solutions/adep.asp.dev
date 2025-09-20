# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6)

**Tags:** ApexSigma, API, FastMCP, MAR, Plan, MCP, Python, Upgrade, Monorepo, Strategic-Evolution

---

## 1. Strategic Context: Post-Monorepo Genesis Evolution

The successful completion of **Operation: Monorepo Genesis** has fundamentally altered the strategic landscape for this upgrade. The v5 plan is now deprecated. This v6 plan is the new single source of truth, reflecting a synthesis of analyses from multiple AI strategists.

Key strategic advantages we must now leverage are:

*   **Centralized Shared Libraries**: The `libs/apexsigma-core` directory is the heart of the ecosystem for shared code, models, and interfaces.
*   **Unified Development Environment**: A single, root-level `docker-compose.yml` and Dagster workspace will orchestrate all services.
*   **Simplified CI/CD**: The monorepo allows for a unified build, test, and deployment pipeline.
*   **Cross-Service Integration**: Shared infrastructure for Redis (caching/state) and RabbitMQ (messaging) is now trivial to implement.

---

## 2. Workflow Protocol

1.  **Single Source of Truth**: This document is the master plan. All work aligns with it.
2.  **Strict Sequential Order**: The workflow is strictly sequential. A task's Reviewer cannot begin until the Implementer's work is formally submitted. The project does not proceed until the current task is approved and its checkbox is marked complete.
3.  **Monorepo-First Principle**: All implementations must leverage the new monorepo structure, particularly the `libs/` directory and unified service architecture.

---

### Phase 0: Monorepo Foundation & Integration

**Strategic Imperative**: Before implementing any core memOS functionality, we must first establish the foundational monorepo infrastructure. This phase is non-negotiable and all subsequent phases depend on its successful completion.

*   [ ] **Task ID: MEMOS-P0-T1**
    *   **Description**: Scaffold the `libs/apexsigma-core` shared library. This package will house all common code: Pydantic models for MCP protocols, unified storage backend interfaces (abstract base classes), protocol enums, database connectors, and shared utilities for observability and configuration.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   `libs/apexsigma-core` package exists with a `pyproject.toml`.
        *   Abstract base classes for all planned storage backends are defined.
        *   The package can be installed as an editable dependency (`pip install -e libs/apexsigma-core`) in any service.
        *   The CI pipeline successfully builds and runs unit tests on the shared library.

*   [ ] **Task ID: MEMOS-P0-T2**
    *   **Description**: Create the root-level `docker-compose.yml` for the entire ecosystem and establish a unified environment variable management strategy. This includes refactoring all existing service paths and dependencies to align with the new structure.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   A root-level `docker-compose.yml` orchestrates all ecosystem services (including databases, Dagster, etc.).
        *   All services communicate over a shared Docker network using service names.
        *   A hierarchical `.env` structure is implemented (e.g., root `.env` for shared vars, `services/memos.as/.env` for specifics).
        *   All Python import paths in existing code are updated to reflect the `services/` and `libs/` structure.
        *   The entire development environment starts successfully with a single `docker-compose up` command.

*   [ ] **Task ID: MEMOS-P0-T3**
    *   **Description**: Establish a monorepo-wide Dagster workspace at the repository root, with individual services defined as code locations.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   A root `workspace.yaml` is configured with `services/memos.as` (and others) as code locations.
        *   The Dagster UI loads successfully and displays the unified workspace.
        *   Shared asset definitions can be imported from `libs/apexsigma-core`.
        *   The Dagster daemon and UI run as services in the root `docker-compose.yml`.

---

### Phase 1: Solidify the Core memOS.as Service ("Tools" Layer)

**Strategic Imperative**: Build the core memOS service on top of the new monorepo foundation, establishing the pluggable storage architecture.

*   [ ] **Task ID: MEMOS-P1-T1**
    *   **Description**: Scaffold the new `memOS.as` service using the FastMCP 2.0 (FastAPI) template, ensuring deep integration with the `libs/apexsigma-core` shared library.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   The service is created in `services/memos.as`.
        *   It successfully imports and utilizes Pydantic models and storage interfaces from `libs/apexsigma-core`.
        *   A "hello world" endpoint is deployed and accessible via the unified Docker network.
        *   The CI pipeline builds and tests the service within the monorepo context.

*   [ ] **Task ID: MEMOS-P1-T2**
    *   **Description**: Implement the Pluggable Storage Backend for **Tier 1 & 2** (Redis for cache/session, PostgreSQL for persistent metadata) using the shared interfaces from `libs/apexsigma-core`.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   A Redis adapter implements the shared caching interface, handling session state and TTL-bound data.
        *   A PostgreSQL adapter implements the durable storage interface.
        *   The active storage backend is configurable via environment variables.
        *   API endpoints for agent metadata and session data are fully functional and unit-tested.

*   [ ] **Task ID: MEMOS-P1-T3**
    *   **Description**: Implement the Pluggable Storage Backend for **Tier 3 & 4** (Qdrant for semantic search, Neo4j for relationship graphs) using the shared interface pattern.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   A Qdrant adapter implements the vector storage interface, providing semantic search capabilities.
        *   A Neo4j adapter implements the graph storage interface, enabling relationship queries.
        *   API endpoints for semantic search and graph traversal are functional and tested.

*   [ ] **Task ID: MEMOS-P1-OMEGA**
    *   **Description**: Perform an **Omega Ingest** of the final Phase 1 architecture, API documentation, shared library patterns, and all MAR sign-off reports into the master knowledge graph.
    *   **Done means Done**: All Phase 1 artifacts are synthesized, deduplicated, and accessible in the knowledge graph.

---

### Phase 2: Integrate the Orchestrator (Unified Dagster)

**Strategic Imperative**: Weave the memOS service into the ecosystem's data fabric, enabling cross-service orchestration.

*   [ ] **Task ID: MEMOS-P2-T1**
    *   **Description**: Formally define `memOS.as` assets within its Dagster code location, enabling cross-service data awareness.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   All core memOS data entities (e.g., agent sessions, memory objects) are represented as Dagster assets.
        *   Assets are visible and can be materialized from the unified Dagster UI.
        *   Cross-service asset dependencies (e.g., an asset in `tools.as` depending on a `memos.as` asset) can be defined and executed.

*   [ ] **Task ID: MEMOS-P2-T2**
    *   **Description**: Implement maintenance jobs and data synchronization pipelines using Dagster to ensure ecosystem health and consistency.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   Scheduled jobs for data cleanup, backup, and indexing run successfully.
        *   Asset freshness monitoring and alerting are configured and functional.
        *   A data synchronization pipeline between `memos.as` and another service is demonstrated.

*   [ ] **Task ID: MEMOS-P2-OMEGA**
    *   **Description**: Perform an **Omega Ingest** of the unified Dagster project configuration, the cross-service asset catalog, and key orchestration patterns.
    *   **Done means Done**: All Phase 2 orchestration artifacts are synthesized and accessible in the knowledge graph.

---

### Phase 3: Deploy the Intelligence ("Workers" Layer)

**Strategic Imperative**: Bring the agent swarm to life, enabling distributed intelligence and task execution.

*   [ ] **Task ID: MEMOS-P3-T1**
    *   **Description**: Scaffold the **Agent Swarm** project, implementing the core `AgentRole`, `AgentContext`, and `MCPAgent` classes using the shared library foundations. Architect for asynchronous communication.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   Agent base classes leverage shared protocols from `libs/apexsigma-core`.
        *   A single `MCPAgent` can be initialized and can communicate with the `memOS.as` service.
        *   The architecture is explicitly designed for a message bus (RabbitMQ) to be plugged in for inter-agent communication.

*   [ ] **Task ID: MEMOS-P3-T2**
    *   **Description**: Implement the `MCPAgentSwarm` class and integrate it with the `tools.as` service registry and a RabbitMQ message bus for robust, distributed task delegation.
    *   **Implementer**: Gemini (CLI)
    *   **Reviewer**: Qwen
    *   **Done means Done**:
        *   The `MCPAgentSwarm` can delegate tasks to multiple agents across different services.
        *   Task distribution uses RabbitMQ for reliable, asynchronous messaging.
        *   Integration with the `tools.as` service registry for tool discovery is functional.
        *   Load balancing and failure recovery mechanisms are demonstrated.

*   [ ] **Task ID: MEMOS-P3-OMEGA**
    *   **Description**: Perform the final **Omega Ingest** of the complete memOS ecosystem design, agent swarm architecture, cross-service integration patterns, and all MAR sign-off reports.
    *   **Done means Done**: The completed memOS ecosystem is fully documented and verified in the master knowledge graph.

---

## 3. Future-Ready Technologies & Edge Cases

The monorepo architecture prepares us for future enhancements. These are not in scope for v6 but should inform our design choices.

| Category          | Technology          | Use Case & Rationale                                                                                                                   |
| :---------------- | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------- |
| **Observability** | OpenTelemetry       | Implement from Phase 0 in `libs/apexsigma-core` for unified, distributed tracing across all services. Non-negotiable.                  |
| **Event Streaming** | Apache Kafka / Redpanda | For when RabbitMQ is insufficient for high-throughput, replayable event logs from the agent swarm.                                     |
| **Orchestration** | Kubernetes          | The natural evolution from Docker Compose for production-grade, auto-scaling deployments.                                              |
| **Workflow**      | Temporal.io         | For managing complex, long-running, stateful workflows that go beyond Dagster's data asset scope.                                      |
| **ML Operations** | MLflow / Feast      | For managing the lifecycle of agent models and serving features consistently across the swarm.                                         |

---

## 4. Risk Assessment & Mitigation

| Risk Category | Risk                               | Probability | Impact | Mitigation Strategy                                                                                                                                    |
| :------------ | :--------------------------------- | :---------- | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Technical** | Path dependency hell               | High        | Medium | Execute **MEMOS-P0-T2** meticulously. Implement automated path validation and linting in the CI pipeline.                                              |
| **Technical** | Shared library version conflicts   | Medium      | High   | Enforce strict semantic versioning and a clear CHANGELOG policy for `libs/apexsigma-core`.                                                           |
| **Operational** | Docker network conflicts           | Medium      | High   | Standardize service discovery patterns and network naming conventions in **MEMOS-P0-T2**.                                                              |
| **Performance** | Messaging bus latency              | Low         | High   | Benchmark Redis Pub/Sub vs. RabbitMQ for specific use cases. Start with Redis for simple cases, use RabbitMQ for guaranteed delivery.                  |
| **Security**  | Cross-service auth                 | Medium      | High   | Implement a unified authentication/authorization strategy within `libs/apexsigma-core` from the start. Plan for Vault integration.                     |
