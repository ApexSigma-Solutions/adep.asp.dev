# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6p0)

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