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