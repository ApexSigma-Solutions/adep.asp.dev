# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6p3)

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

## Phase 3: Deploy the Intelligence ("Workers" Layer)

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