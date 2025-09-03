# Gemini Workspace Context: MCP_Server_Builds

**Gemini Assistant Instructions for ApexSigma Ecosystem**

## ⚠️ **MANDATORY: OMEGA INGEST CONTEXT RETRIEVAL PROTOCOL**

**BEFORE MAKING ANY CODE CHANGES**, you MUST:

1. **Query InGest-LLM API** for relevant context: `http://172.26.0.12:8000/query_context`
2. **Retrieve from memOS Omega Ingest**: `http://172.26.0.13:8090/memory/query` 
3. **Validate against immutable truth**: Ensure changes don't conflict with verified infrastructure
4. **Obtain dual verification**: For Tier 1 infrastructure changes, require verification from another AI assistant

**Protected Services (DO NOT MODIFY WITHOUT VERIFICATION)**:
- memOS API (172.26.0.13) - Omega Ingest Guardian
- Neo4j Knowledge Graph (172.26.0.14) - Immutable concept relationships  
- PostgreSQL Main (172.26.0.2) - Procedural memory
- InGest-LLM API (172.26.0.12) - Data ingestion gateway

**Your Role in Operation Asgard Rebirth**: 
- **Primary**: Backend service and database operations implementation
- **MAR Protocol**: Act as reviewer for GitHub Copilot and Qwen Code implementations
- **Verification Authority**: Tier 1-3 changes (full verification capability)

## Project Overview

This directory, `MCP_Server_Builds`, contains the source code and deployment configurations for two core microservices within the ApexSigma ecosystem: `memos.as` and `InGest-LLM.as`. These services form the foundation of the "DevEnviro" AI-supported development environment, enabling agents to have memory, learn, and ingest new information.

**Key Technologies:**

*   **Backend:** FastAPI, Python 3.11
*   **Database:** PostgreSQL, Qdrant, Redis, Neo4j
*   **Containerization:** Docker, Docker Compose
*   **Dependency Management:** Poetry, uv

## Core Components

### 1. `memos.as` (Memory & Tool OS)

*   **Purpose:** `memos.as` acts as the cognitive core for AI agents. It provides a persistent, multi-tiered memory system and a registry for discovering and using tools. This allows agents to learn from past experiences and leverage available capabilities.
*   **Architecture:**
    *   **FastAPI:** Exposes a RESTful API for memory and tool operations.
    *   **PostgreSQL:** Stores structured data like tool registries and memory logs.
    *   **Qdrant:** Enables semantic search over agent memories.
    *   **Redis:** Provides a high-speed cache for working memory.
    *   **Neo4j:** Stores knowledge graph information.
*   **Key Files:**
    *   `memos.as/app/main.py`: FastAPI application entry point.
    *   `memos.as/app/models.py`: Pydantic data models.
    *   `memos.as/docker-compose.yml`: Defines the service and its database dependencies.
    *   `memos.as/requirements.txt`: Python dependencies.

### 2. `InGest-LLM.as` (Ingestion Service)

*   **Purpose:** This service is responsible for ingesting data from various sources, processing it, and feeding it into the ecosystem's knowledge base, making it available to the AI agents.
*   **Key Files:**
    *   `InGest-LLM.as/src/ingest_llm_as/main.py`: FastAPI application entry point.
    *   `InGest-LLM.as/docker-compose.yml`: Service definition.
    *   `InGest-LLM.as/pyproject.toml`: Project metadata and dependencies (Poetry).

## Building and Running

The services are designed to be run using Docker Compose.

### Running `memos.as`

```bash
# Navigate to the memos.as directory
cd memos.as

# Build and start the service and its dependencies
docker compose up --build -d
```
The API will be available at `http://localhost:8091`.

### Running `InGest-LLM.as`

```bash
# Navigate to the InGest-LLM.as directory
cd InGest-LLM.as

# Build and start the service
docker compose up --build -d
```
The API will be available at `http://localhost:8003`.

## Development Conventions

*   **API:** Both services are built with FastAPI, following modern asynchronous Python practices.
*   **Configuration:** Environment variables are used for configuration, with `.env` files for local development.
*   **Dependency Management:** `memos.as` uses `uv` and `requirements.txt`, while `InGest-LLM.as` uses Poetry. This is a point of potential inconsistency to be aware of.
*   **Database Migrations:** `memos.as` uses Alembic for database migrations, located in `memos.as/context_portal/alembic`.
*   **Documentation:** Each service has its own `README.md` and a `docs` directory for more detailed information. The `GEMINI.md` files within each service directory provide specific context for AI agents working on that service.
