---
tags:
  - ApexSigma
  - API
  - FastMCP
  - MAR
  - Plan
  - MCP
  - Client
  - Python
  - Upgrade
---
## Workflow Protocol

1.  **Strict Sequential Order**: The workflow for each task is strictly sequential. The Implementer and Reviewer roles are not concurrent. The project cannot proceed to the next task in the sequence until the Reviewer has formally approved the current task and marked its checkbox as complete in this document.

2.  **Asynchronous Execution (Concurrency)**: Tasks are not to be completed asynchronously. The only exception is if the task plan explicitly defines a multi-agent team for a specific task (e.g., two Implementers and one Reviewer).

3.  **Handoff Procedure**: The Reviewer's role for any given task must not begin until the Implementer has formally completed and submitted their work.

---

## Phase 1: Solidify the Core (memOS.as Service / "Tools" Layer)

-   [ ] **Task ID: MEMOS-P1-T1**
    -   **Description**: Scaffold the new `memOS.as` service using the **FastMCP 2.0 (FastAPI)** template.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Execute all technical aspects of the task as described. Upon completion, submit the work and a brief implementation report to the Reviewer.
    -   **Reviewer**: Qwen
        -   **Role**: Awaiting the Implementer's submission. Upon receipt, conduct a formal review of the work against all "Done means Done" criteria. **Upon approval, the Reviewer must mark this task's checkbox as complete.**
    -   **Done means Done**: A "hello world" endpoint is deployed and accessible. The CI pipeline runs successfully. The work has been reviewed and signed off by the Reviewer.

-   [ ] **Task ID: MEMOS-P1-T2**
    -   **Description**: Implement the **Pluggable Storage Backend - Tier 1 & 2** (Redis & PostgreSQL).
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Execute all technical aspects of the task as described. Upon completion, submit the work and a brief implementation report to the Reviewer.
    -   **Reviewer**: Qwen
        -   **Role**: Awaiting the Implementer's submission. Upon receipt, conduct a formal review of the work against all "Done means Done" criteria. **Upon approval, the Reviewer must mark this task's checkbox as complete.**
    -   **Done means Done**: API endpoints for session data and agent metadata are fully functional and unit-tested. The work has been reviewed and signed off by the Reviewer.

-   [ ] **Task ID: MEMOS-P1-T3**
    -   **Description**: Implement the **Pluggable Storage Backend - Tier 3 & 4** (Qdrant & Neo4j).
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Execute all technical aspects of the task as described. Upon completion, submit the work and a brief implementation report to the Reviewer.
    -   **Reviewer**: Qwen
        -   **Role**: Awaiting the Implementer's submission. Upon receipt, conduct a formal review of the work against all "Done means Done" criteria. **Upon approval, the Reviewer must mark this task's checkbox as complete.**
    -   **Done means Done**: API endpoints for semantic search and relationship queries are functional and tested. The work has been reviewed and signed off by the Reviewer.

-   [ ] **Task ID: MEMOS-P1-OMEGA**
    -   **Description**: Perform an **Omega Ingest** of the final Phase 1 architecture, API documentation, and all MAR sign-off reports into the master knowledge graph.
    -   **Done means Done**: All Phase 1 artifacts are synthesized and accessible.

---

## Phase 2: Integrate the Orchestrator (Dagster)

-   [ ] **Task ID: MEMOS-P2-T1**
    -   **Description**: Initialize a new **Dagster** project and define `memOS.as` as a code location.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Execute all technical aspects of the task as described. Upon completion, submit the work and a brief implementation report to the Reviewer.
    -   **Reviewer**: Qwen
        -   **Role**: Awaiting the Implementer's submission. Upon receipt, conduct a formal review of the work against all "Done means Done" criteria. **Upon approval, the Reviewer must mark this task's checkbox as complete.**
    -   **Done means Done**: The Dagster UI is running and can successfully load the memOS repository. The work has been reviewed and signed off by the Reviewer.

-   [ ] **Task ID: MEMOS-P2-T2**
    -   **Description**: Define Dagster assets for key data entities within memOS and implement maintenance jobs.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Execute all technical aspects of the task as described. Upon completion, submit the work and a brief implementation report to the Reviewer.
    -   **Reviewer**: Qwen
        -   **Role**: Awaiting the Implementer's submission. Upon receipt, conduct a formal review of the work against all "Done means Done" criteria. **Upon approval, the Reviewer must mark this task's checkbox as complete.**
    -   **Done means Done**: Data assets are visible and jobs run successfully. The work has been reviewed and signed off by the Reviewer.

-   [ ] **Task ID: MEMOS-P2-OMEGA**
    -   **Description**: Perform an **Omega Ingest** of the Dagster project configuration and data asset catalog.
    -   **Done means Done**: All Phase 2 artifacts are synthesized and accessible.

---

## Phase 3: Deploy the Intelligence ("Workers" Layer)

-   [ ] **Task ID: MEMOS-P3-T1**
    -   **Description**: Scaffold the **Agent Swarm** project, implementing the core `AgentRole`, `AgentContext`, and `MCPAgent` classes.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Execute all technical aspects of the task as described. Upon completion, submit the work and a brief implementation report to the Reviewer.
    -   **Reviewer**: Qwen
        -   **Role**: Awaiting the Implementer's submission. Upon receipt, conduct a formal review of the work against all "Done means Done" criteria. **Upon approval, the Reviewer must mark this task's checkbox as complete.**
    -   **Done means Done**: A single `MCPAgent` can be initialized. The work has been reviewed and signed off by the Reviewer.

-   [ ] **Task ID: MEMOS-P3-T2**
    -   **Description**: Implement the `MCPAgentSwarm` class and integrate it with the `tools.as` service registry.
    -   **Implementer**: Gemini (CLI)
        -   **Role**: Execute all technical aspects of the task as described. Upon completion, submit the work and a brief implementation report to the Reviewer.
    -   **Reviewer**: Qwen
        -   **Role**: Awaiting the Implementer's submission. Upon receipt, conduct a formal review of the work against all "Done means Done" criteria. **Upon approval, the Reviewer must mark this task's checkbox as complete.**
    -   **Done means Done**: The `MCPAgentSwarm` can delegate a task to multiple agents. The work has been reviewed and signed off by the Reviewer.

-   [ ] **Task ID: MEMOS-P3-OMEGA**
    -   **Description**: Perform the final **Omega Ingest** of the agent swarm's design and all MAR sign-off reports.
    -   **Done means Done**: The completed memOS ecosystem is fully documented and verified in the master knowledge graph.