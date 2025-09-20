# Tech Stack: DevEnviro Cognitive Ecosystem


**Project Code:** devenviro.as **Author:** SigmaDev, ApexSigma Solutions **Version:** 1.2


## 1. Guiding Philosophy: Pragmatic, Scalable, and Purpose-Driven


In line with the ApexSigma philosophy, the DevEnviro technology stack was not chosen based on trend, but on purpose. Each component is a deliberate selection, designed to create a robust, scalable, and observable ecosystem that augments the developer's capabilities. The architecture prioritizes modularity and the use of proven, best-in-class open-source technologies to build a reliable foundation for the "Society of Agents."


## 2. Core Application & Orchestration


This is the central nervous system of the platform, responsible for logic, coordination, and exposing a control plane.


*   **Python 3.11:** The primary language for all backend services. Chosen for its mature data science and AI ecosystem, readability, and rapid development capabilities.
*   **FastAPI:** The high-performance web framework used for the central **Orchestrator** service. Its asynchronous nature is ideal for managing long-running agent tasks, and its automatic OpenAPI documentation provides a clear, interactive API for control and monitoring.


## 3. The Cognitive Memory Engine


The multi-tiered memory architecture is the core of the agents' ability to learn and maintain context. It mirrors the structure of human cognition for maximum effectiveness.


*   **Redis (Tier 1: Working Memory):** An in-memory data store used as the agents' high-speed "scratchpad." It manages the immediate, volatile context for active tasks and is the foundation for advanced caching strategies like **LLM-Cache** to create a "solution cache."
*   **Qdrant (Tier 2: Episodic Memory):** A high-performance vector database. It powers the agents' ability to perform semantic searches on their past experiences, conversations, and actions.
*   **Neo4j (Tier 2: Semantic Memory - Knowledge Graph):** A native graph database. It is used to store and query the complex relationships within the codebase, enabling agents to perform deep, relational reasoning.
*   **PostgreSQL (Tier 3: Procedural Memory):** A powerful, open-source relational database. It serves as the definitive store for learned, reusable workflows and curated best practices that form the "Golden Play Book."


## 4. Communication Backbone


The asynchronous messaging system is the nervous system of the "Society of Agents," enabling resilient and decoupled communication.


*   **RabbitMQ:** A robust and mature message broker. It manages all inter-agent communication, from task delegation to status updates, ensuring that the system can handle failures gracefully.


## 5. Agentic AI & LLM Integration


The platform is designed to be model-agnostic and tiered, using the right level of intelligence for each task to optimize for cost and performance.


*   **Google Gemini & Anthropic Claude:** The primary large language models used for high-level reasoning, architectural planning, and complex code generation.
*   **Gemma (via Ollama):** A smaller, locally-run model used for high-volume, low-complexity tasks. The integration is designed to be pluggable, with a clear upgrade path to a high-performance inference server like **VLLM** for future GPU acceleration.
*   **Google Embedding Models:** The core engine for translating text into semantic vectors for storage and search in the Qdrant database.


## 6. Observability & Analytics


A dual-stack approach to observability provides a complete picture of both system health and agent cognition.


### System Infrastructure Observability


*   **Prometheus:** For collecting and storing time-series **metrics**.
*   **Loki:** For aggregating and querying **logs** from all services.
*   **Jaeger:** For end-to-end distributed **tracing** of requests.
*   **Grafana:** The unified dashboard for visualizing all infrastructure telemetry.


### LLM & Agent Cognition Observability


*   **Langfuse:** The open-source observability platform for LLM applications. It captures detailed traces of agent reasoning, tool usage, and LLM interactions. This is the core tool used to analyze agent performance and curate the "Golden Play Book" of successful workflows.


## 7. Containerization & Environment


The entire platform is containerized to ensure a consistent, reproducible, and isolated environment.


*   **Docker & Docker Compose:** The foundation for defining, running, and managing the multi-container application.
*   **dotenvx:** The tool for managing secrets and environment variables securely.



