#!/usr/bin/env bash
# scripts/integrity-check.sh
# ApexSigma Ecosystem Referential Integrity Validator
# Validates git submodules, Poetry lockfiles, and Docker build contexts

set -euo pipefail

echo "🔍 ApexSigma Integrity Check - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILURES=0

# === 1. Validate Git Submodules ===
echo ""
echo "📦 Checking Git Submodules..."
if git submodule status | grep -q '^-'; then
    echo -e "${RED}❌ Uninitialized submodules detected${NC}"
    git submodule status
    echo "Auto-fixing: Initializing submodules..."
    git submodule update --init --recursive
    ((FAILURES++))
else
    echo -e "${GREEN}✅ All submodules initialized${NC}"
fi

# Validate submodule HEAD commits
echo "Validating submodule commits..."
git submodule foreach 'git rev-parse HEAD > /dev/null 2>&1 || exit 1' || {
    echo -e "${RED}❌ Submodule HEAD validation failed${NC}"
    ((FAILURES++))
}

# === 2. Validate Poetry Lockfiles ===
echo ""
echo "🔒 Checking Poetry Lockfiles..."
LOCK_ISSUES=0

for service_dir in services/*/; do
    if [ -f "${service_dir}pyproject.toml" ]; then
        service_name=$(basename "$service_dir")
        echo "  Checking ${service_name}..."
        
        pushd "$service_dir" > /dev/null
        
        # Check if lock exists
        if [ ! -f "poetry.lock" ]; then
            echo -e "${YELLOW}  ⚠️  Missing poetry.lock - generating...${NC}"
            poetry lock --no-update
            ((LOCK_ISSUES++))
        else
            # Validate lock is up to date
            if ! poetry check --lock 2>/dev/null; then
                echo -e "${YELLOW}  ⚠️  Lockfile out of sync - updating...${NC}"
                poetry lock --no-update
                ((LOCK_ISSUES++))
            else
                echo -e "${GREEN}  ✅ Lockfile valid${NC}"
            fi
        fi
        
        popd > /dev/null
    fi
done

if [ $LOCK_ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ All Poetry lockfiles valid${NC}"
else
    echo -e "${YELLOW}⚠️  Fixed ${LOCK_ISSUES} lockfile issues${NC}"
    ((FAILURES++))
fi

# === 3. Validate Docker Compose Configuration ===
echo ""
echo "🐳 Validating Docker Compose..."
if docker compose -f docker-compose.unified.yml config > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker Compose configuration valid${NC}"
else
    echo -e "${RED}❌ Docker Compose validation failed${NC}"
    docker compose -f docker-compose.unified.yml config
    ((FAILURES++))
fi

# === 4. Check for Docker Build Context Issues ===
echo ""
echo "🏗️  Validating Docker Build Contexts..."
CONTEXT_ISSUES=0

# Check if shared libs path exists for services that need it
for dockerfile in services/*/Dockerfile; do
    service_dir=$(dirname "$dockerfile")
    service_name=$(basename "$service_dir")
    
    if grep -q "COPY.*libs/apexsigma-core" "$dockerfile"; then
        echo "  Checking ${service_name} apexsigma-core dependency..."
        
        # Check if pyproject.toml references correct path
        pyproject="${service_dir}/pyproject.toml"
        if [ -f "$pyproject" ]; then
            if grep -q 'path = "./libs/apexsigma-core"' "$pyproject"; then
                # Path in pyproject is relative to service dir
                if [ ! -d "${service_dir}/libs/apexsigma-core" ] && [ ! -d "libs/apexsigma-core" ]; then
                    echo -e "${RED}  ❌ apexsigma-core not found for ${service_name}${NC}"
                    echo "     Expected: ${service_dir}/libs/apexsigma-core OR libs/apexsigma-core"
                    ((CONTEXT_ISSUES++))
                else
                    echo -e "${GREEN}  ✅ apexsigma-core path valid${NC}"
                fi
            fi
        fi
    fi
done

if [ $CONTEXT_ISSUES -gt 0 ]; then
    echo -e "${RED}❌ Found ${CONTEXT_ISSUES} build context issues${NC}"
    ((FAILURES++))
fi

# === 5. Check Environment Configuration ===
echo ""
echo "⚙️  Validating Environment Configuration..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
    
    # Check for critical missing vars (using .env.example as template)
    if [ -f ".env.example" ]; then
        missing_vars=()
        while IFS='=' read -r key value; do
            # Skip comments and empty lines
            [[ "$key" =~ ^#.*$ ]] && continue
            [[ -z "$key" ]] && continue
            
            if ! grep -q "^${key}=" .env 2>/dev/null; then
                missing_vars+=("$key")
            fi
        done < .env.example
        
        if [ ${#missing_vars[@]} -gt 0 ]; then
            echo -e "${YELLOW}⚠️  Missing environment variables:${NC}"
            printf '    - %s\n' "${missing_vars[@]}"
            ((FAILURES++))
        fi
    fi
else
    echo -e "${RED}❌ .env file missing - copy from .env.example${NC}"
    ((FAILURES++))
fi

# === 6. Validate Service Pydantic Settings ===
echo ""
echo "🔧 Validating Pydantic Settings Usage..."
SETTINGS_ISSUES=0

for service_dir in services/*/; do
    if [ -d "${service_dir}app" ]; then
        service_name=$(basename "$service_dir")
        
        # Check if service has settings.py or config.py with BaseSettings
        if find "${service_dir}app" -name "*.py" -exec grep -l "BaseSettings" {} \; | head -1 > /dev/null; then
            echo -e "${GREEN}  ✅ ${service_name} uses Pydantic BaseSettings${NC}"
        else
            echo -e "${YELLOW}  ⚠️  ${service_name} may not use Pydantic BaseSettings${NC}"
            ((SETTINGS_ISSUES++))
        fi
    fi
done

# === 7. Check for Configuration Drift ===
echo ""
echo "🔍 Checking for Configuration Drift..."

# Check if ClickHouse is defined but not running
if grep -q "clickhouse:" docker-compose.unified.yml; then
    if docker ps --filter "name=clickhouse" --format "{{.Names}}" | grep -q "clickhouse"; then
        echo -e "${GREEN}✅ ClickHouse service defined and running${NC}"
    else
        echo -e "${YELLOW}⚠️  ClickHouse defined but not running${NC}"
        echo "   Run: docker-compose -f docker-compose.unified.yml up -d clickhouse"
    fi
fi

# === Summary ===
echo ""
echo "=================================================="
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}✅ All integrity checks passed!${NC}"
    
    # Optional: Purge stale Docker cache
    echo ""
    echo "🧹 Purging stale Docker cache..."
    docker builder prune -f --filter "until=24h" || echo "⚠️  Could not prune Docker cache"
    
    exit 0
else
    echo -e "${RED}❌ Found ${FAILURES} integrity issues${NC}"
    echo ""
    echo "Some issues were auto-fixed. Please review changes and commit if necessary."
    exit 1
fi
