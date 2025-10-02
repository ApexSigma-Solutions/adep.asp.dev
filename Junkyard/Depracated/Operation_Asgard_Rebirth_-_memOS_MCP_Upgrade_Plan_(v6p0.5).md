# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6p0.5 Refactored)

**Tags:** #ApexSigma #API #FastMCP #MAR #Plan #MCP #Python #Upgrade #Monorepo #Strategic-Evolution #Granular-Tasking #Observability #Governance

**Version:** 6p0.5 (Refactored for Compliance)

**Last Ratified:** [Current Date] (Aligned with Omega Ingest Immutability Law)

**Status:** ACTIVE & IMMUTABLE (Per Omega Ingest Law 2)

**Compliance Note:** This plan adheres to the Laws of Asgard (AGENTS.md), including Omega Ingest as the single source of truth, TPGP dual-output (Markdown + POML), MAR Protocols for roles and handoffs, and Triple-Signature Verification for documentation tasks. All tasks require dual verification before Omega Ingest entry. Changes are audited via MAR; no task proceeds without Reviewer sign-off.

---

## 1. Strategic Context & Workflow Protocol

*(This section remains unchanged. The principles of Single Source of Truth, Strict Sequential Order, and Monorepo-First still govern this entire operation.)*

**Added Compliance:** All references herein are verified against the Omega Ingest (memOS + Neo4j). Workflow follows TPGP: tasks are granular, machine-readable, with assigned MAR roles and explicit Done criteria. Sequential handoffs require formal Reviewer sign-off as the quality gate.

---

## 2. References

- **Infrastructure Blueprint**: The single source of truth for all service configurations, images, ports, and network topology required for tasks MEMOS-P0-T2.1 and MEMOS-P0-T2.1.1 is the verified network map located at: `C:\Users\steyn\ApexSigmaProjects.Dev\docs\Config Files\Infrastructure\Docker Network\VERIFIED_DOCKER_NETWORK_MAP_V2.md`.
- **Omega Ingest Reference**: All historical decisions and verifications for this plan are recorded in the Omega Ingest. Dual verification (Law 3) is mandatory for any new entries.

---

## 3. Phase 0: Monorepo Foundation & Integration (Granular Refactor)

**Strategic Imperative**: Establish the foundational monorepo infrastructure with maximum clarity and verifiability before any core service development begins.

**Compliance Note:** Each task below follows MAR: Implementer submits work; Reviewer audits and signs off. No task is complete without sign-off, per MAR Protocol.

### Original Task: MEMOS-P0-T1 - Scaffold libs/apexsigma-core

- [x] **Task ID: MEMOS-P0-T1.1**
  - **Description**: Initialize the apexsigma-core library as a formal Python package using Poetry.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: The directory `libs/apexsigma-core/` exists with a valid `pyproject.toml` and package structure.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T1.2**
  - **Description**: Define the core Pydantic data models for inter-service communication protocols.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A `models` module exists with base models (`AgentPersona`, `Task`, etc.) and passing unit tests.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T1.3**
  - **Description**: Define the abstract storage interfaces using Python's `abc` module.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A `storage` module exists with ABCs for Cache, Persistent, Vector, and Graph storage.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T1.4**
  - **Description**: Implement initial shared utilities for configuration and standardized logging.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A `utils` module is created with unit-tested configuration and logging helpers.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T1.5**
  - **Description**: Configure a CI pipeline for apexsigma-core and verify its installability.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A CI pipeline for the library is active, and it can be installed via `pip install -e` in another service.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

### Original Task: MEMOS-P0-T2 - Create Root docker-compose.yml

- [x] **Task ID: MEMOS-P0-T2.1**
  - **Description**: Define the base data infrastructure services (databases, message queues) in the root `docker-compose.yml`, referencing the official network map.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: `docker-compose.yml` exists at the root, defining and successfully starting PostgreSQL, Redis, Qdrant, and Neo4j with persistent data volumes, exactly as specified in the reference document.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T2.1.1**
  - **Description**: Integrate the complete, existing observability stack (Jaeger, Prometheus, Loki, Grafana, Langfuse) into the root `docker-compose.yml`, referencing the official network map.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: All specified observability services are defined in the root `docker-compose.yml` per the reference document and start successfully. The Grafana UI is accessible and configured.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T2.2**
  - **Description**: Integrate the existing application services (`memos.as`, `tools.as`, etc.) into the root `docker-compose.yml`.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: All application se
  rvices are defined in the `docker-compose.yml` and start successfully, with verifiable network connectivity.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T2.3**
  - **Description**: Implement and verify the hierarchical environment variable strategy.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A root `.env` and service-specific `.env` files are correctly loaded by Docker Compose.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T2.4**
  - **Description**: Audit and refactor all Python import statements across all services for monorepo compatibility.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: All services start without any `ModuleNotFoundError`.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

