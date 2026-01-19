# 🧪 SatyaAI Testing Guide

## Overview
This document explains how to run tests for SatyaAI.

## Test Structure
```
tests/
├── unit/                    # Unit tests (no external dependencies)
│   ├── test_validators.py
│   ├── test_embeddings.py
│   ├── test_narrative_intelligence.py
│   ├── test_risk_engine.py
│   └── test_temporal_engine.py
└── integration/             # Integration tests (requires running services)
    ├── test_api.py         # API endpoint tests
    └── test_pipeline.py    # Complete workflow tests
```

## Running Tests

### Quick Start
```bash
# Run all tests
python run_tests.py
```

### Using pytest directly
```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests only (requires API server running)
pytest tests/integration/ -v

# Specific test file
pytest tests/unit/test_validators.py -v

# Specific test class
pytest tests/unit/test_validators.py::TestYearValidation -v

# Specific test function
pytest tests/unit/test_validators.py::TestYearValidation::test_valid_year -v
```

### With Coverage
```bash
# Generate coverage report
pytest tests/ --cov=core --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Manual Quick Test
```bash
# Run quick manual test
python quick_test.py
```

## Integration Tests

**Important:** Integration tests require services to be running.

### For API tests:
```bash
# Terminal 1: Start API server
python api/run.py

# Terminal 2: Run API tests
pytest tests/integration/test_api.py -v
```

## Test Requirements

Install test dependencies:
```bash
pip install pytest pytest-cov pytest-asyncio httpx
```

## Writing New Tests

### Unit Test Example
```python
import pytest
from core.utils.validators import validate_year

def test_valid_year():
    """Test valid year validation"""
    assert validate_year(2024) == 2024
    assert validate_year("2020") == 2020
```

### Integration Test Example
```python
import requests

def test_api_endpoint():
    """Test API endpoint"""
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
```

## Continuous Integration

Tests can be run automatically on GitHub Actions:
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python run_tests.py
```

## Troubleshooting

### "API server not running" error
- Start the API server: `python api/run.py`
- Or skip integration tests: `pytest tests/unit/ -v`

### Import errors
- Ensure you're in the project root directory
- Install all dependencies: `pip install -r requirements.txt`

### Qdrant errors
- Initialize Qdrant: `python -m core.qdrant.schema`
- Check `qdrant_data/` directory exists

## Test Coverage Goals
- Unit tests: 80%+ coverage
- Critical paths: 100% coverage
- Integration tests: All API endpoints