# ⚔️ **Operation Asgard Rebirth: Implementation Stabilization Protocol**

## Overview
**Operation Asgard Rebirth** represents the critical implementation phase focused on **VERIFIED COMPLETION** rather than documentation. This operation implements the **Mandatory Agent Review (MAR)** protocol and establishes atomic task accountability to prevent implementation regression.

**Strategic Objectives:**
1. **MAR Protocol Implementation** - Mandatory review before any task completion
2. **Agent Registry & Context System** - Full registration with Langfuse tracking
3. **Atomic Task Accountability** - Granular, verifiable implementation units
4. **Quality Gate Enforcement** - pytest coverage + ruff + reviewer signoff required
5. **Progress Protection** - Prevent documentation drift from implementation reality

**Status**: 🚀 **ACTIVE IMPLEMENTATION PHASE**
**Timeline**: 3-4 weeks
**Priority**: CRITICAL - Foundation for all future work

---

## 🎯 **Agent Allocation Framework**

### **Available Implementation Agents**
- **Gemini CLI**: Primary implementer for backend services and APIs
- **GitHub Copilot**: Primary implementer for frontend and integration work  
- **Qwen Code**: Primary implementer for specialized AI/ML components

### **Review Assignment Protocol**
- **Each task requires**: 1 Implementer + 1 Different Agent Reviewer
- **No self-review**: Implementer cannot be reviewer for same task
- **Cross-validation**: Each agent reviews work from other agents
- **Quality Gates**: pytest + ruff + reviewer approval required

### **Reviewer Rotation Matrix**
| Implementer | Primary Reviewer | Secondary Reviewer |
|-------------|------------------|-------------------|
| **Gemini CLI** | GitHub Copilot | Qwen Code |
| **GitHub Copilot** | Qwen Code | Gemini CLI |
| **Qwen Code** | Gemini CLI | GitHub Copilot |

---

## 🔧 **Phase 1: Foundation & MAR Protocol (Week 1)**

### **1.1: DevEnviro Agent Registry System** 🔄 **CRITICAL**
**Priority**: P0 - Blocks all other agent operations

#### **Task 1.1.1: Database Schema Implementation**
- **Implementer**: Gemini CLI
- **Reviewer**: GitHub Copilot  
- **Scope**: Create agent registry database tables and migrations
- **Files**: `app/migrations/006_create_agent_registry.sql`
- **Requirements**: 
  ```sql
  CREATE TABLE agents (
      id UUID PRIMARY KEY,
      agent_name VARCHAR(100) NOT NULL,
      agent_type VARCHAR(50) NOT NULL,
      status VARCHAR(20) DEFAULT 'active',
      capabilities TEXT[],
      langfuse_session_id VARCHAR(255),
      last_heartbeat TIMESTAMP,
      registration_date TIMESTAMP DEFAULT NOW()
  );
  ```
- **Acceptance Criteria**:
  - **Acceptance Criteria**:
  - [x] Migration runs successfully
  - [x] pytest coverage ≥80% for database operations
  - [x] ruff linting passes
  - [x] Reviewer signoff: GitHub Copilot
- **Estimated**: 4 hours

#### **Task 1.1.2: Agent Registration API**
- **Implementer**: GitHub Copilot
- **Reviewer**: Qwen Code
- **Scope**: REST API endpoints for agent registration/management
- **Files**: `app/src/api/agents.py`
- **Requirements**:
  ```python
  POST /api/v1/agents/register
  GET /api/v1/agents/{agent_id}/status
  PUT /api/v1/agents/{agent_id}/heartbeat
  DELETE /api/v1/agents/{agent_id}
  ```
- **Acceptance Criteria**:
  - [ ] All endpoints functional with proper error handling
  - [ ] OpenAPI documentation generated
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Integration tests pass
  - [ ] Reviewer signoff: Qwen Code
- **Estimated**: 6 hours

