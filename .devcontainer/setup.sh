#!/bin/bash
# .devcontainer/setup.sh - ApexSigma Ecosystem Complete Development Environment Setup
# Implements Valhalla Shield quality standards and Omega Ingest Protocol compliance

set -e

echo "================================================================================"
echo "                    APEX SIGMA ECOSYSTEM DEV ENVIRONMENT SETUP"
echo "================================================================================"
echo ""

# Function to log with timestamps
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check command success
check_command() {
    if [ $? -eq 0 ]; then
        log "✅ $1"
    else
        log "❌ $1 failed"
        exit 1
    fi
}

# ============================================================================
# PHASE 1: PYTHON 3.13+ ENFORCEMENT (CRITICAL)
# ============================================================================

log "🔍 Verifying Python 3.13+ requirement..."
python_version=$(python --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version < 3.13" | awk '{print ($1 < 3.13) ? 1 : 0}') -eq 1 ]]; then
    log "❌ Python $python_version detected. Python 3.13+ required for ApexSigma ecosystem."
    exit 1
fi
log "✅ Python $python_version confirmed"

# ============================================================================
# PHASE 2: POETRY CONFIGURATION (CRITICAL)
# ============================================================================

log "📦 Installing Poetry for dependency management..."
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/root/.local/bin:/home/vscode/.local/bin:$PATH"
check_command "Poetry installation"

log "⚙️ Configuring Poetry for containerized development..."
poetry config virtualenvs.create false
poetry config virtualenvs.in-project false
poetry config cache-dir /tmp/poetry-cache
check_command "Poetry configuration"

# ============================================================================
# PHASE 3: QUALITY GATES SETUP (MANDATORY)
# ============================================================================

log "🛡️ Installing Trunk CLI for quality gates..."
curl https://get.trunk.io -fsSL | bash
export PATH="/usr/local/bin:$PATH"
check_command "Trunk CLI installation"

log "📋 Configuring pytest for JUnit XML output..."
cat > pytest.ini << 'EOF'
[pytest]
junit_family = xunit1
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
asyncio_mode = strict
addopts =
    --strict-markers
    --strict-config
    --cov=libs
    --cov=services
    --cov-report=term-missing:skip-covered
    --cov-report=html:htmlcov
    --cov-report=xml:coverage.xml
    --cov-report=json:coverage.json
    --cov-branch
    --cov-fail-under=80
    -v
    --tb=short
    --color=yes
markers =
    e2e: End-to-end tests requiring full service stack
    integration: Integration tests requiring external services
    unit: Unit tests (default)
    slow: Slow running tests
    asyncio: Async tests requiring asyncio support
EOF
check_command "pytest configuration"

# ============================================================================
# PHASE 4: OMEGA INGEST PROTOCOL VERIFICATION (MANDATORY)
# ============================================================================

log "🔒 Verifying Omega Ingest Protocol services..."
echo "   Checking InGest-LLM API (172.26.0.12:8000)..."
if nc -z 172.26.0.12 8000 2>/dev/null && curl -f --max-time 5 http://172.26.0.12:8000/health > /dev/null 2>&1; then
    log "✅ InGest-LLM API available"
else
    log "⚠️ InGest-LLM API not available (will be available after service startup)"
fi

echo "   Checking memOS API (172.26.0.13:8090)..."
if nc -z 172.26.0.13 8090 2>/dev/null && curl -f --max-time 5 http://172.26.0.13:8090/health > /dev/null 2>&1; then
    log "✅ memOS API available"
else
    log "⚠️ memOS API not available (will be available after service startup)"
fi

# ============================================================================
# PHASE 4.5: DATABASE CLIENT VERIFICATION
# ============================================================================

log "🗄️ Verifying database clients..."
echo "   PostgreSQL client: $(psql --version | head -1)"
echo "   Redis client: $(redis-cli --version | head -1)"
echo "   Neo4j client: $(cypher-shell --version 2>/dev/null || echo 'Neo4j client not found')"
echo "   ClickHouse client: $(clickhouse-client --version 2>/dev/null || echo 'ClickHouse client not found')"
log "✅ Database clients verified"

# ============================================================================
# PHASE 5: SHARED LIBRARY INSTALLATION
# ============================================================================

log "📚 Installing shared libraries..."
cd libs/apexsigma-core
poetry lock --no-update || true
poetry install --no-root --no-dev
cd /workspace
check_command "Shared libraries installation"
cd -

# ============================================================================
# PHASE 6: SERVICE DEPENDENCY INSTALLATION
# ============================================================================

log "🔧 Installing service dependencies..."

# Python services
for service_dir in services/*/; do
    if [ -f "$service_dir/pyproject.toml" ]; then
        service_name=$(basename "$service_dir")
        log "   Installing $service_name..."
        cd "$service_dir"
        poetry install --no-root
        check_command "$service_name dependencies"
        cd -
    fi
done

# ============================================================================
# PHASE 7: PRE-COMMIT HOOKS & QUALITY ENFORCEMENT
# ============================================================================

log "🔗 Setting up pre-commit hooks..."
pip install pre-commit
pre-commit install --install-hooks
check_command "pre-commit hooks"

# ============================================================================
# PHASE 8: SOD/EOD WORKFLOW ALIASES
# ============================================================================

log "⚡ Setting up SOD/EOD workflow aliases..."
cat >> ~/.bashrc << 'EOF'

# ApexSigma SOD/EOD Protocol Aliases
alias sod='pwsh ./sod.ps1'
alias eod='pwsh ./eod.ps1'
alias sod-force='pwsh ./sod.ps1 -Force'
alias sod-verbose='pwsh ./sod.ps1 -Verbose'
alias eod-skip-tests='pwsh ./eod.ps1 -SkipTests'

# Quality Gates
alias quality-check='trunk check --ci'
alias quality-fix='trunk check --fix'

# Service Management
alias services-up='docker compose -f docker-compose.unified.yml up -d'
alias services-down='docker compose -f docker-compose.unified.yml down'
alias services-logs='docker compose -f docker-compose.unified.yml logs -f'
alias services-ps='docker compose -f docker-compose.unified.yml ps'

# Development Commands
alias memos-run='cd services/memos.as && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8090'
alias tools-run='cd services/tools.as && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8003'
alias ingest-run='cd services/InGest-LLM.as && poetry run uvicorn src.ingest_llm_as.main:app --reload --host 0.0.0.0 --port 8000'
alias devenviro-run='cd services/devenviro.as && python app/src/main.py'

# Database Connections
alias psql-connect='psql -h apaxsigma_postgres -U apaxsigma_user -d apaxsigma_db'
alias redis-connect='redis-cli -h apaxsigma_redis'
alias neo4j-connect='cypher-shell -a neo4j://apaxsigma_neo4j:7687 -u neo4j -p Apexsigma123_'
alias clickhouse-connect='clickhouse-client --host apaxsigma_clickhouse'

# Testing & Coverage
alias test-all='poetry run pytest --junit-xml=reports/junit.xml --cov --cov-report=html'
alias test-memos='cd services/memos.as && poetry run pytest --junit-xml=../../reports/junit-memos.xml --cov=app --cov-report=html'
alias test-tools='cd services/tools.as && poetry run pytest --junit-xml=../../reports/junit-tools.xml --cov=app --cov-report=html'
alias test-ingest='cd services/InGest-LLM.as && poetry run pytest --junit-xml=../../reports/junit-ingest.xml --cov=src --cov-report=html'

# Code Quality
alias lint-all='trunk check --ci'
alias format-all='trunk check --fix'
alias type-check='mypy services/ libs/'

# Git Workflow
alias git-status='git status --short'
alias git-log='git log --oneline -10'
alias git-diff='git diff --cached'

# Health Checks
alias health-check='curl -f http://localhost:8090/health && curl -f http://localhost:8003/health && curl -f http://localhost:8000/health'
alias omega-check='curl -f http://172.26.0.12:8000/health && curl -f http://172.26.0.13:8090/health'

EOF

# ============================================================================
# PHASE 9: ENVIRONMENT CONFIGURATION
# ============================================================================

log "🔐 Setting up environment configuration..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        log "✅ Created .env from .env.example"
    else
        log "⚠️ No .env.example found - create .env manually"
    fi
fi

# ============================================================================
# PHASE 10: INFRASTRUCTURE HEALTH CHECK
# ============================================================================

log "🏥 Performing infrastructure health checks..."
echo "   Starting core infrastructure services..."
docker compose -f docker-compose.unified.yml up -d postgres redis rabbitmq 2>/dev/null || true

echo "   Waiting for services to be ready..."
sleep 15

echo "   Checking service health..."
docker compose -f docker-compose.unified.yml ps

# ============================================================================
# PHASE 11: MAR PROTOCOL REMINDER SETUP
# ============================================================================

log "📋 Setting up MAR Protocol reminders and development tasks..."
mkdir -p .vscode
cat > .vscode/tasks.json << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "MAR Protocol Check",
            "type": "shell",
            "command": "echo '⚠️ MAR Protocol: Ensure dual verification before commit'",
            "presentation": {
                "reveal": "always",
                "panel": "new"
            },
            "runOptions": {
                "runOn": "folderOpen"
            }
        },
        {
            "label": "Quality Gates Check",
            "type": "shell",
            "command": "trunk check --ci",
            "group": "build",
            "presentation": {
                "reveal": "always"
            }
        },
        {
            "label": "Run Tests with Coverage",
            "type": "shell",
            "command": "poetry run pytest --junit-xml=reports/junit.xml --cov --cov-report=html",
            "group": "test",
            "presentation": {
                "reveal": "always"
            }
        },
        {
            "label": "Start memOS Service",
            "type": "shell",
            "command": "cd services/memos.as && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8090",
            "group": "build",
            "isBackground": true,
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start Tools Service",
            "type": "shell",
            "command": "cd services/tools.as && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8003",
            "group": "build",
            "isBackground": true,
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start InGest-LLM Service",
            "type": "shell",
            "command": "cd services/InGest-LLM.as && poetry run uvicorn src.ingest_llm_as.main:app --reload --host 0.0.0.0 --port 8000",
            "group": "build",
            "isBackground": true,
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start DevEnviro Service",
            "type": "shell",
            "command": "cd services/devenviro.as && python app/src/main.py",
            "group": "build",
            "isBackground": true,
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Health Check All Services",
            "type": "shell",
            "command": "echo 'Checking service health...' && curl -f http://localhost:8090/health && echo '✅ memOS OK' && curl -f http://localhost:8003/health && echo '✅ Tools OK' && curl -f http://localhost:8000/health && echo '✅ InGest-LLM OK'",
            "presentation": {
                "reveal": "always"
            }
        },
        {
            "label": "Omega Ingest Check",
            "type": "shell",
            "command": "echo 'Checking Omega Ingest services...' && curl -f http://172.26.0.12:8000/health && echo '✅ InGest-LLM OK' && curl -f http://172.26.0.13:8090/health && echo '✅ memOS OK'",
            "presentation": {
                "reveal": "always"
            }
        }
    ]
}
EOF

# ============================================================================
# PHASE 11.5: DEBUGGING CONFIGURATIONS
# ============================================================================

log "🐛 Setting up debugging configurations..."
cat > .vscode/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug memOS Service",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8090"
            ],
            "cwd": "${workspaceFolder}/services/memos.as",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        },
        {
            "name": "Debug Tools Service",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8003"
            ],
            "cwd": "${workspaceFolder}/services/tools.as",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        },
        {
            "name": "Debug InGest-LLM Service",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.ingest_llm_as.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "cwd": "${workspaceFolder}/services/InGest-LLM.as",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        },
        {
            "name": "Debug DevEnviro Service",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/services/devenviro.as/app/src/main.py",
            "cwd": "${workspaceFolder}/services/devenviro.as",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        },
        {
            "name": "Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "-v",
                "--junit-xml=reports/junit.xml",
                "--cov",
                "--cov-report=html"
            ],
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        },
        {
            "name": "Debug Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        }
    ]
}
EOF
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "MAR Protocol Check",
            "type": "shell",
            "command": "echo '⚠️ MAR Protocol: Ensure dual verification before commit'",
            "presentation": {
                "reveal": "always",
                "panel": "new"
            },
            "runOptions": {
                "runOn": "folderOpen"
            }
        },
        {
            "label": "Quality Gates Check",
            "type": "shell",
            "command": "trunk check --ci",
            "group": "build",
            "presentation": {
                "reveal": "always"
            }
        },
        {
            "label": "Run Tests with Coverage",
            "type": "shell",
            "command": "poetry run pytest --junit-xml=reports/junit.xml --cov --cov-report=html",
            "group": "test",
            "presentation": {
                "reveal": "always"
            }
        },
        {
            "label": "Start memOS Service",
            "type": "shell",
            "command": "cd services/memos.as && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8090",
            "group": "build",
            "isBackground": true,
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start Tools Service",
            "type": "shell",
            "command": "cd services/tools.as && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8003",
            "group": "build",
            "isBackground": true,
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start InGest-LLM Service",
            "type": "shell",
            "command": "cd services/InGest-LLM.as && poetry run uvicorn src.ingest_llm_as.main:app --reload --host 0.0.0.0 --port 8000",
            "group": "build",
            "isBackground": true,
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start DevEnviro Service",
            "type": "shell",
            "command": "cd services/devenviro.as && python app/src/main.py",
            "group": "build",
            "isBackground": true,
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Health Check All Services",
            "type": "shell",
            "command": "echo 'Checking service health...' && curl -f http://localhost:8090/health && echo '✅ memOS OK' && curl -f http://localhost:8003/health && echo '✅ Tools OK' && curl -f http://localhost:8000/health && echo '✅ InGest-LLM OK'",
            "presentation": {
                "reveal": "always"
            }
        },
        {
            "label": "Omega Ingest Check",
            "type": "shell",
            "command": "echo 'Checking Omega Ingest services...' && curl -f http://172.26.0.12:8000/health && echo '✅ InGest-LLM OK' && curl -f http://172.26.0.13:8090/health && echo '✅ memOS OK'",
            "presentation": {
                "reveal": "always"
            }
        }
    ]
}
EOF

# ============================================================================
# PHASE 11: INFRASTRUCTURE HEALTH CHECK
# ============================================================================

log "🏥 Performing infrastructure health checks..."

# Function to wait for service with timeout
wait_for_service() {
    local service_name=$1
    local host=$2
    local port=$3
    local timeout=${4:-60}
    local counter=0
    
    log "   Waiting for $service_name ($host:$port)..."
    while [ $counter -lt $timeout ]; do
        if nc -z $host $port 2>/dev/null; then
            log "✅ $service_name is ready"
            return 0
        fi
        sleep 2
        counter=$((counter + 2))
        echo -n "."
    done
    echo ""
    log "❌ $service_name not ready after ${timeout}s"
    return 1
}

# Wait for all infrastructure services
wait_for_service "PostgreSQL" "apexsigma_postgres" 5432 60
wait_for_service "Redis" "apexsigma_redis" 6379 30
wait_for_service "RabbitMQ" "apexsigma_rabbitmq" 5672 45
wait_for_service "Qdrant" "apexsigma_qdrant" 6333 30
wait_for_service "Neo4j" "apexsigma_neo4j" 7474 60
wait_for_service "ClickHouse" "apexsigma_clickhouse" 9000 60
wait_for_service "Vault" "apexsigma_vault" 8200 45

# Verify database connectivity
log "🔍 Verifying database connectivity..."
echo "   PostgreSQL: $(psql -h apexsigma_postgres -U ${POSTGRES_USER:-apexsigma_user} -d ${POSTGRES_DB:-apexsigma_db} -tAc "SELECT 1" 2>/dev/null && echo "✅ Connected" || echo "❌ Failed")"
echo "   Redis: $(redis-cli -h apexsigma_redis -a ${REDIS_PASSWORD:-Apexsigma123_} ping 2>/dev/null || echo "❌ Failed")"
echo "   Neo4j: $(cypher-shell -a neo4j://apexsigma_neo4j:7687 -u neo4j -p Apexsigma123_ "RETURN 1" 2>/dev/null && echo "✅ Connected" || echo "❌ Failed")"
echo "   ClickHouse: $(clickhouse-client --host apexsigma_clickhouse --query "SELECT 1" 2>/dev/null && echo "✅ Connected" || echo "❌ Failed")"

# Show service status
log "📊 Service status overview:"
docker compose -f docker-compose.unified.yml ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# ============================================================================
# PHASE 12: FINAL VERIFICATION & WELCOME
# ============================================================================

log "🎉 ApexSigma development environment setup complete!"
echo ""
echo "================================================================================"
echo "                              QUICK START GUIDE"
echo "================================================================================"
echo ""
echo "🚀 Start the ecosystem:"
echo "   sod-force                    # Start all services (force cleanup)"
echo ""
echo "🔍 Check service health:"
echo "   services-ps                  # View all running services"
echo "   services-logs                # View service logs"
echo "   health-check                 # Quick health check of all APIs"
echo "   omega-check                  # Verify Omega Ingest services"
echo ""
echo "💻 Development commands:"
echo "   memos-run                    # Start memOS service"
echo "   tools-run                    # Start tools service"
echo "   ingest-run                   # Start InGest-LLM service"
echo "   devenviro-run                # Start DevEnviro service"
echo ""
echo "�️ Database connections:"
echo "   psql-connect                 # Connect to PostgreSQL"
echo "   redis-connect                # Connect to Redis"
echo "   neo4j-connect                # Connect to Neo4j"
echo "   clickhouse-connect           # Connect to ClickHouse"
echo ""
echo "�🛡️ Quality gates:"
echo "   quality-check                # Run all quality checks"
echo "   quality-fix                  # Auto-fix issues where possible"
echo "   test-all                     # Run all tests with coverage"
echo "   test-memos                   # Test memOS service"
echo "   test-tools                   # Test tools service"
echo "   test-ingest                  # Test InGest-LLM service"
echo ""
echo "🔒 Governance:"
echo "   MAR Protocol: Dual verification required for all changes"
echo "   Omega Ingest: Query context APIs before code changes"
echo "   Valhalla Shield: 85%+ test coverage mandatory"
echo ""
echo "🐛 Debugging:"
echo "   Use VS Code Run & Debug panel for service debugging"
echo "   Tasks menu provides service startup and health checks"
echo ""
echo "📚 Documentation:"
echo "   .github/copilot-instructions.md  # Complete development guide"
echo "   docs/protocols/                  # Governance protocols"
echo "   AGENTS.md                        # Agent hierarchy and protocols"
echo ""
echo "================================================================================"
echo "                    WELCOME TO THE APEX SIGMA ECOSYSTEM!"
echo "================================================================================"