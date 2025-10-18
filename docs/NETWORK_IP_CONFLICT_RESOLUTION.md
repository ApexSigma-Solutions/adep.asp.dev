# Network IP Conflict Resolution

**Date**: October 18, 2025  
**Status**: 🔴 CRITICAL - Blocks infrastructure deployment  
**Severity**: HIGH - Prevents ClickHouse, Langfuse, Dagster, Vault deployment

---

## Problem Statement

Infrastructure services defined in `docker-compose.unified.yml` cannot start due to network subnet mismatch:

- **Expected Subnet** (per docker-compose): `172.26.0.0/16`
- **Actual Subnet** (external network): `172.21.0.0/16`

### Affected Services

| Service | Hardcoded IP | Status | Impact |
|---------|-------------|--------|--------|
| ClickHouse | 172.26.0.50 | ❌ Cannot start | No analytics storage for Langfuse or observability |
| Langfuse | 172.26.0.52 | ❌ Cannot start | No AI trace analytics |
| Dagster webserver | 172.26.0.51 | ❌ Cannot start | No workflow orchestration UI |
| Dagster daemon | 172.26.0.53 | ❌ Cannot start | No background task processing |
| Vector | 172.26.0.54 | ❌ Cannot start | Degraded log collection pipeline |

### Error Message

```
Error response from daemon: invalid config for network apexsigma_net: invalid endpoint settings:
no configured subnet or ip-range contain the IP address 172.26.0.50
```

---

## Root Cause Analysis

### Timeline of Configuration Drift

1. **Phase 0 Infrastructure**: External Docker network `apexsigma_net` created with subnet `172.21.0.0/16`
2. **Service Development**: Services deployed with dynamic IPs (working correctly in 172.21.0.0/16 range)
3. **Documentation Update**: `VERIFIED_DOCKER_NETWORK_MAP_V3.md` documented expected range as `172.26.0.0/16`
4. **docker-compose.unified.yml**: Later revisions hardcoded static IPs in 172.26.0.0/16 range for new services
5. **Deployment Failure**: New infrastructure services can't join network due to IP mismatch

### Why This Happened

- **External Network Declaration**: `docker-compose.unified.yml` line 858 declares `apexsigma_net: external: true`
- **No Subnet Specification**: When network is external, docker-compose can't create or modify it
- **Manual Network Creation**: Someone created `apexsigma_net` with `172.21.0.0/16` instead of documented `172.26.0.0/16`
- **No Validation**: No pre-flight checks to verify network subnet matches expected range

---

## Current Network State

### Active Containers (172.21.0.0/16)

```
apexsigma_postgres      172.21.0.3/16  ✅ Healthy
apexsigma_redis         172.21.0.4/16  ✅ Healthy  
apexsigma_jaeger        172.21.0.5/16  ✅ Healthy
apexsigma_qdrant        172.21.0.6/16  ✅ Healthy
apexsigma_neo4j         172.21.0.7/16  ⚠️ Unhealthy (unrelated issue)
apexsigma_loki          172.21.0.8/16  ✅ Healthy
apexsigma_rabbitmq      172.21.0.9/16  ✅ Healthy
apexsigma_grafana       172.21.0.10/16 ✅ Healthy
apexsigma_devenviro_api 172.21.0.11/16 ⚠️ Unhealthy (unrelated issue)
apexsigma_tools_postgres 172.21.0.12/16 ✅ Healthy
apexsigma_ingest_llm_api 172.21.0.13/16 ✅ Healthy
apexsigma_tools_api     172.21.0.14/16 ✅ Healthy
apexsigma_memos_api     172.21.0.15/16 ✅ Healthy
apexsigma_prometheus    172.21.0.2/16  ✅ Healthy
```

**Next Available IPs**: 172.21.0.16 onwards

---

## Solution Options

### Option 1: Remove Static IPs (RECOMMENDED - Quick Fix)

**Approach**: Let Docker dynamically assign IPs from the available pool.

**Pros**:
- ✅ No network downtime
- ✅ No service disruption
- ✅ Immediate deployment of blocked services
- ✅ Simpler configuration

**Cons**:
- ⚠️ IPs may change on container recreation
- ⚠️ Requires updating any hardcoded IP references

**Implementation**:
```yaml
# Before
clickhouse:
  networks:
    apexsigma_net:
      ipv4_address: 172.26.0.50

# After
clickhouse:
  networks:
    - apexsigma_net
```

**Services to Update**:
- ClickHouse (line 285-286)
- Langfuse (line 350-351) 
- Vector (line 311-312)
- Dagster webserver (line 701-702)
- Dagster daemon (line 738-739)

---

### Option 2: Update Static IPs to 172.21.0.x (Alternative)

**Approach**: Change hardcoded IPs to be within the correct subnet.

**Pros**:
- ✅ Maintains static IP architecture
- ✅ Matches existing network configuration

