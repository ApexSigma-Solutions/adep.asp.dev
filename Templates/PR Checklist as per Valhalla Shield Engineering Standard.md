---
title: PR Checklist as per Valhalla Shield Engineering Standard
Version: "1.3"
tags:
  - Quality_Standard
  - valhalla-shield
  - Checklist
  - Audit
  - ApexSigma
  - PR
noteTYPE: prCHECKLIST
date created: <% tp.date.now("YYYYMMDD") %>
date modified:
---
# PR Checklist: Valhalla Shield Engineering Standard v1.3

**Instructions:** This checklist and the traceability block MUST be included in the body of every Pull Request. Every item must be filled out and checked ✅ for the PR to be eligible for review.

### **Traceability & Context**

> This block provides the unbroken lineage from strategic objective to this specific implementation. It is mandatory for audit and automation.

- **Pull Request UUID:** `[A unique UUID generated for this PR]`
    
- **Date Created:** `[YYYY-MM-DDTHH:MM:SSZ]`
    
- **Parent Plan:** `[Link to the Master Plan, Roadmap, or Operation Document]`
    
- **Work Order / Task ID:** `[Link to the specific Task Work Order in Obsidian]`
    
- **Linear Issue ID:** `[e.g., OVS-01]`
    

### Category 1: Repository & Environment

- [ ] **Standard Structure:** `.vscode/`, `.github/`, `.gitignore`, `.dockerignore`, and `Dockerfile` are present and correct.
    
- [ ] **Environment Management:** Python version is managed by `pyenv`. All configuration is loaded from `.env` via Pydantic `BaseSettings`. A `.env.template` exists. No secrets are committed.
    
- [ ] **Code Hygiene:** Repo is clean of unnecessary files, scripts, and commented-out code.
    

### Category 2: Deployment & Configuration

- [ ] **Containerization:** The service is containerized in a lean, multi-stage `Dockerfile`.
    
- [ ] **Scripted Launch:** A `run.sh` script provides a single command for a clean build and run (`docker compose up --build`).
    

### Category 3: Architecture & Dependencies

- [ ] **Statelessness:** The service is stateless. Persistent data uses an external Docker Volume.
    
- [ ] **Dependency Management:** All dependencies are managed by `Poetry`. `pyproject.toml` and `poetry.lock` are committed.
    
- [ ] **Health Check:** A `/health` endpoint is exposed and functioning.
    

### Category 4: Code Quality & Automation

- [ ] **Formatting:** Codebase is 100% formatted with `black`. (`poetry run format` produces no changes).
    
- [ ] **Linting:** Codebase is 100% free of linting errors according to `Ruff`. (`poetry run lint` produces no errors).
    

### Category 5: Testing & Validation

- [ ] **Test Suite & Pass Rate:** A `tests/` directory exists. The `pytest` suite has a 100% pass rate.
    
- [ ] **Test Coverage:** The test suite achieves >= 85% code coverage.
    
- [ ] **API Testing:** All API endpoints are tested with mock calls.
    

### Category 6: Observability & Monitoring

- [ ] **Structured Logging:** Service outputs structured (JSON) logs to `stdout`.
    
- [ ] **Traceability:** Service is instrumented with OpenTelemetry, exporting to Langfuse and Jaeger.
    
- [ ] **Metrics Exposition:** A `/metrics` endpoint is exposed in Prometheus format.
    

### Category 7: Documentation & Maintainability

- [ ] **API Documentation:** A Swagger/OpenAPI specification is available and up-to-date.
    
- [ ] **Code Documentation:** All public functions, classes, and modules have clear docstrings.
    
- [ ] **Comprehensive README:** The `README.md` is fully updated with purpose, setup, config, and run instructions.