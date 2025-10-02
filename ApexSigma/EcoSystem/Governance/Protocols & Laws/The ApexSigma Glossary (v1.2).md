---
tags:
  - ApexSigma
  - Glossary
---
# The ApexSigma Glossary (v1.2)

This document serves as the master glossary for all terms, protocols, and concepts used within the ApexSigma ecosystem.

## A

### Agent
- An autonomous or semi-autonomous entity, typically powered by an LLM, designed to perform specific tasks or roles within the ApexSigma Ecosystem. Examples include [[Gemini (CLI)]] and [[QWEN]].

### ApexSigma Ecosystem
- The integrated environment of agents, protocols, services, and architectural components governed by ApexSigma Solutions. It is designed for the collaborative and autonomous execution of complex technical projects.

### ApexSigma Solutions
- The technical software development organization founded by Sean Steyn (SigmaDev11). Its goal is to solve real-world problems by combining human creativity with AI technology.

## C

### Configuration Fragility
- A core problem identified within the ApexSigma ecosystem, referring to system instability caused by inconsistent or poorly managed service configurations.

## D

### Dagster
- The designated data orchestrator used for the 'Orchestrator' layer in the [[Three-Layer Architecture]]. It is responsible for scheduling, executing, and monitoring the workflows of the agent swarm.

### "Done Means Done"
- A strict enforcement policy and verifiable checklist defining the criteria for a task's completion, including configuration, code quality, testing, observability, containerization, documentation, and successful review under the [[Valhalla Shield Engineering Standard]].

### Dual Verification Requirement
- A core tenet of the [[Omega Ingest Laws]] mandating that any new information must be independently verified by at least two separate sources or agents before it can be committed to the master knowledge graph.

## E

### eBPF (extended Berkeley Packet Filter)
- A technology implemented for zero-code, system-level observability, providing deep insights into container communication and resource usage without modifying the application.

## F

### FastMCP 2.0
- The FastAPI-based framework used to build high-performance, concurrent agentic services like [[memOS.as]].

## G

### Gemini (CLI)
- The designated AI Implementer agent, responsible for executing technical tasks such as coding, scaffolding, and deployment.

### GitOps
- An infrastructure management methodology used to reduce configuration-related incidents by managing infrastructure as code, enabling automated rollbacks and providing a complete audit trail.

## I

### Implementer
- A designated role for an agent responsible for executing the technical development of a task, such as writing code or configuring infrastructure. The primary implementer is currently [[Gemini (CLI)]].

## K

### Knowledge Graph
- The central, structured repository of interconnected data and concepts within the ecosystem. It serves as the long-term, episodic memory for the [[Society of Agents]] and is governed by the [[Omega Ingest Laws]].

## M

### MAR (Mandatory Agent Review) Protocol
- The mandatory quality gatekeeper workflow. It requires a designated [[Reviewer]] agent to formally approve or reject the work of an [[Implementer]] before a task can be considered complete.

### MAR Implementation Report
- A standardized document submitted by the [[Implementer]] to formally hand off a completed task for review. It details the work done and links to all relevant artifacts.

### MAR Review Report
- A standardized document completed by the [[Reviewer]] that provides the official outcome (APPROVED or REJECTED) of a MAR check, including feedback and required revisions.

### memOS.as
- The core memory service of the ecosystem. It provides a multi-tiered, [[Pluggable Storage Architecture]] for agents, enabling short-term, long-term, semantic, and episodic memory.

### MLflow
- A tool integrated for performance intelligence to track, monitor, and establish baselines for machine learning model performance, focusing on context retrieval latency and relevance scores.

## O

### Omega Ingest Laws
- The immutable principles governing the master [[Knowledge Graph]]. Key tenets include the principles of a [[Single Source of Truth (SST)]], Immutability of Verified Data, and a mandatory [[Dual Verification Requirement]] for all new entries.

### Operation Asgard Rebirth
- The active, ecosystem-wide operation to correct discrepancies between documented designs and the actual implementation state. Its primary goal is to bring all services to a fully operational and verified status.

### Orchestrator Layer
- The top layer of the [[Three-Layer Architecture]], responsible for managing and coordinating the 'Workers' layer. It handles workflow scheduling, execution, and monitoring, with [[Dagster]] as the primary tool.

### OVS-01
- The identifier for the immediate stabilization protocol for the [[memOS.as]] service, designed to prove the effectiveness of the [[Valhalla Shield Engineering Standard]].

## P

