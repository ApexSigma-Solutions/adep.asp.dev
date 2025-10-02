Protocols & Laws\Apex Sigma Docker Network Convention.md
```md
---
title: Apex Sigma Docker Network Convention
aliases:
  - docker.net.instruct.as
tags:
  - ApexSigma
  - Docker
  - Network
  - standardization
  - convention
  - container
---
```markdown
# Guide: Docker Network Configuration for ApexSigma

This is a step-by-step manual for configuring the `docker-compose.yml` file to ensure all 13 containers can communicate correctly, both internally and with the host machine.

## Communication Flow Diagram

This diagram illustrates how the services communicate over the shared `apexsigma_net` Docker network.

```mermaid
graph TD
    subgraph External Access
        Developer/User -->|HTTP API Calls| Memos_API[memos.as];
        Developer/User -->|HTTP API Calls| Ingest_API[ingest-llm.as];
        Developer/User -->|Web UI on Port 3000| Grafana;
    end

    subgraph "ApexSigma Docker Network (apexsigma_net)"
        subgraph Core Services
            Memos_API -->|Reads/Writes Data| Postgres_Memos[PostgreSQL for memOS];
            Memos_API -->|Caches Data| Redis_Memos[Redis for memOS];
            Memos_API -->|Pub/Sub Events| RabbitMQ;
            Ingest_API -->|Sends Tasks| RabbitMQ;
        end

        subgraph Dependency Services
            Postgres_Memos;
            Redis_Memos;
            RabbitMQ;
            Qdrant;
            Postgres_Langfuse[PostgreSQL for Langfuse];
            Redis_Langfuse[Redis for Langfuse];
            Langfuse_Server[Langfuse Server];
        end

        subgraph Observability Stack
            Prometheus -->|Scrapes Metrics| Memos_API;
            Prometheus -->|Scrapes Metrics| Ingest_API;
            Loki -->|Collects Logs| Memos_API;
            Jaeger -->|Collects Traces| Memos_API;
            Grafana -->|Queries Data| Prometheus;
            Grafana -->|Queries Logs| Loki;
            Grafana -->|Queries Traces| Jaeger;
        end

        %% Connections
        Memos_API --> Qdrant;
        Ingest_API --> Qdrant;
        Langfuse_Server --> Postgres_Langfuse;
        Langfuse_Server --> Redis_Langfuse;
    end

    style Developer/User fill:#f9f,stroke:#333,stroke-width:2px

```

## Step 1: Define a Custom Network

First, create a custom **bridge network** to provide better isolation and allow containers to resolve each other by name. Add this block at the very end of your `docker-compose.yml` file:

```yaml
networks:
  apexsigma_net:
    driver: bridge

```

## Step 2: Assign All Services to the Custom Network

For **every service** defined in your `docker-compose.yml` file, you must tell it to connect to the `apexsigma_net`.

**Example (memos-api service):**

```yaml
services:
  memos-api:
    image: memos-api-image:latest
    container_name: memos-api
    # ... other configurations like environment variables ...
    networks:
      - apexsigma_net

```

**Instruction:** Apply this `networks` block to all 13 services.

## Step 3: Internal Communication (Container-to-Container)

Once on the same network, services communicate using their **service name as the hostname**.

Example:

The `memos-api` service needs to connect to its PostgreSQL database, which is named `postgres-memos` in `docker-compose.yml`.

  * **Service Name:** `postgres-memos`
  * **Database Port (internal):** `5432`
  * **Connection String:** `postgresql://user:password@postgres-memos:5432/memos_db`

Docker's internal DNS will automatically resolve `postgres-memos` to the correct container's internal IP address. **Do not use `localhost` or an IP address for inter-service communication.**

## Step 4: External Access (Connecting from Your Machine)

To access a container from your host machine (e.g., browser, Postman), you must map a port from the container to your host using the `ports` directive in the format `"HOST_PORT:CONTAINER_PORT"`.

Example (memos-api service):

The API runs on port `8000` inside its container. To access it from your computer, map it to a port on your host, like `8001`.

```yaml
services:
  memos-api:
    # ... other configurations ...
    ports:
      - "8001:8000" # Exposes container port 8000 on host port 8001
    networks:
      - apexsigma_net

```

**Instruction:** Now, to send a request to the API from your machine, you would use `http://localhost:8001`.

Apply this logic to any service that needs external access:

  * **Grafana:** map to `3000:3000` to access the UI at `http://localhost:3000`.
  * **Langfuse:** map to `3300:3000` to access its UI at `http://localhost:3300`.

<!-- end list -->

``` 
 
```

```

Protocols & Laws\apexsigma.glossary.as.md
```md
# The ApexSigma Glossary (v1.1)