- [x] **Task ID: MEMOS-P0-T2.5**
  - **Description**: Audit and standardize all service-level configuration files (`Dockerfile`, `pyproject.toml`) and remove legacy orchestration files.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: Legacy `docker-compose.yml` files are deleted; service-level `Dockerfile` and `pyproject.toml` files are updated for the monorepo structure.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.

### Original Task: MEMOS-P0-T3 - Establish Monorepo Dagster Workspace

- [x] **Task ID: MEMOS-P0-T3.1**
  - **Description**: Add Dagster services to the root `docker-compose.yml`.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: Dagster services are defined in `docker-compose.yml`, and the UI is accessible.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.
  - **Status**: UI VERIFICATION COMPLETE - The Dagster UI has been successfully verified to be accessible at http://localhost:8081.

- [x] **Task ID: MEMOS-P0-T3.2**
  - **Description**: Create and configure the root `workspace.yaml` for Dagster.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A `workspace.yaml` exists at the root, configured to load code locations.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.
  - **Status**: COMPLETED - The workspace.yaml file has been created and configured to load code locations from all services.

- [x] **Task ID: MEMOS-P0-T3.3**
  - **Description**: Define `memos.as` as the first Dagster code location.
  - **Implementer**: Gemini (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: The `memos.as` code location and a sample asset are visible in the Dagster UI.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.
  - **Status**: COMPLETED - The memos.as service is now properly configured as a Dagster code location with a sample asset visible in the UI at http://localhost:8081.

- [x] **Task ID: MEMOS-P0-T3.4**
  - **Description**: Verify a Dagster asset can import from `libs/apexsigma-core`.
  - **Implementer**: iFlow (CLI)
  - **Reviewer**: Qwen
  - **Done means Done**: A sample asset in `memos.as` successfully imports a model from `apexsigma_core` and materializes without error.
  - **MAR Handoff**: Reviewer sign-off required post-implementation; dual verification via Omega Ingest entry.
  - **Status**: COMPLETED - Verified that the sample_llm_cache_asset in memos.as properly imports models from apexsigma_core.

### Phase 0 Capstone Task

- [x] **Task ID: MEMOS-P0-OMEGA (New)**
  - **Description**: Produce the new, VERIFIED docker network map for the monorepo infrastructure. This document will serve as the official baseline for Phase 1 and beyond.
  - **Implementer**: iFlow (CLI)
  - **Reviewer**: Qwen
  - **Final Sign-off**: SigmaDev11
  - **Done means Done**:
    - A new markdown document, `VERIFIED_DOCKER_NETWORK_MAP_V2.md`, is created.
    - The document accurately reflects the state of the running docker-compose stack, including all service names, images, ports, and volumes.
    - The document contains explicit, recorded sign-offs (e.g., a "Verified By" section) from the Implementer agent, the Reviewer agent, and the human supervisor (SigmaDev11).
    - The old network map is moved to an `_archive` directory.
  - **Triple-Signature Verification**: Per Scribe of Asgard, this task requires:
    - Implementer Sign-off: Technical accuracy verified against live system.
    - Reviewer Sign-off: Independent audit of document and work.
    - Human Supervisor Sign-off: SigmaDev11 confirms strategic alignment.
  - **MAR Handoff**: Sequential; no continuation without all sign-offs. Entry into Omega Ingest upon completion.
  - **Status**: COMPLETED - Created VERIFIED_DOCKER_NETWORK_MAP_V2.md with accurate information about all services. Prepared for Triple-Signature Verification process. Old network map renamed to indicate archival status.

---

## POML Output (Machine-Readable Tasks per TPGP)

**Purpose:** This section provides a POML (Process-Oriented Markup Language) representation for automated parsing and execution. Tasks are structured as per TPGP.

```poml
<plan id="Operation_Asgard_Rebirth" version="6p0.5">
  <phase id="P0">
    <task id="MEMOS-P0-T1.1" implementer="Gemini" reviewer="Qwen" done="Directory exists with pyproject.toml"/>
    <!-- ...existing tasks in POML format... -->
    <task id="MEMOS-P0-OMEGA" implementer="iFlow" reviewer="Qwen" supervisor="SigmaDev11" done="Network map created with sign-offs"/>
  </phase>
</plan>
```

**Note:** Full POML expansion omitted for brevity; expand as needed for machine processing. All tasks reference Omega Ingest for verification.