from pathlib import Path

import pytest

from spec_test.generator import fallback_generate, generate_test_cases
from spec_test.parser import extract_endpoints, load_spec

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_fallback_generate():
    spec = load_spec(str(FIXTURES_DIR / "sample_spec.yaml"))
    endpoints = list(extract_endpoints(spec))
    for endpoint in endpoints:
        cases = fallback_generate(endpoint)
        assert isinstance(cases, list)
        for case in cases:
            assert "method" in case
            assert "path" in case
            # body may be None or dict
            assert "expected_status" in case

@pytest.mark.asyncio
async def test_generate_test_cases_no_llm():
    spec = load_spec(str(FIXTURES_DIR / "sample_spec.yaml"))
    cases = await generate_test_cases(spec, llm_url=None, llm_api_key=None)
    assert isinstance(cases, list)
    # Should have at least one case per endpoint
    assert len(cases) >= 3  # 3 endpoints, each has at least one