This document serves as the master glossary for all terms, protocols, and concepts used within the ApexSigma ecosystem.

## A

### Agent
- An autonomous or semi-autonomous entity, typically powered by an LLM, designed to perform specific tasks or roles within the ApexSigma Ecosystem. Examples include [[Gemini (CLI)]] and [[Qwen]].

### ApexSigma Ecosystem
- The integrated environment of agents, protocols, services, and architectural components governed by ApexSigma Solutions. It is designed for the collaborative and autonomous execution of complex technical projects.

### ApexSigma Solutions
- The technical software development organization founded by Sean Steyn (SigmaDev11). Its goal is to solve real-world problems by combining human creativity with AI technology.

## D

### Dagster
- The designated data orchestrator used for the 'Orchestrator' layer in the [[Three-Layer Architecture]]. It is responsible for scheduling, executing, and monitoring the workflows of the agent swarm.

### Dual Verification Requirement
- A core tenet of the [[Omega Ingest Laws]] mandating that any new information must be independently verified by at least two separate sources or agents before it can be committed to the master knowledge graph.

## F

### FastMCP 2.0
- The FastAPI-based framework used to build high-performance, concurrent agentic services like [[memOS.as]].

## G

### Gemini (CLI)
- The designated AI Implementer agent, responsible for executing technical tasks such as coding, scaffolding, and deployment.

## I

### Implementer
- A designated role for an agent responsible for executing the technical development of a task, such as writing code or configuring infrastructure. The primary implementer is currently [[Gemini (CLI)]].

## K

### Knowledge Graph
- The central, structured repository of interconnected data and concepts within the ecosystem. It serves as the long-term, episodic memory for the [[Society of Agents]] and is governed by the [[Omega Ingest Laws]].

## M

### MAR Implementation Report
- A standardized document submitted by the **Implementer** to formally hand off a completed task for review. It details the work done and links to all relevant artifacts.

### MAR (Mandatory Agent Review) Protocol
- The mandatory quality gatekeeper workflow. It requires a designated **Reviewer** agent to formally approve or reject the work of an **Implementer** before a task can be considered complete.

### MAR Review Report
- A standardized document completed by the **Reviewer** that provides the official outcome (APPROVED or REJECTED) of a MAR check, including feedback and required revisions.

### memOS.as
- The core memory service of the ecosystem. It provides a multi-tiered, pluggable storage architecture for agents, enabling short-term, long-term, semantic, and episodic memory.

## O

### Omega Ingest Laws
- The immutable principles governing the master knowledge graph. Key tenets include the principles of a Single Source of Truth, Immutability of Verified Data, and a mandatory Dual Verification Requirement for all new entries.

### Operation Asgard Rebirth
- The active, ecosystem-wide operation to correct discrepancies between documented designs and the actual implementation state. Its primary goal is to bring all services to a fully operational and verified status.

### Orchestrator Layer
- The top layer of the [[Three-Layer Architecture]], responsible for managing and coordinating the 'Workers' layer. It handles workflow scheduling, execution, and monitoring, with [[Dagster]] as the primary tool.

## P

### Pluggable Storage Architecture
- The four-tier storage design for [[memOS.as]], consisting of Redis (cache), PostgreSQL (metadata), Qdrant (semantic recall), and Neo4j (episodic memory).

### POML (Prompt Orchestration Markup Language)
- The mandated standard for formatting knowledge components to ensure efficient and targeted tokenization for LLMs interacting with the knowledge graph.

### Product Requirements Document (prd.txt)
- The standardized input document for the [[TaskMaster MCP Framework]]. It outlines the goals, scope, requirements, and constraints of a project, serving as the primary directive for the executing agent.

## Q

### Qwen
- The designated AI Reviewer agent, responsible for conducting the **MAR Protocol** checks on work submitted by the Implementer.

## R

### Reviewer
- A designated role for an agent responsible for quality assurance and adherence to protocols. It formally assesses the work of an [[Implementer]] according to the [[MAR (Mandatory Agent Review) Protocol]]. The primary reviewer is currently [[Qwen]].

## S

### Society of Agents
- The collaborative structure of specialized agents (e.g., Gemini, Qwen) that work together to execute complex projects within the ecosystem.

### Single Source of Truth (SST)
- A thorough report of the whole ApexSigma EcoSystem, performed monthly at minimum or after all major changes. This is a full audit on the current state of the ecosystem. This report must comply with the Omega Ingest Laws, and MAR protocol.

## T

### TaskMaster MCP Framework
- An autonomous agent framework that orchestrates an LLM's execution based on a structured Product Requirements Document (prd.txt). It ensures strict alignment between a project's goals and the agent's actions.

