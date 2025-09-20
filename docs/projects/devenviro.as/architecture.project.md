``` markdown
# DevEnviro Technical Architecture & Observability Blueprint

**Version: 1.1**

This document details the architectural blueprint and core implementation patterns for the DevEnviro platform. It serves as the primary source of truth for how all system components are structured, how they interact, and how they are monitored.

---

## 1. Overall System Architecture: The Society of Agents

The platform is built as a **Microservices Architecture** centered around a "Society of Agents." This design promotes modularity, resilience, and scalability.

-   **Agents:** Specialized, single-purpose AI instances (e.g., Gemini, Claude, Gemma) that perform specific tasks.
-   **Orchestrator:** A central service responsible for decomposing complex user requests into granular sub-tasks and intelligently delegating them to the most suitable agents.
-   **Communication Backbone:** **RabbitMQ** serves as the central, asynchronous message broker for all inter-agent communication. This ensures loose coupling and fault tolerance.
-   **Multi-Tiered Memory Engine:**
    -   **Redis (Tier 1):** In-memory store for high-speed working memory and caching.
    -   **Qdrant (Tier 2):** Vector database for episodic (experiential) memory.
    -   **Neo4j (Tier 2):** Graph database for semantic memory, mapping the relationships within the codebase.
    -   **PostgreSQL (Tier 3):** Relational database for procedural memory (the "Golden Play Book") and structured logs.

---

## 2. Observability & Analytics: A Dual-Stack Approach

The system's health and performance are monitored through a comprehensive, dual-stack approach that provides insight into both system infrastructure and agent cognition.

### System Infrastructure Observability (The Three Pillars)

-   **Metrics (Prometheus):** Monitors the numeric health of our services over time (e.g., CPU, request rates).
-   **Logs (Loki):** Stores and queries timestamped text messages from our services for event analysis and error tracking.
-   **Traces (Jaeger):** Visualizes the end-to-end flow of requests across all microservices to identify bottlenecks.
-   **Visualization (Grafana):** Provides a unified dashboard for all infrastructure telemetry.

### LLM & Agent Cognition Observability

-   **Langfuse:** The open-source observability platform for LLM applications. It captures detailed traces of agent reasoning, tool usage, and LLM interactions. This is the core tool used to analyze agent performance and curate the "Golden Play Book" of successful workflows.

---

This architecture ensures a robust, observable, and resilient system that allows for proactive problem-solving and rapid debugging.

```