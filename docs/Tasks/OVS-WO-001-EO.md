# 📋 WORK ORDER EXECUTION INSTRUCTIONS
```yaml
Title: Fix Application Service Dependencies
Task ID: OVS-WO-001
Priority: CRITICAL (Phase 0 Blocker)
Implementer: @iFlow
Reviewer: @Qwen
```

## 🎯 MISSION OBJECTIVE

__PRIMARY GOAL__: Restore core application services (memos.as & devenviro.as) to operational state by resolving all ModuleNotFoundError dependency issues.

__STRATEGIC IMPORTANCE__: This is the Phase 0 foundation blocker - no further ecosystem development can proceed until these services are operational.

### 🔍 CURRENT SITUATION ANALYSIS

Verified Dependencies Status (from [VERIFIED_DOCKER_NETWORK_MAP_V2.md](../VERIFIED_DOCKER_NETWORK_MAP_V2.md)):

✅ memos.as pyproject.toml - Contains required dependencies:

langfuse = ">=2.0.0,<3.0.0" ✅
qdrant-client = ">=1.0.0,<2.0.0" ✅
structlog = ">=20.0.0,<30.0.0" ✅

✅ devenviro.as pyproject.toml - Contains required dependencies:

langfuse = "*" ✅
qdrant-client = ">=1.7.0" ✅

__Root Cause Analysis__

The dependencies appear to be declared but may not be properly installed or there may be version conflicts in the poetry.lock files.

## ⚡ EXECUTION PROTOCOL

__Phase 1__: Dependency Audit & Validation

Check Current Poetry Lock Status

```powershell
cd services/memos.as
poetry show --tree
poetry check
```
Check DevEnviro Dependencies

```powershell
cd services/devenviro.as
poetry show --tree
poetry check
```

Identify Missing or Conflicting Dependencies

Compare poetry show output with pyproject.toml declarations
Look for version conflicts in dependency resolution
Check for missing system-level dependencies
Phase 2: Dependency Resolution
Clear Existing Locks (if corrupted)


## For each service

Update Dependencies with Explicit Versions

Ensure all critical dependencies have compatible version ranges
Update to latest stable versions where possible
Fix any version conflicts identified in Phase 1
Verify Core Dependencies

```powershell
poetry run python -c "import langfuse; print('langfuse OK')"poetry run python -c "import qdrant_client; print('qdrant-client OK')"  poetry run python -c "import structlog; print('structlog OK')"
```
Phase 3: Service Startup Testing/

Test memos.as Service Startup

```powershell
cd services/memos.as
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8090 --reload
# Monitor logs for ModuleNotFoundError exceptions
```
Test devenviro.as Service Startup

```powershell
cd services/devenviro.as
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
# Monitor logs for ModuleNotFoundError exceptions
```

__Docker Container Testing__

```powershell
cd services/memos.as
# Test via docker-compose
docker-compose -f docker-compose.unified.yml up apexsigma_memos_api -d
docker-compose -f docker-compose.unified.yml logs apexsigma_memos_api
```
## Phase 4: Quality Assurance

__Run Trunk Quality Checks__

```powershell
trunk check --ci
trunk fmt
```

__Test Suite Execution__


## For each service

Health Endpoint Validation

```curl
curl -f http://localhost:8090/health  # memos.as
curl -f http://localhost:8000/health  # devenviro.as (if applicable)
```
### ✅ "DONE MEANS DONE" VERIFICATION CHECKLIST

__Criterion 1__:

 memos.as Service Operational
 poetry install completes without errors
 Service starts without ModuleNotFoundError exceptions
 All imports (langfuse, qdrant_client, structlog) succeed
 Health endpoint responds successfully
 Docker container starts and maintains healthy status

__Criterion 2__: 
 
 devenviro.as Service Operational
 poetry install completes without errors
 Service starts without ModuleNotFoundError exceptions
 All imports succeed (including langfuse, qdrant_client)
 Service can be accessed via configured port
 Docker container starts and maintains healthy status

__Criterion 3__: 

 Repository Compliance
 pyproject.toml files updated with correct dependency versions
 poetry.lock files regenerated and committed
 All changes committed to repository with clear commit messages
 Branch ready for Pull Request submission

__Criterion 4__: 

 Valhalla Shield Compliance
 trunk check --ci passes with no failures
 All formatting issues resolved via trunk fmt
 Test suites pass (if applicable)
 No security vulnerabilities introduced
 PR checklist requirements met

## 🚨 KNOWN POTENTIAL ISSUES & SOLUTIONS

__Issue 1__: 

 Python Version Conflicts
 Symptom: Poetry fails to resolve dependencies Solution: Ensure all services use compatible Python version ranges (>=3.9 vs >=3.13)

__Issue 2__: 

 Path Dependencies
 Symptom: apexsigma-core path dependency issues Solution: Verify apexsigma-core path exists and is accessible

__Issue 3__: 

 Docker Build Context
 Symptom: Docker builds fail due to missing dependencies
 Solution: Ensure Dockerfile properly copies and installs from poetry files

__Issue 4__: 

 Version Pinning Conflicts
 Symptom: Dependencies can't be resolved due to conflicting version requirements Solution: Use broader version ranges or update conflicting packages

### 📊 SUCCESS METRICS

 Zero ModuleNotFoundError exceptions in service startup logs
 Successful Docker container startup for both services
 Clean poetry check output for both services
 Passing trunk quality gates
 Functional health endpoints (where implemented)

### 🔄 HANDOFF PROTOCOL

Implementation Completion Signal

Upon completion, @iFlow must:

 ✅ Update this work order with completion status
 📋 Create Implementation Report documenting:
 Changes made to each pyproject.toml
 Dependency versions resolved
 Testing results and verification logs
 Any issues encountered and solutions applied
 🔗 Submit Pull Request with all changes
 📢 Notify @Qwen for MAR Protocol review

Review Trigger

@Qwen review begins when:

 Implementation Report is complete
 Pull Request is submitted
 All "Done Means Done" criteria claimed as met
 Services demonstrably operational

### 📚 REFERENCE DOCUMENTS

[Network topology and service configurations](VERIFIED_DOCKER_NETWORK_MAP_V2.md)
[Review process requirements](MAR Protocol Documentation.md)
[Quality and compliance requirements](Valhalla Shield Engineering Standard v1.2.md)
[Strategic context and Phase 0 objectives](Operation Asgard Rebirth Plan.md)

**AUTHORIZATION**: SigmaDev11 (Human Orchestrator)
**ISSUED**: September 29, 2025
**STATUS**: ACTIVE - IMMEDIATE EXECUTION REQUIRED