### Pluggable Storage Architecture
- The four-tier storage design for [[memOS.as]], consisting of Redis (cache), PostgreSQL (metadata), Qdrant (semantic recall), and Neo4j (episodic memory).

### POML (Prompt Orchestration Markup Language)
- The mandated standard for formatting knowledge components to ensure efficient and targeted tokenization for LLMs interacting with the [[Knowledge Graph]].

### Predictive Context System
- A machine learning-driven system designed to proactively pre-load context, optimize resource allocation, and enhance workflows based on user and system patterns.

### Product Requirements Document (prd.txt)
- The standardized input document for the [[TaskMaster MCP Framework]]. It outlines the goals, scope, requirements, and constraints of a project, serving as the primary directive for the executing agent.

## Q

### Qwen
- The designated AI Reviewer agent, responsible for conducting the [[MAR (Mandatory Agent Review) Protocol]] checks on work submitted by the Implementer.

## R

### Reviewer
- A designated role for an agent responsible for quality assurance and adherence to protocols. It formally assesses the work of an [[Implementer]] according to the [[MAR (Mandatory Agent Review) Protocol]]. The primary reviewer is currently [[QWEN]].

## S

### Sequential Execution Protocol
- The defined workflow for tasks, progressing through the stages: Backlog → Todo → In-Progress → MAR → Done.

### Single Source of Truth (SST)
- A thorough report of the whole ApexSigma EcoSystem, performed monthly at minimum or after all major changes. This is a full audit on the current state of the ecosystem. This report must comply with the [[Omega Ingest Laws]], and [[MAR (Mandatory Agent Review) Protocol]].

### Society of Agents
- The collaborative structure of specialized agents (e.g., [[Gemini (CLI)]], [[QWEN]]) that work together to execute complex projects within the ecosystem.

## T

### TaskMaster MCP Framework
- An autonomous agent framework that orchestrates an LLM's execution based on a structured [[Product Requirements Document (prd.txt)]]. It ensures strict alignment between a project's goals and the agent's actions.

### Three-Layer Architecture
- The strategic architectural model for the evolved [[memOS.as]] ecosystem. It consists of a 'Tools' layer (the core memOS API), a 'Workers' layer (the agent swarm), and an 'Orchestrator' layer ([[Dagster]]).

### Tools Layer
- The foundational layer of the [[Three-Layer Architecture]], providing the core services and APIs that agents in the 'Workers' layer use to perform their tasks. This layer is primarily composed of [[memOS.as]].

### Triple-Verification Process
- A validation framework requiring sign-offs from the implementer (technical accuracy), a reviewer (quality audit), and documentation in Omega Ingest (immutable record).

## V

### Valhalla Shield Engineering Standard
- A set of disciplined engineering practices (v1.2) designed to transform fragile services into stable, production-ready components. It is the foundation for the [[Done Means Done]] criteria.

### Vector Database
- A technology integrated to enhance context architecture, enabling semantic search, improving relevant memory retrieval, and facilitating cross-agent knowledge sharing through embeddings.

### Vulcan Protocol
- A protocol that governs the process of assigning a single development task to two or more independent AI implementation agents to generate competing solutions, with the goal of identifying the superior implementation through structured comparison.

## W

### WASM (WebAssembly)-Sandboxed Execution
- A technology used to provide a secure execution environment for cross-tool integrations, isolating processes to prevent system-wide failures.

### Workers Layer
- The middle layer of the [[Three-Layer Architecture]], consisting of the [[Society of Agents]] (the "agent swarm"). These agents consume services from the 'Tools' layer to execute tasks assigned by the 'Orchestrator' layer.

#### Sources:

[^1]: [[2025-09-25 I found an app that makes deep work feel like takeoff and I’m hooked]]
[^2]: [[2025-09-08 I now use this offline AI assistant instead of cloud chatbots]]
[^3]: [[Request for Software and Hardware Upgrade to Suppo]]
[^4]: [[DavidAULlama-3.2-8X3B-MOE-Dark-Champion-Instruct-uncensored-abliterated-18.4B-GGUF · Hugging Face]]
[^5]: [[2025-09-26 How To Build AI Agents With Lifelong Learning]]
[^6]: [[2025-09-11T10_27_08.173+02_00]]
[^7]: [[Gemini Settings]]
[^8]: [[21-09-2025]]
[^9]: [[I don't see any mention of Dagster data pipeline o]]
[^10]: [[iFlow CLI_ Advanced Gemini CLI Fork with Enhanced]]
[^11]: [[20+ Years of Google Photos, 100GB of Files, One Po]]