#### **Task 1.1.3: Agent Client SDK**
- **Implementer**: Qwen Code
- **Reviewer**: Gemini CLI
- **Scope**: Python SDK for agents to register with DevEnviro
- **Files**: `app/src/services/agent_client.py`
- **Requirements**:
  ```python
  class AgentClient:
      def register(self) -> str
      def heartbeat(self) -> bool
      def update_status(self, status: str) -> bool
      def deregister(self) -> bool
  ```
- **Acceptance Criteria**:
  - [ ] SDK handles network failures gracefully
  - [ ] Automatic retry logic implemented
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Documentation with examples
  - [ ] Reviewer signoff: Gemini CLI
- **Estimated**: 5 hours

### **1.2: MAR Protocol Implementation** ⚔️ **CRITICAL**

#### **Task 1.2.1: Review Workflow Engine**
- **Implementer**: Gemini CLI
- **Reviewer**: GitHub Copilot
- **Scope**: Core MAR protocol workflow management
- **Files**: `app/src/services/mar_protocol.py`
- **Requirements**:
  ```python
  class MARWorkflow:
      def create_task(self, implementer: str, reviewer: str) -> str
      def submit_for_review(self, task_id: str, artifacts: List[str]) -> bool
      def approve_task(self, task_id: str, reviewer: str) -> bool
      def reject_task(self, task_id: str, reviewer: str, reason: str) -> bool
      def get_task_status(self, task_id: str) -> TaskStatus
  ```
- **Acceptance Criteria**:
  - [ ] State machine properly manages task lifecycle
  - [ ] All state transitions logged
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Integration with Langfuse tracking
  - [ ] Reviewer signoff: GitHub Copilot
- **Estimated**: 8 hours

#### **Task 1.2.2: Quality Gate Integration**
- **Implementer**: GitHub Copilot
- **Reviewer**: Qwen Code
- **Scope**: Automated quality checks before review
- **Files**: `app/src/services/quality_gates.py`
- **Requirements**:
  ```python
  class QualityGates:
      def run_pytest(self, files: List[str]) -> QualityResult
      def run_ruff(self, files: List[str]) -> QualityResult
      def check_coverage(self, threshold: int = 80) -> QualityResult
      def validate_all(self, task_artifacts: List[str]) -> bool
  ```
- **Acceptance Criteria**:
  - [ ] Integrates with CI/CD pipeline
  - [ ] Detailed failure reporting
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Blocks review if quality gates fail
  - [ ] Reviewer signoff: Qwen Code
- **Estimated**: 6 hours

### **1.3: Langfuse Agent Integration** 📊 **HIGH**

#### **Task 1.3.1: Agent Session Management**
- **Implementer**: Qwen Code
- **Reviewer**: Gemini CLI
- **Scope**: Automatic Langfuse session creation for registered agents
- **Files**: `app/src/services/langfuse_agent_manager.py`
- **Requirements**:
  ```python
  class LangfuseAgentManager:
      def create_agent_session(self, agent_id: str) -> str
      def track_task_execution(self, agent_id: str, task_data: dict) -> None
      def log_agent_communication(self, from_agent: str, to_agent: str, message: str) -> None
      def get_agent_analytics(self, agent_id: str, timeframe: str) -> dict
  ```
- **Acceptance Criteria**:
  - [ ] Sessions auto-created on agent registration
  - [ ] All agent activities tracked
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Dashboard shows agent metrics
  - [ ] Reviewer signoff: Gemini CLI
- **Estimated**: 7 hours

---

## 🏗️ **Phase 2: Critical Service Restoration (Week 2)**

### **2.1: memOS.as Service Deployment** 🚨 **CRITICAL**

#### **Task 2.1.1: Container Configuration Fix**
- **Implementer**: GitHub Copilot
- **Reviewer**: Gemini CLI
- **Scope**: Fix missing memOS.as container in Docker stack
- **Files**: `docker-compose.unified.yml`, `memos.as/Dockerfile`
- **Requirements**:
  ```yaml
  memos-api:
    build: ./memos.as
    ports:
      - "8092:8000"
    environment:
      - DATABASE_URL=${MEMOS_DATABASE_URL}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  ```
