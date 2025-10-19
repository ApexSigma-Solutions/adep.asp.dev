# Security Patching Strategy - ApexSigma Ecosystem

**Document Version:** 1.0  
**Last Updated:** October 19, 2025  
**Owner:** SigmaDev11  
**Status:** Active

---

## Executive Summary

This document outlines the ApexSigma ecosystem's security vulnerability management strategy, including triage processes, patch testing procedures, and emergency response protocols. All security operations follow the **Valhalla Shield Engineering Standard** and are governed by the **MAR (Mandatory Agent Review) Protocol**.

---

## 1. Vulnerability Triage Process

### 1.1 Severity Classification

| Severity | Response Time | Action Required | Example |
|----------|---------------|-----------------|---------|
| **Critical** | < 4 hours | Immediate patch + emergency deployment | Remote code execution, authentication bypass |
| **High** | < 24 hours | Priority patch + scheduled deployment | Path traversal, DoS vulnerabilities |
| **Medium** | < 7 days | Standard patch cycle | Information disclosure, mild DoS |
| **Low** | < 30 days | Routine maintenance cycle | Minor security hardening |

### 1.2 Dependency Source Classification

**Active Production Dependencies** (CRITICAL PATH):
- Python packages in active services (`services/devenviro.as`, `services/memos.as`, `services/InGest-LLM.as`, `services/tools.as`)
- Shared libraries (`libs/apexsigma-core`)
- Infrastructure dependencies (docker-compose.unified.yml services)

**Archived Dependencies** (LOW PRIORITY):
- Packages in `_archive/unused-services/` directory
- **Action:** Dismiss Dependabot alerts with `dismissed_reason=not_used`

**Development-Only Dependencies** (MEDIUM PRIORITY):
- `[tool.poetry.group.dev.dependencies]` sections
- Testing, linting, and documentation tools

---

## 2. Patch Implementation Workflow

### 2.1 Standard Patch Process

```bash
# 1. Identify vulnerability via Dependabot
gh api /repos/ApexSigma-Solutions/{repo}/dependabot/alerts

# 2. Check patch version
gh api /repos/ApexSigma-Solutions/{repo}/dependabot/alerts/{alert_id} \
  --jq '{package: .security_vulnerability.package.name, patched: .security_vulnerability.first_patched_version.identifier}'

# 3. Update pyproject.toml
# Edit affected service's pyproject.toml with minimum secure version

# 4. Update Poetry lock file
cd services/{service}.as
poetry lock --no-update

# 5. Test service functionality
poetry install
poetry run pytest --junit-xml=reports/junit.xml --cov=app --cov-report=html

# 6. Commit with security tag
git add pyproject.toml poetry.lock
git commit -m "security: patch {package} vulnerability (CVE-YYYY-NNNNN)"

# 7. Push and verify alert closure
git push origin alpha
gh api /repos/ApexSigma-Solutions/{repo}/dependabot/alerts/{alert_id}
```

### 2.2 Emergency Patch Process (Critical Vulnerabilities)

For **CRITICAL** severity vulnerabilities requiring immediate response:

1. **Immediate Action** (< 15 minutes):
   - Alert all team members via Slack/Discord
   - Lock affected services from external access (firewall rules)
   - Begin patch investigation

2. **Patch Development** (< 2 hours):
   - Create emergency branch: `hotfix/security-{CVE-ID}`
   - Apply security patches
   - Run minimum viable test suite
   - **Skip full CI/CD pipeline** if necessary

3. **Deployment** (< 4 hours total):
   - Deploy to production immediately
   - Monitor service health for 1 hour
   - Run full test suite post-deployment
   - Document incident in `docs/Security/Incidents/`

4. **Post-Incident Review** (< 24 hours):
   - Complete MAR Protocol review
   - Update security documentation
   - Perform root cause analysis
   - Implement preventative measures

---

## 3. Patch Testing Procedures

### 3.1 Service-Level Testing

**Required Tests Before Deployment:**
- ✅ Unit tests pass (`pytest`)
- ✅ Integration tests pass (Docker Compose services)
- ✅ Health check endpoints respond (`/health`)
- ✅ Prometheus metrics endpoint responds (`/metrics`)
- ✅ Service starts successfully (Docker healthcheck)

**Test Execution:**
```bash
# Run tests with coverage
poetry run pytest --junit-xml=reports/junit.xml \
  --cov=app \
  --cov-report=html \
  --cov-report=xml \
  --cov-fail-under=85

# Start service in Docker
docker-compose -f docker-compose.unified.yml up -d {service}_api

# Verify health
curl http://localhost:{port}/health
curl http://localhost:{port}/metrics
```

### 3.2 Integration Testing

