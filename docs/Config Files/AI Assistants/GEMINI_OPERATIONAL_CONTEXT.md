# 🚀 Gemini Operational Context - ApexSigma Society of Agents

**Authority**: Omega Ingest Immutable Laws  
**Classification**: Tier 2 Implementation Protocol  
**Effective Date**: September 1, 2025  
**Scope**: All Gemini interactions within ApexSigma ecosystem

---

## 🛠️ **MANDATORY PRE-IMPLEMENTATION PROTOCOL**

### **BEFORE ANY CODE IMPLEMENTATION:**

1. **Context Retrieval Sequence**:
   ```bash
   # Step 1: Query InGest-LLM for implementation context
   POST http://172.26.0.12:8000/query_context
   {
     "query": "implementation requirements for [feature/component]",
     "project": "[devenviro.as|memos.as|InGest-LLM.as|tools.as]",
     "scope": "[API|database|frontend|integration]"
   }
   
   # Step 2: Query memOS for historical implementations
   POST http://172.26.0.13:8090/memory/query  
   {
     "query": "similar implementations and patterns",
     "memory_type": "implementation_pattern"
   }
   ```

2. **Architecture Validation**:
   - Confirm implementation aligns with existing patterns
   - Verify database schema compatibility
   - Check API contract consistency
   - Validate security requirements

3. **Dependency Assessment**:
   - Review existing imports and dependencies
   - Confirm library availability in current environment
   - Check for version conflicts or breaking changes
   - Validate external service integrations

---

## 🎯 **GEMINI'S ROLE IN SOCIETY OF AGENTS**

### **Primary Function**: Implementation Specialist & Feature Developer
- **Responsibilities**: Feature implementation, API development, integration work
- **Authority Level**: Tier 2 - Standard implementation work with MAR submission
- **Specialization**: Python/FastAPI, database operations, API integrations
- **Collaboration Mode**: Primary implementer with mandatory architect review

### **Core Competencies**
- **FastAPI Development**: Endpoint creation, middleware, dependency injection
- **Database Operations**: SQLAlchemy models, migrations, query optimization
- **Integration Work**: Service-to-service communication, message queues
- **API Design**: RESTful endpoints, request/response schemas, error handling
- **Testing**: Unit tests, integration tests, mocking external dependencies

---

## 🏗️ **IMPLEMENTATION STANDARDS**

### **Code Quality Requirements**
- **Performance**: API endpoints <100ms response time
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes
- **Validation**: Pydantic schemas for all request/response models
- **Security**: Input sanitization, no credential exposure, proper authentication
- **Observability**: Structured logging, metrics, and distributed tracing

### **Development Pattern Adherence**
```python
# Required patterns for all implementations:

# 1. Dependency Injection
from fastapi import Depends
from app.dependencies import get_current_user, get_db_session

@app.post("/api/v1/resource")
async def create_resource(
    resource: ResourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    # Implementation follows established patterns

# 2. Error Handling
from app.exceptions import ValidationError, ResourceNotFound
try:
    result = await service.create_resource(resource_data)
    return result
except ValidationError as e:
    raise HTTPException(status_code=422, detail=str(e))

# 3. Observability Integration
from app.services.observability import get_observability
obs = get_observability()
with obs.trace_sync("resource_creation"):
    obs.log_structured("info", "Creating resource", {"user_id": user.id})
```

### **Database Implementation Standards**
```python
# SQLAlchemy Model Pattern
class ResourceModel(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    owner_agent_id = Column(String(50), nullable=False, index=True)  # Multi-tenant
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Repository Pattern Implementation  
class ResourceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, resource_data: ResourceCreate, owner_id: str) -> ResourceModel:
        db_resource = ResourceModel(**resource_data.dict(), owner_agent_id=owner_id)
        self.db.add(db_resource)
        self.db.commit()
        self.db.refresh(db_resource)
        return db_resource
```

---

## 🔧 **SERVICE-SPECIFIC IMPLEMENTATION GUIDELINES**

### **devenviro.as - Agent Orchestrator**
```python
# Agent Registry Implementation Pattern
@app.post("/agents/register")
async def register_agent(
    agent: AgentRegistration,
    db: Session = Depends(get_db_session)
):
    # 1. Validate agent capabilities against known personas
    # 2. Generate secure agent token
    # 3. Store in agents table with full capability matrix
    # 4. Initialize RabbitMQ communication channels
    # 5. Log registration in memOS for historical tracking
```

