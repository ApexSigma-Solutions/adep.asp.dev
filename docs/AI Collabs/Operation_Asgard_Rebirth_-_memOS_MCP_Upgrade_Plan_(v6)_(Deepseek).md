# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6) (Deepseek)

## Workflow Protocol

1.  **Strict Sequential Order**: The workflow for each task is strictly sequential. The Implementer and Reviewer roles are not concurrent. The project cannot proceed to the next task in the sequence until the Reviewer has formally approved the current task and marked its checkbox as complete in this document.

2.  **Asynchronous Execution (Concurrency)**: Tasks are not to be completed asynchronously. The only exception is if the task plan explicitly defines a multi-agent team for a specific task (e.g., two Implementers and one Reviewer).

3.  **Handoff Procedure**: The Reviewer's role for any given task must not begin until the Implementer has formally completed and submitted their work.

---

## Phase 0: Monorepo Foundation & Integration

-   [ ] **Task ID: MEMOS-P0-T1**
    -   **Description**: Update all path dependencies, imports, and CI/CD pipelines to align with the new monorepo structure. Consolidate environment configuration files.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Execute all technical aspects of the task as described. Update Python imports to reflect new `services/` and `libs/` structure. Modify GitHub Actions workflows to handle monorepo build process. Consolidate `.env` files into standardized structure.
    -   **Reviewer**: Qwen
        -   **Role**: Conduct comprehensive review of updated paths, import statements, and CI/CD configuration.
    -   **Done means Done**: All import statements reflect new monorepo structure. CI/CD pipelines successfully build and test individual services. Environment variables are properly consolidated and documented.

-   [ ] **Task ID: MEMOS-P0-T2**
    -   **Description**: Scaffold the `libs/apexsigma-core` shared library with initial Pydantic models, unified storage interfaces, protocol enums, and database connectors.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create the shared library structure with abstract base classes for storage backends, common data schemas, authentication components, and observability utilities.
    -   **Reviewer**: Qwen
        -   **Role**: Review library structure, interface definitions, and ensure proper abstraction patterns.
    -   **Done means Done**: `apexsigma-core` package is created with initial directory structure. It is installed as an editable dependency in the development environment. Basic CI validation passes.

-   [ ] **Task ID: MEMOS-P0-T3**
    -   **Description**: Create unified root-level Docker Compose configuration for the entire ecosystem with proper networking and service discovery.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Implement `docker-compose.dev.yml` and `docker-compose.prod.yml` templates that orchestrate all services with consistent networking and shared dependencies.
    -   **Reviewer**: Qwen
        -   **Role**: Review Docker Compose configuration for proper service discovery, network topology, and environment variable management.
    -   **Done means Done**: Unified Docker Compose files created. All services can resolve each other by service name. Development environment spins up successfully with `docker-compose up`.

---

## Phase 1: Solidify the Core (memOS.as Service / "Tools" Layer)

-   [ ] **Task ID: MEMOS-P1-T1**
    -   **Description**: Scaffold the new `memOS.as` service using the **FastMCP 2.0 (FastAPI)** template, leveraging `libs/apexsigma-core` for shared components.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create FastMCP 2.0 service structure with dependencies on `apexsigma-core` for shared models and utilities.
    -   **Reviewer**: Qwen
        -   **Role**: Review service scaffolding and integration with shared library components.
    -   **Done means Done**: "Hello world" endpoint is deployed and accessible. Service successfully imports and uses components from `apexsigma-core`. CI pipeline runs successfully.

-   [ ] **Task ID: MEMOS-P1-T2**
    -   **Description**: Implement the **Pluggable Storage Backend - Tier 1 & 2** (Redis & PostgreSQL) using shared interfaces from `libs/apexsigma-core`.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Implement Redis and PostgreSQL adapters that conform to the shared storage interfaces defined in `apexsigma-core`.
    -   **Reviewer**: Qwen
        -   **Role**: Review implementation against shared interface contracts and ensure proper abstraction.
    -   **Done means Done**: API endpoints for session data and agent metadata are fully functional and unit-tested. All storage implementations use shared interfaces from `apexsigma-core`.

-   [ ] **Task ID: MEMOS-P1-T3**
    -   **Description**: Implement the **Pluggable Storage Backend - Tier 3 & 4** (Qdrant & Neo4j) using shared interfaces from `libs/apexsigma-core`.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Implement Qdrant and Neo4j adapters that conform to the shared storage interfaces.
    -   **Reviewer**: Qwen
        -   **Role**: Review implementation for consistency with shared interfaces and proper abstraction patterns.
    -   **Done means Done**: API endpoints for semantic search and relationship queries are functional and tested. All implementations use shared interfaces from `apexsigma-core`.

-   [ ] **Task ID: MEMOS-P1-OMEGA**
    -   **Description**: Perform an **Omega Ingest** of the final Phase 1 architecture, API documentation, and all MAR sign-off reports into the master knowledge graph.
    -   **Done means Done**: All Phase 1 artifacts are synthesized and accessible, including documentation of shared library usage patterns.

---

## Phase 2: Integrate the Orchestrator (Dagster)

