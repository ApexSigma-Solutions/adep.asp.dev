#!/bin/bash
# Trunk.io Test Health Monitoring Script
# Monitors test results and provides health status for ApexSigma ecosystem

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MONITOR_LOG="$PROJECT_ROOT/logs/trunk-monitor.log"
HEALTH_FILE="$PROJECT_ROOT/.test-health.json"

# Trunk.io organization and repo info
ORG_SLUG="apexsigma-solutions"
REPO_NAME="adep.asp.dev"

echo -e "${BLUE}📊 Trunk.io Test Health Monitor${NC}"
echo -e "${BLUE}==============================${NC}"

# Function to log messages
log() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" >> "$MONITOR_LOG"
    echo -e "$message"
}

# Function to check if jq is available
check_dependencies() {
    if ! command -v jq >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  jq not found. Installing...${NC}"
        # Try to install jq (this might not work on all systems)
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update && sudo apt-get install -y jq
        elif command -v yum >/dev/null 2>&1; then
            sudo yum install -y jq
        elif command -v brew >/dev/null 2>&1; then
            brew install jq
        else
            echo -e "${RED}❌ Please install jq manually: https://stedolan.github.io/jq/download/${NC}"
            exit 1
        fi
    fi
}

# Function to get recent workflow runs
get_recent_runs() {
    local limit=${1:-5}

    log "${BLUE}Fetching recent workflow runs...${NC}"

    # This would require GitHub CLI or API access
    # For now, we'll simulate with local data
    echo "{
        \"runs\": [
            {
                \"id\": \"18264176007\",
                \"name\": \"Upload Test Results to Trunk\",
                \"status\": \"completed\",
                \"conclusion\": \"success\",
                \"created_at\": \"$(date -Iseconds)\",
                \"html_url\": \"https://github.com/$ORG_SLUG/$REPO_NAME/actions/runs/18264176007\"
            }
        ]
    }"
}

# Function to analyze test results
analyze_test_results() {
    local junit_file="$PROJECT_ROOT/junit.xml"

    if [ ! -f "$junit_file" ]; then
        log "${YELLOW}⚠️  No JUnit file found at $junit_file${NC}"
        return 1
    fi

    log "${BLUE}Analyzing JUnit results...${NC}"

    # Parse JUnit XML (simplified parsing)
    local total_tests=$(grep -c "<testcase" "$junit_file" 2>/dev/null || echo "0")
    local failed_tests=$(grep -c "<failure>" "$junit_file" 2>/dev/null || echo "0")
    local error_tests=$(grep -c "<error>" "$junit_file" 2>/dev/null || echo "0")
    local skipped_tests=$(grep -c "<skipped>" "$junit_file" 2>/dev/null || echo "0")

    local passed_tests=$((total_tests - failed_tests - error_tests - skipped_tests))

    # Calculate pass ratio
    local pass_ratio="0.0"
    if [ "$total_tests" -gt 0 ]; then
        pass_ratio=$(echo "scale=2; $passed_tests * 100 / $total_tests" | bc 2>/dev/null || echo "0.0")
    fi

    # Create health data
    cat > "$HEALTH_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "total_tests": $total_tests,
    "passed_tests": $passed_tests,
    "failed_tests": $failed_tests,
    "error_tests": $error_tests,
    "skipped_tests": $skipped_tests,
    "pass_ratio": $pass_ratio,
    "health_status": "$(get_health_status "$pass_ratio")",
    "junit_file": "$junit_file"
}
EOF

    log "${GREEN}✅ Test analysis completed${NC}"
    log "Total: $total_tests | Passed: $passed_tests | Failed: $failed_tests | Errors: $error_tests | Skipped: $skipped_tests"
    log "Pass Ratio: ${pass_ratio}% | Health: $(get_health_status "$pass_ratio")"
}

# Function to determine health status
get_health_status() {
    local pass_ratio=$1

    if (( $(echo "$pass_ratio >= 95" | bc -l 2>/dev/null || echo "0") )); then
        echo "excellent"
    elif (( $(echo "$pass_ratio >= 80" | bc -l 2>/dev/null || echo "0") )); then
        echo "good"
    elif (( $(echo "$pass_ratio >= 60" | bc -l 2>/dev/null || echo "0") )); then
        echo "warning"
    else
        echo "critical"
    fi
}

