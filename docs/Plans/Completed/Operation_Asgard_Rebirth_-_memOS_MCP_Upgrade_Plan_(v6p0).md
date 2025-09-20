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

### Phase 0: Monorepo Foundation & Integration

**Strategic Imperative**: Before implementing any core memOS functionality, we must first establish the foundational monorepo infrastructure. This phase is non-negotiable and all subsequent phases depend on its successful completion.

*   [ ] **Task ID: MEMOS-P0-T1**
  * **Description**: Scaffold the `libs/apexsigma-core` shared library. This package will house all common code: Pydantic models for MCP protocols, unified storage backend interfaces (abstract base classes), protocol enums, database connectors, and shared utilities for observability and configuration.
  * **Implementer**: Gemini (CLI)
  * **Reviewer**: Qwen
  * **Done means Done**:
    * `libs/apexsigma-core` package exists with a `pyproject.toml`.
    * Abstract base classes for all planned storage backends are defined.
    * The package can be installed as an editable dependency (`pip install -e libs/apexsigma-core`) in any service.
    * The CI pipeline successfully builds and runs unit tests on the shared library.

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
  * **Description**: Establish a monorepo-wide Dagster workspace at the repository root, with individual services defined as code locations.
  * **Implementer**: Gemini (CLI)
  * **Reviewer**: Qwen
  * **Done means Done**:
    * A root `workspace.yaml` is configured with `services/memos.as` (and others) as code locations.
    * The Dagster UI loads successfully and displays the unified workspace.
    * Shared asset definitions can be imported from `libs/apexsigma-core`.
    * The Dagster daemon and UI run as services in the root `docker-compose.yml`.