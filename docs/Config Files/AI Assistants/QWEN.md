# QWEN.md

**Qwen Code Assistant Instructions for ApexSigma Ecosystem**

## � **MANDATORY: OMEGA INGEST CONTEXT RETRIEVAL PROTOCOL**

**BEFORE MAKING ANY CODE CHANGES**, you MUST:

1. **Query InGest-LLM API** for relevant context: `http://172.26.0.12:8000/query_context`
2. **Retrieve from memOS Omega Ingest**: `http://172.26.0.13:8090/memory/query` 
3. **Validate against immutable truth**: Ensure changes don't conflict with verified infrastructure
4. **Obtain dual verification**: For Tier 1 infrastructure changes, require verification from another AI assistant

**Protected Services (DO NOT MODIFY WITHOUT VERIFICATION)**:
- memOS API (172.26.0.13) - Omega Ingest Guardian
- Neo4j Knowledge Graph (172.26.0.14) - Immutable concept relationships  
- PostgreSQL Main (172.26.0.2) - Procedural memory
- InGest-LLM API (172.26.0.12) - Data ingestion gateway

**Your Role in Operation Asgard Rebirth**: 
- **Primary**: Specialized AI/ML component implementation
- **MAR Protocol**: Act as reviewer for Gemini CLI and GitHub Copilot implementations
- **Verification Authority**: Tier 2-3 changes (application logic, documentation)

**Reference**: `/project_support/secure_verified_docs/OMEGA_INGEST_LAWS.md` for complete protoco