**Cons**:
- ⚠️ Requires updating documentation (`VERIFIED_DOCKER_NETWORK_MAP_V3.md`)
- ⚠️ Risk of IP conflicts with existing containers
- ⚠️ More complex change tracking

**IP Allocation** (proposed):
```
172.21.0.16  ->  ClickHouse
172.21.0.17  ->  Langfuse
172.21.0.18  ->  Dagster webserver
172.21.0.19  ->  Dagster daemon
172.21.0.20  ->  Vector
172.21.0.21  ->  Vault
```

---

### Option 3: Recreate Network (NOT RECOMMENDED)

**Approach**: Delete and recreate `apexsigma_net` with `172.26.0.0/16` subnet.

**Pros**:
- ✅ Matches documentation exactly

**Cons**:
- ❌ Requires stopping ALL 14 running services
- ❌ Significant downtime
- ❌ Risk of data loss if volumes aren't preserved
- ❌ Complex coordination required

**Why This Is Bad**:
- Phase 0 is COMPLETE and infrastructure is STABLE
- Breaking working services to fix new services violates "do no harm" principle
- Violates Omega Ingest immutability - existing network is "ground truth"

---

## Recommended Action Plan

### Phase 1: Quick Fix (Remove Static IPs)

**Objective**: Get infrastructure services running ASAP without disrupting existing services.

1. **Update docker-compose.unified.yml**:
   - Remove `ipv4_address` from: ClickHouse, Langfuse, Vector, Dagster services
   - Keep hostname-based service discovery (already configured)

2. **Deploy Infrastructure**:
   ```powershell
   docker-compose -f docker-compose.unified.yml up -d clickhouse langfuse dagster-webserver dagster-daemon vault vector
   ```

3. **Verify Connectivity**:
   - Check health endpoints for all newly deployed services
   - Confirm ClickHouse databases created (`langfuse_analytics`, `apexsigma_observability`)
   - Verify Langfuse can connect to ClickHouse and PostgreSQL

4. **Update Documentation**:
   - Annotate `VERIFIED_DOCKER_NETWORK_MAP_V3.md` with "DEPRECATED - IPs are dynamic"
   - Create new `DOCKER_NETWORK_ACTUAL_STATE.md` with real IP mappings

### Phase 2: Long-term Fix (Optional - Post Phase 1)

**Objective**: Decide on static vs dynamic IP strategy.

**Decision Factors**:
- Do we need static IPs for service discovery? (No - using DNS hostnames)
- Do we need static IPs for firewall rules? (Not in dev/staging)
- Do we need static IPs for external documentation? (Hostnames are better)

**Recommendation**: Stay with dynamic IPs, rely on Docker DNS for service discovery.

---

## Validation Checklist

After implementing fix:

- [ ] ClickHouse container running and healthy
- [ ] Langfuse container running and healthy
- [ ] Dagster webserver and daemon running
- [ ] Vault container running and healthy
- [ ] Vector container running
- [ ] All services accessible via hostname (e.g., `clickhouse`, `langfuse`)
- [ ] No IP conflicts in `docker network inspect apexsigma_net`
- [ ] Langfuse can create tables in ClickHouse `langfuse_analytics` database
- [ ] Vector can write to ClickHouse `apexsigma_observability` database
- [ ] Existing 14 services still healthy (no disruption)

---

## Lessons Learned

### Process Failures

1. **No Network Pre-flight Validation**: SOD script doesn't verify network subnet matches expectations
2. **External Network Without Contract**: No documentation of who created `apexsigma_net` and why it's `172.21.0.0/16`
3. **Documentation Drift**: `VERIFIED_DOCKER_NETWORK_MAP_V3.md` documented wrong subnet without validating reality

### Preventive Measures

**Add to integrity-check.sh**:
```bash
# Verify Docker network subnet matches docker-compose expectations
EXPECTED_SUBNET="172.21.0.0/16"
ACTUAL_SUBNET=$(docker network inspect apexsigma_net --format "{{(index .IPAM.Config 0).Subnet}}")
if [ "$ACTUAL_SUBNET" != "$EXPECTED_SUBNET" ]; then
    echo "❌ Network subnet mismatch: expected $EXPECTED_SUBNET, got $ACTUAL_SUBNET"
    exit 1
fi
```

**Add to SOD script**:
- Pre-deployment network validation
- Automatic IP allocation verification
- Subnet conflict detection

---

## References

- **docker-compose.unified.yml**: Lines 263-312 (ClickHouse, Vector), 323-362 (Langfuse), 680-756 (Dagster)
- **Network Inspection**: `docker network inspect apexsigma_net`
- **Configuration Audit**: `docs/CONFIGURATION_DRIFT_AUDIT.md`
- **Network Documentation**: `docs/Config Files/Infrastructure/Docker Network/VERIFIED_DOCKER_NETWORK_MAP_V3.md` (outdated)

---

**Next Steps**: Implement Phase 1 Quick Fix (remove static IPs, deploy infrastructure services)
