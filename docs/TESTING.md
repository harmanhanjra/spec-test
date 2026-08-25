# Testing

## Unit Tests

Located in `tests/`. Run with:

```bash
pytest tests -q
```

Current coverage:
- `parser.py`: covered by test_parser.py (load, extract).
- `generator.py`: covered by test_generator.py (fallback, no-LLM).
- `runner.py`: covered by test_runner.py (mocked HTTP).
- `reporter.py`: indirectly exercised by runner tests (not yet directly unit-tested).

## Integration Tests

No integration tests yet. To add:
- Spin up a local FastAPI server with a known spec.
- Run spec-test against it and assert output.

## Fixtures

- `tests/fixtures/sample_spec.yaml`: a minimal valid OpenAPI spec with three endpoints.

## Test Dependencies

- `pytest`, `pytest-asyncio`, `pytest-mock` are in `[test]` extra.

## Continuous Integration

GitHub Actions workflow (to be added) should run:
- `ruff check` and `bandit` (see SECURITY.md).
- `pytest` with coverage.
- Enforce no secrets in code.

## Known Gaps

- Reporter functions not unit-tested directly (but covered via runner tests).
- No property-based or fuzz tests for generator.
- LLM integration not tested in CI (requires mock server).