**Docker Compose Test Stack:**
```bash
# Start test environment
docker-compose -f docker-compose.ci.yml up -d

# Run integration tests
poetry run pytest tests/integration/ --junit-xml=reports/junit-integration.xml

# Cleanup
docker-compose -f docker-compose.ci.yml down -v
```

### 3.3 Regression Testing

**Critical Functionality Validation:**
- Database connectivity (PostgreSQL, Redis, Neo4j, Qdrant)
- Message queue functionality (RabbitMQ)
- Authentication/authorization flows
- API endpoint responses
- Background task processing

---

## 4. Dependency Update Schedule

### 4.1 Routine Maintenance Windows

| Schedule | Scope | Process |
|----------|-------|---------|
| **Weekly** (Monday 09:00 UTC) | Development dependencies | Automated Dependabot PRs |
| **Bi-weekly** (1st & 15th, 14:00 UTC) | Production dependencies (non-security) | Scheduled maintenance |
| **Monthly** (First Tuesday, 16:00 UTC) | Major version upgrades | Planned migration window |
| **Quarterly** | Python version upgrades | Major ecosystem update |

### 4.2 Security-Driven Updates

**Triggered by Dependabot alerts:**
- Critical: Immediate (no schedule)
- High: Next business day
- Medium: Next bi-weekly window
- Low: Next monthly window

### 4.3 Poetry Lock File Management

**Synchronization Strategy:**
```bash
# Update all dependencies to latest compatible versions
poetry update

# Update specific package
poetry update {package}

# Update lock file only (no version changes)
poetry lock --no-update

# Verify lock file integrity
poetry check
```

---

## 5. Emergency Patch Protocols

### 5.1 Critical Vulnerability Response (CVE with Active Exploit)

**IMMEDIATE ACTIONS (< 15 minutes):**
1. **Isolate affected services:**
   ```bash
   docker-compose -f docker-compose.unified.yml stop {affected_service}
   ```
2. **Block external traffic:**
   ```bash
   # Add temporary firewall rule
   sudo ufw deny from any to any port {service_port}
   ```
3. **Alert team:**
   - Post to `#security-alerts` channel
   - Email to SigmaDev11
   - Update status page

**PATCH DEVELOPMENT (< 2 hours):**
```bash
# Create hotfix branch
git checkout -b hotfix/security-CVE-YYYY-NNNNN

# Apply patches
# Update pyproject.toml with secure versions
poetry lock --no-update

# Minimal testing
poetry run pytest tests/unit/ --maxfail=1

# Commit
git commit -m "security(CRITICAL): patch CVE-YYYY-NNNNN - {vulnerability description}"
git push origin hotfix/security-CVE-YYYY-NNNNN
```

**DEPLOYMENT (< 4 hours total):**
```bash
# Build new image
docker-compose -f docker-compose.unified.yml build {service}

# Deploy with zero-downtime rolling update
docker-compose -f docker-compose.unified.yml up -d --no-deps {service}

# Monitor health
watch -n 5 'docker-compose -f docker-compose.unified.yml ps'
watch -n 5 'curl -s http://localhost:{port}/health | jq'

# Re-enable external traffic
sudo ufw delete deny from any to any port {service_port}
```

### 5.2 Rollback Procedure

If patch causes service degradation:

```bash
# Rollback to previous image
docker-compose -f docker-compose.unified.yml stop {service}
docker tag {service}:previous {service}:latest
docker-compose -f docker-compose.unified.yml up -d {service}

# Revert code changes
git revert HEAD
git push origin alpha

# Document rollback reason
echo "Rollback due to: {reason}" >> docs/Security/Incidents/rollback-$(date +%Y%m%d).md
```

---

## 6. October 2025 Security Patch Summary

### 6.1 Vulnerabilities Addressed

