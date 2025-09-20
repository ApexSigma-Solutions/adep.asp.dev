# The ApexSigma Glossary (v1.0)

This document serves as the master glossary for all terms, protocols, and concepts used within the ApexSigma ecosystem.

## A

### ApexSigma Solutions

- The technical software development organization founded by Sean Steyn (SigmaDev11). Its goal is to solve real-world problems by combining human creativity with AI technology.

## F

### FastMCP 2.0

- The FastAPI-based framework used to build high-performance, concurrent agentic services like memOS.as.

## G

### Gemini (CLI)

- The designated AI Implementer agent, responsible for executing technical tasks such as coding, scaffolding, and deployment.

## I

### Implementation Report

- A standardized document submitted by the **Implementer** to formally hand off a completed task for review. It details the work done and links to all relevant artifacts.

## M

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

## P

### Pluggable Storage Architecture

- The four-tier storage design for memOS.as, consisting of Redis (cache), PostgreSQL (metadata), Qdrant (semantic recall), and Neo4j (episodic memory).

### POML (Prompt Orchestration Markup Language)

- The mandated standard for formatting knowledge components to ensure efficient and targeted tokenization for LLMs interacting with the knowledge graph.

## Q

### Qwen

- The designated AI Reviewer agent, responsible for conducting the **MAR Protocol** checks on work submitted by the Implementer.

## S

### Society of Agents

- The collaborative structure of specialized agents (e.g., Gemini, Qwen) that work together to execute complex projects within the ecosystem.

## T

### TaskMaster MCP Framework

- An autonomous agent framework that orchestrates an LLM's execution based on a structured Product Requirements Document (prd.txt). It ensures strict alignment between a project's goals and the agent's actions.

### Three-Layer Architecture

- The strategic architectural model for the evolved memOS.as ecosystem. It consists of a 'Tools' layer (the core memOS API), a 'Workers' layer (the agent swarm), and an 'Orchestrator' layer (Dagster).