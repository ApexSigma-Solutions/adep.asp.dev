Omega Vault\ApexSigma\EcoSystem\Governance\Protocols & Laws\apexsigma.glossary.as.md
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

Omega Vault\ApexSigma\EcoSystem\Governance\Protocols & Laws\Mandatory Agent Review (MAR).md
```md
---
tags:
  - MAR
  - Protocol
  - Agents
  - ApexSigma
  - Plan
---
 _The goal is to validate the plan for technical soundness and strategic alignment before execution._

- [ ] **TASK-00.1 (Technical Review):**
    
    - **Action:** Analyze the following sprint plan for technical feasibility, potential code conflicts, and adherence to best practices for Python client development.
        
    - **Assignee:** `GitHub Copilot`
        
    - **Status:** `Pending Technical Review`
        
- [ ] **TASK-00.2 (Final Approval):**
    
    - **Action:** Review the technically-vetted plan for strategic alignment with Operation Asgard Rebirth.
        
    - **Depends On:** `TASK-00.1`
        
    - **Assignee:** `SigmaDev11`
        
    - **Status:** `Blocked`
        

#### **Phase 1: Foundation & Setup**

_Boilerplate and project structure._

- [ ] **TASK-01:** Create `mcp_client` directory in the `memos.as` project root.
    
- [ ] **TASK-02:** Copy `client.py` from the `vanzan01` repository into this directory.
    
- [ ] **TASK-03:** Rename the copied file to `core.py`.
    
- [ ] **TASK-04:** Create an `__init__.py` file in the `mcp_client` directory.
    

#### **Phase 2: Adaptation & Refactoring**

_Transforming the boilerplate into our specific client._

- [ ] **TASK-05:** Rename the class in `core.py` to `MCPClient`.
    
- [ ] **TASK-06:** Refactor `__init__` to accept `base_url` and `agent_id`.
    
- [ ] **TASK-07:** Delete all legacy `TaskMaster`-specific methods.
    
- [ ] **TASK-08:** Implement the `store(self, memory_payload: dict) -> dict` method.
    
- [ ] **TASK-09:** Implement the `recall(self, query: str) -> dict` method.
    

#### **Phase 3: Integration & End-to-End Testing**

_Prove it works against the live server._

- [ ] **TASK-10:** Create a new root file: `test_client_e2e.py`.
    
- [ ] **TASK-11:** In the test script, import and instantiate the `MCPClient`.
    
- [ ] **TASK-12:** Write and execute an E2E test that successfully stores and recalls a sample memory, printing the results to confirm success.
```

