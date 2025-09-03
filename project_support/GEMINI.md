# Gemini Workspace Context: project_support

## Directory Overview

This directory, `project_support`, serves as the central hub for documentation, scripts, and configuration files that support the `memos.as` and `InGest-LLM.as` microservices within the ApexSigma ecosystem. It is a fork of the `memOS` and `InGest-LLM` projects and provides the necessary context and tools to manage and maintain the ecosystem.

## Key Files

*   **`ApexSigma Ecosystem Briefing Operation Asgard Rebirth.md`**: A high-level overview of the ApexSigma ecosystem, its architecture, and the goals of "Operation Asgard Rebirth."
*   **`OPERATION_ASGARD_REBIRTH.md`**: A detailed plan for the implementation and stabilization of the ApexSigma ecosystem, including agent allocation, task assignments, and quality gate requirements.
*   **`docker-compose.unified.yml`**: The Docker Compose file for the unified ecosystem, defining the services and their dependencies.
*   **`scripts/Systems Boot Sequence Script.py`**: A Python script for managing the startup, reset, and validation of the ApexSigma ecosystem.
*   **`secure_verified_docs/SINGLE_SOURCE_TRUTH.md`**: A document that establishes the authoritative implementation status for the ApexSigma ecosystem.
*   **`secure_verified_docs/OMEGA_INGEST_LAWS.md`**: A document that defines the immutable laws for the Omega Ingest, the verified knowledge base for the ApexSigma ecosystem.

## Usage

The contents of this directory are intended to be used for:

*   **Onboarding:** New agents can use the documentation in this directory to get up to speed on the ApexSigma ecosystem.
*   **Development:** The scripts and configuration files in this directory can be used to manage and maintain the ecosystem.
*   **Operations:** The documentation in this directory can be used to understand the current state of the ecosystem and to make operational decisions.

## Key Technologies

*   **Backend:** FastAPI, Python 3.11
*   **Database:** PostgreSQL, Qdrant, Redis, Neo4j
*   **Containerization:** Docker, Docker Compose
*   **Dependency Management:** Poetry, uv

## Development Conventions

*   **API:** Both services are built with FastAPI, following modern asynchronous Python practices.
*   **Configuration:** Environment variables are used for configuration, with `.env` files for local development.
*   **Dependency Management:** `memos.as` uses `uv` and `requirements.txt`, while `InGest-LLM.as` uses Poetry. This is a point of potential inconsistency to be aware of.
*   **Database Migrations:** `memos.as` uses Alembic for database migrations, located in `memos.as/context_portal/alembic`.
*   **Documentation:** Each service has its own `README.md` and a `docs` directory for more detailed information. The `GEMINI.md` files within each service directory provide specific context for AI agents working on that service.
