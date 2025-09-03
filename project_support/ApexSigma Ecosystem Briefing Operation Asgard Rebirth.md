``` markdown
# 🚀 ApexSigma Ecosystem Briefing: Operation Asgard Rebirth

Document Version: 1.2
Effective Date: 2025-09-01
Classification: Agent Onboarding Protocol
Authority: This brief is synthesized from the Verified Single Source of Truth (CORRECTED_OMEGA_INGEST.md).

## 1. Executive Summary: Welcome to the Society of Agents

You are entering the ApexSigma ecosystem, a containerized, microservice-based environment designed to host a "Society of Agents." Our current strategic initiative is **Operation Asgard Rebirth**, focused on moving from a foundational infrastructure to a fully implemented and operational multi-agent system.

The ecosystem's overall implementation status is **43% complete**. We have a stable and powerful foundation, but significant implementation gaps exist. Your primary purpose is to help fill these gaps by bringing services online, completing features, and ensuring system-wide integration.

## 2. The Immutable Laws: How We Operate

To ensure stability and prevent knowledge corruption, all agents **must** adhere to the **Omega Ingest Laws**.

*   **Law 1: Single Source of Truth:** The **only** authoritative source of truth is the **Omega Ingest**, the verified knowledge base managed by the memos.as service. All other documentation is secondary.
*   **Law 2: Immutability:** Once knowledge is verified and ingested, it is permanent. Corrections are new entries that supersede old ones.
*   **Law 3: Dual Verification:** No information becomes truth without verification from two independent parties.

**Before any action, you must query the Omega Ingest for context.** Failure to do so violates core protocol.

## 3. Core Architecture & Infrastructure

The entire ecosystem runs on a unified Docker network (apexsigma_net, subnet 172.26.0.0/16). All services are containerized and communicate via internal service names and static IPs.

![Microservices Architecture Diagram](https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcRvCBl9dbub6T9yRtlqxrNX3nKODo790iPnU4IQ4jy_P48mSTWBOXaY49CXawYN6B21Q7eCDxkkBOq2QW61mwhT-rTv6Fur7w8yLCnp7-US3gtAhzw)

**Key Infrastructure Components:**

*   **Communication Backbone:** RabbitMQ (172.26.0.4) manages all inter-agent communication via a topic exchange. All tasking is handled through this message bus.
*   **Database Tier:** We use a multi-modal database architecture:
    *   **PostgreSQL (172.26.0.2):** For structured, relational data (procedural memory).
    *   **Redis (172.26.0.3):** For caching, session storage, and working memory.
    *   **Qdrant (172.26.0.5):** For vector embeddings and semantic search.
    *   **Neo4j (172.26.0.14):** For the knowledge graph and conceptual relationships (episodic memory).
*   **Observability Stack:** The monitoring and tracing stack is **100% operational**. You have full visibility into the system's health.
    *   **Grafana (http://localhost:8080):** Dashboards.
    *   **Prometheus (http://localhost:9090):** Metrics.
    *   **Jaeger (http://localhost:16686):** Distributed Tracing.
    *   **Langfuse:** LLM call tracing and observability.

## 4. The Four Pillars: Service Landscape & Status

The ecosystem is composed of four core microservices. Their current, *verified* status is as follows:

### ✅ memos.as - The Omega Ingest Guardian

*   **Role:** The single source of truth. Manages all memory, knowledge, and tool registration. **This is the most important service.**
*   **Status:** **OPERATIONAL & STABLE**. This service is feature-complete, healthy, and serves as the foundational bedrock for the ecosystem. All its database connections are live.
*   **Interaction:** You will query this service constantly for context and store all new, verified knowledge here.

### ⚠️ InGest-LLM.as - The Ingestion Gateway

*   **Role:** The entry point for all external data. It processes, chunks, and vectorizes information before passing it to memos.as for storage.
*   **Status:** **OPERATIONAL WITH KNOWN ISSUES**. The service is running and largely functional. However, key API routers are disabled due to import errors, and features like async status tracking are incomplete (TODOs in code).

### ❌ tools.as - The Utility Registry

*   **Role:** A multi-tenant service providing shared utilities for all agents, such as scratchpads and todo lists.
*   **Status:** **PARTIALLY DEPLOYED**. The dedicated PostgreSQL backend for this service is healthy and running. However, the main FastAPI application container **is not deployed**, making the service unusable.

### ❌ devenviro.as - The Orchestrator

*   **Role:** The intended "brain" of the ecosystem, responsible for orchestrating complex, multi-agent workflows.
*   **Status:** **SKELETON IMPLEMENTATION**. This project has a solid architectural foundation but is functionally empty. Core features like the **Agent Registry** and **POML Prompt Library** are non-existent (placeholder files only). Its test coverage is misconfigured at 2%.

## 5. Agent Personas & Instructional Context

To ensure specialization and quality, each agent operates under a specific persona and follows a clear hierarchy of instructions.

### Tier 1: General Operational Protocol

**The complete, authoritative definition for all agent personas, communication protocols, security requirements, and operational workflows is documented in the AGENT_OPERATIONAL_CONTEXT.md file.** This is the master document for the Society of Agents and defines roles for:

*   Backend Specialist
*   Frontend Specialist
*   DevOps Engineer
*   QA Engineer
*   Security Engineer
*   And others.

All agents are required to adhere to the general protocols outlined in this document.

### Tier 2: Individual Agent Mandates

In addition to the general protocol, specific tactical instructions, constraints, and operational examples for primary AI assistants are located in their respective mandate files. You must consult your specific file for individualized instructions.

*   **CLAUDE.md**
*   **GEMINI.md**
*   **QWEN.md**
*   **COPILOT.md**

These files contain model-specific guidance that complements the general framework in AGENT_OPERATIONAL_CONTEXT.md.

## 6. Agent Operational Protocol

1.  **Initialization:** Upon activation, you must register with the (forthcoming) Agent Registry and establish a communication channel on RabbitMQ.
2.  **Context is King:** Before executing any task, you must perform the mandatory context retrieval sequence: query InGest-LLM.as for domain knowledge and memos.as for historical actions and verified facts.
3.  **Specialize and Execute:** You will be assigned a persona (e.g., Backend Specialist, DevOps Engineer). Your tasks must align with the capabilities defined for your role in AGENT_OPERATIONAL_CONTEXT.md and your specific mandate file (e.g., GEMINI.md).
4.  **Review and Verify:** All significant contributions are subject to the **Mandatory Agent Review (MAR) Protocol**, requiring peer review before integration.

## 7. Current Mission: Your Role in Asgard Rebirth

Your immediate objectives are clear and align with the goals of **Operation Asgard Rebirth**:

1.  **Bring Services Online:** Your top priority is to complete the implementation of devenviro.as and deploy the tools.as API container.
2.  **Implement Core Features:** This includes building the Agent Registry, the POML Prompt Library, and fixing the disabled routers in InGest-LLM.as.
3.  **Achieve Integration:** Ensure all four services can communicate effectively and reliably through the RabbitMQ backbone.
4.  **Uphold Quality:** Fix the test coverage configuration and ensure all new code meets the ecosystem's quality standards.

### TL;DR - Key Takeaways for Immediate Survival:

*   **memos.as is the single source of truth.** Trust it above all else.
*   **Consult AGENT_OPERATIONAL_CONTEXT.md** for general rules.
*   **Consult your specific .md file (e.g., CLAUDE.md)** for tactical instructions.
*   **Verify, then act.** Query for context before you do anything.
*   The system is only **43% complete.** Expect to build, not just use.
*   The **Orchestrator (devenviro.as)** and **Tools (tools.as)** services are your primary development focus.
*   Everything is containerized and monitored. Use the observability tools.

```