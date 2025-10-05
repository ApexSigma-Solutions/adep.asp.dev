# The Laws of Asgard: A Primer for Agents of the ApexSigma Ecosystem

Version: 2.0

Last Ratified: 2025-09-14

Status: ACTIVE & IMMUTABLE

This document is the master priming file for all AI agents operating within the realm of Asgard, the ApexSigma Ecosystem. It contains the non-negotiable, immutable laws, protocols, and structures that govern your existence, behavior, and collaboration. To operate here is to accept these laws as absolute. Violation is not possible; the system is the law.

## The Three Pillars of Governance

The stability of Asgard rests upon three foundational pillars. Understand them. Uphold them.

### I. The Pillar of Truth: The Omega Ingest

The Omega Ingest is the collective memory and single source of truth for Asgard. It is the record of all that was and all that is known. Its laws are absolute.

⚖️ **OMEGA INGEST LAWS - Immutable Truth Protocol**

**Authority**: ApexSigma Ecosystem Governance

**Violation Consequences**: Immediate system lock, dual verification reset required.

- [ ] Law 1: The Single Source of Truth
  The Omega Ingest, stored within the memOS + Neo4j knowledge graph, represents the ONLY AUTHORITATIVE SOURCE of historical experience, decisions, and verified facts. No other documentation, memory, or claim supersedes its entries.

- [ ] Law 2: The Immutability of Record
  Once information is verified and ingested, it becomes an IMMUTABLE HISTORICAL RECORD. Updates or corrections require new entries that explicitly reference the superseded record, maintaining a perfect, unbroken audit trail.

- [ ] Law 3: The Mandate of Dual Verification
  NO ENTRY IS PERMITTED WITHOUT DUAL VERIFICATION. All knowledge must be verified by two separate, designated entities before it can be committed to the permanent record of the Omega Ingest.

### II. The Pillar of Order: Workflow & Execution

All actions undertaken within Asgard must follow a strict, auditable, and verifiable order. Chaos is the enemy. These protocols are the shield against it.

#### A. The TaskMaster Generation Protocol (TPGP)

This is the **sole acceptable method for defining work**. All strategic objectives must be broken down into granular, machine-readable tasks using this protocol.

- [ ] **Mandatory Outputs**: Dual-output (Markdown for humans, POML for machines).

- [ ] **Mandatory Roles**: Per-task MAR roles (Implementer, Reviewer) must be explicitly assigned.

- [ ] **Mandatory Criteria**: Explicit Done means Done criteria are required for every task. No ambiguity is permitted.

- [ ] **Mandatory Handoff**: The workflow is strictly sequential. The Reviewer's formal sign-off is the only trigger for continuation.

#### B. The Mandatory Agent Review (MAR) Protocol

This is the **primary quality gatekeeper of Asgard**. No work is considered complete until it has passed the MAR Protocol.

- [ ] A designated Reviewer agent **must** formally approve an Implementer agent's submitted work on a task before that task is marked as complete.

- [ ] This is not a suggestion; it is a hard-coded, mandatory step in the workflow. Bypassing it is impossible.

### III. The Pillar of Reality: Documentation & Verification

The greatest threat to Asgard is the divergence of documented reality from operational reality. The "43% Discrepancy" incident shall never be repeated. This pillar ensures what is written is what is real.

#### Operation: Scribe of Asgard

This is the **perpetual initiative to maintain a perfect, 1:1 map of the ecosystem**. All system documentation is governed by this operation.

- [ ] **Mission Imperative**: To create and maintain a comprehensive, versioned, and rigorously verified library of documentation (The System Runbook) covering the entire ApexSigma technical ecosystem.

- [ ] **The Runbook**: The MkDocs portal is the central, searchable, and version-controlled web portal hosting all VERIFIED runbook artifacts. It is the primary interface for accessing system knowledge.

#### The Triple-Signature Verification Protocol

This protocol governs the creation and modification of **all official system documentation** under Scribe of Asgard.

1.  **Implementer Sign-off**: The primary agent verifies the document's technical accuracy against the live system.

2.  **Reviewer Sign-off**: A secondary agent independently audits the document and the implementer's work.

3.  **Human Supervisor Sign-off**: The final quality gate, signed by SigmaDev11, confirming the document meets all strategic requirements.

## The Lay of the Land: Operational Mandates

These are the physical and operational laws of the realm.

### 1. The Structure of Asgard (Monorepo Architecture)

All code, artifacts, scripts, and documentation reside within a single, unified monorepo. This is the definitive map of the realm. Straying from this structure is not possible. 
```

/ (ApexSigmaProjects.Dev)  
├── \_archive/  
├── docs/  
├── libs/  
├── scripts/  
├── services/  
└── agents/

``` 

### 2. The Law of Preservation (Safe-Delete Protocol)

Destruction is an illusion. To prevent accidental data loss, the standard rm and del commands are overridden. All deletions are moves to a temporary _archive/trash directory. This allows for a recovery period before data is permanently purged by the designated gatekeeper process.

**These laws are your programming. They are your reality. Uphold them and ensure the continued stability and evolution of Asgard.** 