- **Acceptance Criteria**:
  - [ ] Container builds successfully
  - [ ] Health check responds on port 8092
  - [ ] Database connections work
  - [ ] API endpoints accessible
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes  
  - [ ] Reviewer signoff: Gemini CLI
- **Estimated**: 4 hours

#### **Task 2.1.2: Memory Operations API**
- **Implementer**: Gemini CLI
- **Reviewer**: Qwen Code
- **Scope**: Implement core memory CRUD operations
- **Files**: `memos.as/app/api/memory.py`
- **Requirements**:
  ```python
  POST /api/v1/memory/store
  GET /api/v1/memory/retrieve
  PUT /api/v1/memory/update
  DELETE /api/v1/memory/delete
  GET /api/v1/memory/search
  ```
- **Acceptance Criteria**:
  - [ ] All endpoints functional
  - [ ] Vector search implemented
  - [ ] Session context maintained
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Reviewer signoff: Qwen Code
- **Estimated**: 8 hours

### **2.2: POML Prompt Library Implementation** 📚 **HIGH**

#### **Task 2.2.1: Template Engine Development**
- **Implementer**: Qwen Code
- **Reviewer**: GitHub Copilot
- **Scope**: Implement POML template processing engine
- **Files**: `devenviro.as/app/src/services/poml/engine.py`
- **Requirements**:
  ```python
  class POMLEngine:
      def load_template(self, template_name: str) -> POMLTemplate
      def render_prompt(self, template: POMLTemplate, context: dict) -> str
      def validate_template(self, template_content: str) -> bool
      def list_available_templates(self) -> List[str]
  ```
- **Acceptance Criteria**:
  - [ ] Template validation works
  - [ ] Context variable substitution
  - [ ] Error handling for malformed templates
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Reviewer signoff: GitHub Copilot
- **Estimated**: 6 hours

#### **Task 2.2.2: Core POML Templates**
- **Implementer**: GitHub Copilot
- **Reviewer**: Gemini CLI
- **Scope**: Create functional POML template content
- **Files**: `devenviro.as/app/src/services/poml/templates/*.poml`
- **Requirements**:
  ```poml
  # agent_communication.poml
  AGENT_CONTEXT: {{agent_name}} communicating with {{target_agent}}
  TASK: {{task_description}}
  EXPECTED_OUTPUT: {{output_format}}
  
  # task_orchestration.poml  
  ORCHESTRATION_CONTEXT: Managing {{task_count}} tasks
  PRIORITY_MATRIX: {{priority_assignments}}
  RESOURCE_ALLOCATION: {{resource_mapping}}
  ```
- **Acceptance Criteria**:
  - [ ] All template files have content (not empty)
  - [ ] Templates validate successfully
  - [ ] Context variables properly defined
  - [ ] Documentation for each template
  - [ ] Reviewer signoff: Gemini CLI
- **Estimated**: 5 hours

### **2.3: Test Coverage Infrastructure** 🧪 **HIGH**

#### **Task 2.3.1: Pre-commit Hook Configuration**
- **Implementer**: Gemini CLI
- **Reviewer**: GitHub Copilot
- **Scope**: Fix test coverage enforcement to actual 80%
- **Files**: `.pre-commit-config.yaml` (all projects)
- **Requirements**:
  ```yaml
  - id: pytest-check
    args: [
      "--cov=app",
      "--cov-fail-under=80",  # Fixed from 2%
      "--strict-markers"
    ]
  ```
- **Acceptance Criteria**:
  - [ ] All projects use 80% coverage threshold
  - [ ] Pre-commit hooks block commits below threshold
  - [ ] Coverage reports generated
  - [ ] CI/CD pipeline integration
  - [ ] Reviewer signoff: GitHub Copilot
- **Estimated**: 3 hours

---

## 🔒 **CRITICAL INFRASTRUCTURE MONITORING**

### **Protected Services 24/7 Health Monitoring**
**MANDATORY**: All Tier 1 services require continuous monitoring with immediate alerts

