# memOS Evolution: A Strategic Implementation Plan

**Mandate:** To execute a strategy to incrementally upgrade the memOS.as service from its current FastMCP 2.0 skeleton into a robust, concurrent, and scalable memory backbone for the ApexSigma ecosystem of AI assistants.

**Current State:** The memOS.as service is a functional, non-persistent FastMCP 2.0 server with two core tools: `store_memory` and `query_memory`.

This plan outlines three distinct phases to achieve the project's vision.

## Phase 1: Foundation - From Demo to Durable Persistence (1-2 Weeks)

**Objective:** To replace the current in-memory database with a production-grade, persistent storage layer. This is the most critical next step to ensure data durability and enable advanced search capabilities.

### Key Tasks:

1.  **Integrate PostgreSQL for Structured Memory:**
    *   [ ] **Action:** Create a `database.py` module to manage an asynchronous connection to your PostgreSQL instance.
    *   [ ] **Action:** Define a `Memory` table using SQLAlchemy or a similar ORM to store the core memory components (ID, content, metadata, timestamps).
    *   [ ] **Action:** Modify the `store_memory` tool in `main.py` to write new memory entries to this PostgreSQL table instead of the `fake_memory_db` list.

2.  **Integrate a Vector Database for Semantic Recall:**
    *   [ ] **Action:** Set up a vector database instance (e.g., Qdrant, Weaviate, as suggested in technical documents).
    *   [ ] **Action:** Create a `vector_store.py` module to handle interactions with the vector database.
    *   [ ] **Action:** Enhance the `store_memory` tool: upon receiving new content, generate a vector embedding (e.g., using `sentence-transformers`) and upsert it along with the memory's ID into the vector database.
    *   [ ] **Action:** Upgrade the `query_memory` tool: transform the incoming text query into an embedding, perform a semantic search against the vector database to get relevant memory IDs, and then retrieve the full memory content from PostgreSQL using those IDs.

3.  **Implement Configuration Management:**
    *   [ ] **Action:** Remove all hardcoded database credentials and connection strings. Use a library like Pydantic Settings to manage configuration via environment variables (`.env` file) for security and flexibility.

**Deliverable:** A fully persistent memOS.as server. Memories stored are durable across restarts, and the query functionality is powered by semantic search.

## Phase 2: Architecture - The Plugin System & Tiered Memory (2-3 Weeks)

**Objective:** To refactor the server into an extensible plugin-based architecture, enabling the implementation of the advanced memory tiers (short-term, long-term, episodic) outlined in the strategic brief.

### Key Tasks:

1.  **Implement the Core Plugin Architecture:**
    *   [ ] **Action:** As detailed in the `Week_1_memOS_Plugin_Architecture_&_Context_Management.md` document, create a `plugins` directory.
    *   [ ] **Action:** Implement a `MemOSPlugin` abstract base class and a `PluginRegistry` that can discover, initialize, and route tool calls to registered plugins.

2.  **Develop the `ContextPlugin` for Short-Term Memory:**
    *   [ ] **Action:** Create `context_plugin.py`. This plugin will manage the volatile, session-specific state of a developer's workflow.
    *   [ ] **Action:** Implement the MCP tools defined in your architecture plans, such as `store_session_context` (to save working directory, open files, etc.) and `restore_session_context`. This plugin would likely use Redis for fast, TTL-based storage.

3.  **Develop the `EpisodicPlugin` for Event-Based Memory:**
    *   [ ] **Action:** Create `episodic_plugin.py`.
    *   [ ] **Action:** Implement a tool like `log_event`, which writes timestamped, immutable events (e.g., "ran tests," "committed feature X," "encountered error Y") to a dedicated table in PostgreSQL. This creates a searchable timeline of actions.

**Deliverable:** An extensible memOS.as server with a clear separation of concerns. The server now supports distinct, queryable memory types beyond simple long-term storage, laying the groundwork for sophisticated agent interactions.

## Phase 3: Integration - The `as-cli` Smart Shell & Dogfooding (Ongoing)

**Objective:** To make memOS.as an indispensable part of the daily development workflow by integrating it directly with your CLI tools, as universally recommended by the strategy documents. This provides a crucial feedback loop for iterative improvement.

### Key Tasks:

1.  **Build and Refine the `as-cli` Wrapper:**
    *   [ ] **Action:** Using the provided `as-cli.py` and `mcp_client.py` files as a starting point, build the smart shell wrapper.
    *   [ ] **Action:** Implement session management (e.g., `as-cli --session poml-processor`) that tags all memories created within that session.

2.  **Integrate memOS Plugins into the Workflow:**
    *   [ ] **Action:** Before executing a command (e.g., `as-cli gemini "..."`), the wrapper will call `restore_session_context` from the `ContextPlugin` to retrieve the latest state for the current project.
    *   [ ] **Action:** The recalled context (semantic memories, recent events, and session state) will be prepended to the user's prompt, giving the AI agent full awareness.
    *   [ ] **Action:** After the agent responds, the wrapper will call `store_session_context` and `log_event` to save the updated state and the interaction itself.

3.  **Establish a "Dogfooding" Cadence:**
    *   [ ] **Action:** Commit to using the `as-cli` wrapper for all development interactions with Gemini, Qwen, and other agents.
    *   [ ] **Action:** At the end of each week, review the episodic memory logs to identify friction points, assess the quality of recalled context, and plan improvements for the next iteration.

**Deliverable:** A tangible increase in development velocity. The `as-cli` wrapper, powered by a multi-tiered memOS backend, will create a stateful, context-aware AI assistant that remembers, learns, and actively collaborates in the development process.

```