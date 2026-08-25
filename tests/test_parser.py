from pathlib import Path

import pytest

from spec_test.parser import extract_endpoints, load_spec

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_load_spec_valid():
    spec = load_spec(str(FIXTURES_DIR / "sample_spec.yaml"))
    assert "openapi" in spec
    assert spec["info"]["title"] == "Sample API"

def test_load_spec_invalid():
    with pytest.raises(OSError):
        load_spec(str(FIXTURES_DIR / "nonexistent.yaml"))

def test_extract_endpoints():
    spec = load_spec(str(FIXTURES_DIR / "sample_spec.yaml"))
    endpoints = list(extract_endpoints(spec))
    # Expect GET /users, POST /users, GET /users/{id}
    assert len(endpoints) == 3
    methods = {m for m, p, op in endpoints}
    assert "GET" in methods
    assert "POST" in methods
    paths = {p for m, p, op in endpoints}
    assert "/users" in paths
    assert "/users/{id}" in paths
