# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6p0.5 Refactored)

**Tags:** [[ApexSigma]] [[API]] [[FastMCP]] [[MAR]] [[Plan]] [[MCP]] [[Python]] [[Upgrade]] [[Monorepo]] [[Strategic-Evolution]] [[Granular-Tasking]] [[Observability]] [[Governance]]

---

## 1. Strategic Context & Workflow Protocol

*(This section remains unchanged. The principles of Single Source of Truth, Strict Sequential Order, and Monorepo-First still govern this entire operation.)*

---

## 2. References

- **Infrastructure Blueprint**: The single source of truth for all service configurations, images, ports, and network topology required for tasks MEMOS-P0-T2.1 and MEMOS-P0-T2.1.1 is the verified network map located at: `C:\Users\steyn\ApexSigmaProjects.Dev\docs\Config Files\Infrastructure\Docker Network\VERIFIED_DOCKER_NETWORK_MAP.md`.

---

## 3. Phase 0: Monorepo Foundation & Integration (Granular Refactor)

**Strategic Imperative**: Establish the foundational monorepo infrastructure with maximum clarity and verifiability before any core service development begins.

### Original Task: MEMOS-P0-T1 - Scaffold libs/apexsigma-core

- [ ] **Task ID: MEMOS-P0-T1.1**
  - **Description**: Initialize the apexsigma-core library as a formal Python package using Poetry.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: The directory `libs/apexsigma-core/` exists with a valid `pyproject.toml` and package structure.

- [ ] **Task ID: MEMOS-P0-T1.2**
  - **Description**: Define the core Pydantic data models for inter-service communication protocols.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A `models` module exists with base models (`AgentPersona`, `Task`, etc.) and passing unit tests.

- [ ] **Task ID: MEMOS-P0-T1.3**
  - **Description**: Define the abstract storage interfaces using Python's `abc` module.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A `storage` module exists with ABCs for Cache, Persistent, Vector, and Graph storage.

- [ ] **Task ID: MEMOS-P0-T1.4**
  - **Description**: Implement initial shared utilities for configuration and standardized logging.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A `utils` module is created with unit-tested configuration and logging helpers.

- [ ] **Task ID: MEMOS-P0-T1.5**
  - **Description**: Configure a CI pipeline for apexsigma-core and verify its installability.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A CI pipeline for the library is active, and it can be installed via `pip install -e` in another service.

### Original Task: MEMOS-P0-T2 - Create Root docker-compose.yml

- [ ] **Task ID: MEMOS-P0-T2.1**
  - **Description**: Define the base data infrastructure services (databases, message queues) in the root `docker-compose.yml`, referencing the official network map.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: `docker-compose.yml` exists at the root, defining and successfully starting PostgreSQL, Redis, Qdrant, and Neo4j with persistent data volumes, exactly as specified in the reference document.

- [ ] **Task ID: MEMOS-P0-T2.1.1**
  - **Description**: Integrate the complete, existing observability stack (Jaeger, Prometheus, Loki, Grafana, Langfuse) into the root `docker-compose.yml`, referencing the official network map.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: All specified observability services are defined in the root `docker-compose.yml` per the reference document and start successfully. The Grafana UI is accessible and configured.

- [ ] **Task ID: MEMOS-P0-T2.2**
  - **Description**: Integrate the existing application services (`memos.as`, `tools.as`, etc.) into the root `docker-compose.yml`.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: All application services are defined in the `docker-compose.yml` and start successfully, with verifiable network connectivity.

- [ ] **Task ID: MEMOS-P0-T2.3**
  - **Description**: Implement and verify the hierarchical environment variable strategy.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A root `.env` and service-specific `.env` files are correctly loaded by Docker Compose.

- [ ] **Task ID: MEMOS-P0-T2.4**
  - **Description**: Audit and refactor all Python import statements across all services for monorepo compatibility.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: All services start without any `ModuleNotFoundError`.

- [ ] **Task ID: MEMOS-P0-T2.5**
  - **Description**: Audit and standardize all service-level configuration files (`Dockerfile`, `pyproject.toml`) and remove legacy orchestration files.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: Legacy `docker-compose.yml` files are deleted; service-level `Dockerfile` and `pyproject.toml` files are updated for the monorepo structure.

### Original Task: MEMOS-P0-T3 - Establish Monorepo Dagster Workspace

- [ ] **Task ID: MEMOS-P0-T3.1**
  - **Description**: Add Dagster services to the root `docker-compose.yml`.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: Dagster services are defined in `docker-compose.yml`, and the UI is accessible.

- [ ] **Task ID: MEMOS-P0-T3.2**
  - **Description**: Create and configure the root `workspace.yaml` for Dagster.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A `workspace.yaml` exists at the root, configured to load code locations.

- [ ] **Task ID: MEMOS-P0-T3.3**
  - **Description**: Define `memos.as` as the first Dagster code location.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: The `memos.as` code location and a sample asset are visible in the Dagster UI.

- [ ] **Task ID: MEMOS-P0-T3.4**
  - **Description**: Verify a Dagster asset can import from `libs/apexsigma-core`.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A sample asset in `memos.as` successfully imports a model from `apexsigma_core` and materializes without error.

### Phase 0 Capstone Task

- [ ] **Task ID: MEMOS-P0-OMEGA (New)**
  - **Description**: Produce the new, VERIFIED docker network map for the monorepo infrastructure. This document will serve as the official baseline for Phase 1 and beyond.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Final Sign-off**: SigmaDev11
  - **Done means Done**:
    - A new markdown document, `VERIFIED_DOCKER_NETWORK_MAP_V2.md`, is created.
    - The document accurately reflects the state of the running docker-compose stack, including all service names, images, ports, and volumes.
    - The document contains explicit, recorded sign-offs (e.g., a "Verified By" section) from the Implementer agent, the Reviewer agent, and the human supervisor (SigmaDev11).
    - The old network map is moved to an `_archive` directory.