**Main Repository (adep.asp.dev):**
- ✅ **Dismissed:** `multer` DoS vulnerabilities (#10-13) - packages in archived unused services
- ✅ **Patched:** `h11` malformed Chunked-Encoding (#4) - upgraded to 0.16.0+
- ✅ **Patched:** `starlette` multipart DoS (#3) - upgraded to 0.40.0+

**InGest-LLM.as:**
- ✅ **Patched:** `starlette` multipart DoS (#1) - upgraded to 0.40.0+
- ✅ **Patched:** `h11` malformed Chunked-Encoding - added explicit h11>=0.16.0

**memos.as:**
- ✅ **Patched:** `h11` malformed Chunked-Encoding (#2) - upgraded to 0.16.0+
- ✅ **Patched:** `setuptools` path traversal (#3) - upgraded to 78.1.1+
- ✅ **Patched:** `urllib3` redirect vulnerabilities (#5, #6) - upgraded to 2.5.0+
- ✅ **Patched:** `requests` credential leak (#4) - upgraded to 2.32.4+
- ✅ **Patched:** `jinja2` sandbox breakout (#1) - upgraded to 3.1.6+
- ✅ **Patched:** `dagster` local file inclusion (#8) - upgraded to 1.10.16+
- ✅ **Patched:** `starlette` multipart DoS (#7) - upgraded to 0.47.2+

### 6.2 Patch Versions Applied

| Package | Previous Version | Patched Version | Vulnerability Type |
|---------|------------------|-----------------|-------------------|
| `h11` | 0.14.0 | ≥0.16.0 | Malformed request handling |
| `starlette` | 0.27.0 | ≥0.40.0 / ≥0.47.2 | DoS via multipart forms |
| `setuptools` | (any) | ≥78.1.1 | Path traversal |
| `urllib3` | (any) | ≥2.5.0 | Redirect control issues |
| `requests` | (any) | ≥2.32.4 | Credential leak |
| `jinja2` | (any) | ≥3.1.6 | Sandbox escape |
| `dagster` | (any) | ≥1.10.16 | Local file inclusion |

### 6.3 Commits

**Main Repository:**
- Commit: `{hash}` - "security: patch critical Python dependencies (h11, starlette)"

**InGest-LLM.as:**
- Commit: `{hash}` - "security: patch starlette and h11 vulnerabilities"

**memos.as:**
- Commit: `{hash}` - "security: comprehensive dependency security patches (8 vulnerabilities)"

---

## 7. Monitoring & Verification

### 7.1 Dependabot Alert Monitoring

**Daily Checks:**
```bash
# Check all repos for new alerts
for repo in adep.asp.dev InGest-LLM.as memos.as devenviro.as tools.as; do
  echo "=== $repo ==="
  gh api /repos/ApexSigma-Solutions/$repo/dependabot/alerts \
    --jq '.[] | select(.state == "open") | {severity: .security_advisory.severity, package: .security_vulnerability.package.name}'
done
```

**Automated Notifications:**
- GitHub Dependabot notifications enabled
- Slack webhook for critical/high alerts
- Email digest for medium/low alerts

### 7.2 Post-Patch Verification

**Verify alert closure:**
```bash
# Check if alert was automatically closed
gh api /repos/ApexSigma-Solutions/{repo}/dependabot/alerts/{alert_id} \
  --jq '{state: .state, dismissed_at: .dismissed_at, fixed_at: .fixed_at}'
```

**Service health verification:**
```bash
# Check all services are healthy
docker-compose -f docker-compose.unified.yml ps | grep -E "(healthy|Up)"

# Verify metrics collection
curl http://localhost:9090/api/v1/query?query=up | jq '.data.result[] | select(.value[1] == "1")'
```

---

## 8. MAR Protocol Compliance

### 8.1 Required Reviews

Per AGENTS.md, all security patches require:
1. **Agent Review:** Gemini reviewer validates patch completeness
2. **Human Approval:** SigmaDev11 approves deployment
3. **Documentation:** This document updated with patch details

### 8.2 Review Checklist

- [ ] All affected services identified
- [ ] Patch versions verified against CVE database
- [ ] Test coverage maintained at ≥85%
- [ ] Integration tests pass
- [ ] Service health checks pass
- [ ] Documentation updated
- [ ] Commit messages follow convention: `security: {description}`
- [ ] Dependabot alerts verified closed

---

## 9. Future Improvements

### 9.1 Automation Roadmap

**Q4 2025:**
- [ ] Automated Dependabot PR testing in CI/CD
- [ ] Auto-merge for low-severity development dependency updates
- [ ] Slack bot for security alert notifications

**Q1 2026:**
- [ ] Trivy container image scanning
- [ ] OWASP Dependency-Check integration
- [ ] Automated rollback on failed health checks

### 9.2 Process Enhancements

- [ ] Security Champions program (rotate security lead quarterly)
- [ ] Monthly security review meetings
- [ ] Quarterly penetration testing
- [ ] Annual third-party security audit

---

## 10. References

- **GitHub Dependabot Documentation:** https://docs.github.com/en/code-security/dependabot
- **Python Security Best Practices:** https://python.readthedocs.io/en/stable/library/security_warnings.html
- **NIST Vulnerability Database:** https://nvd.nist.gov/
- **ApexSigma Protocols:** `docs/protocols/The_Laws_of_Asgard_A_Primer_for_Agents_of_the_ApexSigma_Ecosystem.md`
- **MAR Protocol:** `AGENTS.md`
- **Valhalla Shield Standard:** `.github/copilot-instructions.md`

---

**Document History:**
- **v1.0** (2025-10-19): Initial creation following October 2025 security patch cycle
