# Project Spec: SpecTest — AI-Powered API Contract Testing

## Problem
API consumers and providers often ship breaking changes because contracts (OpenAPI/Swagger) are not verified against actual behavior. Existing tools (Postman, Dredd) rely on hand-written examples or simple schema validation; they miss semantic errors, edge cases, and implicit constraints. Engineers waste hours debugging integration failures that could have been caught pre-merge.

## Solution
A CLI tool that:
1. Parses an OpenAPI (v3) specification.
2. Uses a local LLM (via llama.cpp or OpenAI-compatible API) to:
   - Generate a diverse set of request payloads (positive, negative, boundary).
   - Infer expected response status codes and body schemas beyond the spec.
3. Executes these requests against a live or mock server.
4. Compares actual responses to inferred expectations and spec constraints.
5. Produces a human-readable test report (JUnit XML, Markdown, JSON) with coverage metrics.

## Architecture (high-level)
- **CLI** (Click): accepts `--spec`, `--target`, `--llm-url`, `--format`, `--output`.
- **Parser** (openapi-spec-validator + PyYAML): loads and validates spec, extracts endpoint/method/schema.
- **Generator**: constructs a prompt with endpoint metadata and asks LLM for test cases (list of {payload, expected_status, expected_schema_hint}). Falls back to naive fuzzing if LLM unavailable.
- **Runner** (httpx with retries/timeouts): sends requests, collects responses.
- **Reporter**: aggregates results, computes pass/fail, emits chosen format.

## Data Flow
Spec → Parser → Endpoint → Generator (LLM) → Test Cases → Runner (HTTP) → Responses → Reporter → Output.

## Threat Model
- **Input injection**: spec files from untrusted sources could contain malicious YAML; validated with safe loader.
- **Network**: target server may be malicious; limit redirects, enforce timeouts, cap body size.
- **LLM prompt injection**: user-controlled spec descriptions could leak; no system prompt executed; output is validated as JSON.
- **Secrets**: LLM URL may contain API keys; stored in env var only, not in logs.

## Testing Strategy
- **Unit tests**: parser, generator (mock LLM), runner (mock HTTP), reporter.
- **Integration**: run against a local test server (FastAPI) with known spec; assert report contains expected failures.
- **Security**: bandit (B603/B607 with list args and timeouts are acceptable; document as accepted risk).

## Success Criteria
- Can test a 20-endpoint spec in under 60 seconds (excluding LLM inference).
- Report clearly distinguishes contract violations from server errors.
- Zero false positives on a known-good implementation.
- All unit tests pass under uv + pytest.

## Non-Goals
- Authentication handling (beyond API keys in headers) – deferred.
- Performance benchmarking.
- Full spec coverage (focus on request/response bodies).