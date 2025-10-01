🎯 OVS-WO-002 Execution Order for Droid
Based on the ApexSigma Agent Roster & Operational Protocol, I'm issuing this execution order as GitHub Copilot (Human Augment Tool) supporting the Orchestrator (SigmaDev11).

📋 Mission Brief
Task ID: OVS-WO-002
Title: Resolve Port Conflicts
Implementer: @iFlow (Factory Droid)
Reviewer: @Gemini (MAR Protocol)
Priority: HIGH
Status: EXECUTE IMMEDIATELY

🎯 Strategic Objective
Enable the full observability stack by resolving port conflicts and adding missing external port mappings. This is critical for Valhalla Shield Engineering Standard compliance and ecosystem monitoring capabilities.

📊 Root Cause Analysis
Primary Issue: Missing external port mappings in docker-compose.unified.yml, not actual port conflicts.

Current State:

✅ Services running internally (Grafana, Prometheus, Jaeger)
❌ No external access via host ports
❌ Langfuse service missing from observability stack
🛠️ Implementation Specification
Step 1: Add External Port Mappings (15 minutes)
Update docker-compose.unified.yml to add port mappings:


# Add to existing servicesgrafana:  ports:    - "3000:3000"  # Grafana web UIprometheus:  ports:    - "9090:9090"  # Prometheus web UIjaeger:  ports:    - "16686:16686"  # Jaeger web UIdagster-webserver:  ports:    - "8081:8080"  # Avoid port 8080 conflict
Step 2: Add Langfuse Service (10 minutes)
Add complete Langfuse service to observability stack:


langfuse:  image: langfuse/langfuse:latest  container_name: apexsigma_langfuse  environment:    - NEXTAUTH_SECRET=${LANGFUSE_SECRET_KEY:-your-langfuse-secret-here}    - NEXTAUTH_URL=http://localhost:3001    - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}    - NEXT_PUBLIC_LANGFUSE_TRACING_URL=http://localhost:3001  ports:    - "3001:3000"  depends_on:    - postgres  networks:    - apexsigma_net  restart: unless-stopped
Step 3: Update Environment Configuration (5 minutes)
Update .env.example to include Langfuse configuration:


# Langfuse Configuration (AI Tracing)LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key-hereLANGFUSE_SECRET_KEY=sk-lf-your-secret-key-hereLANGFUSE_HOST=http://langfuse:3000
Step 4: Service Restart & Validation (10 minutes)

# Stop current servicesdocker-compose -f docker-compose.unified.yml down# Start with new configurationdocker-compose -f docker-compose.unified.yml up -d# Validate all servicesdocker-compose -f docker-compose.unified.yml ps
✅ "Done Means Done" Criteria
 Criterion 1: Port 8080 conflict identified and resolved
 Criterion 2: docker-compose.unified.yml updated with external port mappings
 Criterion 3: All observability services accessible via browser:
Grafana: http://localhost:3000 (admin/apexsigma123)
Prometheus: http://localhost:9090
Jaeger: http://localhost:16686
Langfuse: http://localhost:3001
Dagster: http://localhost:8081
 Valhalla Shield Compliance: All services running and monitored
🔍 Validation Commands

# Test all endpointscurl -f http://localhost:3000/api/health  # Grafanacurl -f http://localhost:9090/-/healthy   # Prometheuscurl -f http://localhost:16686/           # Jaegercurl -f http://localhost:3001/api/health  # Langfusecurl -f http://localhost:8081/           # Dagster# Check Docker statusdocker-compose -f docker-compose.unified.yml psdocker-compose -f docker-compose.unified.yml logs --tail 50
🚨 Critical Success Requirements
No Breaking Changes: Existing services must continue running
Security Compliance: Only expose necessary ports externally
Quality Gates: Run trunk check --ci after changes
Documentation: Update service access documentation
📋 Implementation Timeline
Total Duration: 40 minutes
Risk Level: LOW (additive changes only)
Rollback Plan: git revert + docker-compose down/up
🎯 MAR Protocol Requirements
Upon completion, provide:

Implementation Report with validation results
Service accessibility confirmation for all endpoints
Quality gate compliance (trunk check --ci passing)
Ready for @Gemini MAR review