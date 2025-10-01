#!/bin/bash
# ApexSigma Phase 2 - Automated Backup & Recovery Script
# Comprehensive backup solution for all critical data

set -euo pipefail

# Configuration
BACKUP_DIR="/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS=30

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Create backup directory structure
mkdir -p "${BACKUP_DIR}/{postgres,redis,qdrant,neo4j,clickhouse,configs}"

# PostgreSQL Backup
backup_postgres() {
    log "Starting PostgreSQL backup..."
    docker exec apexsigma_postgres pg_dumpall -U apexsigma_user > "${BACKUP_DIR}/postgres/postgres_${DATE}.sql"
    gzip "${BACKUP_DIR}/postgres/postgres_${DATE}.sql"
    log "PostgreSQL backup completed: postgres_${DATE}.sql.gz"
}

# Redis Backup
backup_redis() {
    log "Starting Redis backup..."
    docker exec apexsigma_redis redis-cli BGSAVE
    sleep 5  # Wait for background save to complete
    docker cp apexsigma_redis:/data/dump.rdb "${BACKUP_DIR}/redis/redis_${DATE}.rdb"
    gzip "${BACKUP_DIR}/redis/redis_${DATE}.rdb"
    log "Redis backup completed: redis_${DATE}.rdb.gz"
}

# Qdrant Backup
backup_qdrant() {
    log "Starting Qdrant backup..."
    docker exec apexsigma_qdrant tar -czf /tmp/qdrant_${DATE}.tar.gz /qdrant/storage
    docker cp apexsigma_qdrant:/tmp/qdrant_${DATE}.tar.gz "${BACKUP_DIR}/qdrant/"
    docker exec apexsigma_qdrant rm /tmp/qdrant_${DATE}.tar.gz
    log "Qdrant backup completed: qdrant_${DATE}.tar.gz"
}

# Neo4j Backup
backup_neo4j() {
    log "Starting Neo4j backup..."
    docker exec apexsigma_neo4j neo4j-admin database dump --to-path=/tmp neo4j || true
    docker exec apexsigma_neo4j tar -czf /tmp/neo4j_${DATE}.tar.gz /tmp/neo4j.dump /data
    docker cp apexsigma_neo4j:/tmp/neo4j_${DATE}.tar.gz "${BACKUP_DIR}/neo4j/"
    docker exec apexsigma_neo4j rm -f /tmp/neo4j_${DATE}.tar.gz /tmp/neo4j.dump
    log "Neo4j backup completed: neo4j_${DATE}.tar.gz"
}

# ClickHouse Backup
backup_clickhouse() {
    log "Starting ClickHouse backup..."
    docker exec apexsigma_clickhouse clickhouse-client --user=clickhouse_user --password=change_me_securely --query="BACKUP DATABASE apexsigma_observability TO File('/tmp/clickhouse_${DATE}.zip')" || {
        # Fallback: manual export
        docker exec apexsigma_clickhouse clickhouse-client --user=clickhouse_user --password=change_me_securely --query="SELECT * FROM system.tables WHERE database = 'apexsigma_observability' FORMAT CSV" > "${BACKUP_DIR}/clickhouse/schema_${DATE}.csv"
        docker exec apexsigma_clickhouse tar -czf /tmp/clickhouse_${DATE}.tar.gz /var/lib/clickhouse/data/apexsigma_observability
        docker cp apexsigma_clickhouse:/tmp/clickhouse_${DATE}.tar.gz "${BACKUP_DIR}/clickhouse/"
        docker exec apexsigma_clickhouse rm /tmp/clickhouse_${DATE}.tar.gz
    }
    log "ClickHouse backup completed: clickhouse_${DATE}.tar.gz"
}

# Configuration Backup
backup_configs() {
    log "Starting configuration backup..."
    tar -czf "${BACKUP_DIR}/configs/configs_${DATE}.tar.gz" \
        ./config \
        ./docker-compose.unified.yml \
        ./.env \
        ./pyproject.toml \
        ./poetry.lock
    log "Configuration backup completed: configs_${DATE}.tar.gz"
}

# Cleanup old backups
cleanup_old_backups() {
    log "Cleaning up backups older than ${RETENTION_DAYS} days..."
    find "${BACKUP_DIR}" -type f -name "*.gz" -mtime +${RETENTION_DAYS} -delete
    find "${BACKUP_DIR}" -type f -name "*.sql" -mtime +${RETENTION_DAYS} -delete
    find "${BACKUP_DIR}" -type f -name "*.rdb" -mtime +${RETENTION_DAYS} -delete
    find "${BACKUP_DIR}" -type f -name "*.csv" -mtime +${RETENTION_DAYS} -delete
    log "Cleanup completed"
}

# Verify backup integrity
verify_backups() {
    log "Verifying backup integrity..."
    local failed=0
    
    for file in "${BACKUP_DIR}"/*/*.gz; do
        if [[ -f "$file" ]]; then
            if ! gzip -t "$file" 2>/dev/null; then
                error "Corrupted backup: $file"
                ((failed++))
            fi
        fi
    done
    
    if [[ $failed -eq 0 ]]; then
        log "All backups verified successfully"
    else
        error "$failed backup(s) failed verification"
        return 1
    fi
}

# Send notification (placeholder for integration with monitoring)
send_notification() {
    local status=$1
    local message=$2
    
    # Integration point for Slack, email, or other notification systems
    log "Notification: $status - $message"
    
    # Example: Send to monitoring system
    # curl -X POST -H 'Content-type: application/json' \
    #     --data "{\"text\":\"Backup $status: $message\"}" \
    #     "$SLACK_WEBHOOK_URL"
}

# Main execution
main() {
    log "Starting ApexSigma backup process..."
    
    local start_time=$(date +%s)
    local success=true
    
    # Run all backups
    backup_postgres || success=false
    backup_redis || success=false
    backup_qdrant || success=false
    backup_neo4j || success=false
    backup_clickhouse || success=false
    backup_configs || success=false
    
    # Verify backups
    verify_backups || success=false
    
    # Cleanup old backups
    cleanup_old_backups
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    if [[ "$success" == "true" ]]; then
        log "Backup process completed successfully in ${duration} seconds"
        send_notification "SUCCESS" "All backups completed in ${duration} seconds"
    else
        error "Backup process completed with errors in ${duration} seconds"
        send_notification "FAILURE" "Backup process failed after ${duration} seconds"
        exit 1
    fi
}

# Execute main function
main "$@"
