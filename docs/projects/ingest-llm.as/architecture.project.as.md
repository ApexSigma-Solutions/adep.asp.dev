````markdown
# InGest-LLM.as: Technical Architecture Version: 1.0

## Status: Design

## 1. System Overview
InGest-LLM.as is a containerized microservice that functions as the primary data ingestion pipeline for the DevEnviro ecosystem. It is designed to be event-driven and asynchronous, operating independently to process files and populate the shared vector database.

## 2. Architectural Pattern: Asynchronous Pipeline
The service communicates with the rest of the ecosystem asynchronously via the shared database and a message broker, ensuring a decoupled and resilient architecture.

````mermaid
graph TD
    subgraph "DevEnviro Ecosystem"
        A[File System Volume /ingest] --> B(InGest-LLM.as Service);
        B -- "1. Read File" --> A;
        B -- "2. Chunk & Vectorize" --> C((LM Studio));
        B -- "3. Store Vector & Text" --> D[(Qdrant DB)];
        B -- "4. Publish Notification" --> E{RabbitMQ Topic: memos.ingest.complete};
        F[MemOS.as Service] -- "5. Consume Notification" --> E;
        F -- "6. Update Knowledge Graph (Future)" --> G[(Neo4j DB)];
    end

````

## 3\. Core Components & Data Flow

**Source Monitor (watchdog):** An event listener monitors a designated `/ingest` volume mapped into the Docker container. On detecting a new file, it triggers the processing pipeline.

**Processing Pipeline:**

  * **Content Extractor:** A factory module selects the appropriate parser based on the file's extension (.md, .json, .py).
  * **Text Splitter:** The extracted text is chunked into optimal sizes for the embedding model.
  * **Embedding Generator:** It calls the local `nomic-embed-code-GGUF` model via the LM Studio SDK to create a vector embedding for each chunk.

**Data Persistence & Notification:**

  * **Vector Store Loader:** The text chunk, its embedding, and metadata are loaded into the shared Qdrant collection.
  * **MemOS Notifier:** A message containing the metadata of the ingested document is published to a RabbitMQ topic. This allows MemOS.as to be aware of new knowledge without being directly coupled to the ingestion service.

## 4\. Architectural Roadmap

  * **Phase 1 (Current):** Implement the core file-based ingestion pipeline for Markdown, JSON, and Python files.
  * **Phase 2 (Future):** Add a Git repository scanner to automatically ingest knowledge from committed code and documentation.
  * **Phase 3 (Future):** Add support for ingesting data from other sources, such as web URLs or database connectors.

<!-- end list -->

````
