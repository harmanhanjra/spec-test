
import pytest

from spec_test.runner import run_tests


@pytest.mark.asyncio
async def test_run_tests(monkeypatch):
    # Mock responses
    import httpx
    class MockClient:
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            pass
        async def get(self, url, timeout):
            return httpx.Response(200, json={"id": 1, "name": "test"})
        async def post(self, url, json, timeout):
            return httpx.Response(201, json={"id": 2, "name": json.get("name")})
        # others not used in these tests

    # Patch httpx.AsyncClient to return MockClient
    monkeypatch.setattr("httpx.AsyncClient", lambda: MockClient())

    test_cases = [
        {"method": "GET", "path": "/users", "body": None, "expected_status": 200},
        {"method": "POST", "path": "/users", "body": {"name": "alice"}, "expected_status": 201},
    ]
    results = await run_tests(test_cases, "http://localhost")
    assert len(results) == 2
    assert results[0].passed is True
    assert results[1].passed is True
    assert results[0].status_code == 200
    assert results[1].status_code == 201