### Three-Layer Architecture
- The strategic architectural model for the evolved [[memOS.as]] ecosystem. It consists of a 'Tools' layer (the core memOS API), a 'Workers' layer (the agent swarm), and an 'Orchestrator' layer (Dagster).

### Tools Layer
- The foundational layer of the [[Three-Layer Architecture]], providing the core services and APIs that agents in the 'Workers' layer use to perform their tasks. This layer is primarily composed of [[memOS.as]].

## V

### Vulcan Protocol
- The Vulcan Protocol governs the process of assigning a single development task to two or more independent AI implementation agents (e.g., Gemini (CLI), Qwen Code) for the purpose of generating competing solutions. The goal is to identify the objectively superior implementation through a structured, data-driven comparison, thereby increasing code quality, fostering innovation, and providing operational resilience.

## W

### Workers Layer
- The middle layer of the [[Three-Layer Architecture]], consisting of the [[Society of Agents]] (the "agent swarm"). These agents consume services from the 'Tools' layer to execute tasks assigned by the 'Orchestrator' layer.
```

Protocols & Laws\Valhalla Shield Engineering Standard v1.2.md
```md
---
date created: 267,24O September9 2025 12:59 am
date modified: 267,24O September9 2025 01:02 am
tags:
  - engineering-standard
  - valhalla-shield
  - done-means-done
  - software-development
aliases:
  - '"Valhalla Shield Standard", "Done Means Done"'
---
# Valhalla Shield Engineering Standard v1.2

## "Done Means Done" Criteria (The Canonical Standard)"
  
This document defines the complete, non-negotiable standard for a service to be considered "Done". It incorporates the [[Minimum Mandatory Setup]], providing specific tool and process requirements.

-----

### Category 1: Repository & Environment

1. **Standard Structure:** The repository root must contain a properly populated and linted `.vscode/`, `.github/`, `.gitignore`, `.dockerignore`, and `Dockerfile`.
2. **Environment Management:** [[Python]] versioning must be managed by [[pyenv]]. Application configuration must be managed by a `.env.template` file and loaded via [[Pydantic BaseSettings]]. No secrets in the repo.
3. **Code Hygiene:** The repository must be cleaned of all unnecessary or invalid scripts, markdown documents, and outdated tests before work begins.

### Category 2: Deployment & Configuration

1. **Containerization:** The service is fully containerized in a lean, multi-stage [[Dockerfile]].
2. **Scripted Launch:** A `run.sh` script provides a single, reliable command for a clean build and run.

### Category 3: Architecture & Dependencies

1. **Statelessness:** The service is [[Statelessness|stateless]]. All persistent data must be stored on an external [[Docker Volume]].
2. **Dependency Management:** Dependencies are exclusively managed by [[Poetry]], with a committed `pyproject.toml` and `poetry.lock` file.
3. **Health Check:** A `/health` endpoint is exposed for basic [[Liveness Checks]].

### Category 4: Code Quality & Automation

1. **Formatting:** Codebase is formatted with [[Black (formatter)|black]].
2. **Linting:** Codebase is linted with [[Ruff (linter)|ruff]].
3. **Automation:** `pyproject.toml` is configured with `poetry run format` and `poetry run lint` commands.

### Category 5: Testing & Validation

1. **Test Suite & Pass Rate:** A `tests/` directory exists with a [[pytest]] suite. The command `poetry run pytest` must have a 100% pass rate.
2. **Test Coverage:** The test suite must achieve a minimum of 85% code coverage, verified using [[pytest-cov]].
3. **API Testing:** All [[API Endpoints]] must be thoroughly tested using mock API calls.

### Category 6: Observability & Monitoring

1. **Structured Logging:** The service must output structured ([[JSON]]) logs to `stdout`.
2. **Traceability:** The service must be instrumented for end-to-end traceability using [[OpenTelemetry]], exporting to **[[Langfuse]]** and **[[Jaeger]]**.
3. **Metrics Exposition:** The service must expose a `/metrics` endpoint with fine-grained metrics in the **[[Prometheus]]** exposition format.

### Category 7: Documentation & Maintainability

1. **Automated Documentation:** Project documentation is generated automatically using **[[MKDocs]]** from code docstrings and markdown files.
2. **API Documentation:** A **[[Swagger/OpenAPI]]** specification must be available for all public API endpoints.
3. **Code Documentation:** All public functions, classes, and modules must have clear, concise docstrings.
4. **Comprehensive README:** A `README.md` details purpose, configuration, build/run instructions, API reference, and key architectural decisions.  
    Final response to user: 
    
[[apexsigma.glossary.as]]
[[Implementation Report]]
[[MAR (Mandatory Agent Review) Report]]
[[Task Work Order]]
[[]]
```
