# Project Brief: InGest-LLM

**Project Code:** `ingest-llm.as`  
**Parent Ecosystem:** `DevEnviro`  
**Version:** 1.0

## 1\. The Problem: Knowledge Gaps & Manual Data Entry

For the 'Society of Agents' to achieve peak intelligence, its central memory (MemOS.as) must be continuously populated with relevant, up-to-date knowledge. Currently, the system lacks an automated mechanism to absorb and process unstructured data from the outside world (e.g., new code, documentation, logs). This forces manual data entry, creates knowledge silos, and prevents the agent society from learning from its own operational environment in real-time.

## 2\. The Vision: An Automated Sensory System for the Society's Brain

InGest-LLM.as is envisioned as the automated sensory system for MemOS.as. It will act as a dedicated, intelligent data pipeline that constantly watches for new information, processes it into a structured format, and feeds it into the society's collective memory. Our vision is to create a seamless, "fire-and-forget" ingestion service that empowers the ecosystem to learn and adapt without human intervention.

## 3\. The Solution: A Dedicated Ingestion & Vectorization Microservice

InGest-LLM.as will be a standalone microservice responsible for a single, critical task: transforming raw, unstructured data into queryable, vectorized memories.

Its core functions will be:

  * **Source Monitoring:** Actively monitor designated data sources (e.g., file directories, Git repositories) for new or updated information.
  * **Content Processing:** Intelligently parse and chunk various file types (Markdown, JSON, Python code) into contextually relevant segments.
  * **Vectorization:** Use the ecosystem's standard embedding model (`nomic-embed-code-GGUF`) to convert each data chunk into a vector embedding.
  * **Data Handoff:** Load the processed text, metadata, and vector into the shared Qdrant vector database and notify MemOS.as of the new knowledge.
