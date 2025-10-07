param(
    [switch]$Teardown,
    [switch]$IntegrationOnly,
    [switch]$InContainer
)

# Determine script and repo root so paths are robust when invoked from anywhere
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")

Write-Host "Repo root detected: $RepoRoot"

Write-Host "Starting minimal infra for memos tests..."
$compose1 = Join-Path $RepoRoot 'docker-compose.unified.yml'
$compose2 = Join-Path $RepoRoot 'docker-compose.local.override.yml'
docker-compose -f "$compose1" -f "$compose2" up -d neo4j postgres redis qdrant

Write-Host "Waiting for Neo4j bolt on localhost:7687..."
for ($i = 0; $i -lt 30; $i++) {
    try {
        # Try a simple cypher via cypher-shell inside container if available
        $out = docker exec apexsigma_neo4j cypher-shell -u neo4j -p 'Apexsigma123_' "RETURN 1" 2>$null
        if ($out -match '1') {
            Write-Host "Neo4j is ready."
            break
        }
    } catch {
        # ignore
    }
    Start-Sleep -Seconds 2
}

if ($i -ge 30) {
    Write-Host "Warning: Neo4j did not become ready in 60s. Continuing anyway."
}

Write-Host "Running memos tests (pytest)..."
$env:NEO4J_URI = 'bolt://localhost:7687'
$env:NEO4J_USERNAME = 'neo4j'
$env:NEO4J_PASSWORD = 'Apexsigma123_'

Write-Host "Running alembic migrations against test Postgres (if alembic available)..."
try {
    # run migrations to ensure schema exists for integration tests
    poetry run alembic -c services/memos.as/alembic.ini upgrade head
} catch {
    Write-Host "Alembic not available or migration failed; continuing. Error: $_"
}

# Run pytest from repo root so relative test paths resolve correctly
Set-Location $RepoRoot
if ($InContainer) {
    Write-Host "Running tests inside container (docker-compose memos-tests)..."
    # Build and run the memos-tests service and abort on exit so we can capture results
    docker-compose -f "$compose1" -f "$compose2" up --build --abort-on-container-exit memos-tests
    # Grab the exit code of the memos-tests container
    $exitCode = docker inspect apexsigma_memos_tests --format '{{.State.ExitCode}}' 2>$null
    if ($null -ne $exitCode) {
        Write-Host "memos-tests container exit code: $exitCode"
    }
    if ($Teardown) {
        Write-Host "Tearing down infra (after in-container run)..."
        docker-compose -f "$compose1" -f "$compose2" down
    }
    if ([int]$exitCode -ne 0) {
        Write-Host "In-container tests failed with exit code $exitCode"
        exit [int]$exitCode
    }
} else {
    if ($IntegrationOnly) {
        poetry run pytest services/memos.as/app/tests -q -m integration
    } else {
        poetry run pytest services/memos.as/app/tests -q
    }
}

if ($Teardown) {
    Write-Host "Tearing down infra..."
    docker-compose -f "$compose1" -f "$compose2" down
}
