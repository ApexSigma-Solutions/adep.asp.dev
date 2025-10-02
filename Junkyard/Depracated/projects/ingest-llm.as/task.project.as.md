``` markdown
# Project Tasks: InGest-LLM.as

**Version:** 1.4

This file tracks the specific, atomic, and granular tasks for the current development cycle, derived from `plan.project.as.md`.

---

## Milestone 1: Foundational Service & HTTP Pipeline (COMPLETE)

*Tasks TASK-IG-01 to TASK-IG-07 are complete.*

---

## Milestone 2: Integration, Embedding & Advanced Ingestion (COMPLETE)

*Tasks TASK-IG-08 to TASK-IG-19 are complete.*

---

## Milestone 3: Repository & Advanced Ingestion (IN PROGRESS)

### Objective 4: Expand Ingestion Endpoints

- [x] **TASK-IG-20:** Design and implement the POST `/ingest/python-repo` endpoint.
- [ ] **TASK-IG-21:** Design and implement the POST `/ingest/url` endpoint.

---

## Milestone 4: Prompt Modernization & Automation (NEW)

### Objective 5: Prototype a POML-based Context Generator

- [ ] **TASK-IG-22:** Research and integrate the POML Python SDK (`pip install poml`) into the `pyproject.toml` dependencies.
- [ ] **TASK-IG-23:** Create the initial prompt component library directory at `/prompts/components/`.
- [ ] **TASK-IG-24:** Create the first set of reusable prompt components as `.poml` files (e.g., `mission_brief.poml`, `project_status.poml`, `critical_blocker.poml`).
- [ ] **TASK-IG-25:** Develop a new service/module responsible for reading the Master Knowledge Graph.
- [ ] **TASK-IG-26:** Implement the core logic to load a master POML template, inject the live data from the knowledge graph as variables, and render the final context string.
- [ ] **TASK-IG-27:** Write integration tests to validate that the dynamically generated context is correctly formatted and contains up-to-date information.

```