# Test Suite

Unit tests for the SuspensePerception project.

## Test Files

- `test_api.py` - Tests for API integration (OpenAI, Together)
- `test_gerrig.py` - Tests for Gerrig experiment functions
- `test_misc.py` - Tests for miscellaneous utility functions
- `test_thriller.py` - Tests for main Thriller application
- `test_utils.py` - Tests for utility functions

## Running Tests

Run all tests:
```bash
uv run pytest tests/
```

Run specific test file:
```bash
uv run pytest tests/test_api.py
```

Run with coverage:
```bash
uv run pytest tests/ --cov=src/thriller
```

## Test Dependencies

Tests use the following fixtures and mocks:
- `unittest.mock` for mocking external dependencies
- `pytest` fixtures for test setup
- Mock API responses for testing without API calls

## Note

Some tests require the `nlpaug` package which may need additional dependencies.
Install with: `uv pip install nlpaug`