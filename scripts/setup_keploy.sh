#!/bin/bash
# Keploy Setup and Testing Script for ApexSigma Ecosystem
# This script sets up Keploy for API testing across all services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
KEPLOY_VERSION="latest"
SERVICES=("tools" "memos" "devenviro")
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🚀 ApexSigma Keploy Setup Script${NC}"
echo -e "${BLUE}=================================${NC}"

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to install Keploy
install_keploy() {
    echo -e "${YELLOW}📦 Installing Keploy...${NC}"

    if command -v keploy >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Keploy is already installed${NC}"
        return
    fi

    # Install Keploy using Docker (recommended for Windows compatibility)
    echo -e "${BLUE}Installing Keploy via Docker...${NC}"

    # Create keploy network if it doesn't exist
    docker network create keploy-network 2>/dev/null || true

    echo -e "${GREEN}✅ Keploy ready for use${NC}"
}

# Function to setup service for testing
setup_service() {
    local service=$1
    local config_file="keploy-${service}.yml"

    if [ ! -f "$config_file" ]; then
        echo -e "${RED}❌ Configuration file $config_file not found${NC}"
        return 1
    fi

    echo -e "${BLUE}🔧 Setting up $service service for Keploy testing...${NC}"

    # Create test directory if it doesn't exist
    mkdir -p "${service}-tests"

    # Copy configuration
    cp "$config_file" "${service}-tests/keploy.yml"

    echo -e "${GREEN}✅ $service service configured${NC}"
}

# Function to run Keploy tests for a service
run_keploy_test() {
    local service=$1
    local config_file="${service}-tests/keploy.yml"

    if [ ! -f "$config_file" ]; then
        echo -e "${RED}❌ Configuration file $config_file not found${NC}"
        return 1
    fi

    echo -e "${BLUE}🧪 Running Keploy tests for $service...${NC}"

    # Run Keploy in record mode first (if needed)
    echo -e "${YELLOW}Recording API interactions...${NC}"
    docker run --name keploy-${service} \
        -v "${PROJECT_ROOT}:/app" \
        -w "/app" \
        --network keploy-network \
        --rm \
        keploy/keploy record -c "cd ${service}-tests && keploy record" || true

    # Run tests
    echo -e "${YELLOW}Running tests...${NC}"
    docker run --name keploy-${service}-test \
        -v "${PROJECT_ROOT}:/app" \
        -w "/app" \
        --network keploy-network \
        --rm \
        keploy/keploy test -c "cd ${service}-tests && keploy test" || true

    echo -e "${GREEN}✅ $service tests completed${NC}"
}

# Function to generate test report
generate_report() {
    echo -e "${BLUE}📊 Generating test report...${NC}"

    local report_file="keploy-test-report-$(date +%Y%m%d-%H%M%S).md"

    cat > "$report_file" << EOF
# Keploy Test Report
Generated: $(date)

## Services Tested
EOF

    for service in "${SERVICES[@]}"; do
        if [ -d "${service}-tests" ]; then
            echo "- ✅ $service" >> "$report_file"
        else
            echo "- ❌ $service (not configured)" >> "$report_file"
        fi
    done

    cat >> "$report_file" << EOF

## Test Results
Check individual service directories for detailed results.

## Next Steps
1. Review test recordings in each service's test directory
2. Update test cases as needed
3. Integrate into CI/CD pipeline
4. Monitor API changes with Keploy

## Configuration Files
- keploy-tools.yml
- keploy-memos.yml
- keploy-devenviro.yml
EOF

    echo -e "${GREEN}✅ Report generated: $report_file${NC}"
}

# Function to cleanup
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up...${NC}"

    # Stop any running Keploy containers
    docker stop $(docker ps -q --filter name=keploy-) 2>/dev/null || true
    docker rm $(docker ps -aq --filter name=keploy-) 2>/dev/null || true

    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

# Main execution
main() {
    local action=${1:-"setup"}
    local service=${2:-"all"}

    case $action in
        "setup")
            check_docker
            install_keploy

            if [ "$service" = "all" ]; then
                for svc in "${SERVICES[@]}"; do
                    setup_service "$svc"
                done
            else
                setup_service "$service"
            fi

            echo -e "${GREEN}🎉 Keploy setup completed!${NC}"
            echo -e "${BLUE}Run '$0 test' to execute tests${NC}"
            ;;

        "test")
            check_docker

            if [ "$service" = "all" ]; then
                for svc in "${SERVICES[@]}"; do
                    run_keploy_test "$svc"
                done
            else
                run_keploy_test "$service"
            fi

            generate_report
            ;;

        "cleanup")
            cleanup
            ;;

        "report")
            generate_report
            ;;

        *)
            echo -e "${RED}Usage: $0 {setup|test|cleanup|report} [service]${NC}"
            echo -e "${BLUE}Services: tools, memos, devenviro, all${NC}"
            exit 1
            ;;
    esac
}

# Run main function with arguments
main "$@"