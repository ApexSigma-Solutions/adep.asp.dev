---
taskTITLE: Fix Application Service Dependencies
taskID: OVS-WO-001
taskplanID: '20250928'
status: Active
priority: Critical
implementer: '"@iFlow"'
reviewer: '"@Qwen"'
tags:
    - TaskWO
    - stabilization
    - blocker
aliases:
    - '"Fix Missing Dependencies"'
---

# Task Work Order: OVS-WO-001 - Fix Application Service Dependencies

## 1. Summary

Restore core application services (`memos.as` & `devenviro.as`) to an operational state by identifying and adding all missing Python dependencies to their respective `pyproject.toml` files.

## 2. Background & Strategic Context

This is the primary blocker for the entire ecosystem, as identified in the `INFRASTRUCTURE_VERIFICATION_REPORT.md`. Core services are failing to start with `ModuleNotFoundError`, preventing any further testing or development. This is the first and most critical action of Phase 0 Stabilization.

## 3. "Done Means Done" Criteria

> This is the contract. A non-negotiable, verifiable checklist of what must be true for the work to be considered complete.

- [x] **Criterion 1:** The `memos.as` service starts successfully without any `ModuleNotFoundError` exceptions in its logs. ✅ 2025-10-02
- [x] **Criterion 2:** The `devenviro.as` service starts successfully without any `ModuleNotFoundError` exceptions in its logs. [completion:: 2025-10-02]
- [x] **Criterion 3:** The `pyproject.toml` and `poetry.lock` files for `memos.as` and `devenviro.as` are correctly updated with all required dependencies (`langfuse`, `qdrant-client`, `structlog`, etc.) and committed to the repository. [completion:: 2025-10-02]
- [x] **Valhalla Shield Compliance:** The final Pull Request MUST pass all checks in the [[PR Checklist as per Valhalla Shield Engineering Standard]]. [completion:: 2025-10-02]

## 4. Dependencies

- [x] N/A [completion:: 2025-09-28]