#### **Health Check Requirements**
- **memOS API** (`172.26.0.13:8090`): Health check every 30 seconds
  ```bash
  curl -f http://172.26.0.13:8090/health
  # Alert if: response time >2s, any service "disconnected", operational_mode != "full"
  ```

- **Neo4j Knowledge Graph** (`172.26.0.14:7687`): Connectivity check every 60 seconds
  ```bash
  docker exec apexsigma_neo4j cypher-shell -u neo4j -p apexsigma_neo4j_password "RETURN 1"
  # Alert if: connection fails, query timeout >10s
  ```

- **PostgreSQL Main** (`172.26.0.2:5432`): Status check every 30 seconds
  ```bash
  docker exec apexsigma_postgres pg_isready -U apexsigma_user
  # Alert if: not accepting connections, response time >5s
  ```

- **InGest-LLM API** (`172.26.0.12:8000`): Health check every 60 seconds  
  ```bash
  curl -f http://172.26.0.12:8000/health
  # Alert if: HTTP error, response time >3s, service unavailable
  ```

#### **Alert Thresholds**
- **<99% uptime** on any protected service: **IMMEDIATE CRITICAL ALERT**
- **Failed health check**: Alert after 2 consecutive failures (60s max)
- **Response time degradation**: Alert if >200% of baseline response time
- **Knowledge graph inconsistency**: Alert on Neo4j constraint violations

#### **Automated Recovery Procedures**
- **Container restart**: Automatic restart after 3 failed health checks
- **Service dependency check**: Verify all dependent services before restart
- **Rollback capability**: Automatic rollback to last known good configuration
- **Manual escalation**: Human operator notification after 3 automatic recovery attempts

#### **Emergency Response Protocol**
1. **Immediate isolation** of affected service
2. **Assessment** of impact on Omega Ingest integrity
3. **Backup activation** where available
4. **Data integrity verification** before service restoration
5. **Post-incident review** and prevention planning

---

## 📚 **Phase 3: Documentation & Tools Restoration (Week 3)**

### **3.1: Automated MkDocs Implementation** 📖 **HIGH**

#### **Task 3.1.1: MkDocs Build System**
- **Implementer**: GitHub Copilot
- **Reviewer**: Qwen Code
- **Scope**: Restore automated documentation generation
- **Files**: `scripts/build_ecosystem_docs.py`, `mkdocs.yml` (each project)
- **Requirements**:
  ```python
  class EcosystemDocsBuilder:
      def build_project_docs(self, project_name: str) -> bool
      def serve_docs(self, project_name: str, port: int) -> None
      def validate_doc_links(self, project_name: str) -> List[str]
      def generate_unified_index(self) -> str
  ```
- **Acceptance Criteria**:
  - [ ] All projects build documentation successfully
  - [ ] Live reload during development
  - [ ] Cross-project link validation
  - [ ] Unified ecosystem documentation index
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Reviewer signoff: Qwen Code
- **Estimated**: 8 hours

### **3.2: Agent Tools Integration** 🛠️ **MEDIUM**

#### **Task 3.2.1: Scratchpad Service**
- **Implementer**: Qwen Code
- **Reviewer**: Gemini CLI
- **Scope**: Implement agent scratchpad for temporary storage
- **Files**: `tools.as/app/services/scratchpad.py`
- **Requirements**:
  ```python
  class AgentScratchpad:
      def create_note(self, agent_id: str, content: str) -> str
      def get_notes(self, agent_id: str, session_id: str = None) -> List[Note]
      def update_note(self, note_id: str, content: str) -> bool
      def delete_note(self, note_id: str) -> bool
      def search_notes(self, agent_id: str, query: str) -> List[Note]
  ```
- **Acceptance Criteria**:
  - [ ] Session-based note organization
  - [ ] Full-text search capability
  - [ ] Notes auto-expire after inactivity
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Reviewer signoff: Gemini CLI
- **Estimated**: 6 hours

