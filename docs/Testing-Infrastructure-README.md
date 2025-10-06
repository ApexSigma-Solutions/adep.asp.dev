# ApexSigma Testing Infrastructure

## Overview

This directory contains the comprehensive testing infrastructure for the ApexSigma ecosystem, providing automated testing, monitoring, and quality assurance across all services.

## Components

### 1. CI/CD Pipeline
- **File**: `.github/workflows/github-actions-trunk-setup.yml`
- **Purpose**: Automated testing pipeline with Trunk.io integration
- **Triggers**: Push to `alpha`, PRs, Daily health checks
- **Features**:
  - Unit test execution with JUnit output
  - Trunk.io result uploads
  - Keploy API testing
  - Health monitoring and reporting

### 2. Keploy API Testing
- **Files**: `keploy-*.yml` (tools, memos, devenviro)
- **Purpose**: Automated API testing and mocking
- **Setup Script**: `scripts/setup_keploy.sh`
- **Features**:
  - Record API interactions
  - Generate test cases automatically
  - Docker-based testing environment

### 3. Test Monitoring
- **Script**: `scripts/monitor_tests.sh`
- **Dashboard**: `docs/Test-Monitoring-Dashboard.md`
- **Features**:
  - Health status analysis
  - Trend monitoring
  - Automated reporting
  - Trunk.io integration tracking

### 4. JUnit Validation
- **Script**: `scripts/validate_junit.py`
- **Purpose**: Local validation of JUnit XML files
- **Usage**: `python scripts/validate_junit.py <file>`

## Quick Start

### 1. Run Local Tests
```bash
# Install dependencies
poetry install

# Run tests with JUnit output
poetry run pytest --junit-xml=junit.xml -o junit_family=xunit1

# Validate results
python scripts/validate_junit.py junit.xml
```

### 2. Monitor Health
```bash
# Analyze test results
./scripts/monitor_tests.sh analyze

# View status
./scripts/monitor_tests.sh status

# Generate dashboard
./scripts/monitor_tests.sh dashboard
```

### 3. Setup Keploy Testing
```bash
# Setup services
./scripts/setup_keploy.sh setup

# Run API tests
./scripts/setup_keploy.sh test

# Generate report
./scripts/setup_keploy.sh report
```

## Configuration

### Environment Variables
- `TRUNK_API_TOKEN`: Required for Trunk.io uploads (set in GitHub secrets)

### Service Ports (for Keploy)
- Tools API: Port 8000
- Memos API: Port 8090
- DevEnviro API: Port 3001

## Monitoring & Health Checks

### Health Status Levels
- 🟢 **Excellent**: ≥95% pass rate
- 🟢 **Good**: ≥80% pass rate
- 🟡 **Warning**: ≥60% pass rate
- 🔴 **Critical**: <60% pass rate

### Automated Monitoring
- Daily health reports (6 AM UTC)
- CI/CD pipeline status tracking
- Trunk.io integration monitoring
- Artifact collection and storage

## Troubleshooting

### Common Issues

#### CI/CD Pipeline Failures
1. Check GitHub Actions logs
2. Verify `TRUNK_API_TOKEN` is set
3. Review test dependencies

#### Keploy Issues
1. Ensure Docker is running
2. Check service network connectivity
3. Verify API endpoints are accessible

#### Test Failures
1. Run tests locally first
2. Check environment configuration
3. Review service dependencies

### Debug Tools
```bash
# Validate test output
python scripts/validate_junit.py junit.xml --verbose

# Check monitoring logs
tail -f logs/trunk-monitor.log

# Test Docker connectivity
docker network inspect keploy-network
```

## Development Workflow

### Adding New Tests
1. Write tests following existing patterns
2. Ensure JUnit output compatibility
3. Update monitoring scripts if needed
4. Test locally before committing

### Modifying CI/CD Pipeline
1. Edit `.github/workflows/github-actions-trunk-setup.yml`
2. Test changes on feature branch
3. Update documentation
4. Monitor pipeline performance

### API Testing with Keploy
1. Update service configurations in `keploy-*.yml`
2. Test locally with `./scripts/setup_keploy.sh`
3. Update CI/CD pipeline if needed
4. Document new test scenarios

## Integration Points

### Trunk.io
- Test result analytics and tracking
- Flaky test detection
- Historical performance monitoring
- Team collaboration features

### GitHub Actions
- Automated testing on PRs and pushes
- Artifact storage and retrieval
- Integration with GitHub ecosystem
- Scheduled health monitoring

### Docker Ecosystem
- Service isolation for testing
- Network management for inter-service communication
- Volume management for test data
- Container lifecycle management

## Performance Optimization

### Test Execution
- Parallel test execution where possible
- Selective test running based on changes
- Caching of dependencies and artifacts
- Optimized Docker layer usage

### Monitoring
- Efficient log processing
- Minimal resource usage for health checks
- Smart alerting thresholds
- Automated cleanup of old artifacts

## Security Considerations

### Secrets Management
- GitHub secrets for API tokens
- Environment variable isolation
- Secure artifact storage
- Access control for monitoring data

### Test Data Security
- Sanitized test outputs
- Secure handling of mock data
- Compliance with data protection requirements
- Audit trails for test results

## Future Enhancements

### Planned Features
- Advanced test analytics dashboard
- AI-powered test failure prediction
- Automated test case generation
- Performance regression detection
- Integration with additional monitoring tools

### Scalability Improvements
- Distributed test execution
- Cloud-based testing infrastructure
- Advanced caching strategies
- Real-time monitoring dashboards

---

## Support

For issues or questions:
1. Check the monitoring dashboard
2. Review CI/CD pipeline logs
3. Consult Trunk.io documentation
4. Create an issue in the repository

**Last Updated**: October 5, 2025