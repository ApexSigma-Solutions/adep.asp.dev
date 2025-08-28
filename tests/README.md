# ApexSigma Core Integration Test Suite

This directory contains the core integration testing suite for validating the workflow between **InGest-LLM.as** and **memOS.as** services in the ApexSigma ecosystem.

## 🎯 Purpose

This test suite fulfills the **P1-CC-02** task requirement: *"Establish Core Integration Testing Suite between InGest-LLM.as and memOS.as"*. It provides comprehensive validation of:

- Service-to-service communication
- End-to-end data flow
- Memory tier selection and storage
- Error handling and recovery
- Performance characteristics
- Concurrent processing capabilities

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `test_core_integration_e2e.py` | Main integration test suite with comprehensive test cases |
| `run_integration_tests.py` | Test runner script with service health checks |
| `pytest.ini` | Pytest configuration for optimal test execution |
| `README.md` | This documentation file |

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Both services running:
  - **InGest-LLM.as** on port 8000
  - **memOS.as** on port 8091
- Required Python packages: `pytest`, `httpx`, `asyncio`

### Install Dependencies
```bash
# If using Poetry (recommended)
poetry install

# Or using pip
pip install pytest httpx asyncio pytest-asyncio
```

### Run All Tests
```bash
# Using the test runner (recommended)
python run_integration_tests.py

# Or directly with pytest
pytest test_core_integration_e2e.py -v -s
```

### Run Specific Test Categories
```bash
# Test service connectivity only
python run_integration_tests.py --category connectivity

# Test core workflow integration
python run_integration_tests.py --category workflow

# Test error handling and recovery
python run_integration_tests.py --category error

# Test performance characteristics
python run_integration_tests.py --category performance
```

## 🧪 Test Categories

### 1. Service Connectivity Tests (`TestServiceConnectivity`)
- **Purpose**: Validate that both services are healthy and accessible
- **Key Tests**:
  - `test_ingest_service_detailed_health()`: InGest-LLM.as health validation
  - `test_memos_service_detailed_health()`: memOS.as health and database connectivity

### 2. Core Integration Workflow Tests (`TestCoreIntegrationWorkflow`)
- **Purpose**: Validate end-to-end integration between services
- **Key Tests**:
  - `test_text_content_integration_flow()`: Complete text content workflow
  - `test_code_content_integration_flow()`: Code content with procedural memory
  - `test_concurrent_ingestion_workflow()`: Concurrent processing validation

### 3. Error Handling Tests (`TestErrorHandlingAndRecovery`)
- **Purpose**: Validate system resilience and error recovery
- **Key Tests**:
  - `test_malformed_content_handling()`: Invalid content handling
  - `test_service_recovery_simulation()`: Timeout and recovery scenarios

### 4. Performance Validation Tests (`TestPerformanceValidation`)
- **Purpose**: Validate system performance characteristics
- **Key Tests**:
  - `test_large_content_processing()`: Large content handling efficiency

## 🔧 Configuration

### Service URLs
Update the following constants in the test files if your services run on different ports:

```python
INGEST_SERVICE_URL = "http://localhost:8000"  # InGest-LLM.as
MEMOS_SERVICE_URL = "http://localhost:8091"   # memOS.as
```

### Test Timeouts
Adjust timeouts based on your system performance:

```python
REQUEST_TIMEOUT = 60        # HTTP request timeout
RETRY_ATTEMPTS = 3          # Service readiness retry attempts  
RETRY_DELAY = 2            # Delay between retries (seconds)
```

## 📊 Test Data Patterns

The test suite uses structured test data that mimics real-world usage:

### Documentation Content
- Multi-paragraph technical documentation
- Appropriate for semantic memory tier testing
- Contains searchable keywords for validation

### Code Content  
- Python code samples with classes and functions
- Automatically routed to procedural memory tier
- Includes metadata for language detection

### Concurrent Test Data
- Multiple unique content pieces for parallel processing
- Session-based identification for result tracking
- Validates system stability under load

## 🔍 Test Validation Patterns

### Response Validation
Each test validates comprehensive response structures:
- Required field presence
- Data type correctness
- Business logic compliance
- Cross-service data consistency

### Memory Tier Validation
Tests ensure content is stored in appropriate memory tiers:
- **Text/Documentation** → Semantic memory (Tier 2/3)
- **Code** → Procedural memory (Tier 2)
- **Task Data** → Episodic memory (Tier 2)

### Integration Flow Validation
1. **Ingestion Request** → InGest-LLM.as processes content
2. **Memory Storage** → Content forwarded to memOS.as
3. **Storage Confirmation** → Memory IDs returned
4. **Retrieval Validation** → Stored content accessible
5. **Search Validation** → Content findable via search

## 🚨 Troubleshooting

### Common Issues

#### Services Not Ready
```
❌ InGest-LLM.as : unreachable - http://localhost:8000 (Connection refused)
```
**Solution**: Ensure services are started:
```bash
# Start InGest-LLM.as
cd InGest-LLM.as && poetry run uvicorn src.ingest_llm_as.main:app --reload

# Start memOS.as  
cd memos.as && uvicorn app.main:app --host 0.0.0.0 --port 8091 --reload
```

#### Database Connection Issues
```
❌ memOS.as health check returned 503
```
**Solution**: Ensure database services are running:
```bash
# Check PostgreSQL, Redis, Qdrant connections
docker-compose up postgres redis qdrant -d
```

#### Test Timeout Issues
```
httpx.TimeoutException: Request timed out
```
**Solution**: Increase timeout values or check service performance:
```python
REQUEST_TIMEOUT = 120  # Increase from default 60
```

### Debug Mode
For detailed debugging, run tests with maximum verbosity:
```bash
pytest test_core_integration_e2e.py -v -s --tb=long
```

## 📈 Performance Expectations

### Baseline Performance Targets
- **Text Ingestion**: < 2s per KB of content
- **Code Ingestion**: < 1.5s per KB of content  
- **Memory Retrieval**: < 500ms per request
- **Search Operations**: < 1s for standard queries
- **Concurrent Processing**: 5 parallel requests without degradation

### Memory Utilization
- Each test creates 2-5 memory entries
- Tests clean up after themselves where possible
- Monitor database growth during extended test runs

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Integration Tests
on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      
      - name: Start Services
        run: |
          docker-compose up -d
          sleep 30  # Wait for services to initialize
      
      - name: Run Integration Tests
        run: |
          python tests/run_integration_tests.py
```

## 📚 Additional Resources

- [InGest-LLM.as Documentation](../InGest-LLM.as/README.md)
- [memOS.as Documentation](../memos.as/README.md) 
- [DevEnviro.as Documentation](../devenviro.as/README.md)
- [ApexSigma Architecture Overview](../CLAUDE.md)

## 🤝 Contributing

When adding new integration tests:

1. Follow the existing test class structure
2. Use the `ServiceValidator` helper for response validation
3. Include comprehensive error handling
4. Add appropriate test markers (`@pytest.mark.integration`)
5. Update this README with new test descriptions

## 📄 License

This test suite is part of the ApexSigma project and follows the same licensing terms.