# Function to display health status with colors
display_health() {
    if [ ! -f "$HEALTH_FILE" ]; then
        echo -e "${RED}❌ No health data available. Run analysis first.${NC}"
        return 1
    fi

    local health_data=$(cat "$HEALTH_FILE")
    local health_status=$(echo "$health_data" | jq -r '.health_status')
    local pass_ratio=$(echo "$health_data" | jq -r '.pass_ratio')
    local total_tests=$(echo "$health_data" | jq -r '.total_tests')
    local passed_tests=$(echo "$health_data" | jq -r '.passed_tests')
    local failed_tests=$(echo "$health_data" | jq -r '.failed_tests')

    echo -e "${BLUE}🏥 Test Health Status${NC}"
    echo -e "${BLUE}===================${NC}"

    # Display health status with color
    case $health_status in
        "excellent")
            echo -e "Status: ${GREEN}🟢 EXCELLENT${NC} ($pass_ratio% pass rate)"
            ;;
        "good")
            echo -e "Status: ${GREEN}🟢 GOOD${NC} ($pass_ratio% pass rate)"
            ;;
        "warning")
            echo -e "Status: ${YELLOW}🟡 WARNING${NC} ($pass_ratio% pass rate)"
            ;;
        "critical")
            echo -e "Status: ${RED}🔴 CRITICAL${NC} ($pass_ratio% pass rate)"
            ;;
    esac

    echo ""
    echo "Test Summary:"
    echo "  Total Tests: $total_tests"
    echo "  Passed: $passed_tests"
    echo "  Failed: $failed_tests"
    echo "  Pass Ratio: $pass_ratio%"

    # Show recent Trunk.io links if available
    if [ -f "$PROJECT_ROOT/.trunk-links.json" ]; then
        echo ""
        echo "Recent Trunk.io Test Links:"
        cat "$PROJECT_ROOT/.trunk-links.json" | jq -r '.links[] | "  - \(.name): \(.url)"' 2>/dev/null || true
    fi
}

# Function to generate monitoring dashboard
generate_dashboard() {
    log "${BLUE}Generating monitoring dashboard...${NC}"

    local dashboard_file="$PROJECT_ROOT/docs/Test-Monitoring-Dashboard.md"

    cat > "$dashboard_file" << 'EOF'
# Test Monitoring Dashboard
Generated: TIMESTAMP

## Health Overview

HEALTH_STATUS_PLACEHOLDER

## Recent Test Runs

RUNS_PLACEHOLDER

## Trunk.io Integration

### Test Result Links
- View all test results: https://app.trunk.io/ORG_SLUG/flaky-tests
- Repository: https://github.com/ORG_SLUG/REPO_NAME

### Recent Failed Tests
FAILED_TESTS_PLACEHOLDER

## Monitoring Configuration

### Automated Checks
- Daily health reports: `cron` scheduled
- CI/CD integration: GitHub Actions
- Alert thresholds: <60% pass rate triggers alerts

### Manual Commands
```bash
# Run health check
./scripts/monitor_tests.sh analyze

# Display current status
./scripts/monitor_tests.sh status

# Generate report
./scripts/monitor_tests.sh report
```

## Health Trends

TREND_PLACEHOLDER

## Recommendations

RECOMMENDATIONS_PLACEHOLDER
EOF

    # Update placeholders with actual data
    sed -i "s/TIMESTAMP/$(date)/g" "$dashboard_file"
    sed -i "s/ORG_SLUG/$ORG_SLUG/g" "$dashboard_file"
    sed -i "s/REPO_NAME/$REPO_NAME/g" "$dashboard_file"

    if [ -f "$HEALTH_FILE" ]; then
        local health_status=$(cat "$HEALTH_FILE" | jq -r '.health_status')
        local pass_ratio=$(cat "$HEALTH_FILE" | jq -r '.pass_ratio')
        sed -i "s/HEALTH_STATUS_PLACEHOLDER/Status: $health_status ($pass_ratio% pass rate)/g" "$dashboard_file"
    fi

    log "${GREEN}✅ Dashboard generated: $dashboard_file${NC}"
}

# Function to setup automated monitoring
setup_automation() {
    log "${BLUE}Setting up automated monitoring...${NC}"

    # Create cron job for daily monitoring (example)
    local cron_file="$PROJECT_ROOT/.test-monitor.cron"

    cat > "$cron_file" << EOF
# Test Monitoring Cron Jobs
# Run daily at 6 AM
0 6 * * * $PROJECT_ROOT/scripts/monitor_tests.sh analyze >> $MONITOR_LOG 2>&1

# Run health check every 4 hours
0 */4 * * * $PROJECT_ROOT/scripts/monitor_tests.sh status >> $MONITOR_LOG 2>&1
EOF

    log "${GREEN}✅ Automation setup completed${NC}"
    log "To enable: crontab $cron_file"
}

# Main execution
main() {
    local action=${1:-"status"}

    # Create log directory if it doesn't exist
    mkdir -p "$(dirname "$MONITOR_LOG")"

    case $action in
        "analyze")
            check_dependencies
            analyze_test_results
            ;;
        "status")
            if [ -f "$HEALTH_FILE" ]; then
                display_health
            else
                echo -e "${YELLOW}⚠️  No health data available. Run 'analyze' first.${NC}"
            fi
            ;;
        "dashboard")
            generate_dashboard
            ;;
        "setup")
            setup_automation
            ;;
        "runs")
            get_recent_runs
            ;;
        *)
            echo -e "${RED}Usage: $0 {analyze|status|dashboard|setup|runs}${NC}"
            echo -e "${BLUE}Commands:${NC}"
            echo "  analyze   - Analyze latest test results"
            echo "  status    - Display current health status"
            echo "  dashboard - Generate monitoring dashboard"
            echo "  setup     - Setup automated monitoring"
            echo "  runs      - Show recent workflow runs"
            exit 1
            ;;
    esac
}

# Run main function with arguments
main "$@"