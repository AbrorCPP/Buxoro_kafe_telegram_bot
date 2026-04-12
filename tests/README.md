# Tests

This directory contains tests for the Telegram bot project.

## Running Tests

Install dependencies:
```
pip install -r requirements.txt
```

Run unit tests:
```
pytest tests/
```

Run performance tests:
```
pytest tests/test_performance.py
```

Run stress tests with Locust:
```
locust -f locustfile.py
```

## Test Types

- **Unit Tests**: Test individual functions and methods.
- **Integration Tests**: Test interactions between components.
- **Performance Tests**: Measure response times and resource usage.
- **Stress Tests**: Simulate high load to test system limits.