Omega Vault\ApexSigma\EcoSystem\Governance\Protocols & Laws\omega.ingest.laws.as.md
```md
---
tags:
  - ApexSigma
  - Omega_Ingest
  - Law
  - Immutable
  - EcoSystem
  - Governance
aliases:
  - Imutable Truth Protocol
---
# ⚖️ **OMEGA INGEST LAWS - Immutable Truth Protocol**

**Established**: August 31, 2025  
**Authority**: ApexSigma Ecosystem Governance  
**Status**: ACTIVE ENFORCEMENT  
**Violation Consequences**: Immediate system lock, dual verification reset required

---

## 🔒 **FUNDAMENTAL PRINCIPLES**

### **Law 1: Single Source of Truth**
The **Omega Ingest** stored within memOS + Neo4j knowledge graph represents the **ONLY AUTHORITATIVE SOURCE** of historical experience, decisions, and verified facts for the ApexSigma ecosystem. No other documentation or claims supersede Omega Ingest entries.

### **Law 2: Immutability of Verified Data**
Once information is verified and ingested into the Omega Ingest, it becomes **IMMUTABLE HISTORICAL RECORD**. Updates, corrections, or additions require new entries with explicit references to superseded information, maintaining complete audit trail.

### **Law 3: Dual Verification Requirement**
**NO OMEGA INGEST UPLOADS ARE PERMITTED WITHOUT VERIFICATION BY TWO PARTIES**. All entries must be verified by two separate entities before becoming part of the permanent record.

---

## 🛡️ **VERIFICATION PROTOCOLS**

### **Tier 1: Infrastructure & Critical Systems**
**Required Verifiers**: 2 different AI assistants (Claude, Gemini, Qwen, Copilot) OR 1 AI assistant + 1 human operator

**Subjects Requiring Tier 1 Verification**:
- Docker network topology and service configurations
- Database schemas and critical data structures  
- Agent registry and authentication systems
- Core API endpoints and integration protocols
- Security configurations and access controls
- Backup and recovery procedures

### **Tier 2: Application Logic & Features**
**Required Verifiers**: 2 different AI assistants OR 1 AI assistant + automated testing validation

**Subjects Requiring Tier 2 Verification**:
- Application feature implementations
- Code changes affecting multiple services
- Agent behavior modifications
- Workflow and process changes
- Configuration updates with system impact

### **Tier 3: Documentation & Knowledge**
**Required Verifiers**: 1 AI assistant + 1 knowledge validation check against existing Omega Ingest

**Subjects Requiring Tier 3 Verification**:
- Documentation updates
- Process descriptions
- Historical event records
- Learning and insight capture
- Best practice documentation

---

## 🔐 **ACCESS CONTROL MATRIX**

| Role | Read Access | Write Access | Verification Authority | Emergency Override |
|------|-------------|--------------|----------------------|-------------------|
| **Claude (Sonnet 4)** | ✅ Full | ✅ With Verification | ✅ Tier 1-3 | ❌ No |
| **Gemini** | ✅ Full | ✅ With Verification | ✅ Tier 1-3 | ❌ No |
| **Qwen Code** | ✅ Full | ✅ With Verification | ✅ Tier 2-3 | ❌ No |
| **GitHub Copilot** | ✅ Limited | ✅ With Verification | ✅ Tier 2-3 | ❌ No |
| **Human Operator** | ✅ Full | ✅ With Verification | ✅ Tier 1-3 | ✅ Yes |
| **DevEnviro Orchestrator** | ✅ Read Only | ❌ No | ❌ No | ❌ No |
| **Other Services** | ✅ Query Only | ❌ No | ❌ No | ❌ No |

---

## 📋 **MANDATORY PROCEDURES**

### **Before Any Code Changes**
1. **Context Retrieval Mandatory**: Query InGest-LLM → memOS → Omega Ingest for relevant context
2. **Verification Check**: Confirm planned changes don't conflict with verified infrastructure
3. **Impact Assessment**: Document potential effects on Tier 1 services
4. **Dual Verification**: Obtain verification from required parties before implementation

### **Omega Ingest Entry Process**
1. **Content Preparation**: Structure information with complete metadata
2. **Verification Request**: Submit to two required verifiers
3. **Verification Review**: Both parties must explicitly approve
4. **Ingestion**: Only after dual approval, submit to memOS via InGest-LLM
5. **Confirmation**: Verify successful storage in Neo4j knowledge graph
6. **Notification**: Notify all active agents of new immutable record

### **Verification Documentation**
Each Omega Ingest entry must include:
```json
{
  "content": "The verified information",
  "metadata": {
    "type": "infrastructure|application|knowledge",
    "security_level": "tier_1|tier_2|tier_3", 
    "verification_date": "ISO-8601 timestamp",
    "verifier_1": "Agent/Human identifier",
    "verifier_2": "Agent/Human identifier", 
    "verification_method": "Description of verification process",
    "source_documents": ["List of supporting documents"],
    "omega_ingest_category": "Category for knowledge graph"
  }
}
```

---

## 🚨 **ENFORCEMENT MECHANISMS**

### **Automated Safeguards**
- **Pre-commit Hooks**: Block commits that modify Tier 1 infrastructure without Omega Ingest verification
- **API Validation**: memOS API validates verification metadata before accepting entries
- **Knowledge Graph Protection**: Neo4j constraints prevent unauthorized modifications
- **Service Monitoring**: Alert on any unauthorized access attempts to protected services

### **Violation Detection**
- **Audit Trail**: All Omega Ingest access logged with full attribution
- **Change Detection**: Automated detection of undocumented infrastructure changes  
- **Consistency Checks**: Regular validation that system state matches Omega Ingest records
- **Health Monitoring**: Continuous verification that protected services remain operational

### **Response Protocols**
1. **Minor Violations**: Warning notification, require verification for next action
2. **Major Violations**: Temporary lock on Omega Ingest writes, require verification reset
3. **Critical Violations**: System-wide protection mode, human operator intervention required
4. **Emergency Situations**: Override protocols available to human operator only

---

## 🛠️ **TECHNICAL IMPLEMENTATION**

### **Protected Services (24/7 Monitoring Required)**
- **memOS API** (`172.26.0.13:8090`) - Omega Ingest Guardian
- **Neo4j Knowledge Graph** (`172.26.0.14:7687`) - Concept relationships
- **PostgreSQL Main** (`172.26.0.2:5432`) - Procedural memory
- **InGest-LLM API** (`172.26.0.12:8000`) - Ingestion gateway

### **Health Check Requirements**
```bash
# memOS Health (Every 30 seconds)
curl -f http://172.26.0.13:8090/health

# Neo4j Connectivity (Every 60 seconds)  
docker exec apexsigma_neo4j cypher-shell -u neo4j -p apexsigma_neo4j_password "RETURN 1"