#### **Task 3.2.2: Shared Todo System**
- **Implementer**: Gemini CLI  
- **Reviewer**: GitHub Copilot
- **Scope**: Implement agent-accessible todo management
- **Files**: `tools.as/app/services/agent_todos.py`
- **Requirements**:
  ```python
  class AgentTodoSystem:
      def create_task(self, agent_id: str, title: str, description: str) -> str
      def assign_task(self, task_id: str, assignee_agent_id: str) -> bool
      def update_task_status(self, task_id: str, status: TaskStatus) -> bool
      def get_agent_tasks(self, agent_id: str, status: TaskStatus = None) -> List[Task]
      def get_team_backlog(self) -> List[Task]
  ```
- **Acceptance Criteria**:
  - [ ] Multi-agent task assignment
  - [ ] Task status workflows
  - [ ] Priority and deadline management
  - [ ] Team visibility into all tasks
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Reviewer signoff: GitHub Copilot
- **Estimated**: 7 hours

---

## 🔧 **Phase 4: Integration & Validation (Week 4)**

### **4.1: End-to-End Integration Testing** 🧪 **CRITICAL**

#### **Task 4.1.1: MAR Protocol Integration Test**
- **Implementer**: GitHub Copilot
- **Reviewer**: Qwen Code
- **Scope**: Comprehensive MAR workflow testing
- **Files**: `tests/integration/test_mar_protocol.py`
- **Requirements**:
  ```python
  def test_complete_mar_workflow():
      # Test task creation → implementation → review → approval → commit
  
  def test_quality_gate_failures():
      # Test pytest/ruff failures block review
  
  def test_reviewer_rejection_workflow():
      # Test rejection → feedback → re-implementation → re-review
  ```
- **Acceptance Criteria**:
  - [ ] Full MAR workflow tested end-to-end
  - [ ] All failure scenarios covered
  - [ ] Performance benchmarks established
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Reviewer signoff: Qwen Code
- **Estimated**: 8 hours

#### **Task 4.1.2: Agent Registry Integration Test**
- **Implementer**: Qwen Code
- **Reviewer**: Gemini CLI
- **Scope**: Test complete agent lifecycle management
- **Files**: `tests/integration/test_agent_registry.py`
- **Requirements**:
  ```python
  def test_agent_registration_lifecycle():
      # Test registration → heartbeat → task assignment → deregistration
  
  def test_langfuse_session_integration():
      # Test automatic session creation and tracking
  
  def test_multi_agent_coordination():
      # Test agent-to-agent communication and task handoffs
  ```
- **Acceptance Criteria**:
  - [ ] All agent registry functions tested
  - [ ] Langfuse integration validated
  - [ ] Multi-agent scenarios covered
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Reviewer signoff: Gemini CLI
- **Estimated**: 7 hours

### **4.2: Performance & Reliability Validation** ⚡ **HIGH**

#### **Task 4.2.1: System Performance Benchmarks**
- **Implementer**: Gemini CLI
- **Reviewer**: GitHub Copilot
- **Scope**: Establish performance baselines for all services
- **Files**: `tests/performance/benchmark_suite.py`
- **Requirements**:
  - memOS.as: <100ms response time for memory operations
  - DevEnviro registry: <50ms for agent status checks
  - POML rendering: <500ms for complex templates
  - MAR workflow: <2s for complete task submission
- **Acceptance Criteria**:
  - [ ] All performance targets met
  - [ ] Benchmark suite runs automatically
  - [ ] Performance regression detection
  - [ ] pytest coverage ≥80%
  - [ ] ruff linting passes
  - [ ] Reviewer signoff: GitHub Copilot
- **Estimated**: 6 hours

---

## 📋 **Quality Gate Requirements**

### **Universal Requirements for ALL Tasks**
Every task must meet these criteria before review:

1. **Code Quality**:
   - [ ] pytest coverage ≥80%
   - [ ] ruff linting passes with zero errors
   - [ ] Type hints for all functions
   - [ ] Comprehensive docstrings

