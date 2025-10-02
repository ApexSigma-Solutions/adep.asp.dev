# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6)

**Tags:** ApexSigma, API, FastMCP, MAR, Plan, MCP, Python, Upgrade, Monorepo, Strategic-Evolution

---

### 1. Strategic Context: Post-Monorepo Genesis Evolution

The successful completion of **Operation: Monorepo Genesis** has fundamentally altered the strategic landscape for this upgrade. The v5 plan is now deprecated. This v6 plan is the new single source of truth, reflecting a synthesis of analyses from multiple AI strategists.

Key strategic advantages we must now leverage are:

*   **Centralized Shared Libraries**: The `libs/apexsigma-core` directory is the heart of the ecosystem for shared code, models, and interfaces.
*   **Unified Development Environment**: A single, root-level `docker-compose.yml` and Dagster workspace will orchestrate all services.
*   **Simplified CI/CD**: The monorepo allows for a unified build, test, and deployment pipeline.
*   **Cross-Service Integration**: Shared infrastructure for Redis (caching/state) and RabbitMQ (messaging) is now trivial to implement.

---

### 2. Workflow Protocol

1.  **Single Source of Truth**: This document is the master plan. All work aligns with it.
2.  **Strict Sequential Order**: The workflow is strictly sequential. A task's Reviewer cannot begin until the Implementer's work is formally submitted. The project does not proceed until the current task is approved and its checkbox is marked complete.
3.  **Monorepo-First Principle**: All implementations must leverage the new monorepo structure, particularly the `libs/` directory and unified service architecture.

---

## Phase 2: Integrate the Orchestrator (Unified Dagster)

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