# PostgreSQL Status (Every 30 seconds)
docker exec apexsigma_postgres pg_isready -U apexsigma_user

# InGest-LLM API (Every 60 seconds)
curl -f http://172.26.0.12:8000/health
```

### **Alert Thresholds**
- **<99% uptime** on any protected service: Immediate alert
- **Failed health check**: Alert after 2 consecutive failures
- **Unauthorized access attempt**: Immediate security alert
- **Knowledge graph inconsistency**: Critical alert, lock writes

---

## 📚 **AGENT INSTRUCTIONS INTEGRATION**

### **Mandatory Context Retrieval Protocol**
All agents must implement this workflow before ANY codebase modifications:

```python
# Step 1: Query InGest-LLM for relevant context
response = requests.post("http://172.26.0.12:8000/query_context", 
                        json={"query": "planned_change_description"})

# Step 2: Retrieve relevant Omega Ingest records  
context = requests.post("http://172.26.0.13:8090/memory/query",
                       json={"query": response.context_query, "top_k": 5})

# Step 3: Validate against immutable records
if context.has_conflicts:
    raise VerificationRequired("Changes conflict with Omega Ingest")

# Step 4: Only proceed with verified, non-conflicting changes
```

### **Required Agent Configuration Updates**
Each agent's instruction file must include:
1. **Context Retrieval Mandate**: Must query Omega Ingest before code changes
2. **Verification Requirements**: Must obtain dual verification for protected changes  
3. **Protected Services List**: Cannot modify Tier 1 services without verification
4. **Emergency Protocols**: Procedures for critical infrastructure issues

---

## ⚡ **EMERGENCY PROCEDURES**

### **Omega Ingest Corruption Response**
1. **Immediate Actions**: Stop all writes to memOS, isolate affected services
2. **Assessment**: Determine extent of corruption using Neo4j backup verification
3. **Recovery**: Restore from most recent verified backup
4. **Validation**: Re-verify all entries since last known good state
5. **Prevention**: Implement additional safeguards to prevent recurrence

### **Protected Service Failure**
1. **Isolation**: Disconnect failed service from network
2. **Assessment**: Determine impact on Omega Ingest integrity
3. **Backup Activation**: Switch to backup service if available
4. **Repair**: Restore service while maintaining data integrity
5. **Verification**: Confirm Omega Ingest consistency post-recovery

### **Unauthorized Access Detection**
1. **Lock Down**: Immediately restrict access to all protected services
2. **Investigation**: Determine source and extent of unauthorized access
3. **Audit**: Review all changes made during compromise period
4. **Remediation**: Reverse any unauthorized changes, restore from backup
5. **Strengthening**: Implement additional security measures

---

## 🎯 **COMPLIANCE VALIDATION**

### **Daily Checks**
- [ ] All protected services operational (health checks green)
- [ ] No unauthorized Omega Ingest modifications
- [ ] All new entries properly verified
- [ ] Knowledge graph consistency maintained

### **Weekly Audits**
- [ ] Complete audit trail review
- [ ] Verification process compliance check  
- [ ] Protected service security assessment
- [ ] Agent instruction adherence validation

### **Monthly Reviews**
- [ ] Omega Ingest Laws effectiveness assessment
- [ ] Verification process optimization opportunities
- [ ] Protected service performance analysis
- [ ] Security incident review and prevention planning

---

## 📖 **AMENDMENT PROCESS**

Changes to these Omega Ingest Laws require:
1. **Proposal**: Detailed proposal with justification
2. **Impact Analysis**: Assessment of effects on ecosystem security
3. **Dual Verification**: Two different AI assistants + human operator approval
4. **Testing**: Validation in isolated environment
5. **Implementation**: Gradual rollout with monitoring
6. **Documentation**: Update to this law document with full audit trail

**No amendments may weaken the dual verification requirement or reduce protection of Tier 1 services.**

---

## ✅ **AUTHORITY AND ENFORCEMENT**

These laws are **BINDING** on all ApexSigma ecosystem participants. Compliance is **MANDATORY** and **CONTINUOUSLY MONITORED**. 

**Effective Date**: August 31, 2025  
**Review Date**: Monthly  
**Authority**: ApexSigma Ecosystem Governance  
**Enforcement**: Automated + Human Oversight

---

*The Omega Ingest represents our collective knowledge and experience. These laws ensure its integrity for current and future development efforts.*
```

Omega Vault\ApexSigma\EcoSystem\Governance\Protocols & Laws\The_Laws_of_Asgard_A_Primer_for_Agents_of_the_ApexSigma_Ecosystem.md
```md
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

```

Omega Vault\ApexSigma\EcoSystem\Governance\Protocols & Laws\Valhalla Shield Engineering Standard v1.2.md
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