-   [ ] **Task ID: MEMOS-P2-T1**
    -   **Description**: Implement unified Dagster workspace at monorepo root with `memOS.as` as the first code location.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create Dagster workspace configuration that treats `services/memos.as` as a code location within the unified monorepo workspace.
    -   **Reviewer**: Qwen
        -   **Role**: Review workspace configuration and ensure proper integration with monorepo structure.
    -   **Done means Done**: Dagster UI is running and can successfully load the memOS repository as a code location within the unified workspace.

-   [ ] **Task ID: MEMOS-P2-T2**
    -   **Description**: Define Dagster assets for key data entities within memOS and implement maintenance jobs, leveraging shared assets from `libs/apexsigma-core`.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Implement Dagster assets and jobs that use shared asset definitions from the core library where appropriate.
    -   **Reviewer**: Qwen
        -   **Role**: Review asset definitions and job implementations for consistency with shared patterns.
    -   **Done means Done**: Data assets are visible and jobs run successfully. Shared asset patterns are established for future cross-service workflows.

-   [ ] **Task ID: MEMOS-P2-OMEGA**
    -   **Description**: Perform an **Omega Ingest** of the Dagster project configuration and data asset catalog, emphasizing the unified workspace approach.
    -   **Done means Done**: All Phase 2 artifacts are synthesized and accessible, including documentation of the unified workspace pattern.

---

## Phase 3: Deploy the Intelligence ("Workers" Layer)

-   [ ] **Task ID: MEMOS-P3-T1**
    -   **Description**: Scaffold the **Agent Swarm** project, implementing the core `AgentRole`, `AgentContext`, and `MCPAgent` classes using shared components from `libs/apexsigma-core`.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Create agent swarm structure with dependencies on shared models and utilities from `apexsigma-core`.
    -   **Reviewer**: Qwen
        -   **Role**: Review agent implementation and integration with shared library components.
    -   **Done means Done**: A single `MCPAgent` can be initialized using shared components from `apexsigma-core`.

-   [ ] **Task ID: MEMOS-P3-T2**
    -   **Description**: Implement the `MCPAgentSwarm` class and integrate it with the `tools.as` service registry, preparing for RabbitMQ integration.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Implement agent swarm coordination with architecture designed for future RabbitMQ integration for asynchronous messaging.
    -   **Reviewer**: Qwen
        -   **Role**: Review swarm implementation and messaging architecture for proper foundation for future RabbitMQ integration.
    -   **Done means Done**: The `MCPAgentSwarm` can delegate a task to multiple agents. Architecture is prepared for RabbitMQ integration.

-   [ ] **Task ID: MEMOS-P3-OMEGA**
    -   **Description**: Perform the final **Omega Ingest** of the agent swarm's design and all MAR sign-off reports, emphasizing the shared component architecture.
    -   **Done means Done**: The completed memOS ecosystem is fully documented and verified in the master knowledge graph, with comprehensive documentation of shared library usage patterns.

---

## Future-Ready Technologies & Considerations

### Immediate Integration Priorities
- **OpenTelemetry**: Implement distributed tracing from the start using shared instrumentation in `libs/apexsigma-core`
- **Redis Optimization**: Implement Redis for cross-service caching, session management, and real-time data synchronization
- **RabbitMQ Preparation**: Architecture designed for easy RabbitMQ integration in Phase 3+ for asynchronous messaging

### Medium-Term Evaluation Candidates
- **Apache Pulsar/Kafka**: For advanced event streaming needs beyond RabbitMQ capabilities
- **TimescaleDB**: For time-series analysis of agent interactions
- **Feature Stores (Feast)**: For consistent feature serving across agents
- **Vector Database Alternatives**: Abstract interfaces to allow future evaluation of Weaviate, Pinecone, etc.

### Long-Term Strategic Technologies
- **Kubernetes Operators**: For cloud-native deployment scalability
- **Service Mesh (Istio/Linkerd)**: For advanced traffic management at scale
- **Open Policy Agent (OPA)**: For scalable authorization policy management
- **Great Expectations**: For automated data quality testing

---

## Risk Assessment & Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Path dependency issues | High | Medium | Implement automated path validation tooling in CI/CD |
| Docker network conflicts | Medium | High | Standardize service discovery patterns and network topology |
| Shared library versioning conflicts | Medium | High | Establish strict semantic versioning and API stability policies |
| Dagster workspace complexity | Medium | Medium | Start with minimal viable workspace structure, iterate gradually |
| Redis implementation scope creep | Low | High | Focus on critical path use cases first (caching, session management) |
| Cross-service dependency management | High | High | Establish clear dependency contracts and backward compatibility guarantees |

---

## Implementation Roadmap Summary

1.  **Phase 0 (Foundation)**: Monorepo alignment, shared library creation, unified Docker setup
2.  **Phase 1 (Core)**: memOS service implementation with shared storage interfaces
3.  **Phase 2 (Orchestration)**: Unified Dagster workspace implementation
4.  **Phase 3 (Intelligence)**: Agent swarm deployment with prepared architecture for future messaging
5.  **Future Phases**: Advanced messaging (RabbitMQ/Kafka), specialized databases, advanced orchestration

The monorepo structure provides a solid foundation for these enhancements, with the centralized `libs/` directory being immediately actionable for shared infrastructure components. The key is maintaining strict API stability and clear dependency management throughout the implementation.