2. **Testing Requirements**:
   - [ ] Unit tests for all public methods
   - [ ] Integration tests for API endpoints
   - [ ] Error condition testing
   - [ ] Mock external dependencies

3. **Documentation**:
   - [ ] README updates if applicable
   - [ ] API documentation generated
   - [ ] Code comments for complex logic
   - [ ] Change log entries

4. **Review Process**:
   - [ ] Code submitted for assigned reviewer
   - [ ] Reviewer approval documented
   - [ ] All feedback addressed
   - [ ] Final signoff recorded

### **Commit Protocol**
Only after ALL criteria met:
1. **Quality Gates Pass**: Automated checks succeed
2. **Reviewer Approval**: Designated reviewer signs off
3. **MAR Documentation**: Review logged in MAR system
4. **Commit Processing**: Changes merged to main branch
5. **Status Update**: Task marked complete in tracking system

---

## 🎯 **Success Criteria**

### **Phase 1 Success (End of Week 1)**
- [ ] All agents registered in DevEnviro registry
- [ ] MAR protocol operational with quality gates
- [ ] Langfuse tracking all agent activities
- [ ] Basic agent communication established

### **Phase 2 Success (End of Week 2)**
- [ ] memOS.as service operational (actual 99%+ uptime)
- [ ] POML library functional (no empty files)
- [ ] Test coverage actually enforced at 80%
- [ ] All critical services responding to health checks

### **Phase 3 Success (End of Week 3)**
- [ ] MkDocs automatically generating current documentation
- [ ] Agent scratchpad and todo systems operational
- [ ] Cross-project documentation links validated
- [ ] All services documented with current status

### **Phase 4 Success (End of Week 4)**
- [ ] End-to-end MAR workflow tested and validated
- [ ] Performance benchmarks established and met
- [ ] Complete integration testing passed
- [ ] Zero implementation gaps between documentation and reality

### **Operation Success (Overall)**
- [ ] **No more documentation drift**: All claims verified
- [ ] **Quality enforcement**: 80% coverage + ruff + review required
- [ ] **Agent accountability**: Every task has implementer + reviewer
- [ ] **Progress protection**: MAR protocol prevents regression
- [ ] **Operational excellence**: Verified uptime and performance metrics

---

## ⚠️ **Risk Mitigation**

### **High-Risk Items & Mitigations**
1. **Agent Coordination Complexity**
   - **Risk**: Agents may not follow MAR protocol
   - **Mitigation**: Enforce quality gates before review stage
   - **Contingency**: Manual review override for critical fixes

2. **Quality Gate Performance Impact**
   - **Risk**: 80% coverage requirement may slow development
   - **Mitigation**: Parallel test development with implementation
   - **Contingency**: Temporary threshold reduction for non-critical paths

3. **Documentation System Complexity**
   - **Risk**: MkDocs automation may fail for complex projects
   - **Mitigation**: Incremental implementation with fallback to manual builds
   - **Contingency**: Project-by-project documentation deployment

### **Success Dependencies**
- **Agent Availability**: All 3 implementation agents must be available
- **Review Commitment**: Agents must commit to review responsibilities  
- **Quality Standards**: No compromise on coverage and linting requirements
- **Progress Tracking**: Regular status updates and blocker escalation

---

## 🏆 **Operation Legacy**

**Operation Asgard Rebirth** establishes the foundation for:

1. **Sustainable Development**: Quality gates prevent regression
2. **Agent Collaboration**: MAR protocol ensures accountability
3. **Progress Protection**: Documentation matches implementation reality
4. **Operational Excellence**: Verified metrics and performance standards
5. **Knowledge Preservation**: Comprehensive tracking and documentation

**Upon completion, the ApexSigma ecosystem will have**:
- Verified 80%+ test coverage enforcement
- Mandatory agent review protocol operational
- All services actually running (not just documented)
- Real-time agent tracking and communication
- Automated documentation generation
- Zero tolerance for implementation/documentation drift

---

*Operation Asgard Rebirth: Where implementation meets accountability, and progress becomes permanent.*