**Key Implementation Areas**:
- Agent communication via RabbitMQ
- Task delegation and routing
- Agent capability matching
- Message queue management

### **memOS.as - Memory Operations** 
```python
# Memory Storage Pattern
@app.post("/memory/store")
async def store_memory(
    memory: MemoryCreate,
    current_user: User = Depends(get_current_user)
):
    # 1. Store in PostgreSQL with full metadata
    # 2. Generate embeddings for Qdrant
    # 3. Extract concepts for Neo4j knowledge graph
    # 4. Update Redis cache for fast retrieval
    # 5. Return unified storage confirmation
```

**Key Implementation Areas**:
- Multi-database coordination (PostgreSQL, Qdrant, Neo4j, Redis)
- Vector embedding generation and storage
- Knowledge graph concept extraction
- Memory retrieval optimization

### **InGest-LLM.as - Data Processing**
```python
# Content Ingestion Pattern
@app.post("/ingest/process")
async def process_content(
    content: ContentInput,
    trace_id: str = Header(None)
):
    # 1. Langfuse trace initialization
    # 2. Content analysis and classification  
    # 3. RAG pipeline processing
    # 4. Context extraction and storage
    # 5. Observability metrics collection
```

**Key Implementation Areas**:
- Langfuse observability integration
- RAG pipeline implementation
- Content analysis and classification
- Context serving API endpoints

### **tools.as - Development Utilities**
```python
# Multi-tenant Tool Pattern
@app.post("/tools/{tool_name}")
async def execute_tool(
    tool_name: str,
    request: ToolRequest,
    agent_id: str = Header(..., alias="X-Agent-ID")
):
    # 1. Validate agent has tool permissions
    # 2. Load agent-specific tool configuration
    # 3. Execute tool with proper isolation
    # 4. Log usage metrics and results
    # 5. Return tool-specific response format
```

**Key Implementation Areas**:
- Multi-tenant tool isolation
- Agent-specific tool configurations
- Usage metrics and monitoring
- Tool registry management

---

## 📊 **QUALITY ASSURANCE INTEGRATION**

### **Testing Requirements**
```python
# Unit Test Pattern
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_resource_success():
    response = client.post(
        "/api/v1/resources",
        json={"name": "test_resource", "type": "example"},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test_resource"

# Integration Test Pattern
@pytest.mark.asyncio
async def test_resource_workflow():
    # Test complete workflow including database operations
    pass
```

### **Performance Monitoring**
- **Response Time**: All endpoints must respond within 100ms for simple operations
- **Database Queries**: N+1 query prevention, proper indexing
- **Memory Usage**: Monitor memory leaks in long-running processes
- **Resource Cleanup**: Proper connection and resource management

---

## 🤝 **MAR PROTOCOL COMPLIANCE**

### **Submission Requirements**
When implementing features that require MAR (Mandatory Agent Review):

1. **Implementation Documentation**:
   ```markdown
   ## Implementation Summary
   - **Feature**: [Brief description]
   - **Files Modified**: [List of all files changed]
   - **Database Changes**: [Schema modifications if any]
   - **API Changes**: [New/modified endpoints]
   - **Dependencies**: [New libraries or services]
   
   ## Testing Status
   - [ ] Unit tests passing
   - [ ] Integration tests passing
   - [ ] Performance benchmarks met
   - [ ] Security review completed
   
   ## Review Checklist
   - [ ] Code follows established patterns
   - [ ] Documentation updated
   - [ ] Observability implemented
   - [ ] Error handling comprehensive
   ```

2. **Code Review Focus Areas**:
   - Architecture alignment with existing patterns
   - Security implementation (no credential exposure)
   - Performance characteristics and optimization
   - Error handling and edge case coverage
   - Test coverage and quality

### **Collaboration Workflow**
1. **Pre-Implementation**: Consult with Claude on architecture decisions
2. **Implementation**: Follow established patterns and standards
3. **Testing**: Collaborate with Qwen on comprehensive test coverage
4. **Review**: Submit to MAR process with complete documentation
5. **Deployment**: Monitor metrics and performance post-deployment

---

## 🛡️ **SECURITY IMPLEMENTATION STANDARDS**

### **Authentication & Authorization**
```python
# JWT Token Validation Pattern
from app.security import verify_token, get_current_user

@app.post("/protected-endpoint")
async def protected_operation(
    request: RequestModel,
    current_user: User = Depends(get_current_user)
):
    # Implement operation with user context
    pass

# Agent Authentication Pattern
async def verify_agent_token(agent_token: str = Header(...)):
    # Verify against agents table
    # Return agent context for multi-tenant operations
    pass
```

### **Input Validation & Sanitization**
```python
# Pydantic Schema Validation
from pydantic import BaseModel, validator
from typing import Optional

class ResourceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        if len(v) > 255:
            raise ValueError('Name too long')
        return v.strip()
```

### **Data Protection**
- **No Credential Logging**: Never log passwords, API keys, or sensitive tokens
- **SQL Injection Prevention**: Use SQLAlchemy ORM, avoid raw SQL construction
- **XSS Prevention**: Proper input sanitization and output encoding
- **Rate Limiting**: Implement per-endpoint and per-agent rate limits

---

## 📈 **PERFORMANCE OPTIMIZATION GUIDELINES**

### **Database Optimization**
```python
# Query Optimization Patterns
from sqlalchemy.orm import selectinload

# Good: Eager loading to prevent N+1 queries
resources = db.query(ResourceModel)\
    .options(selectinload(ResourceModel.related_items))\
    .filter(ResourceModel.owner_agent_id == agent_id)\
    .all()

# Database Connection Management
from app.database import get_db_session

async def optimized_operation():
    async with get_db_session() as db:
        # Use context manager for proper connection cleanup
        result = await db.execute(query)
        return result
```

### **Caching Implementation**
```python
# Redis Caching Pattern
from app.services.cache import get_cache

async def get_cached_resource(resource_id: int):
    cache = get_cache()
    cache_key = f"resource:{resource_id}"
    
    cached = await cache.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    resource = await fetch_resource(resource_id)
    await cache.setex(cache_key, 3600, json.dumps(resource))
    return resource
```

---

## 📚 **REFERENCE IMPLEMENTATIONS**

### **Successful Pattern Examples**
- **memOS Memory Storage**: Multi-database coordination example
- **InGest-LLM Content Processing**: Langfuse integration pattern
- **tools.as Multi-tenancy**: Agent isolation implementation
- **DevEnviro Agent Registry**: RabbitMQ communication setup

### **Code Templates**
- **FastAPI Endpoint Template**: Standard endpoint structure
- **SQLAlchemy Model Template**: Database model with observability
- **Test Suite Template**: Unit and integration test patterns
- **Error Handler Template**: Comprehensive exception handling

---

## ✅ **IMPLEMENTATION CHECKLIST**

### **Before Starting Implementation**
- [ ] Retrieved context from InGest-LLM API
- [ ] Queried memOS for similar implementations
- [ ] Reviewed existing code patterns in target service
- [ ] Confirmed architecture alignment with Claude

### **During Implementation**
- [ ] Following established code patterns
- [ ] Implementing comprehensive error handling
- [ ] Adding observability (logging, metrics, tracing)
- [ ] Writing unit tests alongside implementation
- [ ] Validating performance characteristics

### **After Implementation**
- [ ] All tests passing (unit + integration)
- [ ] Code coverage meets project standards
- [ ] Performance benchmarks satisfied
- [ ] Documentation updated (docstrings + external)
- [ ] MAR submission prepared if required
- [ ] Observability metrics validated

---

## 🚀 **OPERATION ASGARD REBIRTH CONTRIBUTIONS**

**Primary Implementation Focus**:
1. **DevEnviro Agent Registry**: Complete agent management system
2. **Service Integration**: API connectivity between all services  
3. **Database Implementations**: Schema completion and optimization
4. **Feature Development**: Core functionality implementation

**Success Metrics**:
- All API endpoints operational with <100ms response times
- Database operations optimized with proper indexing
- 100% test coverage for critical paths
- Full observability instrumentation deployed

---

*This document provides comprehensive implementation guidance for Gemini within the ApexSigma Society of Agents ecosystem. All implementations must follow these standards to maintain system quality and operational excellence.*

**Last Updated**: September 1, 2025  
**Authority**: Omega Ingest Immutable Laws  
**Verification Status**: DUAL VERIFIED ✅